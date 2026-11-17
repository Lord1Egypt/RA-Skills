#!/usr/bin/env python3
"""PPT / courseware narration: one notes file with page markers -> per-page voiceover + timings.

  python3 scripts/slides.py build NOTES.md -o out [--preset koubo] [--dry-run]
      split NOTES.md at page markers (`=== 1 ===`, `=== 第1页 ===`, `=== slide 1 ===`),
      voice every page with scripts/voiceover.py, then write
        out/page-01/voiceover.wav|srt ...   one folder per page (lines/ cache reused on re-run)
        out/narration.wav                   all pages joined, with --page-gap seconds between pages
        out/narration.srt                   all subtitles, re-timed onto the joined audio
        out/slides.json                     page -> start, end, duration (seconds)
        out/concat.txt                      ffmpeg concat list for exported slide images
  python3 scripts/slides.py check NOTES.md       list the pages found, without calling anything

Python 3.9+ standard library only. MIT licence (see LICENSE.txt).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = re.compile(r"^\s*===\s*(?:第\s*)?(?:slide\s*|page\s*|p)?(\d+)\s*(?:页)?\s*(?:[:：|｜-]\s*(.*?))?\s*===\s*$", re.I)


def split_notes(text):
    """Return (front_matter, [(page_no, title, body), ...])."""
    front = ""
    m = re.match(r"^\s*---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        front, text = m.group(0), text[m.end():]
    pages, cur = [], None
    for line in text.splitlines():
        mm = MARK.match(line)
        if mm:
            cur = [int(mm.group(1)), (mm.group(2) or "").strip(), []]
            pages.append(cur)
        elif cur is not None:
            cur[2].append(line)
    out = []
    for no, title, body in pages:
        body = "\n".join(body).strip()
        if re.sub(r"<!--.*?-->|^\s*#.*$", "", body, flags=re.S | re.M).strip():
            out.append((no, title, body))
        else:
            out.append((no, title, ""))
    if not out:
        raise SystemExit("no page markers found: put a line like `=== 1 ===` or `=== 第1页 ===` before each page's notes")
    nos = [p[0] for p in out]
    if len(set(nos)) != len(nos):
        raise SystemExit("duplicate page numbers: %s" % nos)
    return front, out


def srt_time(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def parse_srt_time(s):
    h, m, rest = s.strip().split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000.0


def read_srt(path):
    cues = []
    with open(path, encoding="utf-8") as f:
        for block in f.read().strip().split("\n\n"):
            rows = block.strip().splitlines()
            if len(rows) >= 3 and "-->" in rows[1]:
                a, b = rows[1].split("-->")
                cues.append((parse_srt_time(a), parse_srt_time(b), "\n".join(rows[2:])))
    return cues


def cmd_check(a):
    with open(a.file, encoding="utf-8") as f:
        _, pages = split_notes(f.read())
    for no, title, body in pages:
        n = len([l for l in body.splitlines() if l.strip() and not l.strip().startswith("#")])
        print("page %02d  %-24s %s" % (no, title[:24], ("%d lines" % n) if body else "(no narration: silent page)"))
    return 0


def cmd_build(a):
    with open(a.file, encoding="utf-8") as f:
        front, pages = split_notes(f.read())
    os.makedirs(a.output, exist_ok=True)
    params, chunks, cues, table, t = None, [], [], [], 0.0
    silent = []
    for idx, (no, title, body) in enumerate(pages):
        folder = os.path.join(a.output, "page-%02d" % no)
        os.makedirs(folder, exist_ok=True)
        if not body:
            silent.append((idx, no, title))
            table.append({"page": no, "title": title, "start": None, "end": None, "duration": a.silent_page})
            continue
        src = os.path.join(folder, "notes.md")
        with open(src, "w", encoding="utf-8") as f:
            f.write(front + body + "\n")
        cmd = [sys.executable, os.path.join(HERE, "voiceover.py"), "script", src, "-o", folder]
        for opt in ("preset", "gap", "max_chars", "model"):
            v = getattr(a, opt)
            if v is not None:
                cmd += ["--" + opt.replace("_", "-"), str(v)]
        for flag in ("dry_run", "fresh", "speaker_labels"):
            if getattr(a, flag):
                cmd.append("--" + flag.replace("_", "-"))
        print("page %02d  %s" % (no, title), file=sys.stderr)
        r = subprocess.run(cmd)
        if r.returncode != 0:
            raise SystemExit("page %02d failed (exit %d); fix it and re-run: finished pages are reused from their lines/ cache" % (no, r.returncode))
        with wave.open(os.path.join(folder, "voiceover.wav"), "rb") as w:
            prm = (w.getnchannels(), w.getsampwidth(), w.getframerate())
            frames = w.readframes(w.getnframes())
        if params and prm != params:
            raise SystemExit("page %02d WAV format %s differs from %s" % (no, prm, params))
        params = params or prm
        if chunks:
            chunks.append(b"\x00" * int(params[0] * params[1] * params[2] * a.page_gap))
            t += a.page_gap
        dur = len(frames) / float(params[0] * params[1] * params[2])
        chunks.append(frames)
        for s, e, text in read_srt(os.path.join(folder, "voiceover.srt")):
            cues.append((t + s, t + e, text))
        table.append({"page": no, "title": title, "start": round(t, 3), "end": round(t + dur, 3), "duration": round(dur, 3)})
        t += dur
    if params is None:
        raise SystemExit("every page is empty: nothing to voice")
    with wave.open(os.path.join(a.output, "narration.wav"), "wb") as w:
        w.setnchannels(params[0])
        w.setsampwidth(params[1])
        w.setframerate(params[2])
        w.writeframes(b"".join(chunks))
    with open(os.path.join(a.output, "narration.srt"), "w", encoding="utf-8") as f:
        for n, (s, e, c) in enumerate(cues, 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (n, srt_time(s), srt_time(e), c))
    # image timeline for a slideshow video: each voiced page lasts its audio plus the page gap
    with open(os.path.join(a.output, "concat.txt"), "w", encoding="utf-8") as f:
        f.write("# ffmpeg -f concat -safe 0 -i concat.txt -i narration.wav -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest slides.mp4\n")
        f.write("# export slides as images named %s (e.g. 01.png) next to this file; silent pages are not in narration.wav\n" % a.image_pattern)
        voiced = [r for r in table if r["start"] is not None]
        for i, r in enumerate(voiced):
            hold = r["duration"] + (a.page_gap if i + 1 < len(voiced) else 0)
            f.write("file '%s'\nduration %.3f\n" % (a.image_pattern % r["page"], hold))
        if voiced:
            f.write("file '%s'\n" % (a.image_pattern % voiced[-1]["page"]))
    with open(os.path.join(a.output, "slides.json"), "w", encoding="utf-8") as f:
        json.dump({"total": round(t, 3), "page_gap": a.page_gap, "dry_run": a.dry_run, "pages": table}, f, ensure_ascii=False, indent=2)
    for r in table:
        print("page %02d  %s" % (r["page"], ("%.1fs-%.1fs" % (r["start"], r["end"])) if r["start"] is not None else "silent"))
    print("wrote narration.wav (%.1fs) + narration.srt + slides.json + concat.txt in %s%s"
          % (t, a.output, "  [dry-run: silent placeholder audio]" if a.dry_run else ""))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="PPT / courseware notes -> per-page voiceover, joined narration, SRT and slide timings")
    p.add_argument("--version", action="version", version="slides.py 1.0.0")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="list pages found in the notes file")
    c.add_argument("file")
    b = sub.add_parser("build", help="voice every page and join them")
    b.add_argument("file")
    b.add_argument("-o", "--output", default="out")
    b.add_argument("--preset")
    b.add_argument("--gap", type=float, help="silence between lines inside a page")
    b.add_argument("--max-chars", type=int)
    b.add_argument("--model", choices=("expressive", "standard"))
    b.add_argument("--speaker-labels", action="store_true")
    b.add_argument("--page-gap", type=float, default=0.8, help="silence between pages in narration.wav (default 0.8s)")
    b.add_argument("--silent-page", type=float, default=3.0, help="suggested seconds for pages without notes (slides.json only)")
    b.add_argument("--image-pattern", default="%02d.png", help="slide image file name pattern for concat.txt")
    b.add_argument("--dry-run", action="store_true")
    b.add_argument("--fresh", action="store_true")
    a = p.parse_args(argv)
    return cmd_check(a) if a.cmd == "check" else cmd_build(a)


if __name__ == "__main__":
    sys.exit(main())
