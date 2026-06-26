#!/usr/bin/env python3
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def run_ffprobe(path: Path) -> Dict[str, Any]:
    cmd = ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)]
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    return json.loads(out)


def fmt_duration(seconds: Optional[float]) -> str:
    if seconds is None:
        return ""
    total = int(round(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def ts(seconds: Optional[float]) -> str:
    return fmt_duration(seconds)


def whisper_available() -> Tuple[bool, str]:
    if shutil.which("whisper"):
        return True, "cli"
    try:
        import whisper  # type: ignore
        return True, "python"
    except Exception:
        return False, ""


def transcribe_with_cli(path: Path, out_dir: Path) -> Optional[Dict[str, Any]]:
    txt_dir = out_dir / "whisper_raw"
    txt_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "whisper", str(path),
        "--task", "transcribe",
        "--output_format", "json",
        "--output_dir", str(txt_dir),
    ]
    subprocess.check_call(cmd)
    json_path = txt_dir / f"{path.stem}.json"
    if not json_path.exists():
        return None
    return json.loads(json_path.read_text(encoding="utf-8"))


def transcribe_with_python(path: Path) -> Optional[Dict[str, Any]]:
    import whisper  # type: ignore
    model = whisper.load_model("base")
    result = model.transcribe(str(path))
    return result


def simple_summary(text: str, max_sentences: int = 5) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return ""
    sentences = re.split(r"(?<=[.!?。！？])\s+", cleaned)
    if len(sentences) <= max_sentences:
        return " ".join(s.strip() for s in sentences if s.strip())
    words = re.findall(r"[\w']+", cleaned.lower())
    stop = {
        "the", "a", "an", "and", "or", "but", "to", "of", "in", "on", "for", "with",
        "is", "are", "was", "were", "be", "it", "that", "this", "as", "at", "by", "from",
        "i", "you", "we", "they", "he", "she", "them", "our", "your", "not", "have", "has",
    }
    freq = Counter(w for w in words if len(w) > 2 and w not in stop)
    scored = []
    for idx, sent in enumerate(sentences):
        tokens = re.findall(r"[\w']+", sent.lower())
        score = sum(freq.get(t, 0) for t in tokens)
        scored.append((score, idx, sent.strip()))
    top = sorted(scored, reverse=True)[:max_sentences]
    ordered = [s for _, _, s in sorted(top, key=lambda x: x[1]) if s]
    return " ".join(ordered)


def extract_key_excerpts(transcript: Dict[str, Any], limit: int = 8) -> List[Dict[str, Any]]:
    segments = transcript.get("segments") or []
    excerpts: List[Dict[str, Any]] = []
    for seg in segments:
        text = re.sub(r"\s+", " ", str(seg.get("text", "")).strip())
        if len(text) < 30:
            continue
        start = seg.get("start")
        end = seg.get("end")
        excerpts.append({
            "start_seconds": start,
            "end_seconds": end,
            "start": ts(start if isinstance(start, (int, float)) else None),
            "end": ts(end if isinstance(end, (int, float)) else None),
            "text": text,
            "score": len(text),
        })
    excerpts = sorted(excerpts, key=lambda x: x["score"], reverse=True)[:limit]
    excerpts = sorted(excerpts, key=lambda x: (x["start_seconds"] is None, x["start_seconds"]))
    for item in excerpts:
        item.pop("score", None)
    return excerpts


def file_record(path: Path, probe: Dict[str, Any]) -> Dict[str, Any]:
    st = path.stat()
    fmt = probe.get("format", {})
    streams = probe.get("streams", [])
    duration = None
    try:
        if fmt.get("duration") is not None:
            duration = float(fmt["duration"])
    except Exception:
        duration = None
    codecs = [s.get("codec_name") for s in streams if s.get("codec_name")]
    return {
        "path": str(path),
        "filename": path.name,
        "type": "video" if any(s.get("codec_type") == "video" for s in streams) else "audio",
        "duration": fmt_duration(duration),
        "duration_seconds": duration,
        "file_size_bytes": st.st_size,
        "modified_time": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
        "format_name": fmt.get("format_name"),
        "bit_rate": fmt.get("bit_rate"),
        "codecs": codecs,
        "stream_count": len(streams),
    }


def analyze_one(path: Path, per_file_dir: Path) -> Dict[str, Any]:
    probe = run_ffprobe(path)
    record = file_record(path, probe)
    whisper_ok, mode = whisper_available()
    transcript = None
    transcript_status = "unavailable"
    transcript_text = ""
    if whisper_ok:
        try:
            transcript = transcribe_with_cli(path, per_file_dir) if mode == "cli" else transcribe_with_python(path)
            if transcript:
                transcript_status = "available"
                transcript_text = transcript.get("text", "").strip()
        except Exception as e:
            transcript_status = f"failed: {e}"
    summary = simple_summary(transcript_text) if transcript_text else ""
    excerpts = extract_key_excerpts(transcript) if transcript else []
    record.update({
        "transcript_status": transcript_status,
        "whisper_used": bool(whisper_ok),
        "summary": summary,
        "key_excerpts": excerpts,
        "transcript_text": transcript_text,
    })
    transcript_json = per_file_dir / f"{path.stem}_analysis.json"
    transcript_json.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def write_reports(records: List[Dict[str, Any]], out_dir: Path) -> None:
    json_path = out_dir / "report.json"
    csv_path = out_dir / "report.csv"
    md_path = out_dir / "report.md"

    json_path.write_text(json.dumps({"files": records}, ensure_ascii=False, indent=2), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "filename", "path", "type", "duration", "duration_seconds", "file_size_bytes",
            "modified_time", "format_name", "bit_rate", "stream_count", "transcript_status",
            "whisper_used", "summary"
        ])
        writer.writeheader()
        for r in records:
            row = {k: r.get(k) for k in writer.fieldnames}
            writer.writerow(row)

    lines = ["# Media Analysis Report", ""]
    for r in records:
        lines.extend([
            f"## File: {r['filename']}",
            f"- path: `{r['path']}`",
            f"- type: {r['type']}",
            f"- duration: {r['duration'] or '-'}",
            f"- size (bytes): {r['file_size_bytes']}",
            f"- modified time: {r['modified_time']}",
            "",
            "### Technical metadata",
            f"- format: {r.get('format_name') or '-'}",
            f"- codecs: {', '.join(r.get('codecs') or []) or '-'}",
            f"- bit rate: {r.get('bit_rate') or '-'}",
            f"- stream count: {r.get('stream_count')}",
            "",
            "### Transcript status",
            f"- available: {'yes' if r.get('transcript_status') == 'available' else 'no'}",
            f"- whisper used: {'yes' if r.get('whisper_used') else 'no'}",
            f"- detail: {r.get('transcript_status')}",
            "",
            "### Summary",
            r.get('summary') or "Transcript unavailable or empty; no content summary generated.",
            "",
            "### Key excerpts",
        ])
        excerpts = r.get("key_excerpts") or []
        if excerpts:
            for i, ex in enumerate(excerpts, start=1):
                lines.append(f"{i}. [{ex.get('start') or '?'} - {ex.get('end') or '?'}] {ex.get('text')}")
        else:
            lines.append("No transcript-based key excerpts available.")
        lines.append("")
    lines.extend([
        "## Output files",
        f"- `{md_path.name}`",
        f"- `{json_path.name}`",
        f"- `{csv_path.name}`",
        "",
    ])
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Deep-analyze selected media files.")
    ap.add_argument("files", nargs="+", help="One or more media files to analyze")
    ap.add_argument("--out-dir", default="./media_analysis", help="Output directory")
    args = ap.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for file_str in args.files:
        path = Path(file_str).expanduser().resolve()
        if not path.exists() or not path.is_file():
            print(f"Skipping missing file: {path}", file=sys.stderr)
            continue
        per_file_dir = out_dir / path.stem
        per_file_dir.mkdir(parents=True, exist_ok=True)
        try:
            records.append(analyze_one(path, per_file_dir))
        except Exception as e:
            records.append({
                "filename": path.name,
                "path": str(path),
                "type": "unknown",
                "duration": "",
                "duration_seconds": None,
                "file_size_bytes": path.stat().st_size,
                "modified_time": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
                "format_name": None,
                "bit_rate": None,
                "stream_count": None,
                "transcript_status": f"failed: {e}",
                "whisper_used": False,
                "summary": "",
                "key_excerpts": [],
            })

    write_reports(records, out_dir)
    print(str(out_dir / "report.json"))
    print(str(out_dir / "report.csv"))
    print(str(out_dir / "report.md"))


if __name__ == "__main__":
    main()
