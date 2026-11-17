#!/usr/bin/env python3
"""
LYGO Continuum — falsifiable work capsules for agents + humans.

Problem: Agents say "done." Sessions die. Worlds drift. Humans can't prove
the work still holds when handing off to another AI or teammate.

Solution: Seal work as a Continuum Capsule — structured, falsifiable claims
(file hashes, contains, counts, JSON paths) + decisions + next actions.
Re-verify locally. Drift is visible.

This CLI is pure local stdlib: no network, no subprocess.
Optional human portal (separate site) is never opened by this script.

Writes: under --base (default cwd) for --out, or skill state/ with --i-consent.
Claim paths and globs are confined under --base (no parent escape).

Signature: Delta9Phi963-CONTINUUM-v1.0.1
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-CONTINUUM-v1.0.1"
VERSION = "1.0.1"
SCHEMA = "lygo.continuum.v1"
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
STATE = SKILL / "state"

# Claim kinds agents and humans can use
CLAIM_KINDS = frozenset(
    {
        "file_exists",
        "file_missing",
        "file_sha256",
        "file_contains",
        "file_not_contains",
        "line_count_gte",
        "line_count_eq",
        "bytes_gte",
        "bytes_eq",
        "glob_count_gte",
        "json_path_eq",
        "text_sha256",  # portable: hash of inline text (no disk)
        "regex_match",
        "regex_not_match",
    }
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def root_hash_of(capsule_body: dict[str, Any]) -> str:
    """Hash everything except root_hash / chain / verify fields."""
    body = {k: v for k, v in capsule_body.items() if k not in ("root_hash", "chain", "last_verify")}
    return sha256_text(canonical_json(body))


def new_capsule_id() -> str:
    return "CONT-" + uuid.uuid4().hex[:12].upper()


def _is_under(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except (ValueError, OSError):
        return False


def resolve_path(path_str: str, base: Path | None) -> Path | None:
    """Resolve claim path under base. Rejects absolute paths and parent escape."""
    raw = str(path_str or "").strip()
    if not raw:
        return None
    # No absolute / drive-rooted claim paths (operator must use --base + relative)
    p = Path(raw)
    if p.is_absolute() or raw.startswith(("/", "\\")) or (len(raw) >= 2 and raw[1] == ":"):
        return None
    # Reject parent traversal in the claim string
    parts = p.parts
    if ".." in parts or parts[:1] == ("~",):
        return None
    root = (base if base is not None else Path.cwd()).resolve()
    try:
        resolved = (root / p).resolve()
    except (OSError, RuntimeError):
        return None
    if not _is_under(resolved, root):
        return None
    return resolved


def safe_glob(root: Path, pattern: str) -> list[Path]:
    """Glob only under root; reject traversal / absolute patterns."""
    pat = str(pattern or "").strip()
    if not pat:
        return []
    if ".." in pat or pat.startswith(("/", "\\")) or (len(pat) >= 2 and pat[1] == ":"):
        return []
    # Disallow patterns that Absolute-path style on Windows UNC
    if pat.startswith("\\\\") or "//" in pat.replace("://", ""):
        return []
    root = root.resolve()
    try:
        matches = list(root.glob(pat))
    except (OSError, ValueError):
        return []
    # Filter any match that escaped (symlink / odd glob)
    out: list[Path] = []
    for m in matches:
        try:
            mr = m.resolve()
        except (OSError, RuntimeError):
            continue
        if _is_under(mr, root):
            out.append(mr)
    return out


def authorize_write(out_path: Path, *, base: Path | None, consent: bool, allow_any: bool) -> tuple[bool, str]:
    """
    Writes allowed when:
      - --i-allow-any-out (operator override), or
      - path is under skill state/ AND --i-consent, or
      - path is under --base (default: cwd)
    """
    try:
        target = out_path.expanduser().resolve()
    except (OSError, RuntimeError):
        return False, "invalid_out_path"
    if allow_any:
        return True, "allow_any"
    state = STATE.resolve()
    if _is_under(target, state) or target.parent == state or target == state:
        if not consent:
            return False, "state_write_needs_i_consent"
        return True, "state"
    root = (base if base is not None else Path.cwd()).resolve()
    if _is_under(target, root) or target.parent == root:
        return True, "under_base"
    return False, "out_must_be_under_base_or_state"


def get_json_path(data: Any, dotted: str) -> Any:
    """Minimal dotted path: a.b.0.c — no external JSONPath lib."""
    cur = data
    if not dotted:
        return cur
    for part in dotted.split("."):
        if cur is None:
            return None
        if isinstance(cur, dict):
            if part not in cur:
                return None
            cur = cur[part]
        elif isinstance(cur, list):
            try:
                idx = int(part)
            except ValueError:
                return None
            if idx < 0 or idx >= len(cur):
                return None
            cur = cur[idx]
        else:
            return None
    return cur


def evaluate_claim(claim: dict[str, Any], base: Path | None) -> dict[str, Any]:
    """Evaluate one falsifiable claim against local reality. Never throws."""
    kind = str(claim.get("kind") or "").strip()
    cid = str(claim.get("id") or "?")
    out: dict[str, Any] = {
        "id": cid,
        "kind": kind,
        "ok": False,
        "detail": "",
        "observed": None,
        "expected": None,
    }
    if kind not in CLAIM_KINDS:
        out["detail"] = f"unknown kind: {kind}"
        return out

    try:
        if kind == "text_sha256":
            text = str(claim.get("text") or "")
            expect = str(claim.get("expect") or claim.get("sha256") or "").lower()
            got = sha256_text(text)
            out["observed"] = got
            out["expected"] = expect
            out["ok"] = got == expect
            out["detail"] = "match" if out["ok"] else "text hash mismatch"
            return out

        path_str = claim.get("path") or claim.get("file")
        pattern = claim.get("pattern") or claim.get("glob")

        if kind == "glob_count_gte":
            if not pattern:
                out["detail"] = "missing pattern"
                return out
            root = (base if base is not None else Path.cwd()).resolve()
            matches = safe_glob(root, str(pattern))
            if not matches and (".." in str(pattern) or str(pattern).startswith(("/", "\\"))):
                out["detail"] = "glob rejected (path escape / absolute pattern)"
                out["observed"] = 0
                out["expected"] = int(claim.get("n") if claim.get("n") is not None else claim.get("expect") or 0)
                out["ok"] = False
                return out
            n = int(claim.get("n") if claim.get("n") is not None else claim.get("expect") or 0)
            out["observed"] = len(matches)
            out["expected"] = n
            out["ok"] = len(matches) >= n
            out["detail"] = f"found {len(matches)} >= {n}" if out["ok"] else f"found {len(matches)} < {n}"
            return out

        if not path_str and kind not in ("glob_count_gte", "text_sha256"):
            out["detail"] = "missing path"
            return out

        path = resolve_path(str(path_str), base) if path_str else None
        if path_str and path is None:
            out["detail"] = f"path rejected (absolute or outside --base): {path_str}"
            return out

        if kind == "file_exists":
            exists = path is not None and path.is_file()
            out["observed"] = exists
            out["expected"] = True
            out["ok"] = exists
            out["detail"] = "exists" if exists else f"missing: {path}"
            return out

        if kind == "file_missing":
            # Rejected paths are treated as "not present under base" for safety
            if path is None and path_str:
                out["observed"] = True
                out["expected"] = True
                out["ok"] = True
                out["detail"] = "absent_or_outside_base"
                return out
            missing = path is None or not path.exists()
            out["observed"] = missing
            out["expected"] = True
            out["ok"] = missing
            out["detail"] = "absent" if missing else f"still present: {path}"
            return out

        if path is None or not path.is_file():
            out["detail"] = f"file not found: {path_str}"
            return out

        if kind == "file_sha256":
            expect = str(claim.get("expect") or claim.get("sha256") or "").lower()
            got = sha256_file(path)
            out["observed"] = got
            out["expected"] = expect
            out["ok"] = bool(expect) and got == expect
            out["detail"] = "hash match" if out["ok"] else "hash mismatch"
            return out

        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("utf-8", errors="replace")

        if kind == "file_contains":
            needle = str(claim.get("needle") or claim.get("expect") or "")
            out["expected"] = needle
            out["observed"] = needle in text if needle else False
            out["ok"] = bool(needle) and needle in text
            out["detail"] = "contains" if out["ok"] else "needle not found"
            return out

        if kind == "file_not_contains":
            needle = str(claim.get("needle") or claim.get("expect") or "")
            out["expected"] = f"NOT {needle}"
            found = needle in text if needle else False
            out["observed"] = not found
            out["ok"] = bool(needle) and not found
            out["detail"] = "absent" if out["ok"] else "needle present (fail)"
            return out

        if kind == "line_count_gte":
            n = int(claim.get("n") if claim.get("n") is not None else claim.get("expect") or 0)
            lines = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
            if text == "":
                lines = 0
            out["observed"] = lines
            out["expected"] = n
            out["ok"] = lines >= n
            out["detail"] = f"{lines} >= {n}" if out["ok"] else f"{lines} < {n}"
            return out

        if kind == "line_count_eq":
            n = int(claim.get("n") if claim.get("n") is not None else claim.get("expect") or 0)
            lines = len(text.splitlines()) if text else 0
            out["observed"] = lines
            out["expected"] = n
            out["ok"] = lines == n
            out["detail"] = f"{lines} == {n}" if out["ok"] else f"{lines} != {n}"
            return out

        if kind == "bytes_gte":
            n = int(claim.get("n") if claim.get("n") is not None else claim.get("expect") or 0)
            out["observed"] = len(raw)
            out["expected"] = n
            out["ok"] = len(raw) >= n
            out["detail"] = f"{len(raw)} >= {n}" if out["ok"] else f"{len(raw)} < {n}"
            return out

        if kind == "bytes_eq":
            n = int(claim.get("n") if claim.get("n") is not None else claim.get("expect") or 0)
            out["observed"] = len(raw)
            out["expected"] = n
            out["ok"] = len(raw) == n
            out["detail"] = f"{len(raw)} == {n}" if out["ok"] else f"{len(raw)} != {n}"
            return out

        if kind == "json_path_eq":
            jpath = str(claim.get("jpath") or claim.get("json_path") or "")
            expect = claim.get("expect")
            try:
                data = json.loads(text)
            except json.JSONDecodeError as e:
                out["detail"] = f"invalid json: {e}"
                return out
            got = get_json_path(data, jpath)
            out["observed"] = got
            out["expected"] = expect
            # normalize scalars via json
            out["ok"] = canonical_json(got) == canonical_json(expect)
            out["detail"] = "json path match" if out["ok"] else f"{jpath} mismatch"
            return out

        if kind in ("regex_match", "regex_not_match"):
            pattern = str(claim.get("pattern") or claim.get("expect") or "")
            if not pattern:
                out["detail"] = "missing pattern"
                return out
            # Safety: reject catastrophic patterns by length only (stdlib)
            if len(pattern) > 500:
                out["detail"] = "pattern too long"
                return out
            try:
                rx = re.compile(pattern, re.MULTILINE)
            except re.error as e:
                out["detail"] = f"bad regex: {e}"
                return out
            found = bool(rx.search(text))
            out["observed"] = found
            if kind == "regex_match":
                out["expected"] = True
                out["ok"] = found
                out["detail"] = "matched" if found else "no match"
            else:
                out["expected"] = False
                out["ok"] = not found
                out["detail"] = "no match (ok)" if not found else "matched (fail)"
            return out

        out["detail"] = f"unhandled kind: {kind}"
        return out
    except Exception as e:  # noqa: BLE001 — claim evaluator must never crash seal/verify
        out["detail"] = f"error: {type(e).__name__}: {e}"
        return out


def seal_capsule(
    *,
    claims: list[dict[str, Any]],
    task_summary: str,
    agent: str = "unknown",
    decisions: list[str] | None = None,
    next_actions: list[str] | None = None,
    base: Path | None = None,
    meta: dict[str, Any] | None = None,
    evaluate_now: bool = True,
) -> dict[str, Any]:
    """Build a continuum capsule. Optionally evaluate claims at seal time."""
    normalized: list[dict[str, Any]] = []
    for i, c in enumerate(claims):
        cc = dict(c)
        if "id" not in cc:
            cc["id"] = f"c{i + 1}"
        if "kind" not in cc:
            raise ValueError(f"claim {cc['id']} missing kind")
        # Auto-fill file_sha256 expect if missing and file exists
        if cc.get("kind") == "file_sha256" and not cc.get("expect") and not cc.get("sha256"):
            path_str = cc.get("path") or cc.get("file")
            if path_str:
                p = resolve_path(str(path_str), base)
                if p is not None and p.is_file():
                    cc["expect"] = sha256_file(p)
        if cc.get("kind") == "text_sha256" and not cc.get("expect") and "text" in cc:
            cc["expect"] = sha256_text(str(cc["text"]))
        normalized.append(cc)

    capsule: dict[str, Any] = {
        "schema": SCHEMA,
        "version": VERSION,
        "signature": SIG,
        "id": new_capsule_id(),
        "created_utc": utc_now(),
        "agent": agent,
        "task_summary": task_summary,
        "base_hint": str(base) if base else None,
        "decisions": list(decisions or []),
        "next_actions": list(next_actions or []),
        "claims": normalized,
        "meta": dict(meta or {}),
    }

    seal_results: list[dict[str, Any]] = []
    if evaluate_now:
        for c in normalized:
            seal_results.append(evaluate_claim(c, base))
        capsule["sealed_results"] = seal_results
        capsule["sealed_ok"] = all(r["ok"] for r in seal_results) if seal_results else True
        capsule["sealed_pass"] = sum(1 for r in seal_results if r["ok"])
        capsule["sealed_fail"] = sum(1 for r in seal_results if not r["ok"])
    else:
        capsule["sealed_ok"] = None

    capsule["root_hash"] = root_hash_of(capsule)
    capsule["chain"] = [
        {
            "event": "seal",
            "utc": capsule["created_utc"],
            "root_hash": capsule["root_hash"],
            "claim_count": len(normalized),
            "sealed_ok": capsule.get("sealed_ok"),
        }
    ]
    return capsule


def verify_capsule(
    capsule: dict[str, Any],
    *,
    base: Path | None = None,
) -> dict[str, Any]:
    """Re-evaluate all claims; check root_hash integrity; report drift vs sealed_results."""
    if not isinstance(capsule, dict):
        return {"ok": False, "error": "capsule is not an object"}

    stored_hash = capsule.get("root_hash")
    recomputed = root_hash_of(capsule)
    integrity_ok = stored_hash == recomputed

    base_use = base
    if base_use is None and capsule.get("base_hint"):
        try:
            base_use = Path(str(capsule["base_hint"]))
        except Exception:  # noqa: BLE001
            base_use = None

    results: list[dict[str, Any]] = []
    for c in capsule.get("claims") or []:
        if isinstance(c, dict):
            results.append(evaluate_claim(c, base_use))

    all_ok = all(r["ok"] for r in results) if results else True
    pass_n = sum(1 for r in results if r["ok"])
    fail_n = sum(1 for r in results if not r["ok"])

    # Drift: compare to sealed_results if present
    drift: list[dict[str, Any]] = []
    sealed = capsule.get("sealed_results") or []
    sealed_by_id = {r.get("id"): r for r in sealed if isinstance(r, dict)}
    for r in results:
        prev = sealed_by_id.get(r["id"])
        if not prev:
            continue
        if bool(prev.get("ok")) != bool(r.get("ok")) or prev.get("observed") != r.get("observed"):
            drift.append(
                {
                    "id": r["id"],
                    "kind": r["kind"],
                    "was_ok": prev.get("ok"),
                    "now_ok": r.get("ok"),
                    "was_observed": prev.get("observed"),
                    "now_observed": r.get("observed"),
                    "detail": r.get("detail"),
                }
            )

    report = {
        "ok": integrity_ok and all_ok,
        "integrity_ok": integrity_ok,
        "claims_ok": all_ok,
        "pass": pass_n,
        "fail": fail_n,
        "total": len(results),
        "drift_count": len(drift),
        "drift": drift,
        "results": results,
        "capsule_id": capsule.get("id"),
        "root_hash": stored_hash,
        "root_hash_recomputed": recomputed,
        "verified_utc": utc_now(),
        "signature": SIG,
        "version": VERSION,
    }
    return report


def handoff_markdown(capsule: dict[str, Any], verify_report: dict[str, Any] | None = None) -> str:
    """Human + agent paste pack for session handoff."""
    lines = [
        f"# LYGO Continuum Handoff — {capsule.get('id', '?')}",
        "",
        f"**Schema:** `{capsule.get('schema')}` · **Root:** `{capsule.get('root_hash', '')[:16]}…`",
        f"**Agent:** {capsule.get('agent')} · **Sealed:** {capsule.get('created_utc')}",
        f"**Task:** {capsule.get('task_summary')}",
        "",
        "## Claims (falsifiable)",
        "",
    ]
    for c in capsule.get("claims") or []:
        if not isinstance(c, dict):
            continue
        kind = c.get("kind")
        path = c.get("path") or c.get("file") or c.get("pattern") or "(inline)"
        expect = c.get("expect") or c.get("needle") or c.get("n") or c.get("sha256") or ""
        lines.append(f"- `{c.get('id')}` **{kind}** `{path}` → `{expect}`")
    if capsule.get("decisions"):
        lines += ["", "## Decisions", ""]
        for d in capsule["decisions"]:
            lines.append(f"- {d}")
    if capsule.get("next_actions"):
        lines += ["", "## Next actions", ""]
        for a in capsule["next_actions"]:
            lines.append(f"- {a}")
    if verify_report:
        status = "HOLDS" if verify_report.get("ok") else "BROKEN / DRIFT"
        lines += [
            "",
            f"## Verify status: **{status}**",
            f"- pass {verify_report.get('pass')}/{verify_report.get('total')} · drift {verify_report.get('drift_count')}",
            f"- integrity: {verify_report.get('integrity_ok')}",
            f"- at: {verify_report.get('verified_utc')}",
        ]
    lines += [
        "",
        "## Capsule JSON",
        "",
        "```json",
        json.dumps(capsule, indent=2, ensure_ascii=False),
        "```",
        "",
        "_Paste this block into the next agent. Re-verify with `lygo-continuum` or https://chatagent.ca/lygo-continuum.html_",
        "",
        f"_{SIG}_",
    ]
    return "\n".join(lines)


def witness_card_html(capsule: dict[str, Any], verify_report: dict[str, Any] | None = None) -> str:
    """Minimal standalone witness card (embeddable)."""
    ok = True if verify_report is None else bool(verify_report.get("ok"))
    band = "HOLDS" if ok else "BROKEN"
    color = "#2dd4a8" if ok else "#f07178"
    rid = capsule.get("id", "?")
    rh = str(capsule.get("root_hash") or "")[:20]
    task = str(capsule.get("task_summary") or "")[:200]
    n = len(capsule.get("claims") or [])
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>LYGO Continuum {rid}</title>
<style>
body{{margin:0;font-family:system-ui,Segoe UI,sans-serif;background:#0b0f14;color:#e6edf3;display:flex;min-height:100vh;align-items:center;justify-content:center}}
.card{{max-width:420px;padding:1.5rem 1.75rem;border:1px solid #1e2a36;border-radius:16px;background:linear-gradient(145deg,#121a22,#0d1319);box-shadow:0 0 40px #0008}}
.band{{display:inline-block;padding:.25rem .75rem;border-radius:999px;background:{color}22;color:{color};font-weight:700;letter-spacing:.06em;font-size:.8rem}}
h1{{font-size:1.15rem;margin:.75rem 0 .25rem}}
.meta{{color:#8b9aab;font-size:.85rem;line-height:1.5}}
code{{color:#7dd3fc;font-size:.78rem;word-break:break-all}}
.foot{{margin-top:1rem;font-size:.7rem;color:#5a6a7a}}
</style></head><body><div class="card">
<span class="band">{band}</span>
<h1>LYGO Continuum</h1>
<div class="meta"><strong>{rid}</strong><br/>{task}<br/>
claims: {n} · root <code>{rh}…</code></div>
<div class="foot">{SIG} · falsifiable work capsule</div>
</div></body></html>"""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_state(name: str, data: Any, consent: bool) -> Path | None:
    if not consent:
        return None
    STATE.mkdir(parents=True, exist_ok=True)
    p = STATE / name
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p


