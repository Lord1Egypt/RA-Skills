#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


ENGINE_DIR_ENV = "LUIS_AUDIO_TRANSLATOR_ENGINE_DIR"
FFMPEG_ENV = "LUIS_AUDIO_TRANSLATOR_FFMPEG"
FFPROBE_ENV = "LUIS_AUDIO_TRANSLATOR_FFPROBE"
UM_ENV = "LUIS_AUDIO_TRANSLATOR_UM"
MUSIC_TOOL_ENV = "LUIS_AUDIO_TRANSLATOR_MUSIC_TOOL"
SILK_ENV = "LUIS_AUDIO_TRANSLATOR_SILK"
KGG_HELPER_ENV = "LUIS_AUDIO_TRANSLATOR_KGG_HELPER"
MUSIC_TOOL_KEY = "e6pkdI95jjNotCCt7tSup9VvMBNb6LcZ"

OUTPUT_FORMATS = {
    "mp3", "wav", "ogg", "flac", "m4a", "m4r", "mp2", "aiff", "ac3",
    "wma", "amr", "aac", "opus", "caf", "au", "mka", "webm"
}

UM_EXTS = {
    "qmc0", "qmc2", "qmc3", "qmcflac", "qmcogg", "tkm",
    "bkcmp3", "bkcflac", "tm0", "tm2", "tm3", "tm6",
    "mflac", "mgg", "mflac0", "mggl", "ofl_en", "oggl",
    "ncm", "kwm", "kgm", "kgma", "vpr", "x2m", "x3m", "mg3d"
}


def emit(obj, code=0):
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def env_path(name):
    value = os.environ.get(name)
    return Path(value).expanduser() if value else None


def resolve_engine_dir(app_dir):
    if app_dir:
        return Path(app_dir).expanduser()
    return env_path(ENGINE_DIR_ENV)


def resolve_tool(env_name, bundled_path=None, path_names=()):
    explicit = env_path(env_name)
    if explicit:
        return explicit
    if bundled_path and bundled_path.exists():
        return bundled_path
    for name in path_names:
        found = shutil.which(name)
        if found:
            return Path(found)
    return None


def app_paths(app_dir):
    engine_dir = resolve_engine_dir(app_dir)
    library = engine_dir / "resources" / "library" if engine_dir else None
    bundled = {}
    if library:
        bundled = {
            "ffmpeg": library / "ffmpeg-shared" / "ffmpeg.exe",
            "ffprobe": library / "ffmpeg-shared" / "ffprobe.exe",
            "um": library / "um" / "um-win32-x64.exe",
            "music_tool": library / "music-tool-v2" / "music-tool.exe",
            "silk": library / "silk" / "silk_codec-windows-static-x64.exe",
            "kgg_helper": library / "kgg" / "kgg-helper.exe",
        }
    return {
        "engine_dir": engine_dir,
        "ffmpeg": resolve_tool(FFMPEG_ENV, bundled.get("ffmpeg"), ("ffmpeg.exe", "ffmpeg")),
        "ffprobe": resolve_tool(FFPROBE_ENV, bundled.get("ffprobe"), ("ffprobe.exe", "ffprobe")),
        "um": resolve_tool(UM_ENV, bundled.get("um")),
        "music_tool": resolve_tool(MUSIC_TOOL_ENV, bundled.get("music_tool")),
        "silk": resolve_tool(SILK_ENV, bundled.get("silk")),
        "kgg_helper": resolve_tool(KGG_HELPER_ENV, bundled.get("kgg_helper")),
    }


def require_file(path, label):
    if not path or not path.exists():
        emit({"ok": False, "error": f"{label} not found", "path": str(path)}, 2)
    return path


def check_format(fmt):
    fmt = fmt.lower().lstrip(".")
    if fmt not in OUTPUT_FORMATS:
        emit({"ok": False, "error": f"unsupported output format: {fmt}"}, 2)
    return fmt


def run(cmd, print_command=False, cwd=None):
    if print_command:
        print(json.dumps({"command": [str(x) for x in cmd]}, ensure_ascii=False), file=sys.stderr)
    proc = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd) if cwd else None,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        emit({
            "ok": False,
            "returncode": proc.returncode,
            "command": [str(x) for x in cmd],
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }, proc.returncode)
    return proc


def unique_path(output_dir, basename, suffix, fmt):
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate = output_dir / f"{basename}{suffix}.{fmt}"
    i = 1
    while candidate.exists():
        candidate = output_dir / f"{basename}{suffix}_{i}.{fmt}"
        i += 1
    return candidate


def parse_time(value):
    if value is None:
        return None
    text = str(value).strip()
    if ":" not in text:
        return float(text)
    parts = [float(x) for x in text.split(":")]
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + part
    return seconds


