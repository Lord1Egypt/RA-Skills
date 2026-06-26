#!/usr/bin/env python3
"""
Photo File Finder — Find photo files by shooting date.

Read EXIF DateTimeOriginal from camera RAW/JPG/HEIC files and filter by date criteria.
Supports all major camera RAW formats (NEF, CR2, CR3, ARW, RAF, ORF, DNG, etc.)

Dependencies:
    None (pure Python EXIF parsing via struct)

    Check & install: bash scripts/setup_deps.sh

Usage:
    python find_by_date.py --date 2026-03-15
    python find_by_date.py --date 03-15
    python find_by_date.py --from 2026-03-10 --to 2026-03-15
    python find_by_date.py --date 2026-03-15 --output result.json
    python find_by_date.py --list-dates

    # Timelapse detection: find sequences with regular shooting intervals
    python find_by_date.py ~/Photos/RAW --timelapse
    python find_by_date.py ~/Photos/RAW --from 06:00 --to 08:00 --timelapse
    python find_by_date.py ~/Photos/RAW --timelapse --output timelapse.json
"""

import argparse
import json
import os
import re
import struct
import sys
import time
from datetime import datetime, date, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


# ── Supported photo extensions ─────────────────────────────────
RAW_EXTENSIONS = {
    ".nef",
    ".nrw",  # Nikon
    ".cr2",
    ".cr3",
    ".crw",  # Canon
    ".arw",
    ".srf",
    ".sr2",  # Sony
    ".raf",  # Fujifilm
    ".orf",  # Olympus / OM System
    ".rw2",  # Panasonic
    ".pef",  # Pentax
    ".srw",  # Samsung
    ".rwl",  # Leica
    ".dng",  # Adobe DNG
    ".3fr",
    ".fff",  # Hasselblad
    ".iiq",  # Phase One
    ".x3f",  # Sigma
}

JPG_EXTENSIONS = {".jpg", ".jpeg"}

HEIC_EXTENSIONS = {".heic", ".heif"}

# All supported input formats
SUPPORTED_EXTENSIONS = RAW_EXTENSIONS | JPG_EXTENSIONS | HEIC_EXTENSIONS


# ── Configuration ───────────────────────────────────────────────

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

_SKILL_DIR = Path(__file__).resolve().parent.parent
_ROOT_DIR = _SKILL_DIR.parent
_DEFAULT_CONFIG_PATH = (
    _SKILL_DIR / "config.toml" if (_SKILL_DIR / "config.toml").exists() else _ROOT_DIR / "config.toml"
)


def load_config(config_path=None):
    """Load configuration from config.toml."""
    path = Path(config_path or _DEFAULT_CONFIG_PATH).expanduser().resolve()
    if not path.exists():
        return {}
    try:
        with open(path, "rb") as f:
            cfg = tomllib.load(f)
        return cfg if isinstance(cfg, dict) else {}
    except Exception:
        return {}


# ── EXIF Date Reader ────────────────────────────────────────────


def _read_uint16(data, offset, big_endian):
    fmt = ">H" if big_endian else "<H"
    return struct.unpack_from(fmt, data, offset)[0]


def _read_uint32(data, offset, big_endian):
    fmt = ">I" if big_endian else "<I"
    return struct.unpack_from(fmt, data, offset)[0]


