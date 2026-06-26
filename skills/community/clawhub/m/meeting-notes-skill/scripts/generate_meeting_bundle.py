#!/usr/bin/env python3
"""
Generate a compact meeting bundle from text minutes:
- structured minutes doc
- brief audio (mp3)
- mindmap (.html)

Fails fast if any required artifact is missing.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SKILL_SLUG = SKILL_ROOT.name
WORKSPACE_ROOT = SKILL_ROOT.parent.parent if SKILL_ROOT.parent.name == "skills" else SKILL_ROOT.parent
DEFAULT_OUTPUT_DIR = WORKSPACE_ROOT / f"{SKILL_SLUG}-data"
PRIVATE_OUTPUT_DIR = Path.home() / "clawdhome_shared" / "private" / f"{SKILL_SLUG}-data"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=False, text=True, capture_output=True)


def parse_kv_lines(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for ln in text.splitlines():
        if "=" not in ln:
            continue
        k, v = ln.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def ensure_file(path_str: str | None, label: str) -> Path:
    if not path_str:
        raise RuntimeError(f"missing {label} in script output")
    p = Path(path_str).expanduser().resolve()
    if not p.exists() or p.stat().st_size <= 0:
        raise RuntimeError(f"{label} missing: {p}")
    return p


def best_effort_delete(paths: list[Path]) -> None:
    for p in paths:
        try:
            if p and p.exists():
                p.unlink()
        except Exception:
            continue


def cleanup_old_outputs(outdir: Path, topic_slug: str, keep: set[Path]) -> dict[str, int]:
    """
    Keep only latest final artifacts for the topic, plus files explicitly kept.
    Remove stale intermediates and older generated outputs.
    """
    removed = 0
    skipped = 0
    keep_resolved = {x.resolve() for x in keep}
    # Keep cleanup scoped to this topic prefix to avoid touching unrelated files.
    for p in outdir.glob(f"{topic_slug}-*"):
        try:
            if p.is_dir():
                skipped += 1
                continue
            if p.resolve() in keep_resolved:
                skipped += 1
                continue
            p.unlink(missing_ok=True)
            removed += 1
        except Exception:
            skipped += 1
            continue
    return {"removed": removed, "skipped": skipped}


def align_final_names(doc: Path, audio: Path, html: Path) -> tuple[Path, Path, Path]:
    """
    Enforce one shared prefix for final 3 deliverables:
    <topic>-<timestamp>.txt/.mp3/.html
    """
    base = doc.with_suffix("")
    target_audio = base.with_suffix(".mp3")
    target_html = base.with_suffix(".html")

    if audio.resolve() != target_audio.resolve():
        target_audio.unlink(missing_ok=True)
        audio.replace(target_audio)
        audio = target_audio

    if html.resolve() != target_html.resolve():
        target_html.unlink(missing_ok=True)
        html.replace(target_html)
        html = target_html

    return doc, audio, html


def extract_topic_slug(doc: Path) -> str:
    stem = doc.stem
    m = re.match(r"^(.*)-\d{8}-\d{6}$", stem)
    return (m.group(1) if m else stem).strip() or "meeting"


def is_writable_dir(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        test = path / ".write_test"
        test.write_text("ok", encoding="utf-8")
        test.unlink(missing_ok=True)
        return True
    except Exception:
        return False


def resolve_output_dir(user_outdir: str | None = None) -> Path:
    candidates: list[Path] = []
    candidates.append(PRIVATE_OUTPUT_DIR.expanduser().resolve())
    if user_outdir:
        candidates.append(Path(user_outdir).expanduser().resolve())
    candidates.append(DEFAULT_OUTPUT_DIR)
    candidates.append(Path.cwd() / f"{SKILL_SLUG}-data")

    for c in candidates:
        if is_writable_dir(c):
            return c
    raise RuntimeError("no writable output directory found")


def publish_quick_access(paths: dict[str, Path]) -> dict[str, Path]:
    """
    Copy generated files to shared private root so users can open them directly
    without entering subdirectories.
    """
    private_root = Path.home() / "clawdhome_shared" / "private"
    out: dict[str, Path] = {}
    try:
        private_root.mkdir(parents=True, exist_ok=True)
    except Exception:
        return out

    for k, src in paths.items():
        dst = private_root / src.name
        try:
            shutil.copy2(src, dst)
            out[k] = dst
        except Exception:
            # Best-effort shortcut publishing; keep primary artifacts unchanged.
            continue
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Text minutes file")
    ap.add_argument("--topic", required=True, help="Meeting topic")
    ap.add_argument("--outdir", default=None, help="Fixed output directory for all generated files")
    ap.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Disable automatic cleanup and keep historical/intermediate files",
    )
    ap.add_argument(
        "--quick-copy",
        action="store_true",
        help="Also copy final 3 artifacts to ~/clawdhome_shared/private root for direct opening",
    )
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent
    bridge = script_dir / "audio_bridge.py"
    mindmap = script_dir / "generate_meeting_mindmap.py"
    outdir = resolve_output_dir(args.outdir)

    inp = Path(args.input).expanduser().resolve()
    if not inp.exists():
        print(f"Error: input not found: {inp}", file=sys.stderr)
        return 1

    tts_cmd = [
        sys.executable,
        str(bridge),
        "tts",
        "--input",
        str(inp),
        "--topic",
        args.topic,
        "--provider",
        "auto",
        "--outdir",
        str(outdir),
    ]
    tts = run(tts_cmd)
    if tts.returncode != 0:
        print(tts.stdout, end="")
        print(tts.stderr, end="", file=sys.stderr)
        return tts.returncode
    info = parse_kv_lines(tts.stdout)

    doc = ensure_file(info.get("doc"), "doc")
    brief_audio = ensure_file(info.get("audio"), "audio")
    spoken = Path(info.get("spoken_script", "")).expanduser().resolve() if info.get("spoken_script") else None
    full_text = Path(info.get("full_text", "")).expanduser().resolve() if info.get("full_text") else None
    full_audio = Path(info.get("audio_full", "")).expanduser().resolve() if info.get("audio_full") else None

    # Hard gate: core audio must be mp3
    if brief_audio.suffix.lower() != ".mp3":
        raise RuntimeError(f"brief audio is not mp3: {brief_audio.name}")

    map_cmd = [
        sys.executable,
        str(mindmap),
        "--minutes",
        str(doc),
        "--topic",
        args.topic,
        "--outdir",
        str(outdir),
        "--formats",
        "html",
    ]
    mp = run(map_cmd)
    if mp.returncode != 0:
        print(mp.stdout, end="")
        print(mp.stderr, end="", file=sys.stderr)
        return mp.returncode
    minfo = parse_kv_lines(mp.stdout)
    data = ensure_file(minfo.get("data"), "mindmap data")
    html = ensure_file(minfo.get("html"), "mindmap html")

    # Keep final artifacts under one unified naming prefix.
    doc, brief_audio, html = align_final_names(doc, brief_audio, html)

    # Keep only the 3 core outputs by default.
    best_effort_delete([p for p in [spoken, full_text, full_audio, data] if p is not None])
    cleanup_stats = {"removed": 0, "skipped": 0}
    if not args.no_cleanup:
        cleanup_stats = cleanup_old_outputs(
            outdir=doc.parent,
            topic_slug=extract_topic_slug(doc),
            keep={doc, brief_audio, html},
        )

    print(f"doc={doc}")
    print(f"audio={brief_audio}")
    print(f"mindmap_html={html}")
    print(f"output_dir={outdir}")
    print(f"cleanup_removed={cleanup_stats['removed']}")
    print(f"cleanup_skipped={cleanup_stats['skipped']}")

    if args.quick_copy:
        quick = publish_quick_access(
            {
                "doc": doc,
                "audio": brief_audio,
                "mindmap_html": html,
            }
        )
        if quick:
            print(f"quick_root={Path.home() / 'clawdhome_shared' / 'private'}")
            for k, v in quick.items():
                print(f"quick_{k}={v}")

    print("status=SUCCESS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
