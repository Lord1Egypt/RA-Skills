#!/usr/bin/env python3
"""将 playlist 文件夹下所有 MP3 拼接成一个带黑色视频流的 MP4 文件。"""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = SKILL_DIR.parent.parent.parent

DEFAULT_PLAYLIST_DIR = WORKSPACE_DIR / "playlist"
DEFAULT_OUTPUT_FILE = WORKSPACE_DIR / "playlist_output.mp4"
DEFAULT_TEMP_DIR = WORKSPACE_DIR / "output"

EXPECTED_WIDTH = 1920
EXPECTED_HEIGHT = 1080
EXPECTED_AUDIO_RATE = "44100"
EXPECTED_AUDIO_CHANNELS = 2


def natural_key(path):
    """按文件名自然排序，确保 10.mp3 排在 9.mp3 后面。"""
    return [
        int(part) if part.isdigit() else part.casefold()
        for part in re.split(r"(\d+)", Path(path).name)
    ]


def resolve_path(value):
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    return path.resolve()


def run_command(cmd, label):
    try:
        return subprocess.run(cmd, check=True, capture_output=True, text=True)
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

    print("依赖检查通过:")
    print(f"  - python: {sys.version.split()[0]}")
    print(f"  - ffmpeg: {shutil.which('ffmpeg')}")
    print(f"  - ffprobe: {shutil.which('ffprobe')}")


def get_mp3_files(playlist_dir):
    if not playlist_dir.is_dir():
        raise RuntimeError(f"playlist 目录不存在: {playlist_dir}")

    files = sorted(playlist_dir.glob("*.mp3"), key=natural_key)
    if not files:
        raise RuntimeError(f"未找到 MP3 文件: {playlist_dir}")
    return files


def quote_concat_path(path):
    return "'" + str(path.resolve()).replace("'", "'\\''") + "'"


def write_concat_list(mp3_files, temp_dir):
    temp_dir.mkdir(parents=True, exist_ok=True)
    list_file = temp_dir / "concat_list.txt"

    with list_file.open("w", encoding="utf-8") as f:
        for mp3 in mp3_files:
            f.write(f"file {quote_concat_path(mp3)}\n")

    return list_file


def merge_to_mp4(mp3_files, output_path, temp_dir):
    """将多个 MP3 文件拼接成一个 MP4 文件。"""
    list_file = write_concat_list(mp3_files, temp_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-f", "lavfi", "-i", "color=black:size=1920x1080:rate=30",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest",
        str(output_path),
    ]

    print(f"正在合并 {len(mp3_files)} 个文件...")
    run_command(cmd, "ffmpeg")
    print(f"输出文件: {output_path}")
    return list_file


def format_bytes(size):
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f}{unit}"
        value /= 1024


def format_duration(seconds):
    total = int(round(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def validate_output(output_path):
    if not output_path.is_file():
        raise RuntimeError(f"输出文件不存在: {output_path}")

    stat_size = output_path.stat().st_size
    if stat_size <= 0:
        raise RuntimeError(f"输出文件为空: {output_path}")

    result = run_command(
        [
            "ffprobe", "-v", "error",
            "-print_format", "json",
            "-show_format", "-show_streams",
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
    probe_size = int(fmt.get("size") or stat_size)

    errors = []
    if duration <= 0:
        errors.append("视频时长为 0")
    if probe_size <= 0:
        errors.append("视频文件大小为 0")
    if video is None:
        errors.append("缺少视频流")
    else:
        if video.get("codec_name") != "h264":
            errors.append(f"视频编码异常: {video.get('codec_name')}")
        if video.get("width") != EXPECTED_WIDTH or video.get("height") != EXPECTED_HEIGHT:
            errors.append(f"视频分辨率异常: {video.get('width')}x{video.get('height')}")
    if audio is None:
        errors.append("缺少音频流")
    else:
        if audio.get("codec_name") != "aac":
            errors.append(f"音频编码异常: {audio.get('codec_name')}")
        if audio.get("sample_rate") != EXPECTED_AUDIO_RATE:
            errors.append(f"音频采样率异常: {audio.get('sample_rate')}")
        if audio.get("channels") != EXPECTED_AUDIO_CHANNELS:
            errors.append(f"音频声道数异常: {audio.get('channels')}")

    if errors:
        raise RuntimeError("输出校验失败:\n  - " + "\n  - ".join(errors))

    print("输出校验通过:")
    print(f"  - 文件大小: {format_bytes(probe_size)}")
    print(f"  - 时长: {format_duration(duration)} ({duration:.3f}s)")
    print(f"  - 视频流: {video.get('codec_name')} {video.get('width')}x{video.get('height')}")
    print(
        f"  - 音频流: {audio.get('codec_name')} "
        f"{audio.get('sample_rate')}Hz {audio.get('channels')}ch"
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="将 playlist 文件夹下的所有 MP3 合并为一个黑色视频 MP4。"
    )
    parser.add_argument(
        "--playlist-dir",
        default=str(DEFAULT_PLAYLIST_DIR),
        help=f"MP3 输入目录，默认: {DEFAULT_PLAYLIST_DIR}",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_FILE),
        help=f"MP4 输出文件，默认: {DEFAULT_OUTPUT_FILE}",
    )
    parser.add_argument(
        "--temp-dir",
        default=str(DEFAULT_TEMP_DIR),
        help=f"临时文件目录，默认: {DEFAULT_TEMP_DIR}",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="跳过合并后的 ffprobe 输出校验。",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    playlist_dir = resolve_path(args.playlist_dir)
    output_path = resolve_path(args.output)
    temp_dir = resolve_path(args.temp_dir)

    try:
        check_dependencies()
        mp3_files = get_mp3_files(playlist_dir)

        print(f"找到 {len(mp3_files)} 个 MP3 文件，合并顺序:")
        for index, path in enumerate(mp3_files, start=1):
            print(f"  {index}. {path.name}")

        list_file = merge_to_mp4(mp3_files, output_path, temp_dir)
        print(f"concat 列表: {list_file}")

        if not args.skip_verify:
            validate_output(output_path)

        print("完成!")
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
