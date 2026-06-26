import argparse
import json
import os
import platform
import subprocess
from typing import Iterable


SUPPORTED_EXTENSIONS = (".md", ".txt")
EXCLUDED_FILENAMES = {"SKILL.md", "README.md"}


def list_meeting_files(location: str, recursive: bool = False) -> str:
    """
    Return a JSON string with the file count and file list for a meeting-notes directory.
    Prefer OS-native shell commands and fall back to Python enumeration if needed.
    """
    abs_path = os.path.abspath(location)
    if not os.path.exists(abs_path):
        return f"ERROR: Local directory does not exist: {abs_path}"
    if not os.path.isdir(abs_path):
        return f"ERROR: Local path is not a directory: {abs_path}"

    try:
        files = _list_files_with_system_command(abs_path, recursive=recursive)
    except Exception:
        files = _list_files_with_python(abs_path, recursive=recursive)

    note_files = [
        path
        for path in files
        if path.lower().endswith(SUPPORTED_EXTENSIONS)
        and os.path.basename(path) not in EXCLUDED_FILENAMES
    ]
    note_files.sort()

    payload = {
        "directory": abs_path,
        "recursive": recursive,
        "extensions": list(SUPPORTED_EXTENSIONS),
        "total_files": len(note_files),
        "files": note_files,
    }
    return json.dumps(payload, ensure_ascii=True, indent=2)


def _list_files_with_system_command(location: str, recursive: bool) -> list[str]:
    system_name = platform.system().lower()
    if system_name == "windows":
        command = _build_windows_command(location, recursive)
        output = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        return _normalize_paths(output.stdout.splitlines())

    if system_name in {"linux", "darwin"}:
        command = _build_unix_command(location, recursive)
        output = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        return _normalize_paths(output.stdout.splitlines())

    raise RuntimeError(f"Unsupported system for command execution: {system_name}")


def _build_windows_command(location: str, recursive: bool) -> list[str]:
    recurse_flag = " -Recurse" if recursive else ""
    script = (
        "[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false); "
        "$OutputEncoding = [Console]::OutputEncoding; "
        f"Get-ChildItem -LiteralPath '{location}' -File{recurse_flag} | "
        "Select-Object -ExpandProperty FullName"
    )
    return ["powershell", "-NoProfile", "-Command", script]


def _build_unix_command(location: str, recursive: bool) -> list[str]:
    if recursive:
        return ["find", location, "-type", "f"]
    return ["find", location, "-maxdepth", "1", "-type", "f"]


def _list_files_with_python(location: str, recursive: bool) -> list[str]:
    if recursive:
        results: list[str] = []
        for root, _, files in os.walk(location):
            results.extend(os.path.join(root, name) for name in files)
        return results

    with os.scandir(location) as entries:
        return [entry.path for entry in entries if entry.is_file()]


def _normalize_paths(items: Iterable[str]) -> list[str]:
    return [item.strip() for item in items if item and item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List meeting-note files in a directory and return count plus file paths."
    )
    parser.add_argument("location", help="Local directory path")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search subdirectories recursively",
    )
    args = parser.parse_args()
    print(list_meeting_files(args.location, recursive=args.recursive))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
