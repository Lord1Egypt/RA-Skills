"""Core data structures: JSONL I/O, upsert, merge, normalize, make_id."""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def utc_now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def parse_iso_utc(value: Any, fallback: dt.datetime) -> dt.datetime:
    try:
        return dt.datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(dt.timezone.utc)
    except Exception:
        return fallback


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text("utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=True, indent=2) + "\n", "utf-8")


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    out: List[Dict[str, Any]] = []
    for line in path.read_text("utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = [json.dumps(r, ensure_ascii=True, separators=(",", ":")) for r in rows]
    text = ("\n".join(serialized) + "\n") if serialized else ""
    path.write_text(text, "utf-8")


def normalize_content(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def make_id(kind: str, content: str) -> str:
    h = 0
    for ch in (kind + "|" + content).encode("utf-8"):
        h = (h * 131 + ch) % 2**32
    return f"{kind[0]}_{h:08x}"


def normalize_for_match(s: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", s.lower())


def is_path_like_text(s: str) -> bool:
    text = s.strip().strip("`")
    if not text:
        return False
    if " " in text:
        return False
    if "/" not in text and not re.search(r"\.(md|json|jsonl|ts|tsx|js|jsx|py|sh|yml|yaml)$", text, re.I):
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9_./:@\-]+", text))


def upsert(items: List[Dict[str, Any]], new_item: Dict[str, Any]) -> List[Dict[str, Any]]:
    by_id = {it.get("id"): it for it in items if it.get("id")}
    eid = new_item.get("id")
    if eid in by_id:
        existing = by_id[eid]
        existing["content"] = new_item.get("content", existing.get("content"))
        existing["confidence"] = max(float(existing.get("confidence") or 0.0), float(new_item.get("confidence") or 0.0))
        existing["importance"] = max(float(existing.get("importance") or 0.0), float(new_item.get("importance") or 0.0))
        existing["last_seen_at"] = new_item.get("last_seen_at") or existing.get("last_seen_at")
        existing["updated_at"] = new_item.get("updated_at") or existing.get("updated_at")
        existing["source"] = existing.get("source") or new_item.get("source")
        existing["tags"] = list({*(existing.get("tags") or []), *(new_item.get("tags") or [])})

        prev_sources = list(existing.get("sources") or ([] if not existing.get("source") else [existing.get("source")]))
        new_source = new_item.get("source")
        if new_source and new_source not in prev_sources:
            prev_sources.append(new_source)
        if prev_sources:
            existing["sources"] = prev_sources[-8:]

        existing["occurrences"] = int(existing.get("occurrences") or 1) + int(new_item.get("occurrences") or 1)
        existing["weight"] = float(min(1.6, max(float(existing.get("weight") or 1.0), float(new_item.get("weight") or 1.0)) + 0.04))
    else:
        new_item = dict(new_item)
        if new_item.get("source") and not new_item.get("sources"):
            new_item["sources"] = [new_item["source"]]
        new_item["occurrences"] = int(new_item.get("occurrences") or 1)
        items.append(new_item)
    return items


def normalize_event_content(line: str, event_type: str) -> str:
    s = normalize_content(line)
    s = re.sub(r"^讨论一个问题[:：]\s*", "问题：", s)
    s = re.sub(r"^突发问题[^：:]*[:：]?\s*", "问题：", s)
    s = re.sub(r"^对了[，, ]*", "", s)
    s = re.sub(r"^需求[:：]\s*", "", s)
    s = re.sub(r"^结论[:：]\s*", "", s)

    if event_type == "issue":
        s = re.sub(r"^(报错|错误|失败|异常|超时|卡死|阻塞)[:：]\s*", "问题：", s)
        # English prefix normalization
        s = re.sub(r"^(?:issue|error|bug|failed|timeout|blocked)[:：]\s*", "问题：", s, flags=re.I)
        if not s.startswith(("问题：", "风险：", "阻塞：", "Issue: ")):
            s = f"问题：{s}"
    elif event_type == "decision":
        s = re.sub(r"^(决定|最终决定|统一)[:：]\s*", "决策：", s)
        s = re.sub(r"^(?:decision|decided)[:：]\s*", "决策：", s, flags=re.I)
        if not s.startswith(("决策：", "决定：", "Decision: ")):
            s = f"决策：{s}"
    elif event_type == "solution":
        s = re.sub(r"^(解决办法|修复方法|处理办法|workaround|止血方案|临时方案|最终做法)[:：]\s*", "方案：", s, flags=re.I)
        s = re.sub(r"^(解决|修复)[:：]\s*", "方案：", s)
        s = re.sub(r"^(?:fix|solution|resolved|workaround|fixed by|changed to|switched to)[:：]\s*", "方案：", s, flags=re.I)
        if not s.startswith(("方案：", "解决：", "修复：", "Fix: ")):
            s = f"方案：{s}"

    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > 160:
        s = s[:157] + "…"
    return s


def row_identity_key(row: Dict[str, Any]) -> str:
    kind = str(row.get("kind") or "")
    if kind == "event":
        event_type = str(row.get("event_type") or "")
        content = normalize_event_content(str(row.get("content") or ""), event_type)
        return f"event|{event_type}|{normalize_for_match(content)}"
    content = normalize_content(str(row.get("content") or ""))
    if kind == "summary":
        m = re.match(r"^近期关键决策/进展聚焦在\s*(.+?)\s*（提及\s*\d+\s*次）", content)
        if m:
            return f"summary|focus|{normalize_for_match(m.group(1))}"
    return f"{kind}|{normalize_for_match(content)}"


def merge_rows_by_identity(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        key = row_identity_key(row)
        if key.endswith("|"):
            continue

        current = dict(row)
        if current.get("kind") == "event":
            event_type = str(current.get("event_type") or "")
            current["content"] = normalize_event_content(str(current.get("content") or ""), event_type)
            current["id"] = make_id("event", f"{event_type}:{current['content']}")
        else:
            current["content"] = normalize_content(str(current.get("content") or ""))
            current["id"] = make_id(str(current.get("kind") or "fact"), current["content"])

        current["occurrences"] = int(current.get("occurrences") or 1)
        if current.get("source") and not current.get("sources"):
            current["sources"] = [current["source"]]

        existing = merged.get(key)
        if not existing:
            merged[key] = current
            continue

        existing["confidence"] = max(float(existing.get("confidence") or 0.0), float(current.get("confidence") or 0.0))
        existing["importance"] = max(float(existing.get("importance") or 0.0), float(current.get("importance") or 0.0))
        existing["weight"] = max(float(existing.get("weight") or 0.0), float(current.get("weight") or 0.0))
        existing["temperature"] = max(float(existing.get("temperature") or 0.0), float(current.get("temperature") or 0.0))
        existing["occurrences"] = int(existing.get("occurrences") or 1) + int(current.get("occurrences") or 1)
        existing["last_seen_at"] = max(str(existing.get("last_seen_at") or ""), str(current.get("last_seen_at") or ""))
        existing["updated_at"] = max(str(existing.get("updated_at") or ""), str(current.get("updated_at") or ""))
        existing["created_at"] = min(
            str(existing.get("created_at") or existing.get("updated_at") or ""),
            str(current.get("created_at") or current.get("updated_at") or ""),
        )
        existing["tags"] = list({*(existing.get("tags") or []), *(current.get("tags") or [])})

        sources = list(existing.get("sources") or ([] if not existing.get("source") else [existing.get("source")]))
        for source in current.get("sources") or ([] if not current.get("source") else [current.get("source")]):
            if source and source not in sources:
                sources.append(source)
        if sources:
            existing["sources"] = sources[-8:]

    return list(merged.values())


def render_row_content(row: Dict[str, Any]) -> Optional[str]:
    content = str(row.get("content") or "").strip()
    if not content:
        return None
    if str(row.get("kind") or "") == "event":
        content = normalize_event_content(content, str(row.get("event_type") or ""))
    else:
        content = normalize_content(content)
    if len(content) > 180:
        content = content[:177] + "…"
    return content


def char_ngrams(text: str, n: int = 3) -> set:
    if not text:
        return set()
    if len(text) <= n:
        return {text}
    return {text[i : i + n] for i in range(len(text) - n + 1)}


def is_reference_match(target: str, candidate: str) -> bool:
    if target == candidate:
        return True
    if not target or not candidate:
        return False
    if abs(len(target) - len(candidate)) > max(12, int(max(len(target), len(candidate)) * 0.4)):
        return False
    g1 = char_ngrams(target)
    g2 = char_ngrams(candidate)
    if not g1 or not g2:
        return False
    sim = len(g1 & g2) / max(1, len(g1 | g2))
    return sim >= 0.72
