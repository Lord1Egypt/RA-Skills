import json
from datetime import datetime
from pathlib import Path


def memory_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "memory"


def ensure_memory_dir() -> Path:
    directory = memory_dir()
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def default_memory_path() -> Path:
    return ensure_memory_dir() / "latest_meeting.json"


def save_meeting_memory(
    source_location: str,
    meeting_text: str,
    summary_text: str,
    memory_path: str | None = None,
) -> str:
    target = Path(memory_path).expanduser().resolve() if memory_path else default_memory_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "source_location": source_location,
        "meeting_text": meeting_text,
        "summary_text": summary_text,
    }
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(target)


def load_meeting_memory(memory_path: str | None = None) -> dict:
    target = Path(memory_path).expanduser().resolve() if memory_path else default_memory_path()
    if not target.exists():
        raise FileNotFoundError(f"Meeting memory file does not exist: {target}")
    return json.loads(target.read_text(encoding="utf-8"))
