#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from luis_audio_translator import (
    app_paths,
    check_format,
    env_path,
    ffmpeg_audio_options,
    require_file,
    unique_path,
)


INFRA_ENV = "LUIS_AUDIO_TRANSLATOR_KUGOU_INFRA_DLL"
DB_ENV = "LUIS_AUDIO_TRANSLATOR_KUGOU_DB"
KUGOU_EXTS = {".kgm", ".kgma", ".kgtemp", ".kgg"}


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def emit(obj, code=0):
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def run(cmd, print_command=False, cwd=None):
    if print_command:
        print(json.dumps({"command": [str(x) for x in cmd]}, ensure_ascii=False))
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
        raise RuntimeError(json.dumps({
            "cmd": [str(x) for x in cmd],
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }, ensure_ascii=False))
    return proc


def is_kugou_file(path):
    name = path.name.lower()
    return path.suffix.lower() in KUGOU_EXTS or name.endswith(".kgm.flac")


def output_stem(path):
    name = path.name
    lower = name.lower()
    if lower.endswith(".kgm.flac"):
        return name[:-len(".kgm.flac")]
    return path.stem


def collect_inputs(items, recursive=False):
    files = []
    for item in items:
        path = Path(item).expanduser()
        if path.is_dir():
            iterator = path.rglob("*") if recursive else path.iterdir()
            files.extend(p for p in iterator if p.is_file() and is_kugou_file(p))
        elif path.is_file() and is_kugou_file(path):
            files.append(path)
    return sorted(dict.fromkeys(files), key=lambda p: str(p).lower())


def appdata_dir():
    value = os.environ.get("APPDATA")
    if value:
        return Path(value)
    return Path.home() / "AppData" / "Roaming"


