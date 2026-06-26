#!/usr/bin/env python
import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path


TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"


def now_ts() -> str:
    return datetime.now().strftime(TIMESTAMP_FMT)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> dict:
    if not path.exists():
        return {
            "user_profiles": {},
            "knowledge_base": [],
            "assistant_knowledge": [],
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    ensure_parent(path)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def user_file(data_root: Path, user_id: str) -> Path:
    return data_root / "users" / user_id / "long_term_user.json"


def assistant_file(data_root: Path, assistant_id: str) -> Path:
    return data_root / "assistants" / assistant_id / "long_term_assistant.json"


def backup_file(path: Path, backup_dir: Path) -> Path | None:
    if not path.exists():
        return None
    ensure_parent(backup_dir / "placeholder")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = backup_dir / f"{path.stem}.{stamp}.bak.json"
    shutil.copy2(path, backup_path)
    return backup_path


def summarize(data_root: Path, user_id: str, assistant_id: str | None) -> dict:
    user_data = load_json(user_file(data_root, user_id))
    profile = user_data.get("user_profiles", {}).get(user_id, {})
    assistant_data = load_json(assistant_file(data_root, assistant_id)) if assistant_id else None
    return {
        "data_root": str(data_root),
        "user_id": user_id,
        "assistant_id": assistant_id,
        "user_profile_exists": bool(profile.get("data")),
        "user_profile_last_updated": profile.get("last_updated"),
        "user_knowledge_count": len(user_data.get("knowledge_base", [])),
        "assistant_knowledge_count_in_user_file": len(user_data.get("assistant_knowledge", [])),
        "assistant_knowledge_count": (
            len(assistant_data.get("assistant_knowledge", [])) if assistant_data else None
        ),
    }


def search_entries(entries: list[dict], query: str, limit: int) -> list[dict]:
    query_l = query.lower()
    matches = []
    for entry in entries:
        text = entry.get("knowledge", "")
        if query_l in text.lower():
            matches.append(
                {
                    "knowledge": text,
                    "timestamp": entry.get("timestamp"),
                }
            )
        if len(matches) >= limit:
            break
    return matches


def add_user_knowledge(data_root: Path, user_id: str, text: str) -> dict:
    path = user_file(data_root, user_id)
    data = load_json(path)
    data.setdefault("knowledge_base", []).append(
        {
            "knowledge": text,
            "timestamp": now_ts(),
            "knowledge_embedding": [],
        }
    )
    save_json(path, data)
    return {"path": str(path), "user_knowledge_count": len(data["knowledge_base"])}


def add_assistant_knowledge(data_root: Path, assistant_id: str, text: str) -> dict:
    path = assistant_file(data_root, assistant_id)
    data = load_json(path)
    data.setdefault("assistant_knowledge", []).append(
        {
            "knowledge": text,
            "timestamp": now_ts(),
            "knowledge_embedding": [],
        }
    )
    save_json(path, data)
    return {"path": str(path), "assistant_knowledge_count": len(data["assistant_knowledge"])}


def set_profile(data_root: Path, user_id: str, profile_text: str) -> dict:
    path = user_file(data_root, user_id)
    data = load_json(path)
    data.setdefault("user_profiles", {})[user_id] = {
        "data": profile_text,
        "last_updated": now_ts(),
    }
    save_json(path, data)
    return {"path": str(path), "profile_length": len(profile_text)}


def export_markdown(data_root: Path, user_id: str, assistant_id: str | None, output: Path) -> dict:
    user_data = load_json(user_file(data_root, user_id))
    profile = user_data.get("user_profiles", {}).get(user_id, {})
    user_knowledge = user_data.get("knowledge_base", [])
    assistant_knowledge = []
    if assistant_id:
        assistant_knowledge = load_json(assistant_file(data_root, assistant_id)).get(
            "assistant_knowledge", []
        )

    lines = [
        f"# MemoryOS Export",
        "",
        f"- Generated: {now_ts()}",
        f"- Data root: `{data_root}`",
        f"- User ID: `{user_id}`",
        f"- Assistant ID: `{assistant_id or ''}`",
        "",
        "## User Profile",
        "",
        profile.get("data", "None"),
        "",
        "## User Knowledge",
        "",
    ]

    if user_knowledge:
        for item in user_knowledge:
            lines.append(f"- {item.get('knowledge', '')} ({item.get('timestamp', '')})")
    else:
        lines.append("- None")

    lines.extend(["", "## Assistant Knowledge", ""])
    if assistant_knowledge:
        for item in assistant_knowledge:
            lines.append(f"- {item.get('knowledge', '')} ({item.get('timestamp', '')})")
    else:
        lines.append("- None")

    ensure_parent(output)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"output": str(output)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Administer MemoryOS long-term memory files.")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p: argparse.ArgumentParser, need_assistant: bool = False) -> None:
        p.add_argument("--data-root", required=True, type=Path)
        p.add_argument("--user-id")
        if need_assistant:
            p.add_argument("--assistant-id", required=True)
        else:
            p.add_argument("--assistant-id")

    p = sub.add_parser("summary")
    add_common(p)

    p = sub.add_parser("backup")
    add_common(p)
    p.add_argument("--backup-dir", type=Path)

    p = sub.add_parser("search-user")
    add_common(p)
    p.add_argument("--query", required=True)
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("search-assistant")
    add_common(p, need_assistant=True)
    p.add_argument("--query", required=True)
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("add-user-knowledge")
    add_common(p)
    p.add_argument("--text", required=True)

    p = sub.add_parser("add-assistant-knowledge")
    add_common(p, need_assistant=True)
    p.add_argument("--text", required=True)

    p = sub.add_parser("set-profile")
    add_common(p)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--text")
    group.add_argument("--profile-file", type=Path)

    p = sub.add_parser("export-markdown")
    add_common(p)
    p.add_argument("--output", required=True, type=Path)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command in {"summary", "backup", "search-user", "add-user-knowledge", "set-profile", "export-markdown"} and not args.user_id:
        parser.error("--user-id is required for this command")

    if args.command == "summary":
        print(json.dumps(summarize(args.data_root, args.user_id, args.assistant_id), ensure_ascii=False, indent=2))
        return 0

    if args.command == "backup":
        backup_dir = args.backup_dir or (args.data_root / "_backups")
        result = {}
        if args.user_id:
            result["user_backup"] = str(
                backup_file(user_file(args.data_root, args.user_id), backup_dir) or ""
            )
        if args.assistant_id:
            result["assistant_backup"] = str(
                backup_file(assistant_file(args.data_root, args.assistant_id), backup_dir) or ""
            )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "search-user":
        data = load_json(user_file(args.data_root, args.user_id))
        print(json.dumps(search_entries(data.get("knowledge_base", []), args.query, args.limit), ensure_ascii=False, indent=2))
        return 0

    if args.command == "search-assistant":
        data = load_json(assistant_file(args.data_root, args.assistant_id))
        print(json.dumps(search_entries(data.get("assistant_knowledge", []), args.query, args.limit), ensure_ascii=False, indent=2))
        return 0

    if args.command == "add-user-knowledge":
        print(json.dumps(add_user_knowledge(args.data_root, args.user_id, args.text), ensure_ascii=False, indent=2))
        return 0

    if args.command == "add-assistant-knowledge":
        print(json.dumps(add_assistant_knowledge(args.data_root, args.assistant_id, args.text), ensure_ascii=False, indent=2))
        return 0

    if args.command == "set-profile":
        profile_text = args.text if args.text is not None else args.profile_file.read_text(encoding="utf-8")
        print(json.dumps(set_profile(args.data_root, args.user_id, profile_text), ensure_ascii=False, indent=2))
        return 0

    if args.command == "export-markdown":
        print(json.dumps(export_markdown(args.data_root, args.user_id, args.assistant_id, args.output), ensure_ascii=False, indent=2))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
