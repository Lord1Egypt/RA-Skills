#!/usr/bin/env python3
import argparse
import csv
import json
import mimetypes
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

MEDIA_EXTS = {
    ".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".ts", ".mpg", ".mpeg",
    ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".aiff", ".wma",
}


def is_media_file(path: Path) -> bool:
    if path.suffix.lower() in MEDIA_EXTS:
        return True
    mime, _ = mimetypes.guess_type(str(path))
    return bool(mime and (mime.startswith("audio/") or mime.startswith("video/")))


def human_bytes(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    val = float(size)
    for unit in units:
        if val < 1024 or unit == units[-1]:
            return f"{val:.1f} {unit}" if unit != "B" else f"{int(val)} B"
        val /= 1024
    return f"{size} B"


def probe_media(path: Path) -> Dict:
    cmd = [
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", str(path)
    ]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        data = json.loads(out)
    except Exception as e:
        return {"probe_error": str(e)}

    streams = data.get("streams", [])
    fmt = data.get("format", {})
    has_video = any(s.get("codec_type") == "video" for s in streams)
    has_audio = any(s.get("codec_type") == "audio" for s in streams)

    duration = fmt.get("duration")
    duration_sec: Optional[float] = None
    if duration is not None:
        try:
            duration_sec = float(duration)
        except ValueError:
            duration_sec = None

    media_type = "video" if has_video else "audio" if has_audio else "unknown"
    return {
        "media_type": media_type,
        "duration_seconds": duration_sec,
        "stream_count": len(streams),
        "has_audio": has_audio,
        "has_video": has_video,
    }


def gather_files(target: Path) -> List[Path]:
    if target.is_file():
        return [target] if is_media_file(target) else []
    files = []
    for p in target.rglob("*"):
        if p.is_file() and is_media_file(p):
            files.append(p)
    return sorted(files)


def fmt_dt(ts: float) -> str:
    return datetime.fromtimestamp(ts).isoformat(timespec="seconds")


def fmt_duration(seconds: Optional[float]) -> str:
    if seconds is None:
        return ""
    total = int(round(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Scan local media files and produce candidate lists.")
    ap.add_argument("target", help="File or directory to scan")
    ap.add_argument("--out-dir", default="./media_scan", help="Output directory")
    args = ap.parse_args()

    target = Path(args.target).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    files = gather_files(target)
    rows = []
    audio_count = 0
    video_count = 0

    for path in files:
        st = path.stat()
        probe = probe_media(path)
        media_type = probe.get("media_type", "unknown")
        if media_type == "audio":
            audio_count += 1
        elif media_type == "video":
            video_count += 1
        rows.append({
            "filename": path.name,
            "path": str(path),
            "duration": fmt_duration(probe.get("duration_seconds")),
            "duration_seconds": probe.get("duration_seconds"),
            "type": media_type,
            "file_size_bytes": st.st_size,
            "file_size": human_bytes(st.st_size),
            "modified_time": fmt_dt(st.st_mtime),
        })

    payload = {
        "scanned_path": str(target),
        "files_found": len(rows),
        "audio_files": audio_count,
        "video_files": video_count,
        "files": rows,
    }

    json_path = out_dir / "scan_results.json"
    csv_path = out_dir / "scan_results.csv"
    md_path = out_dir / "scan_results.md"

    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "filename", "path", "duration", "duration_seconds", "type",
            "file_size_bytes", "file_size", "modified_time"
        ])
        writer.writeheader()
        writer.writerows(rows)

    md_lines = [
        "# Media Scan Report",
        "",
        "## Summary",
        f"- scanned path: `{target}`",
        f"- files found: {len(rows)}",
        f"- audio files: {audio_count}",
        f"- video files: {video_count}",
        "",
        "## Candidates",
        "| filename | duration | type | file size | modified time |",
        "|---|---:|---|---:|---|",
    ]
    for row in rows:
        md_lines.append(
            f"| {row['filename']} | {row['duration'] or '-'} | {row['type']} | {row['file_size']} | {row['modified_time']} |"
        )
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(str(json_path))
    print(str(csv_path))
    print(str(md_path))


if __name__ == "__main__":
    main()