def infra_candidates():
    explicit = env_path(INFRA_ENV)
    if explicit:
        yield explicit

    seen = set()
    roots = [Path(value) for value in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")) if value]
    for root in roots:
        if root and root.exists():
            for path in root.glob("KuGou/KGMusic/*/infra.dll"):
                if path not in seen:
                    seen.add(path)
                    yield path

    base = appdata_dir() / "KuGou8" / "AppStore" / "webgl"
    if base.exists():
        for path in base.glob("*/desktop_manager/*/infra.dll"):
            if path not in seen:
                seen.add(path)
                yield path


def kugou_db():
    explicit = env_path(DB_ENV)
    if explicit:
        return explicit
    candidate = appdata_dir() / "KuGou8" / "KGMusicV3.db"
    return candidate if candidate.exists() else None


def decode_um(src, tmp, paths, print_command=False):
    um = require_file(paths["um"], "um decrypt helper")
    before = set(tmp.iterdir())
    run([um, "-i", src, "-o", tmp], print_command=print_command)
    candidates = [p for p in tmp.iterdir() if p not in before and p.is_file()]
    if not candidates:
        candidates = [p for p in tmp.iterdir() if p.is_file()]
    if not candidates:
        raise RuntimeError("um decrypt helper did not create an output file")
    return candidates[0]


def decode_kgg(src, tmp, paths, print_command=False):
    helper = require_file(paths["kgg_helper"], "kgg helper")
    db = kugou_db()
    errors = []
    for infra in infra_candidates():
        if not infra.exists():
            continue
        work = tmp / infra.parent.name
        work.mkdir(parents=True, exist_ok=True)
        copied = work / src.name
        shutil.copy2(src, copied)
        cmd = [helper, "--infra-dll", infra]
        if db and db.exists():
            cmd += ["--db", db]
        cmd += [work]
        proc = subprocess.run(
            [str(x) for x in cmd],
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if print_command:
            print(json.dumps({"command": [str(x) for x in cmd]}, ensure_ascii=False))
        if proc.returncode != 0:
            errors.append({"infra": str(infra), "stdout": proc.stdout, "stderr": proc.stderr})
            continue
        candidates = [p for p in work.iterdir() if p.is_file() and p.suffix.lower() != ".kgg"]
        if candidates:
            return candidates[0], str(infra), str(db) if db else None
        errors.append({"infra": str(infra), "stdout": proc.stdout, "stderr": proc.stderr, "error": "no decoded file"})
    raise RuntimeError(json.dumps({"error": "all kgg decode attempts failed", "attempts": errors}, ensure_ascii=False))


def convert_decoded(decoded, src, args, paths):
    ffmpeg = require_file(paths["ffmpeg"], "ffmpeg")
    fmt = check_format(args.format)
    output_dir = Path(args.output_dir).expanduser() if args.output_dir else src.parent / fmt
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{output_stem(src)}.{fmt}"
    if output.exists() and not args.overwrite:
        output = unique_path(output_dir, output_stem(src), "", fmt)
    cmd = [ffmpeg, "-y" if args.overwrite else "-n", "-hide_banner", "-i", decoded]
    cmd += ffmpeg_audio_options(args, fmt)
    cmd += [output]
    run(cmd, print_command=args.print_command)
    return output


def command_diagnose(args):
    paths = app_paths(args.app_dir)
    result = {
        "ok": True,
        "tools": {
            "ffmpeg": str(paths["ffmpeg"]) if paths["ffmpeg"] else None,
            "um": str(paths["um"]) if paths["um"] else None,
            "kgg_helper": str(paths["kgg_helper"]) if paths["kgg_helper"] else None,
        },
        "kugou": {
            "infra_candidates": [str(p) for p in infra_candidates() if p.exists()],
            "db": str(kugou_db()) if kugou_db() else None,
        },
    }
    result["ready_for_kgm"] = bool(paths["ffmpeg"] and paths["um"])
    result["ready_for_kgg"] = bool(paths["ffmpeg"] and paths["kgg_helper"] and result["kugou"]["infra_candidates"])
    emit(result)


def command_convert(args):
    paths = app_paths(args.app_dir)
    inputs = collect_inputs(args.inputs, args.recursive)
    if not inputs:
        emit({"ok": False, "error": "no supported Kugou files found"}, 2)

    results = []
    for src in inputs:
        tmp = Path(tempfile.mkdtemp(prefix="luis-kugou-"))
        try:
            suffix = src.suffix.lower()
            if suffix == ".kgg":
                decoded, infra, db = decode_kgg(src, tmp, paths, args.print_command)
                engine = {"name": "kgg", "infra": infra, "db": db}
            else:
                decoded = decode_um(src, tmp, paths, args.print_command)
                engine = {"name": "um"}
            output = convert_decoded(decoded, src, args, paths)
            results.append({"input": str(src), "output": str(output), "engine": engine, "status": "ok"})
        except Exception as exc:
            results.append({"input": str(src), "status": "error", "error": str(exc)})
            if args.fail_fast:
                emit({"ok": False, "results": results}, 1)
        finally:
            if args.keep_temp:
                results[-1]["temp_dir"] = str(tmp)
            else:
                shutil.rmtree(tmp, ignore_errors=True)
    emit({"ok": all(item["status"] == "ok" for item in results), "results": results})


def build_parser():
    parser = argparse.ArgumentParser(description="Convert Kugou special audio formats")
    parser.add_argument("--app-dir", help="optional local engine directory; can also set LUIS_AUDIO_TRANSLATOR_ENGINE_DIR")
    parser.add_argument("--print-command", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("diagnose")
    p.set_defaults(func=command_diagnose)

    p = sub.add_parser("convert")
    p.add_argument("inputs", nargs="+", help="Kugou files or directories")
    p.add_argument("--recursive", action="store_true")
    p.add_argument("--format", default="mp3")
    p.add_argument("--output-dir")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--fail-fast", action="store_true")
    p.add_argument("--keep-temp", action="store_true")
    p.add_argument("--bitrate", default="192k")
    p.add_argument("--sample-rate", type=int)
    p.add_argument("--channels", type=int)
    p.add_argument("--volume", type=float)
    p.add_argument("--title")
    p.add_argument("--artist")
    p.add_argument("--album")
    p.add_argument("--date")
    p.add_argument("--genre")
    p.set_defaults(func=command_convert)
    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