def ffmpeg_audio_options(args, fmt):
    opts = ["-vn"]
    if getattr(args, "volume", None) is not None and float(args.volume) != 1.0:
        opts += ["-filter:a", f"volume={args.volume}"]
    if getattr(args, "sample_rate", None):
        opts += ["-ar", str(args.sample_rate)]
    if getattr(args, "bitrate", None):
        opts += ["-b:a", str(args.bitrate)]
    if getattr(args, "channels", None):
        opts += ["-ac", str(args.channels)]
    if fmt == "amr":
        opts += ["-ar", "8000", "-ac", "1"]
    if fmt == "flac":
        opts += ["-sample_fmt", "s16"]
    if fmt == "m4r":
        opts += ["-f", "mp4"]
    for key in ("title", "artist", "album", "date", "genre"):
        value = getattr(args, key, None)
        if value:
            opts += ["-metadata", f"{key}={value}"]
    return opts


def ffprobe_duration(ffprobe, input_path, print_command=False):
    cmd = [
        ffprobe, "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", input_path
    ]
    proc = run(cmd, print_command=print_command)
    try:
        return float(proc.stdout.strip())
    except ValueError:
        emit({"ok": False, "error": "could not read duration", "stdout": proc.stdout}, 2)


def command_info(args):
    paths = app_paths(args.app_dir)
    ffprobe = require_file(paths["ffprobe"], "ffprobe")
    input_path = require_file(Path(args.input), "input")
    cmd = [
        ffprobe, "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", input_path
    ]
    proc = run(cmd, args.print_command)
    data = json.loads(proc.stdout or "{}")
    audio_streams = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
    emit({
        "ok": True,
        "input": str(input_path),
        "file_size": input_path.stat().st_size,
        "duration": data.get("format", {}).get("duration"),
        "bit_rate": data.get("format", {}).get("bit_rate"),
        "audio_streams": audio_streams,
        "raw": data,
    })


def command_convert(args):
    paths = app_paths(args.app_dir)
    ffmpeg = require_file(paths["ffmpeg"], "ffmpeg")
    input_path = require_file(Path(args.input), "input")
    fmt = check_format(args.format)
    output_dir = Path(args.output_dir or input_path.parent)
    basename = args.basename or input_path.stem
    output = Path(args.output) if args.output else unique_path(output_dir, basename, "", fmt)
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ffmpeg, "-y", "-hide_banner", "-i", input_path] + ffmpeg_audio_options(args, fmt) + [output]
    run(cmd, args.print_command)
    emit({"ok": True, "operation": args.command, "outputs": [str(output)], "bytes": output.stat().st_size})


def command_merge(args):
    paths = app_paths(args.app_dir)
    ffmpeg = require_file(paths["ffmpeg"], "ffmpeg")
    inputs = [require_file(Path(x), "input") for x in args.inputs]
    if len(inputs) < 2:
        emit({"ok": False, "error": "merge requires at least two inputs"}, 2)
    fmt = check_format(args.format)
    output_dir = Path(args.output_dir or inputs[0].parent)
    basename = args.basename or f"{inputs[0].stem}_合并"
    output = Path(args.output) if args.output else unique_path(output_dir, basename, "", fmt)
    output.parent.mkdir(parents=True, exist_ok=True)

    cmd = [ffmpeg, "-y", "-hide_banner"]
    for input_path in inputs:
        cmd += ["-i", input_path]

    if args.volume is not None and float(args.volume) != 1.0:
        filters = []
        labels = []
        for i in range(len(inputs)):
            filters.append(f"[{i}:a]volume={args.volume}[a{i}]")
            labels.append(f"[a{i}]")
        filter_complex = ";".join(filters) + ";" + "".join(labels) + f"concat=n={len(inputs)}:v=0:a=1[out]"
    else:
        labels = "".join(f"[{i}:a]" for i in range(len(inputs)))
        filter_complex = labels + f"concat=n={len(inputs)}:v=0:a=1[out]"

    cmd += ["-filter_complex", filter_complex, "-map", "[out]"]
    saved_volume = args.volume
    args.volume = None
    cmd += ffmpeg_audio_options(args, fmt)
    args.volume = saved_volume
    cmd += [output]
    run(cmd, args.print_command)
    emit({"ok": True, "operation": "merge", "outputs": [str(output)], "bytes": output.stat().st_size})