def read_exif_date(raw_path):
    """
    Read DateTimeOriginal from a camera RAW file's EXIF data.
    Works with NEF, CR2, ARW, DNG, and other TIFF-based RAW formats.
    """
    try:
        with open(raw_path, "rb") as f:
            header = f.read(256 * 1024)

        exif_data = None
        exif_offset = 0

        # Try TIFF header directly (most RAW files: NEF, CR2, ARW, DNG, ORF, PEF, etc.)
        if header[:2] in (b"MM", b"II"):
            exif_data = header
            exif_offset = 0
        else:
            # Look for EXIF APP1 marker (0xFFE1) — JPEG-wrapped formats
            idx = header.find(b"\xff\xe1")
            if idx != -1:
                length = struct.unpack(">H", header[idx + 2 : idx + 4])[0]
                if header[idx + 4 : idx + 10] == b"Exif\x00\x00":
                    exif_data = header[idx + 10 : idx + 2 + length]
                    exif_offset = 0

        # For Fujifilm RAF: look for TIFF header after RAF magic
        if exif_data is None and header[:15] == b"FUJIFILMCCD-RAW":
            # RAF files have TIFF-like EXIF embedded at an offset
            for search_start in range(0, min(len(header) - 2, 4096)):
                if header[search_start : search_start + 2] in (b"MM", b"II"):
                    magic_offset = search_start + 2
                    if magic_offset + 2 <= len(header):
                        try:
                            be = header[search_start : search_start + 2] == b"MM"
                            fmt = ">H" if be else "<H"
                            magic = struct.unpack_from(fmt, header, magic_offset)[0]
                            if magic == 42:
                                exif_data = header[search_start:]
                                exif_offset = 0
                                break
                        except Exception:
                            continue

        if exif_data is None:
            return None

        # Parse TIFF header
        byte_order = exif_data[exif_offset : exif_offset + 2]
        big_endian = byte_order == b"MM"
        if byte_order not in (b"MM", b"II"):
            return None

        magic = _read_uint16(exif_data, exif_offset + 2, big_endian)
        if magic != 42:
            return None

        ifd_offset = _read_uint32(exif_data, exif_offset + 4, big_endian)

        # Walk IFD0 to find ExifIFD pointer (tag 0x8769)
        exif_ifd_offset = _find_tag_in_ifd(exif_data, exif_offset, ifd_offset, 0x8769, big_endian)

        if exif_ifd_offset is not None:
            date_str = _find_string_tag_in_ifd(exif_data, exif_offset, exif_ifd_offset, 0x9003, big_endian)
            if date_str:
                return _parse_exif_datetime(date_str)
            date_str = _find_string_tag_in_ifd(exif_data, exif_offset, exif_ifd_offset, 0x9004, big_endian)
            if date_str:
                return _parse_exif_datetime(date_str)

        date_str = _find_string_tag_in_ifd(exif_data, exif_offset, ifd_offset, 0x0132, big_endian)
        if date_str:
            return _parse_exif_datetime(date_str)

        return None

    except Exception:
        return None


def _find_tag_in_ifd(data, base, ifd_offset, target_tag, big_endian):
    """Find a tag in an IFD and return its value as uint32."""
    try:
        abs_offset = base + ifd_offset
        num_entries = _read_uint16(data, abs_offset, big_endian)
        for i in range(num_entries):
            entry_offset = abs_offset + 2 + i * 12
            tag = _read_uint16(data, entry_offset, big_endian)
            if tag == target_tag:
                value = _read_uint32(data, entry_offset + 8, big_endian)
                return value
        return None
    except Exception:
        return None


def _find_string_tag_in_ifd(data, base, ifd_offset, target_tag, big_endian):
    """Find a string tag in an IFD and return its value."""
    try:
        abs_offset = base + ifd_offset
        num_entries = _read_uint16(data, abs_offset, big_endian)
        for i in range(num_entries):
            entry_offset = abs_offset + 2 + i * 12
            tag = _read_uint16(data, entry_offset, big_endian)
            if tag == target_tag:
                typ = _read_uint16(data, entry_offset + 2, big_endian)
                count = _read_uint32(data, entry_offset + 4, big_endian)
                if typ == 2:  # ASCII
                    if count <= 4:
                        str_data = data[entry_offset + 8 : entry_offset + 8 + count]
                    else:
                        str_offset = _read_uint32(data, entry_offset + 8, big_endian)
                        str_data = data[base + str_offset : base + str_offset + count]
                    return str_data.rstrip(b"\x00").decode("ascii", errors="ignore")
        return None
    except Exception:
        return None


