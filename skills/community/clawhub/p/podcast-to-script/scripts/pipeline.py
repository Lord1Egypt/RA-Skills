#!/usr/bin/env python3
"""Pipeline driver for podcast-to-script: preflight, progress, stage gates.

Stages (state lives in the episode dir, $TMPDIR/podcast-to-script/<slug>/):
  0  preflight   environment & dependencies (this script's `preflight`)
  A  fetch       transcribe.py -> raw.mp3 + script.txt
  B1 outline     agent writes outline.md            -> gate: verify-outline
  B2 draft       agent writes script.md (per segment)-> gate: verify-script
  C  notes       agent writes notes.md              -> gate: verify-notes

Resume protocol: run `status --dir <episode_dir>`; continue from the first
stage not marked OK. Every gate exits 0/1 so a broken run stops loudly.

Usage:
  python3 pipeline.py preflight
  python3 pipeline.py status [--dir DIR]            # no --dir: scan all episodes
  python3 pipeline.py verify-outline --dir DIR
  python3 pipeline.py verify-script  --dir DIR
  python3 pipeline.py verify-notes   --dir DIR
  python3 pipeline.py draft-timeline --dir DIR      # MM:SS estimate for notes.md
"""
import argparse
import importlib.util
import json
import re
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(tempfile.gettempdir()) / "podcast-to-script"
SEGMENT_RE = re.compile(r'^##\s+第\s*(\d+)\s*段\s*[·•・]\s*(.+)$')
ZH_CHARS_PER_MIN = 260


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_script", Path(__file__).parent / "check_script.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- preflight

def _try_install_faster_whisper() -> bool:
    """Install faster-whisper into the current interpreter: uv first, pip fallback."""
    import shutil
    import subprocess
    candidates = []
    uv = shutil.which("uv")
    if uv:
        candidates.append([uv, "pip", "install", "--python", sys.executable, "faster-whisper"])
    candidates.append([sys.executable, "-m", "pip", "install", "--user", "faster-whisper"])
    for cmd in candidates:
        print(f"[install] {' '.join(cmd)}", flush=True)
        if subprocess.run(cmd).returncode == 0:
            return True
        print(f"[install] failed, trying next installer...")
    return False


def _prefetch_model(model_name: str = "small.en") -> None:
    """Warm the HF cache so the first transcription does not stall on a download."""
    try:
        from faster_whisper import WhisperModel
        print(f"[install] pre-downloading ASR model '{model_name}' "
              f"(first time ~480MB) ...", flush=True)
        WhisperModel(model_name, device="cpu", compute_type="int8")
        print(f"[OK] ASR model '{model_name}' ready")
    except Exception as e:
        print(f"[warn] model prefetch failed ({type(e).__name__}: {e}) — "
              f"the first ASR run will download it instead")


def cmd_preflight(args) -> int:
    hard_fail = False
    print("== preflight ==")

    v = sys.version_info
    ok = v >= (3, 10)
    hard_fail |= not ok
    print(f"[{'OK' if ok else 'FAIL'}] python {v.major}.{v.minor}.{v.micro} (need >= 3.10)")

    for pkg, pip_name in (("numpy", "numpy"), ("faster_whisper", "faster-whisper")):
        try:
            mod = __import__(pkg)
            print(f"[OK] {pkg} {getattr(mod, '__version__', '?')}")
        except ImportError:
            if getattr(args, "install", False) and pkg == "faster_whisper":
                print(f"[--] {pkg} missing — installing ...")
                if _try_install_faster_whisper():
                    try:
                        mod = __import__(pkg)
                        print(f"[OK] {pkg} {getattr(mod, '__version__', '?')} (just installed)")
                        continue
                    except ImportError:
                        pass
            hard_fail = True
            print(f"[FAIL] {pkg} missing — pip install {pip_name}")

    if getattr(args, "install", False) and not hard_fail:
        _prefetch_model()

    try:
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        probe = BASE_DIR / ".write_probe"
        probe.write_text("ok")
        probe.unlink()
        print(f"[OK] workdir writable: {BASE_DIR}")
    except OSError as e:
        hard_fail = True
        print(f"[FAIL] workdir not writable: {BASE_DIR} ({e})")

    # network probes are warnings only (offline --audio runs still work)
    import urllib.error
    for name, url in (("spotify oembed", "https://open.spotify.com/oembed?url=https://open.spotify.com/episode/x"),
                      ("itunes search", "https://itunes.apple.com/search?term=podcast&limit=1"),
                      ("huggingface", "https://huggingface.co")):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "preflight"})
            with urllib.request.urlopen(req, timeout=6) as r:
                r.read(64)
            print(f"[OK] net: {name}")
        except urllib.error.HTTPError:
            print(f"[OK] net: {name} (server responded)")  # 4xx still means reachable
        except Exception as e:
            print(f"[warn] net: {name} unreachable ({type(e).__name__}) — "
                  f"metadata/model-download paths need it; use --proxy")

    print("== preflight " + ("FAILED ==" if hard_fail else "passed =="))
    return 1 if hard_fail else 0


