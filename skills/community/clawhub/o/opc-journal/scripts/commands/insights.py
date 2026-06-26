"""Journal command: insights (raw context for LLM interpretation)."""
import glob
import os
import re

from utils.storage import build_customer_dir, read_memory_file
from utils.timezone import now_tz
from scripts.commands._meta import get_language


def _find_sources(customer_id: str):
    sources = []
    base = build_customer_dir(customer_id)
    dreams = f"{base}/dreams.md"
    if os.path.exists(os.path.expanduser(dreams)):
        sources.append(("dreams", dreams))
    memory_dir = f"{base}/memory"
    if os.path.exists(os.path.expanduser(memory_dir)):
        files = glob.glob(f"{memory_dir}/*.md")
        files.sort(key=lambda f: _parse_file_date(f))
        sources.extend([("memory", f) for f in files])
    return sources


def _parse_file_date(path: str) -> str:
    basename = os.path.basename(path)
    m = re.search(r"(\d{2}-\d{2}-\d{2})\.md$", basename)
    if m:
        return m.group(1)
    return "00-00-00"


def _read_recent(sources: list, days: int = 7):
    from datetime import datetime
    dated = []
    for source_type, s in sources:
        file_date = _parse_file_date(s)
        if file_date != "00-00-00":
            dated.append((file_date, source_type, s))
        else:
            mtime_str = datetime.fromtimestamp(os.path.getmtime(s), now_tz().tzinfo).strftime("%d-%m-%y")
            dated.append((mtime_str, source_type, s))
    dated.sort(key=lambda x: datetime.strptime(x[0], "%d-%m-%y"))
    recent = dated[-min(days, len(dated)):]
    contents = []
    dates_read = []
    for d, source_type, path in recent:
        res = read_memory_file(path)
        if res.get("success"):
            contents.append(res["content"])
            dates_read.append({"date": d, "type": source_type, "path": path})
    return "\n\n".join(contents), dates_read


def run(customer_id: str, args: dict) -> dict:
    """Return recent journal context for the caller (LLM) to generate insights dynamically."""
    day = args.get("day", 1)
    days_back = args.get("days_back", 7)
    lang = get_language(customer_id)
    sources = _find_sources(customer_id)

    if not sources:
        return {
            "status": "success",
            "result": {
                "day": day,
                "customer_id": customer_id,
                "language": lang,
                "sources": [],
                "raw_text": "",
                "signal_counts": {},
            },
            "message": "No memory sources available",
        }

    raw_text, dates_read = _read_recent(sources, days_back)
    activity_mentions = len([l for l in raw_text.split("\n") if l.strip() and not l.strip().startswith("#")])

    # Language-agnostic structural signals. No hardcoded semantic keywords.
    signal_counts = {
        "action_signals": len(re.findall(r"\b(completed|shipped|launched|sale|signed|revenue|MVP|milestone|breakthrough|decided|adopted)\b", raw_text, re.IGNORECASE)),
        "challenge_signals": len(re.findall(r"\b(stuck|blocked|bottleneck|failed|error|bug|issue|overwhelm|burnout)\b", raw_text, re.IGNORECASE)),
        "learning_signals": len(re.findall(r"\b(learned|first time|new skill|figured out|understood)\b", raw_text, re.IGNORECASE)),
        "pivot_signals": len(re.findall(r"\b(traction|pivot|direction|validation failed)\b", raw_text, re.IGNORECASE)),
        "structural_signals": {
            "exclamation_marks": raw_text.count("!"),
            "question_marks": raw_text.count("?"),
            "all_caps_words": len(re.findall(r"\b[A-Z]{2,}\b", raw_text)),
            "repeated_punctuation": len(re.findall(r"([!?.,])\1+", raw_text)),
        },
        "activity_lines": activity_mentions,
    }

    return {
        "status": "success",
        "result": {
            "customer_id": customer_id,
            "day": day,
            "language": lang,
            "days_back": days_back,
            "sources": dates_read,
            "raw_text": raw_text,
            "signal_counts": signal_counts,
            "generated_at": now_tz().isoformat(),
            "data_source": "openclaw_dreams_memory",
        },
        "message": f"Insight context prepared for Day {day} from the last {len(dates_read)} source(s).",
    }
