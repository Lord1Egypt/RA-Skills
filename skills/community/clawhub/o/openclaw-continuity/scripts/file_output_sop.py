#!/usr/bin/env python3
import argparse
import json
import shutil
from pathlib import Path

from send2trash import send2trash


DESTINATION_MAP = {
    "screenshot": "assistant-workspace/captures",
    "webpage": "assistant-workspace/web-cache",
    "download": "assistant-workspace/downloads",
    "monitor_report": "assistant-workspace/monitoring",
}


def resolve_destination_root(workspace_root: Path, file_type: str) -> Path:
    rel = DESTINATION_MAP.get(file_type)
    if not rel:
        raise ValueError(f"unsupported file_type: {file_type}")
    return workspace_root / rel


def unique_destination_path(destination_root: Path, source_path: Path) -> Path:
    destination_root.mkdir(parents=True, exist_ok=True)
    target = destination_root / source_path.name
    if not target.exists():
        return target
    stem = source_path.stem
    suffix = source_path.suffix
    counter = 1
    while True:
        candidate = destination_root / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def handle_output_file(source_path, file_type, workspace_root):
    source = Path(source_path).expanduser().resolve()
    root = Path(workspace_root).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(source)
    destination_root = resolve_destination_root(root, file_type)
    destination_path = unique_destination_path(destination_root, source)
    shutil.move(str(source), str(destination_path))
    print(f"✅ 已輸出到專區：{destination_path}")
    send2trash(str(destination_path))
    print(f"🗑 已移至垃圾桶待人工驗收（未永久刪除）：{destination_path}")
    return {
        "destination": str(destination_path),
        "trashed_path": str(destination_path),
        "status": "ok",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path")
    parser.add_argument("file_type", choices=sorted(DESTINATION_MAP))
    parser.add_argument("workspace_root")
    args = parser.parse_args()
    result = handle_output_file(args.source_path, args.file_type, args.workspace_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