# ---------------------------------------------------------------- status

def count_cjk(text: str) -> int:
    return sum(1 for c in text if "一" <= c <= "鿿")


def transcript_stats(txt_path: Path) -> str:
    text = txt_path.read_text(encoding="utf-8", errors="replace")
    n_chars = len(text.replace("\n", "").replace(" ", ""))
    if count_cjk(text) > n_chars / 4:
        return f"{n_chars} chars ≈ {n_chars / ZH_CHARS_PER_MIN:.0f} min (zh, {ZH_CHARS_PER_MIN} chars/min)"
    n_words = len(text.split())
    return f"{n_words} words ≈ {n_words / 160:.0f} min (en, ~160 wpm)"


def outline_segments(ep_dir: Path) -> list[str]:
    f = ep_dir / "outline.md"
    if not f.exists():
        return []
    return [m.group(2).strip() for line in f.read_text(encoding="utf-8").splitlines()
            if (m := SEGMENT_RE.match(line.strip()))]


def script_segments(ep_dir: Path) -> list[str]:
    f = ep_dir / "script.md"
    if not f.exists():
        return []
    return [m.group(2).strip() for line in f.read_text(encoding="utf-8").splitlines()
            if (m := SEGMENT_RE.match(line.strip()))]


def stage_report(ep_dir: Path) -> tuple[list[tuple[str, bool, str]], str]:
    """Return ([(stage, ok, detail)], next_action)."""
    checker = load_checker()
    rows = []

    txt = ep_dir / "script.txt"
    a_ok = txt.exists() and txt.stat().st_size > 0
    a_detail = "script.txt missing/empty — run transcribe.py"
    if a_ok:
        imgs = [p for p in (ep_dir / "images").glob("*")
                if p.name != "manifest.json"] if (ep_dir / "images").exists() else []
        a_detail = transcript_stats(txt) + (f", {len(imgs)} image(s)" if imgs else "")
    rows.append(("A fetch", a_ok, a_detail))

    out_segs = outline_segments(ep_dir)
    b1_ok = len(out_segs) > 0
    rows.append(("B1 outline", b1_ok,
                 f"{len(out_segs)} segments planned" if b1_ok else "outline.md missing/no segments"))

    script = ep_dir / "script.md"
    if script.exists():
        issues = checker.validate_script(script)
        done_segs = script_segments(ep_dir)
        missing = [s for s in out_segs if s not in done_segs]
        b2_ok = not issues and (not out_segs or not missing)
        detail = "valid" if b2_ok else "; ".join(
            ([f"{len(issues)} format issue(s)"] if issues else []) +
            ([f"missing segments: {', '.join(missing[:3])}{'…' if len(missing) > 3 else ''}"]
             if missing and out_segs else []))
        rows.append(("B2 draft", b2_ok, f"{len(done_segs)} segments, {detail}"))
    else:
        rows.append(("B2 draft", False, "script.md missing"))

    notes = ep_dir / "notes.md"
    if notes.exists():
        n_issues = checker.validate_notes(notes)
        rows.append(("C notes", not n_issues,
                     "valid" if not n_issues else f"{len(n_issues)} issue(s)"))
    else:
        rows.append(("C notes", False, "notes.md missing"))

    next_stage = next((name for name, ok, _ in rows if not ok), None)
    next_action = {
        "A fetch": "run: transcribe.py <url>",
        "B1 outline": "agent: write outline.md from script.txt",
        "B2 draft": "agent: write/fix script.md per outline.md, then verify-script",
        "C notes": "agent: write notes.md (draft-timeline helps), then verify-notes",
        None: "done — ready for the production pipeline",
    }[next_stage]
    return rows, next_action


