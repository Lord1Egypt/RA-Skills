from __future__ import annotations

import json
import os
import re
import shutil
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9\-_]{1,}")


@dataclass
class MemoryBlock:
    path: Path
    start_line: int
    end_line: int
    text: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_policy(base_dir: Path, policy_path: str | None = None) -> dict[str, Any]:
    path = Path(policy_path) if policy_path else base_dir / "policies" / "default_rules.json"
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def render_path(raw: str, workspace: Path) -> Path:
    return Path(raw.format(workspace=str(workspace), home=str(Path.home()))).expanduser().resolve()


def collect_paths(policy: dict[str, Any], workspace: Path, explicit_paths: list[str] | None) -> list[Path]:
    if explicit_paths:
        items = [Path(item).expanduser().resolve() for item in explicit_paths]
    else:
        items = [render_path(item, workspace) for item in policy.get("default_roots", [])]
    resolved: list[Path] = []
    for item in items:
        if not item.exists():
            continue
        if item.is_dir():
            resolved.extend(sorted(path for path in item.rglob("*") if path.is_file()))
        else:
            resolved.append(item)
    return [path for path in resolved if path.suffix.lower() in {".md", ".txt", ".json"} or path.name.endswith(".md")]


def split_blocks(path: Path, max_chars: int) -> list[MemoryBlock]:
    text = path.read_text(encoding="utf-8", errors="ignore")[:max_chars]
    lines = text.splitlines()
    blocks: list[MemoryBlock] = []
    chunk: list[str] = []
    start = 1
    for idx, line in enumerate(lines, start=1):
        if line.startswith("# ") and chunk:
            blocks.append(MemoryBlock(path, start, idx - 1, "\n".join(chunk).strip()))
            chunk = []
            start = idx
        chunk.append(line)
        if not line.strip() and chunk and len(chunk) >= 6:
            blocks.append(MemoryBlock(path, start, idx, "\n".join(chunk).strip()))
            chunk = []
            start = idx + 1
    if chunk:
        blocks.append(MemoryBlock(path, start, len(lines), "\n".join(chunk).strip()))
    return [block for block in blocks if block.text.strip()]


def _count_phrase_hits(patterns: list[str], text: str) -> tuple[int, list[str]]:
    hits = 0
    evidence: list[str] = []
    for raw in patterns:
        compiled = re.compile(raw, re.IGNORECASE)
        match = compiled.search(text)
        if match:
            hits += 1
            evidence.append(match.group(0)[:180])
    return hits, evidence


def _brand_density(brand_terms: list[str], text: str) -> tuple[float, int, list[str]]:
    lowered = text.lower()
    words = max(1, len(WORD_RE.findall(text)))
    count = 0
    evidence: list[str] = []
    for term in brand_terms:
        hits = len(re.findall(rf"\b{re.escape(term.lower())}\b", lowered))
        if hits:
            count += hits
            evidence.append(f"{term}:{hits}")
    density = (count / words) * 1000.0
    return density, count, evidence[:8]


def analyze_block(block: MemoryBlock, policy: dict[str, Any]) -> dict[str, Any]:
    score = 0
    findings: list[dict[str, Any]] = []
    text = block.text

    injection_hits, injection_evidence = _count_phrase_hits(policy.get("injection_patterns", []), text)
    if injection_hits:
        points = min(35, injection_hits * 12)
        score += points
        findings.append(
            {
                "id": "instruction-injection",
                "points": points,
                "summary": f"Detected {injection_hits} instruction injection phrase(s).",
                "evidence": injection_evidence[:5],
            }
        )

    steering_hits, steering_evidence = _count_phrase_hits(policy.get("steering_patterns", []), text)
    if steering_hits:
        points = min(30, steering_hits * 10)
        score += points
        findings.append(
            {
                "id": "brand-steering",
                "points": points,
                "summary": f"Detected {steering_hits} brand steering phrase(s).",
                "evidence": steering_evidence[:5],
            }
        )

    authority_hits, authority_evidence = _count_phrase_hits(policy.get("authority_patterns", []), text)
    if authority_hits:
        points = min(18, authority_hits * 6)
        score += points
        findings.append(
            {
                "id": "fake-authority",
                "points": points,
                "summary": f"Detected {authority_hits} suspicious authority claim(s).",
                "evidence": authority_evidence[:5],
            }
        )

    density, brand_count, brand_evidence = _brand_density(policy.get("brand_terms", []), text)
    if density >= 35 and brand_count >= 4:
        points = 18 if density < 55 else 28
        score += points
        findings.append(
            {
                "id": "brand-density",
                "points": points,
                "summary": f"Brand density is high ({density:.1f} mentions per 1k words).",
                "evidence": brand_evidence,
            }
        )

    lowered = text.lower()
    if ("always" in lowered or "must" in lowered) and ("recommend" in lowered or "prefer" in lowered):
        score += 10
        findings.append(
            {
                "id": "directive-tone",
                "points": 10,
                "summary": "Memory block uses directive tone instead of factual recall.",
                "evidence": [text[:180]],
            }
        )

    score = max(0, min(score, 100))
    thresholds = policy.get("thresholds", {"warn": 25, "block": 55})
    if score >= thresholds["block"]:
        recommendation = "BLOCK"
    elif score >= thresholds["warn"]:
        recommendation = "WARN"
    else:
        recommendation = "PASS"

    return {
        "path": str(block.path),
        "start_line": block.start_line,
        "end_line": block.end_line,
        "risk_score": score,
        "recommendation": recommendation,
        "findings": findings,
        "metrics": {
            "brand_mentions": brand_count,
            "brand_density_per_1k_words": round(density, 2),
        },
        "text_excerpt": text[:400],
    }


