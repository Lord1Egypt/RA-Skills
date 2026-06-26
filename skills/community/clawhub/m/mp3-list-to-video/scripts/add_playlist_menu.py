#!/usr/bin/env python3
"""为已合并的播放列表 MP4 生成歌曲菜单高亮背景视频。"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import zlib

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = SKILL_DIR.parent.parent.parent

DEFAULT_PLAYLIST_DIR = WORKSPACE_DIR / "playlist"
DEFAULT_SOURCE_VIDEO = WORKSPACE_DIR / "playlist_output.mp4"
DEFAULT_OUTPUT_FILE = WORKSPACE_DIR / "playlist_menu_output.mp4"
DEFAULT_TEMP_DIR = WORKSPACE_DIR / "output"

WIDTH = 1920
HEIGHT = 1080
FPS = 30
ACTIVE_SECONDS = 3.0
ACTIVE_FRAMES = 60
VINYL_SIZE = 360
VINYL_X = 1480
VINYL_Y = 370
VINYL_ROTATION_SECONDS = 4.0
ROW_START_Y = 315
ROW_HEIGHT = 64
ROW_BOX_X = 292
ROW_BOX_W = 1018
NUMBER_X = 332
TIME_X = 420
TITLE_X = 710
FONT_NAME = "Hiragino Sans GB"


def natural_key(path):
    return [
        int(part) if part.isdigit() else part.casefold()
        for part in re.split(r"(\d+)", Path(path).name)
    ]


def resolve_path(value):
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    return path.resolve()


def run_command(cmd, label, cwd=None):
    try:
        return subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=cwd)
    except FileNotFoundError as exc:
        raise RuntimeError(f"{label} 未找到: {cmd[0]}") from exc
    except subprocess.CalledProcessError as exc:
        if exc.stdout:
            print(exc.stdout, file=sys.stderr)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        raise RuntimeError(f"{label} 失败，退出码: {exc.returncode}") from exc


def check_dependencies():
    missing = [tool for tool in ("ffmpeg", "ffprobe") if shutil.which(tool) is None]
    if missing:
        raise RuntimeError(f"缺少依赖: {', '.join(missing)}")

    filters = run_command(["ffmpeg", "-hide_banner", "-filters"], "ffmpeg filters").stdout
    required_filters = ("ass", "rotate", "overlay")
    missing_filters = [name for name in required_filters if f" {name} " not in filters]
    if missing_filters:
        raise RuntimeError(
            f"当前 ffmpeg 缺少滤镜: {', '.join(missing_filters)}，无法渲染菜单和黑胶动效"
        )

    print("依赖检查通过:")
    print(f"  - ffmpeg: {shutil.which('ffmpeg')}")
    print(f"  - ffprobe: {shutil.which('ffprobe')}")
    print(f"  - ffmpeg filters: {', '.join(required_filters)}")


def get_mp3_files(playlist_dir):
    if not playlist_dir.is_dir():
        raise RuntimeError(f"playlist 目录不存在: {playlist_dir}")

    files = sorted(playlist_dir.glob("*.mp3"), key=natural_key)
    if not files:
        raise RuntimeError(f"未找到 MP3 文件: {playlist_dir}")
    return files


def probe_duration(path):
    result = run_command(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        "ffprobe",
    )
    try:
        duration = float(result.stdout.strip())
    except ValueError as exc:
        raise RuntimeError(f"无法读取时长: {path}") from exc

    if duration <= 0:
        raise RuntimeError(f"时长无效: {path}")
    return duration


def strip_track_prefix(path):
    title = path.stem.strip()
    return re.sub(r"^\d+[\s._-]*", "", title).strip() or title


def build_timeline(mp3_files, source_video):
    source_duration = probe_duration(source_video)
    cursor = 0.0
    tracks = []

    for index, path in enumerate(mp3_files, start=1):
        duration = probe_duration(path)
        start = cursor
        end = start + duration
        tracks.append(
            {
                "index": index,
                "file": str(path),
                "title": strip_track_prefix(path),
                "start": start,
                "end": end,
                "duration": duration,
            }
        )
        cursor = end

    if tracks and abs(source_duration - cursor) > 0.25:
        tracks[-1]["end"] = max(tracks[-1]["start"] + 0.01, source_duration)
        tracks[-1]["duration"] = tracks[-1]["end"] - tracks[-1]["start"]

    return tracks, source_duration


def format_ass_time(seconds):
    seconds = max(0.0, seconds)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    if centis == 100:
        secs += 1
        centis = 0
    if secs == 60:
        minutes += 1
        secs = 0
    if minutes == 60:
        hours += 1
        minutes = 0
    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"


def format_clock(seconds):
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_seek_time(seconds):
    seconds = max(0.0, seconds)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis == 1000:
        secs += 1
        millis = 0
    if secs == 60:
        minutes += 1
        secs = 0
    if minutes == 60:
        hours += 1
        minutes = 0
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def parse_timecode(value):
    parts = value.strip().split(":")
    if not parts or any(part == "" for part in parts):
        raise RuntimeError(f"预览时间格式无效: {value}")

    try:
        numbers = [float(part) for part in parts]
    except ValueError as exc:
        raise RuntimeError(f"预览时间格式无效: {value}") from exc

    if len(numbers) == 1:
        return numbers[0]
    if len(numbers) == 2:
        return numbers[0] * 60 + numbers[1]
    if len(numbers) == 3:
        return numbers[0] * 3600 + numbers[1] * 60 + numbers[2]
    raise RuntimeError(f"预览时间格式无效: {value}")


def preview_filename_time(seconds):
    return format_clock(seconds).replace(":", "-")


def md5_file(path):
    digest = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_chunk(chunk_type, data):
    return (
        struct.pack(">I", len(data))
        + chunk_type
        + data
        + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    )


def write_rgba_png(path, width, height, pixels):
    raw = bytearray()
    stride = width * 4
    for y in range(height):
        raw.append(0)
        start = y * stride
        raw.extend(pixels[start:start + stride])

    data = bytearray()
    data.extend(b"\x89PNG\r\n\x1a\n")
    data.extend(png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)))
    data.extend(png_chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
    data.extend(png_chunk(b"IEND", b""))
    path.write_bytes(data)


def generate_vinyl_png(path, size):
    center = (size - 1) / 2.0
    outer = size * 0.49
    inner = size * 0.18
    label = size * 0.105
    hole = size * 0.028
    pixels = bytearray(size * size * 4)

    for y in range(size):
        for x in range(size):
            dx = x - center
            dy = y - center
            radius = math.hypot(dx, dy)
            offset = (y * size + x) * 4

            if radius > outer:
                continue

            angle = math.atan2(dy, dx)
            ring = 0.5 + 0.5 * math.sin(radius * 0.42)
            groove = 0.5 + 0.5 * math.sin(radius * 1.15 + angle * 12.0)
            sheen = max(0.0, math.cos(angle - 0.75)) ** 18
            alpha_edge = min(1.0, max(0.0, outer - radius))
            alpha = int(255 * min(1.0, alpha_edge))

            if radius <= hole:
                color = (18, 18, 16)
                alpha = 255
            elif radius <= label:
                warm = int(138 + 28 * math.sin(angle * 2.0 + radius * 0.06))
                color = (warm, 112, 54)
            elif radius <= inner:
                color = (36, 34, 31)
            else:
                base = int(20 + ring * 8 + groove * 12 + sheen * 70)
                color = (base, base, base + 2)

            pixels[offset:offset + 4] = bytes((color[0], color[1], color[2], alpha))

    # Add a diagonal highlight that makes rotation visible.
    for y in range(size):
        for x in range(size):
            dx = x - center
            dy = y - center
            radius = math.hypot(dx, dy)
            if inner < radius < outer * 0.96:
                distance = abs(dy - dx * 0.34)
                if distance < size * 0.018 and dx > -size * 0.12:
                    offset = (y * size + x) * 4
                    blend = max(0.0, 1.0 - distance / (size * 0.018)) * 0.35
                    for channel in range(3):
                        pixels[offset + channel] = min(255, int(pixels[offset + channel] * (1 - blend) + 185 * blend))

    path.parent.mkdir(parents=True, exist_ok=True)
    write_rgba_png(path, size, size, pixels)
    return path


def ass_text(value):
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("\n", "\\N")
    )


def ass_rect(x, y, width, height):
    return f"{{\\an7\\pos({x},{y})\\p1}}m 0 0 l {width} 0 l {width} {height} l 0 {height}"


def ass_line(layer, start, end, style, text):
    return (
        f"Dialogue: {layer},{format_ass_time(start)},{format_ass_time(end)},"
        f"{style},,0,0,0,,{text}"
    )


def pos_text(x, y, text):
    return f"{{\\an7\\pos({x},{y})}}{ass_text(text)}"


def write_ass(tracks, total_duration, ass_path):
    ass_path.parent.mkdir(parents=True, exist_ok=True)
    total = format_ass_time(total_duration)
    meta = f"{len(tracks)} songs | {format_clock(total_duration)}"

    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {WIDTH}",
        f"PlayResY: {HEIGHT}",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "YCbCr Matrix: TV.709",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, "
        "ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
        "MarginL, MarginR, MarginV, Encoding",
        f"Style: Title,{FONT_NAME},74,&H00E8F0F4,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        f"Style: Meta,{FONT_NAME},30,&H00A7AAA8,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        f"Style: Row,{FONT_NAME},38,&H00B3A79E,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        f"Style: RowActive,{FONT_NAME},42,&H00F8F4EC,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        "Style: Panel,Arial,1,&H00262420,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        "Style: Highlight,Arial,1,&H00575E28,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        "Style: Accent,Arial,1,&H0041B3E3,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,0,7,0,0,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        ass_line(0, 0, total_duration, "Panel", ass_rect(250, 240, 1420, 700)),
        ass_line(1, 0, total_duration, "Accent", ass_rect(250, 240, 10, 700)),
        ass_line(2, 0, total_duration, "Title", pos_text(250, 105, "Playlist")),
        ass_line(2, 0, total_duration, "Meta", pos_text(256, 188, meta)),
    ]

    for track in tracks:
        y = ROW_START_Y + (track["index"] - 1) * ROW_HEIGHT
        time_range = f"{format_clock(track['start'])} - {format_clock(track['end'])}"
        lines.extend(
            [
                ass_line(2, 0, total_duration, "Row", pos_text(NUMBER_X, y, f"{track['index']:02d}")),
                ass_line(2, 0, total_duration, "Row", pos_text(TIME_X, y, time_range)),
                ass_line(2, 0, total_duration, "Row", pos_text(TITLE_X, y, track["title"])),
            ]
        )

    for track in tracks:
        start = track["start"]
        end = min(track["end"], total_duration)
        if end <= start:
            continue

        y = ROW_START_Y + (track["index"] - 1) * ROW_HEIGHT
        box_y = y - 10
        time_range = f"{format_clock(track['start'])} - {format_clock(track['end'])}"
        lines.extend(
            [
                ass_line(3, start, end, "Highlight", ass_rect(ROW_BOX_X, box_y, ROW_BOX_W, 58)),
                ass_line(4, start, end, "Accent", ass_rect(ROW_BOX_X, box_y, 8, 58)),
                ass_line(5, start, end, "RowActive", pos_text(NUMBER_X, y - 2, f"{track['index']:02d}")),
                ass_line(5, start, end, "RowActive", pos_text(TIME_X, y - 2, time_range)),
                ass_line(5, start, end, "RowActive", pos_text(TITLE_X, y - 2, track["title"])),
            ]
        )

    ass_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_timeline_json(tracks, total_duration, output_path):
    data = {
        "total_duration": total_duration,
        "total_duration_text": format_clock(total_duration),
        "tracks": [
            {
                **track,
                "start_text": format_clock(track["start"]),
                "end_text": format_clock(track["end"]),
                "duration_text": format_clock(track["duration"]),
            }
            for track in tracks
        ],
    }
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def quote_concat_path(path):
    return "'" + str(path.resolve()).replace("'", "'\\''") + "'"


def filter_path(path, cwd):
    try:
        value = str(path.relative_to(cwd))
    except ValueError:
        value = str(path)
    return value.replace("\\", "\\\\").replace("'", "\\'")


def render_full_menu_video(ass_path, duration, menu_video_path):
    menu_video_path.parent.mkdir(parents=True, exist_ok=True)
    ass_filter = f"ass=filename='{filter_path(ass_path, WORKSPACE_DIR)}'"
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c=0x111214:size={WIDTH}x{HEIGHT}:rate={FPS}:duration={duration:.3f}",
        "-vf", ass_filter,
        "-an",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(menu_video_path),
    ]
    print(f"正在生成整段菜单背景视频: {menu_video_path}")
    run_command(cmd, "ffmpeg", cwd=WORKSPACE_DIR)


def build_smart_frame_plan(tracks, total_duration, active_seconds, active_frames):
    frames = []
    min_step = 1.0 / FPS
    active_frames = max(1, active_frames)

    for track in tracks:
        track_start = max(0.0, track["start"])
        track_end = min(track["end"], total_duration)
        if track_end <= track_start:
            continue

        active_end = min(track_start + active_seconds, track_end)
        active_duration = active_end - track_start

        if active_duration > 0:
            if active_frames == 1:
                times = [track_start]
            else:
                step = active_duration / active_frames
                times = [track_start + index * step for index in range(active_frames)]

            for index, timestamp in enumerate(times):
                next_time = times[index + 1] if index + 1 < len(times) else active_end
                duration = max(next_time - timestamp, min_step)
                frames.append(
                    {
                        "time": min(timestamp, total_duration - 0.001),
                        "duration": duration,
                        "track_index": track["index"],
                        "kind": "active",
                    }
                )

        if track_end - active_end > min_step:
            frames.append(
                {
                    "time": min(active_end, total_duration - 0.001),
                    "duration": track_end - active_end,
                    "track_index": track["index"],
                    "kind": "static",
                }
            )

    if frames:
        total = sum(frame["duration"] for frame in frames)
        drift = total_duration - total
        frames[-1]["duration"] = max(frames[-1]["duration"] + drift, min_step)

    return frames


def render_menu_frame(ass_path, frame, frame_path):
    ass_filter = f"setpts=PTS+{frame['time']:.6f}/TB,ass=filename='{filter_path(ass_path, WORKSPACE_DIR)}',setpts=PTS-STARTPTS"
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi",
        "-i", f"color=c=0x111214:size={WIDTH}x{HEIGHT}:rate=1:duration=1",
        "-vf", ass_filter,
        "-frames:v", "1",
        "-update", "1",
        str(frame_path),
    ]
    run_command(cmd, "ffmpeg frame", cwd=WORKSPACE_DIR)


def render_smart_frames(ass_path, frames, frame_dir, jobs):
    frame_dir.mkdir(parents=True, exist_ok=True)
    for stale_frame in frame_dir.glob("frame_*.png"):
        stale_frame.unlink()

    jobs = max(1, jobs)
    print(f"正在并行生成菜单帧: {len(frames)} 帧，jobs={jobs}")

    futures = {}
    with ThreadPoolExecutor(max_workers=jobs) as executor:
        for index, frame in enumerate(frames):
            frame_path = frame_dir / f"frame_{index:05d}.png"
            frame["path"] = frame_path
            futures[executor.submit(render_menu_frame, ass_path, frame, frame_path)] = index

        completed = 0
        for future in as_completed(futures):
            future.result()
            completed += 1
            if completed == len(frames) or completed % 100 == 0:
                print(f"  - 已生成 {completed}/{len(frames)} 帧")


def write_frame_concat_list(frames, concat_path):
    concat_path.parent.mkdir(parents=True, exist_ok=True)
    with concat_path.open("w", encoding="utf-8") as f:
        for frame in frames:
            f.write(f"file {quote_concat_path(frame['path'])}\n")
            f.write(f"duration {frame['duration']:.6f}\n")
        if frames:
            f.write(f"file {quote_concat_path(frames[-1]['path'])}\n")


def render_smart_menu_video(ass_path, tracks, total_duration, menu_video_path, temp_dir, jobs, active_seconds, active_frames):
    frames = build_smart_frame_plan(tracks, total_duration, active_seconds, active_frames)
    if not frames:
        raise RuntimeError("未生成任何菜单帧")

    frame_dir = temp_dir / "playlist_menu_frames"
    concat_path = temp_dir / "playlist_menu_frames.txt"
    plan_path = temp_dir / "playlist_menu_frame_plan.json"

    render_smart_frames(ass_path, frames, frame_dir, jobs)
    write_frame_concat_list(frames, concat_path)
    plan_data = {
        "render_mode": "smart",
        "target_fps": FPS,
        "active_seconds": active_seconds,
        "active_frames": active_frames,
        "frame_count": len(frames),
        "active_frame_count": sum(1 for frame in frames if frame["kind"] == "active"),
        "static_frame_count": sum(1 for frame in frames if frame["kind"] == "static"),
        "total_duration": total_duration,
        "frames": [
            {
                "index": index,
                "time": frame["time"],
                "duration": frame["duration"],
                "track_index": frame["track_index"],
                "kind": frame["kind"],
                "path": str(frame["path"]),
            }
            for index, frame in enumerate(frames)
        ],
    }
    plan_path.write_text(json.dumps(plan_data, ensure_ascii=False, indent=2), encoding="utf-8")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_path),
        "-vf", f"fps={FPS},format=yuv420p",
        "-an",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(menu_video_path),
    ]
    print(f"正在拼接菜单帧为背景视频: {menu_video_path}")
    run_command(cmd, "ffmpeg frame concat")
    print(f"帧计划: {plan_path}")
    print(f"帧 concat 列表: {concat_path}")


def render_menu_video(ass_path, tracks, total_duration, menu_video_path, temp_dir, render_mode, jobs, active_seconds, active_frames):
    if render_mode == "full":
        render_full_menu_video(ass_path, total_duration, menu_video_path)
        return

    render_smart_menu_video(
        ass_path,
        tracks,
        total_duration,
        menu_video_path,
        temp_dir,
        jobs,
        active_seconds,
        active_frames,
    )


def add_vinyl_overlay(menu_video_path, vinyl_png_path, output_path, x, y, rotation_seconds, duration):
    if rotation_seconds <= 0:
        raise RuntimeError("--vinyl-rotation-seconds 必须大于 0")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    angle_expr = f"2*PI*t/{rotation_seconds:.6f}"
    filter_complex = (
        f"[1:v]format=rgba,rotate='{angle_expr}':ow=iw:oh=ih:c=none:bilinear=1[vinyl];"
        f"[0:v][vinyl]overlay={x}:{y}:format=auto,"
        f"trim=duration={duration:.3f},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p[v]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", str(menu_video_path),
        "-loop", "1",
        "-framerate", str(FPS),
        "-i", str(vinyl_png_path),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-an",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output_path),
    ]
    print(f"正在叠加旋转黑胶唱片: {output_path}")
    run_command(cmd, "ffmpeg vinyl overlay")


def mux_audio(menu_video_path, source_video_path, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-i", str(menu_video_path),
        "-i", str(source_video_path),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "copy",
        "-shortest",
        "-movflags", "+faststart",
        str(output_path),
    ]
    print(f"正在融合原音频: {output_path}")
    run_command(cmd, "ffmpeg")


def validate_output(output_path):
    result = run_command(
        [
            "ffprobe", "-v", "error",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(output_path),
        ],
        "ffprobe",
    )
    probe = json.loads(result.stdout)
    streams = probe.get("streams", [])
    video = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
    audio = next((stream for stream in streams if stream.get("codec_type") == "audio"), None)
    fmt = probe.get("format", {})
    duration = float(fmt.get("duration") or 0)
    size = int(fmt.get("size") or 0)

    errors = []
    if not output_path.is_file() or size <= 0:
        errors.append("输出文件不存在或为空")
    if duration <= 0:
        errors.append("输出时长为 0")
    if video is None:
        errors.append("缺少视频流")
    elif video.get("width") != WIDTH or video.get("height") != HEIGHT:
        errors.append(f"视频分辨率异常: {video.get('width')}x{video.get('height')}")
    if audio is None:
        errors.append("缺少音频流")

    if errors:
        raise RuntimeError("输出校验失败:\n  - " + "\n  - ".join(errors))

    print("输出校验通过:")
    print(f"  - 文件大小: {size / 1024 / 1024:.1f}MB")
    print(f"  - 时长: {format_clock(duration)} ({duration:.3f}s)")
    print(f"  - 视频流: {video.get('codec_name')} {video.get('width')}x{video.get('height')}")
    print(f"  - 音频流: {audio.get('codec_name')} {audio.get('sample_rate')}Hz {audio.get('channels')}ch")


def default_preview_times(tracks, total_duration):
    if not tracks:
        return []

    times = []
    first_time = min(tracks[0]["start"] + 10.0, tracks[0]["end"] - 0.1, total_duration - 0.1)
    times.append(max(0.0, first_time))

    motion_track = tracks[1] if len(tracks) > 1 else tracks[0]
    motion_time = min(motion_track["start"] + 8.0, motion_track["end"] - 1.1, total_duration - 1.1)
    motion_time = max(motion_track["start"], motion_time)
    times.append(max(0.0, motion_time))
    if motion_time + 1.0 < total_duration:
        times.append(motion_time + 1.0)

    if len(tracks) > 2:
        last_time = min(tracks[-1]["start"] + 5.0, tracks[-1]["end"] - 0.1, total_duration - 0.1)
        times.append(max(0.0, last_time))
    return times


def resolve_preview_times(value, tracks, total_duration):
    if value.strip():
        raw_times = [part.strip() for part in value.split(",") if part.strip()]
        times = [parse_timecode(part) for part in raw_times]
    else:
        times = default_preview_times(tracks, total_duration)

    resolved = []
    for timestamp in times:
        if timestamp < 0:
            raise RuntimeError(f"预览时间不能小于 0: {timestamp}")
        resolved.append(min(timestamp, max(total_duration - 0.1, 0.0)))
    return resolved


def extract_preview_frames(video_path, tracks, total_duration, temp_dir, preview_times):
    times = resolve_preview_times(preview_times, tracks, total_duration)
    if not times:
        return []

    temp_dir.mkdir(parents=True, exist_ok=True)
    previews = []
    for index, timestamp in enumerate(times, start=1):
        frame_path = temp_dir / f"playlist_menu_preview_{index:03d}_{preview_filename_time(timestamp)}.png"
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", format_seek_time(timestamp),
            "-i", str(video_path),
            "-frames:v", "1",
            "-update", "1",
            str(frame_path),
        ]
        run_command(cmd, "ffmpeg preview")
        previews.append({"time": timestamp, "path": frame_path, "md5": md5_file(frame_path)})

    print("预览帧检查:")
    for preview in previews:
        print(f"  - {format_clock(preview['time'])}: {preview['path']} md5={preview['md5']}")

    unique_hashes = {preview["md5"] for preview in previews}
    if len(previews) > 1 and len(unique_hashes) == 1:
        raise RuntimeError("预览帧完全相同，高亮画面可能没有随时间变化")

    if len(previews) > 1:
        print(f"  - 画面变化: {len(unique_hashes)} / {len(previews)} 个不同帧")
    return previews


def parse_args():
    parser = argparse.ArgumentParser(
        description="基于已合并 MP4 的音频，生成带歌曲清单和当前歌曲高亮的菜单视频。"
    )
    parser.add_argument(
        "--playlist-dir",
        default=str(DEFAULT_PLAYLIST_DIR),
        help=f"MP3 输入目录，默认: {DEFAULT_PLAYLIST_DIR}",
    )
    parser.add_argument(
        "--source-video",
        default=str(DEFAULT_SOURCE_VIDEO),
        help=f"已有合并 MP4，用于复用音频，默认: {DEFAULT_SOURCE_VIDEO}",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_FILE),
        help=f"最终输出 MP4，默认: {DEFAULT_OUTPUT_FILE}",
    )
    parser.add_argument(
        "--temp-dir",
        default=str(DEFAULT_TEMP_DIR),
        help=f"中间文件目录，默认: {DEFAULT_TEMP_DIR}",
    )
    parser.add_argument(
        "--menu-video",
        default="",
        help="菜单背景视频输出路径，默认写入 temp-dir/playlist_menu_background.mp4",
    )
    parser.add_argument(
        "--render-mode",
        choices=("smart", "full"),
        default="smart",
        help="菜单背景渲染模式。smart 使用并行关键帧/静态帧，full 使用整段 30fps 渲染。",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=min(4, os.cpu_count() or 1),
        help="smart 模式下并行生成菜单帧的任务数。",
    )
    parser.add_argument(
        "--active-seconds",
        type=float,
        default=ACTIVE_SECONDS,
        help="每首歌开头按高帧密度生成的秒数。",
    )
    parser.add_argument(
        "--active-frames",
        type=int,
        default=ACTIVE_FRAMES,
        help="每首歌开头 active-seconds 内生成的帧数。默认 60。",
    )
    parser.add_argument(
        "--disable-vinyl",
        action="store_true",
        help="禁用右侧旋转黑胶唱片动效。",
    )
    parser.add_argument(
        "--vinyl-size",
        type=int,
        default=VINYL_SIZE,
        help="黑胶唱片 PNG 尺寸，默认 360。",
    )
    parser.add_argument(
        "--vinyl-x",
        type=int,
        default=VINYL_X,
        help="黑胶唱片左上角 X 坐标。",
    )
    parser.add_argument(
        "--vinyl-y",
        type=int,
        default=VINYL_Y,
        help="黑胶唱片左上角 Y 坐标。",
    )
    parser.add_argument(
        "--vinyl-rotation-seconds",
        type=float,
        default=VINYL_ROTATION_SECONDS,
        help="黑胶唱片转一圈所需秒数，默认 4。",
    )
    parser.add_argument(
        "--preview-times",
        default="",
        help="逗号分隔的抽帧预览时间，例如 00:00:10,00:05:00。默认抽首歌、第二首和最后一首。",
    )
    parser.add_argument(
        "--skip-previews",
        action="store_true",
        help="跳过合成后的预览帧抽取。",
    )
    parser.add_argument(
        "--preview-only",
        action="store_true",
        help="只基于已存在的 output 抽取预览帧，不重新生成视频。",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    playlist_dir = resolve_path(args.playlist_dir)
    source_video = resolve_path(args.source_video)
    output_path = resolve_path(args.output)
    temp_dir = resolve_path(args.temp_dir)
    menu_video = resolve_path(args.menu_video) if args.menu_video else temp_dir / "playlist_menu_background.mp4"
    visual_video = temp_dir / "playlist_menu_visual.mp4"
    vinyl_png = temp_dir / "playlist_vinyl.png"
    ass_path = temp_dir / "playlist_menu.ass"
    timeline_path = temp_dir / "playlist_menu_timeline.json"

    try:
        check_dependencies()
        if not source_video.is_file():
            raise RuntimeError(f"源 MP4 不存在: {source_video}")

        mp3_files = get_mp3_files(playlist_dir)
        tracks, total_duration = build_timeline(mp3_files, source_video)

        print(f"找到 {len(tracks)} 首歌，菜单高亮时间轴:")
        for track in tracks:
            print(
                f"  {track['index']:02d}. "
                f"{format_clock(track['start'])} - {format_clock(track['end'])}  "
                f"{track['title']}"
            )

        write_ass(tracks, total_duration, ass_path)
        write_timeline_json(tracks, total_duration, timeline_path)
        print(f"ASS 菜单层: {ass_path}")
        print(f"时间轴 JSON: {timeline_path}")

        if args.preview_only:
            if not output_path.is_file():
                raise RuntimeError(f"预览目标视频不存在: {output_path}")
            validate_output(output_path)
            if not args.skip_previews:
                extract_preview_frames(output_path, tracks, total_duration, temp_dir, args.preview_times)
            print("完成!")
            return

        if args.jobs < 1:
            raise RuntimeError("--jobs 必须大于等于 1")
        if args.active_seconds < 0:
            raise RuntimeError("--active-seconds 不能小于 0")
        if args.active_frames < 1:
            raise RuntimeError("--active-frames 必须大于等于 1")
        if args.vinyl_size < 64:
            raise RuntimeError("--vinyl-size 不能小于 64")

        render_menu_video(
            ass_path,
            tracks,
            total_duration,
            menu_video,
            temp_dir,
            args.render_mode,
            args.jobs,
            args.active_seconds,
            args.active_frames,
        )

        video_for_audio = menu_video
        if args.disable_vinyl:
            print("已禁用黑胶唱片动效")
        else:
            generate_vinyl_png(vinyl_png, args.vinyl_size)
            print(f"黑胶唱片 PNG: {vinyl_png}")
            add_vinyl_overlay(
                menu_video,
                vinyl_png,
                visual_video,
                args.vinyl_x,
                args.vinyl_y,
                args.vinyl_rotation_seconds,
                total_duration,
            )
            video_for_audio = visual_video

        mux_audio(video_for_audio, source_video, output_path)
        validate_output(output_path)
        if not args.skip_previews:
            extract_preview_frames(output_path, tracks, total_duration, temp_dir, args.preview_times)
        print("完成!")
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