def cmd_status(args) -> int:
    if args.dir:
        ep_dirs = [Path(args.dir)]
    else:
        if not BASE_DIR.exists():
            print(f"no episodes yet ({BASE_DIR} does not exist)")
            return 0
        ep_dirs = sorted([d for d in BASE_DIR.iterdir() if d.is_dir()])
        if not ep_dirs:
            print(f"no episodes under {BASE_DIR}")
            return 0
    for ep_dir in ep_dirs:
        print(f"== {ep_dir} ==")
        rows, next_action = stage_report(ep_dir)
        for name, ok, detail in rows:
            print(f"  [{'OK' if ok else '--'}] {name}: {detail}")
        print(f"  next: {next_action}\n")
    return 0


# ---------------------------------------------------------------- gates

def _require_dir(args) -> Path:
    if not args.dir:
        sys.exit("ERROR: --dir is required (episode dir under $TMPDIR/podcast-to-script/)")
    return Path(args.dir)


def cmd_verify_outline(args) -> int:
    ep_dir = _require_dir(args)
    f = ep_dir / "outline.md"
    if not f.exists():
        print(f"FAIL: {f} missing")
        return 1
    segs = outline_segments(ep_dir)
    if not segs:
        print("FAIL: outline.md has no segment headers (## 第 N 段 · 子标题)")
        return 1
    if len(segs) < 2:
        print(f"[warn] only {len(segs)} segment — short episode? usually 3-8")
    print(f"OK: outline.md — {len(segs)} segments")
    for i, s in enumerate(segs, 1):
        print(f"  {i}. {s}")
    return 0


def cmd_verify_script(args) -> int:
    ep_dir = _require_dir(args)
    f = ep_dir / "script.md"
    if not f.exists():
        print(f"FAIL: {f} missing")
        return 1
    checker = load_checker()
    issues = checker.validate_script(f)
    out_segs, done_segs = outline_segments(ep_dir), script_segments(ep_dir)
    missing = [s for s in out_segs if s not in done_segs]
    if missing:
        issues.append(f"outline 中的分段尚未写入 script.md: {', '.join(missing)}")
    for issue in issues:
        print(f"  ⚠️ {issue}")
    if issues:
        print(f"FAIL: {len(issues)} issue(s)")
        return 1
    print(f"OK: script.md — {len(done_segs)} segments, format clean")
    return 0


def cmd_verify_notes(args) -> int:
    ep_dir = _require_dir(args)
    f = ep_dir / "notes.md"
    if not f.exists():
        print(f"FAIL: {f} missing")
        return 1
    checker = load_checker()
    issues = checker.validate_notes(f)
    for issue in issues:
        print(f"  ⚠️ {issue}")
    if issues:
        print(f"FAIL: {len(issues)} issue(s)")
        return 1
    print("OK: notes.md — format clean")
    return 0


def cmd_draft_timeline(args) -> int:
    """Draft `- MM:SS 段名` lines from script.md char counts (260 chars/min zh)."""
    ep_dir = _require_dir(args)
    f = ep_dir / "script.md"
    if not f.exists():
        print(f"FAIL: {f} missing")
        return 1
    checker = load_checker()
    segs, title, cur = [], None, []
    for line in f.read_text(encoding="utf-8").splitlines():
        m = SEGMENT_RE.match(line.strip())
        if m:
            if title is not None:
                segs.append((title, cur))
            title, cur = m.group(2).strip(), []
        elif title is not None:
            cur.append(line.strip())
    if title is not None:
        segs.append((title, cur))
    t = 0.0
    print("# draft timeline (estimate; calibrate after synthesis):")
    for name, lines in segs:
        mm, ss = int(t // 60), int(t % 60)
        print(f"- {mm:02d}:{ss:02d} {name}")
        chars = sum(len(re.sub(r"\s", "", ln)) for ln in lines)
        t += chars / ZH_CHARS_PER_MIN * 60
    mm, ss = int(t // 60), int(t % 60)
    print(f"# total ≈ {mm:02d}:{ss:02d}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("preflight", cmd_preflight),
                     ("status", cmd_status),
                     ("verify-outline", cmd_verify_outline),
                     ("verify-script", cmd_verify_script),
                     ("verify-notes", cmd_verify_notes),
                     ("draft-timeline", cmd_draft_timeline)):
        p = sub.add_parser(name)
        p.add_argument("--dir", help="episode dir (default for status: scan all)")
        if name == "preflight":
            p.add_argument("--install", action="store_true",
                           help="first-run init: install missing deps (faster-whisper) "
                                "and pre-download the default ASR model")
        p.set_defaults(fn=fn)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