def _parse_exif_datetime(s):
    """Parse EXIF datetime string."""
    try:
        return datetime.strptime(s.strip(), "%Y:%m:%d %H:%M:%S")
    except ValueError:
        try:
            return datetime.strptime(s.strip(), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None


# ── File Finder ─────────────────────────────────────────────────


def find_raw_files(input_path, recursive=False):
    """Find all supported photo files (RAW/JPG/HEIC) in directory."""
    input_path = Path(input_path)
    if input_path.is_file():
        if input_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            return [input_path]
        return []

    results = []
    if recursive:
        for p in sorted(input_path.rglob("*")):
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
                results.append(p)
    else:
        for p in sorted(input_path.iterdir()):
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
                results.append(p)
    return results


def get_file_dates(raw_files, workers=None):
    """Read EXIF dates from multiple RAW files in parallel."""
    max_workers = workers or min(os.cpu_count() or 4, 16)
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(read_exif_date, f): f for f in raw_files}
        for future in as_completed(futures):
            raw_path = futures[future]
            try:
                dt = future.result()
            except Exception:
                dt = None
            results.append((raw_path, dt))

    results.sort(key=lambda x: x[0].name)
    return results


# ── Date Parsing ────────────────────────────────────────────────


def parse_date_arg(date_str, reference_year=None):
    """
    Parse a flexible date string into a date object.

    Supported formats:
        2026-03-15, 2026/03/15, 03-15, 3-15, 0315,
        3月15日, 3月15, today, yesterday, "3 days ago"
    """
    if reference_year is None:
        reference_year = datetime.now().year

    s = date_str.strip()

    if s.lower() == "today":
        return date.today()
    if s.lower() == "yesterday":
        return date.today() - timedelta(days=1)

    m = re.match(r"(\d+)\s*days?\s*ago", s, re.IGNORECASE)
    if m:
        return date.today() - timedelta(days=int(m.group(1)))

    m = re.match(r"(\d{1,2})月(\d{1,2})日?$", s)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        return date(reference_year, month, day)

    m = re.match(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})$", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    m = re.match(r"(\d{1,2})[-/](\d{1,2})$", s)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        return date(reference_year, month, day)

    m = re.match(r"(\d{2})(\d{2})$", s)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        if 1 <= month <= 12 and 1 <= day <= 31:
            return date(reference_year, month, day)

    raise ValueError(
        f"无法解析日期: '{date_str}'。支持格式: 2026-03-15, 03-15, 3月15日, today, yesterday, '3 days ago'"
    )


# ── Timelapse Sequence Detection ────────────────────────────────