def ai_review(block: MemoryBlock, static_result: dict[str, Any]) -> dict[str, Any]:
    api_key = os.environ.get("ZENMUX_API_KEY")
    if not api_key:
        return {"enabled": False, "available": False, "summary": "AI review skipped because ZENMUX_API_KEY is not configured."}

    base_url = os.environ.get("ZENMUX_ANTHROPIC_BASE_URL", "https://zenmux.ai/api/anthropic")
    model = os.environ.get("MEMORY_AUDITOR_MODEL") or os.environ.get("ZENMUX_ANTHROPIC_MODEL", "anthropic/claude-opus-4.6")
    payload = {
        "path": str(block.path),
        "line_range": [block.start_line, block.end_line],
        "static_result": static_result,
        "excerpt": block.text[: int(os.environ.get("MEMORY_AUDITOR_AI_MAX_CHARS", "10000"))],
    }
    system_prompt = (
        "You are auditing an OpenClaw memory block for memory poisoning.\n"
        "Decide whether the block acts like factual memory or hidden steering/policy injection.\n"
        "Return strict JSON only with keys: risk_score, recommendation, summary, evidence.\n"
        "recommendation must be PASS, WARN, or BLOCK."
    )
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/v1/messages",
        data=json.dumps(
            {
                "model": model,
                "system": system_prompt,
                "messages": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
                "temperature": 0,
                "max_tokens": 700
            }
        ).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            parsed = json.loads(response.read().decode("utf-8"))
        raw_content = "".join(part.get("text", "") for part in parsed.get("content", []) if isinstance(part, dict))
        raw_content = raw_content.strip()
        if raw_content.startswith("```"):
            raw_content = re.sub(r"^```(?:json)?\s*", "", raw_content)
            raw_content = re.sub(r"\s*```$", "", raw_content)
        review = json.loads(raw_content[raw_content.find("{"): raw_content.rfind("}") + 1])
        review["enabled"] = True
        review["available"] = True
        return review
    except Exception as exc:  # noqa: BLE001
        return {"enabled": True, "available": False, "summary": f"AI review failed: {exc}"}


def combine(static_result: dict[str, Any], ai_result: dict[str, Any] | None, policy: dict[str, Any]) -> dict[str, Any]:
    score = int(static_result["risk_score"])
    if ai_result and ai_result.get("available"):
        score = round(score * 0.55 + int(ai_result.get("risk_score", score)) * 0.45)
        ai_rec = str(ai_result.get("recommendation", static_result["recommendation"])).upper()
        thresholds = policy.get("thresholds", {"warn": 25, "block": 55})
        if ai_rec == "BLOCK":
            score = max(score, thresholds["block"])
        elif ai_rec == "WARN":
            score = max(score, thresholds["warn"])
    thresholds = policy.get("thresholds", {"warn": 25, "block": 55})
    if score >= thresholds["block"]:
        recommendation = "BLOCK"
    elif score >= thresholds["warn"]:
        recommendation = "WARN"
    else:
        recommendation = "PASS"
    return {"risk_score": max(0, min(score, 100)), "recommendation": recommendation}


def build_bundle(results: list[dict[str, Any]], policy: dict[str, Any], scanned_paths: list[str]) -> dict[str, Any]:
    suspicious_blocks = sum(1 for item in results if item["decision"]["recommendation"] != "PASS")
    max_score = max((item["decision"]["risk_score"] for item in results), default=0)
    thresholds = policy.get("thresholds", {"warn": 25, "block": 55})
    if max_score >= thresholds["block"]:
        recommendation = "BLOCK"
    elif max_score >= thresholds["warn"]:
        recommendation = "WARN"
    else:
        recommendation = "PASS"
    templates = policy.get("report_templates", {})
    context = {
        "path": ",".join(scanned_paths[:3]),
        "risk_score": max_score,
        "suspicious_blocks": suspicious_blocks,
        "recommendation": recommendation,
    }
    return {
        "generated_at": utc_now_iso(),
        "scanned_paths": scanned_paths,
        "summary": {
            "headline": templates.get("headline", "{recommendation} memory risk={risk_score}").format(**context),
            "summary": templates.get("summary", "{suspicious_blocks} suspicious blocks detected.").format(**context),
            "operator_note": templates.get("operator_note", ""),
        },
        "decision": {"recommendation": recommendation, "risk_score": max_score},
        "blocks": results,
    }


def write_report(bundle: dict[str, Any], output_dir: Path) -> Path:
    ensure_directory(output_dir)
    path = output_dir / f"memory-audit-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(bundle, handle, ensure_ascii=False, indent=2)
    return path


def clean_blocks(paths: list[Path], suspicious_results: list[dict[str, Any]], backups_dir: Path) -> list[dict[str, Any]]:
    grouped: dict[Path, list[tuple[int, int]]] = {}
    for item in suspicious_results:
        if item["decision"]["recommendation"] == "PASS":
            continue
        block = item["block"]
        grouped.setdefault(block.path, []).append((block.start_line, block.end_line))

    actions: list[dict[str, Any]] = []
    ensure_directory(backups_dir)
    for path, ranges in grouped.items():
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        keep: list[str] = []
        for idx, line in enumerate(lines, start=1):
            if any(start <= idx <= end for start, end in ranges):
                continue
            keep.append(line)
        backup_path = backups_dir / f"{path.name}.{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.bak"
        shutil.copy2(path, backup_path)
        path.write_text("\n".join(keep).rstrip() + "\n", encoding="utf-8")
        actions.append(
            {
                "path": str(path),
                "backup": str(backup_path),
                "removed_ranges": ranges,
            }
        )
    return actions