def command_split(args):
    paths = app_paths(args.app_dir)
    ffmpeg = require_file(paths["ffmpeg"], "ffmpeg")
    ffprobe = require_file(paths["ffprobe"], "ffprobe")
    input_path = require_file(Path(args.input), "input")
    fmt = check_format(args.format)
    segment = parse_time(args.segment_seconds)
    if not segment or segment <= 0:
        emit({"ok": False, "error": "segment duration must be positive"}, 2)
    duration = ffprobe_duration(ffprobe, input_path, args.print_command)
    count = max(1, int(math.ceil(duration / segment)))
    output_dir = Path(args.output_dir or input_path.parent / f"{input_path.stem}_分割")
    if output_dir.exists() and args.clean:
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = []
    for i in range(count):
        start = i * segment
        length = min(segment, max(0.0, duration - start))
        output = output_dir / f"{i + 1}.{fmt}"
        cmd = [
            ffmpeg, "-y", "-hide_banner", "-ss", str(start), "-t", str(length),
            "-i", input_path
        ] + ffmpeg_audio_options(args, fmt) + [output]
        run(cmd, args.print_command)
        outputs.append(str(output))
    emit({"ok": True, "operation": "split", "outputs": outputs})


def command_decrypt(args):
    paths = app_paths(args.app_dir)
    input_path = require_file(Path(args.input), "input")
    output_dir = Path(args.output_dir or input_path.parent / f"{input_path.stem}_decoded")
    output_dir.mkdir(parents=True, exist_ok=True)
    ext = input_path.suffix.lower().lstrip(".")
    engine = args.engine
    if engine == "auto":
        if ext == "silk":
            engine = "silk"
        elif ext == "xm":
            engine = "xm"
        elif ext in {"mflac", "mgg"} and input_path.read_bytes()[-8:] == b"musicex\0":
            engine = "music-tool"
        elif ext in UM_EXTS:
            engine = "um"
        else:
            emit({"ok": False, "error": f"no automatic decrypt engine for .{ext}"}, 2)

    if engine == "silk":
        silk = require_file(paths["silk"], "silk decoder")
        ffmpeg = require_file(paths["ffmpeg"], "ffmpeg")
        pcm = output_dir / "decode.pcm"
        wav = unique_path(output_dir, input_path.stem, "", "wav")
        run([silk, "stp", "-i", input_path, "-o", pcm, "-s", "24000"], args.print_command)
        run([ffmpeg, "-y", "-hide_banner", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", pcm, "-vn", "-f", "wav", wav], args.print_command)
        emit({"ok": True, "operation": "decrypt", "engine": "silk", "outputs": [str(wav)]})

    if engine == "um":
        um = require_file(paths["um"], "um decrypt tool")
        before = set(output_dir.iterdir())
        run([um, "-i", input_path, "-o", output_dir], args.print_command)
        after = [p for p in output_dir.iterdir() if p not in before and p.is_file()]
        if not after:
            after = [p for p in output_dir.iterdir() if p.is_file()]
        emit({"ok": True, "operation": "decrypt", "engine": "um", "outputs": [str(p) for p in after]})

    if engine == "music-tool":
        tool = require_file(paths["music_tool"], "music-tool")
        digest = hashlib.md5(str(input_path).encode("utf-8")).hexdigest()
        output_base = output_dir / digest
        run([tool, "--key", args.key, "--input", input_path, "--output", output_base], args.print_command)
        if not output_base.exists():
            emit({"ok": False, "error": "music-tool did not create expected output", "output_base": str(output_base)}, 2)
        target_ext = ".ogg" if ext == "mgg" else ".flac"
        target = output_base.with_suffix(target_ext)
        output_base.replace(target)
        emit({"ok": True, "operation": "decrypt", "engine": "music-tool", "outputs": [str(target)]})

    if engine == "xm":
        script = Path(__file__).with_name("xm_audio_decoder.py")
        require_file(script, "xm decoder script")
        proc = run([sys.executable, script, input_path, "--output-dir", output_dir], args.print_command)
        try:
            data = json.loads(proc.stdout or "{}")
        except json.JSONDecodeError:
            emit({"ok": False, "error": "xm decoder returned non-JSON output", "stdout": proc.stdout}, 2)
        if not data.get("ok"):
            emit(data, 2)
        emit({"ok": True, "operation": "decrypt", "engine": "xm", "outputs": [data["output"]], "detected_format": data.get("detected_format")})

    emit({"ok": False, "error": f"unknown decrypt engine: {engine}"}, 2)


def build_parser():
    parser = argparse.ArgumentParser(description="Luis-audio-translator local audio wrapper")
    parser.add_argument("--app-dir", help=f"optional local engine directory; can also set {ENGINE_DIR_ENV}")
    parser.add_argument("--print-command", action="store_true", help="print external commands to stderr")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("diagnose")
    p.set_defaults(func=command_diagnose)

    common_audio = argparse.ArgumentParser(add_help=False)
    common_audio.add_argument("--format", required=True, help="target audio format")
    common_audio.add_argument("--output-dir")
    common_audio.add_argument("--output")
    common_audio.add_argument("--basename")
    common_audio.add_argument("--bitrate", help="audio bitrate, e.g. 128k or 192k")
    common_audio.add_argument("--sample-rate", type=int)
    common_audio.add_argument("--channels", type=int)
    common_audio.add_argument("--volume", type=float)
    common_audio.add_argument("--title")
    common_audio.add_argument("--artist")
    common_audio.add_argument("--album")
    common_audio.add_argument("--date")
    common_audio.add_argument("--genre")

    p = sub.add_parser("info")
    p.add_argument("input")
    p.set_defaults(func=command_info)

    p = sub.add_parser("convert", parents=[common_audio])
    p.add_argument("input")
    p.set_defaults(func=command_convert)

    p = sub.add_parser("compress", parents=[common_audio])
    p.add_argument("input")
    p.set_defaults(func=command_convert)

    p = sub.add_parser("clip", parents=[common_audio])
    p.add_argument("input")
    p.add_argument("--start", default="0")
    p.add_argument("--duration")
    p.add_argument("--end")
    p.set_defaults(func=lambda a: clip_adapter(a))

    p = sub.add_parser("merge", parents=[common_audio])
    p.add_argument("inputs", nargs="+")
    p.set_defaults(func=command_merge)

    p = sub.add_parser("split", parents=[common_audio])
    p.add_argument("input")
    p.add_argument("--segment-seconds", required=True)
    p.add_argument("--clean", action="store_true")
    p.set_defaults(func=command_split)

    p = sub.add_parser("decrypt")
    p.add_argument("input")
    p.add_argument("--output-dir")
    p.add_argument("--engine", choices=["auto", "um", "music-tool", "silk", "xm"], default="auto")
    p.add_argument("--key", default=MUSIC_TOOL_KEY)
    p.set_defaults(func=command_decrypt)
    return parser


def clip_adapter(args):
    paths = app_paths(args.app_dir)
    ffmpeg = require_file(paths["ffmpeg"], "ffmpeg")
    input_path = require_file(Path(args.input), "input")
    fmt = check_format(args.format)
    output_dir = Path(args.output_dir or input_path.parent)
    basename = args.basename or f"{input_path.stem}_clip"
    output = Path(args.output) if args.output else unique_path(output_dir, basename, "", fmt)
    output.parent.mkdir(parents=True, exist_ok=True)
    start = parse_time(args.start) or 0
    if args.duration:
        duration = parse_time(args.duration)
    elif args.end:
        duration = parse_time(args.end) - start
    else:
        emit({"ok": False, "error": "clip requires --duration or --end"}, 2)
    if duration <= 0:
        emit({"ok": False, "error": "clip duration must be positive"}, 2)
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-ss", str(start), "-t", str(duration),
        "-i", input_path
    ] + ffmpeg_audio_options(args, fmt) + [output]
    run(cmd, args.print_command)
    emit({"ok": True, "operation": "clip", "outputs": [str(output)], "bytes": output.stat().st_size})


def command_diagnose(args):
    paths = app_paths(args.app_dir)
    result = {
        "ok": True,
        "engine_dir": str(paths["engine_dir"]) if paths["engine_dir"] else None,
        "tools": {},
        "env": {
            ENGINE_DIR_ENV: bool(os.environ.get(ENGINE_DIR_ENV)),
            FFMPEG_ENV: bool(os.environ.get(FFMPEG_ENV)),
            FFPROBE_ENV: bool(os.environ.get(FFPROBE_ENV)),
            UM_ENV: bool(os.environ.get(UM_ENV)),
            MUSIC_TOOL_ENV: bool(os.environ.get(MUSIC_TOOL_ENV)),
            SILK_ENV: bool(os.environ.get(SILK_ENV)),
            KGG_HELPER_ENV: bool(os.environ.get(KGG_HELPER_ENV)),
        },
    }
    for key in ("ffmpeg", "ffprobe", "um", "music_tool", "silk", "kgg_helper"):
        path = paths[key]
        result["tools"][key] = {
            "path": str(path) if path else None,
            "exists": bool(path and path.exists()),
        }
    result["conversion_ready"] = result["tools"]["ffmpeg"]["exists"]
    result["inspection_ready"] = result["tools"]["ffprobe"]["exists"]
    result["xm_ready"] = Path(__file__).with_name("xm_audio_decoder.py").exists()
    result["decrypt_ready"] = result["xm_ready"] or any(result["tools"][key]["exists"] for key in ("um", "music_tool", "silk", "kgg_helper"))
    emit(result)


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