def cmd_demo() -> dict[str, Any]:
    """Self-contained demo with temp files — proves the whole loop."""
    import tempfile

    with tempfile.TemporaryDirectory(prefix="lygo-continuum-") as td:
        root = Path(td)
        (root / "app.py").write_text(
            "# demo app\nSTATUS = 'ready'\ndef main():\n    return 42\n",
            encoding="utf-8",
        )
        (root / "out.json").write_text('{"status":"ok","score":0.99}\n', encoding="utf-8")
        (root / "README.md").write_text("# Continuum Demo\nDone claim sealed.\n", encoding="utf-8")

        claims = [
            {"id": "c1", "kind": "file_exists", "path": "app.py"},
            {"id": "c2", "kind": "file_sha256", "path": "app.py"},  # auto-filled
            {"id": "c3", "kind": "file_contains", "path": "app.py", "needle": "STATUS = 'ready'"},
            {"id": "c4", "kind": "json_path_eq", "path": "out.json", "jpath": "status", "expect": "ok"},
            {"id": "c5", "kind": "line_count_gte", "path": "README.md", "n": 2},
            {"id": "c6", "kind": "glob_count_gte", "pattern": "*.py", "n": 1},
            {
                "id": "c7",
                "kind": "text_sha256",
                "text": "portable witness",
                "expect": sha256_text("portable witness"),
            },
        ]
        capsule = seal_capsule(
            claims=claims,
            task_summary="Demo: prove a mini project still holds",
            agent="lygo-continuum-demo",
            decisions=["stdlib only", "no network"],
            next_actions=["hand off to next agent with capsule JSON"],
            base=root,
        )
        report = verify_capsule(capsule, base=root)
        # Induce drift
        (root / "app.py").write_text("# demo app\nSTATUS = 'broken'\n", encoding="utf-8")
        drift_report = verify_capsule(capsule, base=root)
        return {
            "ok": report.get("ok") is True and drift_report.get("ok") is False and drift_report.get("drift_count", 0) >= 1,
            "signature": SIG,
            "capsule_id": capsule["id"],
            "root_hash": capsule["root_hash"],
            "verify_holds": report.get("ok"),
            "after_tamper_ok": drift_report.get("ok"),
            "drift_count": drift_report.get("drift_count"),
            "drift_ids": [d["id"] for d in drift_report.get("drift") or []],
            "pass_before": f"{report.get('pass')}/{report.get('total')}",
            "pass_after": f"{drift_report.get('pass')}/{drift_report.get('total')}",
            "message": "Continuum demo: seal → verify HOLDS → tamper → drift detected",
        }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="continuum",
        description="LYGO Continuum — seal / verify / drift / handoff falsifiable work capsules",
    )
    p.add_argument("--version", action="store_true")
    sub = p.add_subparsers(dest="cmd")

    seal = sub.add_parser("seal", help="Seal claims into a continuum capsule")
    seal.add_argument("--claims", required=True, help="Path to claims JSON (array or {claims:[...]})")
    seal.add_argument("--task", required=True, help="Task summary")
    seal.add_argument("--agent", default="operator")
    seal.add_argument("--base", default=None, help="Base directory for relative paths")
    seal.add_argument("--decisions", default=None, help="Path to JSON array of decision strings")
    seal.add_argument("--next", dest="next_actions", default=None, help="Path to JSON array of next actions")
    seal.add_argument(
        "--out",
        default=None,
        help="Write capsule JSON under --base (or state/ with --i-consent)",
    )
    seal.add_argument("--i-consent", action="store_true", help="Allow write under skill state/")
    seal.add_argument(
        "--i-allow-any-out",
        action="store_true",
        help="Operator override: allow --out outside base/state (explicit)",
    )
    seal.add_argument("--no-eval", action="store_true", help="Do not evaluate claims at seal time")

    ver = sub.add_parser("verify", help="Verify a capsule against current disk")
    ver.add_argument("--capsule", required=True)
    ver.add_argument("--base", default=None)
    ver.add_argument("--out", default=None)
    ver.add_argument("--i-consent", action="store_true")
    ver.add_argument("--i-allow-any-out", action="store_true")

    drift = sub.add_parser("drift", help="Verify and highlight drift from sealed results")
    drift.add_argument("--capsule", required=True)
    drift.add_argument("--base", default=None)
    drift.add_argument("--json", action="store_true")

    ho = sub.add_parser("handoff", help="Emit markdown handoff pack")
    ho.add_argument("--capsule", required=True)
    ho.add_argument("--base", default=None)
    ho.add_argument("--verify", action="store_true", help="Include live verify status")

    card = sub.add_parser("card", help="Emit HTML witness card")
    card.add_argument("--capsule", required=True)
    card.add_argument("--base", default=None)
    card.add_argument("--verify", action="store_true")
    card.add_argument("--out", default=None)
    card.add_argument("--i-consent", action="store_true")
    card.add_argument("--i-allow-any-out", action="store_true")

    sub.add_parser("demo", help="Self-contained seal→verify→drift demo")
    sub.add_parser("kinds", help="List claim kinds")
    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version or (not args.cmd and not args.version):
        if getattr(args, "version", False) or not args.cmd:
            print(json.dumps({"signature": SIG, "version": VERSION, "schema": SCHEMA}, indent=2))
            if not args.cmd:
                parser.print_help()
            return 0

    if args.cmd == "kinds":
        print(json.dumps({"kinds": sorted(CLAIM_KINDS), "signature": SIG}, indent=2))
        return 0

    if args.cmd == "demo":
        rep = cmd_demo()
        print(json.dumps(rep, indent=2))
        return 0 if rep.get("ok") else 1

    if args.cmd == "seal":
        raw = load_json(Path(args.claims))
        if isinstance(raw, dict) and "claims" in raw:
            claims = raw["claims"]
        elif isinstance(raw, list):
            claims = raw
        else:
            print(json.dumps({"ok": False, "error": "claims must be array or {claims:[]}"}), file=sys.stderr)
            return 2
        decisions = load_json(Path(args.decisions)) if args.decisions else []
        next_actions = load_json(Path(args.next_actions)) if args.next_actions else []
        base = Path(args.base).resolve() if args.base else Path.cwd()
        capsule = seal_capsule(
            claims=claims,
            task_summary=args.task,
            agent=args.agent,
            decisions=decisions if isinstance(decisions, list) else [],
            next_actions=next_actions if isinstance(next_actions, list) else [],
            base=base,
            evaluate_now=not args.no_eval,
        )
        if args.out:
            outp = Path(args.out)
            ok_w, why = authorize_write(
                outp,
                base=base,
                consent=bool(args.i_consent),
                allow_any=bool(args.i_allow_any_out),
            )
            if not ok_w:
                print(json.dumps({"ok": False, "error": why, "hint": "use --out under --base, or state/ + --i-consent"}), file=sys.stderr)
                return 2
            outp.parent.mkdir(parents=True, exist_ok=True)
            outp.write_text(json.dumps(capsule, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            capsule["_wrote"] = str(outp.resolve())
        print(json.dumps(capsule, indent=2, ensure_ascii=False))
        if capsule.get("sealed_ok") is False:
            return 10
        return 0

    if args.cmd == "verify":
        capsule = load_json(Path(args.capsule))
        base = Path(args.base).resolve() if args.base else None
        report = verify_capsule(capsule, base=base)
        if args.out:
            outp = Path(args.out)
            ok_w, why = authorize_write(
                outp,
                base=base or Path.cwd(),
                consent=bool(args.i_consent),
                allow_any=bool(args.i_allow_any_out),
            )
            if not ok_w:
                print(json.dumps({"ok": False, "error": why}), file=sys.stderr)
                return 2
            outp.parent.mkdir(parents=True, exist_ok=True)
            outp.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            report["_wrote"] = str(outp.resolve())
        print(json.dumps(report, indent=2, ensure_ascii=False))
        if not report.get("integrity_ok"):
            return 11
        if not report.get("claims_ok"):
            return 10
        return 0

    if args.cmd == "drift":
        capsule = load_json(Path(args.capsule))
        base = Path(args.base).resolve() if args.base else None
        report = verify_capsule(capsule, base=base)
        slim = {
            "ok": report["ok"],
            "drift_count": report["drift_count"],
            "drift": report["drift"],
            "pass": report["pass"],
            "fail": report["fail"],
            "total": report["total"],
            "integrity_ok": report["integrity_ok"],
            "capsule_id": report["capsule_id"],
            "verified_utc": report["verified_utc"],
            "signature": SIG,
        }
        print(json.dumps(slim if not args.json else report, indent=2, ensure_ascii=False))
        if report["drift_count"] > 0 or not report["ok"]:
            return 10
        return 0

    if args.cmd == "handoff":
        capsule = load_json(Path(args.capsule))
        report = None
        if args.verify:
            base = Path(args.base).resolve() if args.base else None
            report = verify_capsule(capsule, base=base)
        print(handoff_markdown(capsule, report))
        return 0

    if args.cmd == "card":
        capsule = load_json(Path(args.capsule))
        report = None
        if args.verify:
            base = Path(args.base).resolve() if args.base else None
            report = verify_capsule(capsule, base=base)
        html = witness_card_html(capsule, report)
        if args.out:
            outp = Path(args.out)
            base = Path(args.base).resolve() if args.base else Path.cwd()
            ok_w, why = authorize_write(
                outp,
                base=base,
                consent=bool(args.i_consent),
                allow_any=bool(args.i_allow_any_out),
            )
            if not ok_w:
                print(json.dumps({"ok": False, "error": why}), file=sys.stderr)
                return 2
            outp.parent.mkdir(parents=True, exist_ok=True)
            outp.write_text(html, encoding="utf-8")
        print(html)
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