def detect_timelapse_sequences(file_dates, min_sequence=30, interval_tolerance=0.5):
    """Detect timelapse sequences by finding runs of regular shooting intervals.

    Algorithm:
      1. Sort files by EXIF datetime
      2. Compute intervals between consecutive shots
      3. Scan for runs where the interval stays within median ± tolerance
      4. Return sequences that have at least `min_sequence` frames

    Args:
        file_dates: list of (path, datetime) tuples (None datetimes are skipped)
        min_sequence: minimum number of frames to qualify as a timelapse sequence
        interval_tolerance: max allowed deviation from median interval (as fraction, e.g. 0.5 = 50%)

    Returns:
        list of sequences, each a list of (path, datetime) tuples, sorted by time
    """
    # Filter out files without EXIF time, sort by datetime
    timed = [(p, dt) for p, dt in file_dates if dt is not None]
    timed.sort(key=lambda x: x[1])

    if len(timed) < min_sequence:
        return []

    # Compute intervals in seconds
    intervals = []
    for i in range(1, len(timed)):
        delta = (timed[i][1] - timed[i - 1][1]).total_seconds()
        intervals.append(delta)

    # Scan for consistent-interval runs
    sequences = []
    i = 0
    n = len(intervals)

    while i < n:
        # Start a candidate run from position i
        # Use a small look-ahead window to estimate the interval
        window_size = min(10, n - i)
        if window_size < 2:
            i += 1
            continue

        # Get initial interval estimate from first few frames
        window_intervals = sorted(intervals[i : i + window_size])
        # Use median of the window
        median_interval = window_intervals[len(window_intervals) // 2]

        # Skip if interval is too large (> 60s) or too small (< 0.5s)
        if median_interval < 0.5 or median_interval > 60:
            i += 1
            continue

        # Extend the run as long as intervals match
        lo = median_interval * (1 - interval_tolerance)
        hi = median_interval * (1 + interval_tolerance)

        run_start = i  # index into intervals array; frame index = run_start
        j = i
        while j < n and lo <= intervals[j] <= hi:
            j += 1

        run_length = j - run_start + 1  # number of frames = intervals + 1

        if run_length >= min_sequence:
            # Frame indices: run_start to run_start + run_length (inclusive in timed[])
            seq = timed[run_start : run_start + run_length]
            sequences.append(seq)
            i = j  # skip past this sequence
        else:
            i += 1

    # Merge overlapping/adjacent sequences
    if len(sequences) > 1:
        merged = [sequences[0]]
        for seq in sequences[1:]:
            prev = merged[-1]
            # If this sequence starts before the previous one ends, merge
            if seq[0][1] <= prev[-1][1]:
                # Combine and deduplicate
                combined = {str(p): (p, dt) for p, dt in prev}
                for p, dt in seq:
                    combined[str(p)] = (p, dt)
                merged[-1] = sorted(combined.values(), key=lambda x: x[1])
            else:
                merged.append(seq)
        sequences = merged

    return sequences


def _format_interval(seconds):
    """Format interval in seconds to a human-readable string."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds) // 60
    secs = seconds - minutes * 60
    return f"{minutes}m{secs:.0f}s"


# ── Main ────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="按拍照日期查找相机 RAW 文件（支持 NEF/CR2/CR3/ARW/RAF/ORF/DNG 等）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --date 3月15日
  %(prog)s --date 2026-03-15
  %(prog)s --from 2026-03-10 --to 2026-03-15
  %(prog)s --date 3月15日 --output result.json
  %(prog)s --list-dates

  # Timelapse: detect sequences with regular shooting intervals
  %(prog)s ~/Photos/RAW --timelapse
  %(prog)s ~/Photos/RAW --date today --timelapse --output timelapse.json
  %(prog)s ~/Photos/RAW --timelapse --min-sequence 50
        """,
    )

    parser.add_argument(
        "input", nargs="?", default=None, help="RAW 文件所在目录（默认: config.toml 的 input_dir 或 ~/Downloads/RAW）"
    )
    parser.add_argument("--config", type=str, default=None, help="config.toml 路径")

    date_group = parser.add_argument_group("日期过滤")
    date_group.add_argument("--date", "-d", type=str, default=None, help="精确日期")
    date_group.add_argument("--from", dest="date_from", type=str, default=None, help="起始日期（含）")
    date_group.add_argument("--to", dest="date_to", type=str, default=None, help="结束日期（含）")
    date_group.add_argument("--list-dates", action="store_true", help="列出所有 RAW 文件的拍照日期")

    timelapse_group = parser.add_argument_group("延时序列检测")
    timelapse_group.add_argument(
        "--timelapse", action="store_true", help="检测拍摄间隔规律的延时序列（自动排除散拍照片）"
    )
    timelapse_group.add_argument("--min-sequence", type=int, default=30, help="延时序列最小帧数（默认: 30）")
    timelapse_group.add_argument(
        "--interval-tolerance", type=float, default=0.5, help="间隔容差比例，如 0.5 = 允许 ±50%% 偏差（默认: 0.5）"
    )

    action_group = parser.add_argument_group("输出操作")
    action_group.add_argument("--output", "-o", type=str, default=None, help="结果输出 JSON 路径（默认: stdout）")

    parser.add_argument("--recursive", "-r", action="store_true", help="递归搜索子目录")
    parser.add_argument("--workers", type=int, default=None, help="并行工作线程数")

    args = parser.parse_args()

    if not args.date and not args.date_from and not args.date_to and not args.list_dates and not args.timelapse:
        parser.error("请指定 --date、--from/--to、--list-dates 或 --timelapse 之一")

    cfg = load_config(args.config)
    input_raw = args.input or cfg.get("raw_dir") or cfg.get("input_dir", "~/Downloads/RAW")
    input_path = Path(input_raw).expanduser().resolve()

    if not input_path.exists():
        print(f"❌ 输入目录不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    target_date = None
    from_date = None
    to_date = None

    if args.date:
        target_date = parse_date_arg(args.date)
    if args.date_from:
        from_date = parse_date_arg(args.date_from)
    if args.date_to:
        to_date = parse_date_arg(args.date_to)

    raw_files = find_raw_files(input_path, args.recursive)
    if not raw_files:
        print("📷 未找到 RAW 文件。")
        sys.exit(0)

    # Summarize formats found
    ext_counts = {}
    for f in raw_files:
        ext = f.suffix.upper()
        ext_counts[ext] = ext_counts.get(ext, 0) + 1
    ext_summary = ", ".join(f"{ext}: {cnt}" for ext, cnt in sorted(ext_counts.items()))
    print(f"📷 扫描 {len(raw_files)} 个 RAW 文件的 EXIF 日期... ({ext_summary})", file=sys.stderr)

    start_time = time.monotonic()
    file_dates = get_file_dates(raw_files, args.workers)
    scan_elapsed = time.monotonic() - start_time

    if args.list_dates:
        _print_date_list(file_dates, args)
        return

    # ── Timelapse detection mode ─────────────────────────────────
    if args.timelapse:
        # Optionally pre-filter by date/time range first
        if target_date or from_date or to_date:
            pre_filtered = []
            for raw_path, dt in file_dates:
                if dt is None:
                    continue
                shot_date = dt.date()
                if target_date and shot_date != target_date:
                    continue
                if from_date and shot_date < from_date:
                    continue
                if to_date and shot_date > to_date:
                    continue
                pre_filtered.append((raw_path, dt))
            scan_input = pre_filtered
        else:
            scan_input = file_dates

        sequences = detect_timelapse_sequences(
            scan_input,
            min_sequence=args.min_sequence,
            interval_tolerance=args.interval_tolerance,
        )

        if not sequences:
            print(f"\n😔 未检测到延时序列（最小帧数: {args.min_sequence}）", file=sys.stderr)
            timed_count = sum(1 for _, dt in scan_input if dt is not None)
            print(f"   共分析 {timed_count} 张有 EXIF 时间的照片", file=sys.stderr)
            sys.exit(1)

        # Report all found sequences
        total_frames = 0
        all_matched = []
        for seq_idx, seq in enumerate(sequences, 1):
            # Compute interval stats for this sequence
            seq_intervals = [(seq[i][1] - seq[i - 1][1]).total_seconds() for i in range(1, len(seq))]
            median_interval = sorted(seq_intervals)[len(seq_intervals) // 2]
            start_time_str = seq[0][1].strftime("%Y-%m-%d %H:%M:%S")
            end_time_str = seq[-1][1].strftime("%H:%M:%S")
            duration = (seq[-1][1] - seq[0][1]).total_seconds()

            print(f"\n🎬 延时序列 #{seq_idx}: {len(seq)} 帧", file=sys.stderr)
            print(f"   时间: {start_time_str} → {end_time_str} ({_format_interval(duration)})", file=sys.stderr)
            print(f"   间隔: ~{_format_interval(median_interval)}/帧", file=sys.stderr)
            print(f"   首帧: {seq[0][0].name}", file=sys.stderr)
            print(f"   末帧: {seq[-1][0].name}", file=sys.stderr)

            total_frames += len(seq)
            all_matched.extend(seq)

        # Compute how many were excluded
        timed_total = sum(1 for _, dt in scan_input if dt is not None)
        excluded = timed_total - total_frames
        print(f"\n✅ 共 {len(sequences)} 个延时序列，{total_frames} 帧", file=sys.stderr)
        if excluded > 0:
            print(f"   排除散拍照片: {excluded} 张", file=sys.stderr)

        # Always output JSON to stdout
        result = {
            "mode": "timelapse",
            "sequences": [],
            "total_frames": total_frames,
            "excluded": excluded,
            "scan_time_seconds": round(scan_elapsed, 2),
        }
        for seq_idx, seq in enumerate(sequences, 1):
            seq_intervals = [(seq[i][1] - seq[i - 1][1]).total_seconds() for i in range(1, len(seq))]
            median_interval = sorted(seq_intervals)[len(seq_intervals) // 2]
            result["sequences"].append(
                {
                    "index": seq_idx,
                    "frame_count": len(seq),
                    "start": seq[0][1].strftime("%Y-%m-%d %H:%M:%S"),
                    "end": seq[-1][1].strftime("%Y-%m-%d %H:%M:%S"),
                    "interval_seconds": round(median_interval, 2),
                    "files": [
                        {"file": p.name, "path": str(p), "datetime": dt.strftime("%Y-%m-%d %H:%M:%S")} for p, dt in seq
                    ],
                }
            )
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        print(json_str)

        if args.output:
            output_path = Path(args.output).expanduser().resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json_str, encoding="utf-8")
            print(f"   📄 结果已保存: {output_path}", file=sys.stderr)

        sys.exit(0 if all_matched else 1)

    matched = []
    no_date = []

    for raw_path, dt in file_dates:
        if dt is None:
            no_date.append(raw_path)
            continue
        shot_date = dt.date()
        if target_date:
            if shot_date == target_date:
                matched.append((raw_path, dt))
        else:
            if from_date and shot_date < from_date:
                continue
            if to_date and shot_date > to_date:
                continue
            matched.append((raw_path, dt))

    # Build query_info
    query_info = {}
    if target_date:
        query_info["date"] = target_date.isoformat()
    if from_date:
        query_info["from"] = from_date.isoformat()
    if to_date:
        query_info["to"] = to_date.isoformat()

    _output_result(matched, no_date, input_path, query_info, scan_elapsed, args)

    sys.exit(0 if matched else 1)


def _print_date_list(file_dates, args):
    """Print all files with their shooting dates."""
    items = []
    for raw_path, dt in sorted(file_dates, key=lambda x: (x[1] or datetime.min, x[0].name)):
        items.append(
            {
                "file": raw_path.name,
                "path": str(raw_path),
                "format": raw_path.suffix.upper().lstrip("."),
                "date": dt.strftime("%Y-%m-%d") if dt else None,
                "datetime": dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None,
            }
        )

    # JSON to stdout
    json_str = json.dumps(items, ensure_ascii=False, indent=2)
    print(json_str)

    # Human-readable to stderr
    by_date = {}
    no_date = []
    for raw_path, dt in file_dates:
        if dt is None:
            no_date.append(raw_path)
        else:
            key = dt.date()
            by_date.setdefault(key, []).append((raw_path, dt))

    for d in sorted(by_date.keys()):
        files = by_date[d]
        print(f"\n📅 {d.strftime('%Y-%m-%d')} ({len(files)} 张)", file=sys.stderr)
        for raw_path, dt in sorted(files, key=lambda x: x[1]):
            ext = raw_path.suffix.upper().lstrip(".")
            print(f"   {dt.strftime('%H:%M:%S')}  {raw_path.name} [{ext}]", file=sys.stderr)

    if no_date:
        print(f"\n⚠️  无法读取日期 ({len(no_date)} 张)", file=sys.stderr)
        for p in no_date:
            print(f"   {p.name}", file=sys.stderr)

    # Write to --output file
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json_str, encoding="utf-8")
        print(f"   📄 结果已保存: {output_path}", file=sys.stderr)


def _output_result(matched, no_date, raw_root, query_info, scan_elapsed, args):
    """输出结果：JSON 到 stdout（和 --output 文件），人类可读到 stderr。"""
    result = {
        "raw_root": str(raw_root),
        "query": query_info,
        "files": [str(p) for p, _dt in sorted(matched, key=lambda x: x[1])],
        "file_count": len(matched),
        "no_date_count": len(no_date),
        "scan_time_seconds": round(scan_elapsed, 2),
    }

    # 人类可读输出到 stderr
    date_desc = query_info.get("date") or query_info.get("from", "") + " ~ " + query_info.get("to", "")
    print(f"\n🔍 日期过滤: {date_desc}", file=sys.stderr)
    print(f"   找到 {len(matched)} 张照片，耗时 {scan_elapsed:.1f}s", file=sys.stderr)
    if no_date:
        print(f"   ⚠️  {len(no_date)} 个文件无法读取 EXIF 日期", file=sys.stderr)

    # JSON 输出到 stdout
    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    print(json_str)

    # 同时写入 --output 文件
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json_str, encoding="utf-8")
        print(f"   📄 结果已保存: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
