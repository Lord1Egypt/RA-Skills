#!/usr/bin/env python3
"""Publishing package: chapters, attribution/credits, description, checks, and a thumbnail.

Commands
  credits   PROJECT_DIR   write out/chapters.txt, out/credits.txt, out/description.txt and check YouTube limits
  thumbnail PROJECT_DIR --text "3 WORDS" [--source FILE] [--out PATH]   1280x720 JPG under 2 MB, made with FFmpeg

The description is built from project.json -> youtube.description, then chapters, sources, credits and the
disclosure line. Review it: you are responsible for what is published.
"""
import argparse
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402

SRC_NAMES = {"pexels": "Pexels", "pixabay": "Pixabay", "unsplash": "Unsplash", "commons": "Wikimedia Commons",
             "archive": "Internet Archive", "local": ""}


def chapters(project):
    rows, total = c.timeline(project)
    marks = []
    for r in rows:
        ch = (r["scene"].get("chapter") or "").strip()
        if ch and (not marks or marks[-1][1] != ch):
            marks.append((r["start"], ch))
    if marks and marks[0][0] > 0:
        marks.insert(0, (0.0, "Intro"))
    issues = []
    if len(marks) < 3:
        issues.append("YouTube chapters need at least 3 entries starting at 0:00; add 'chapter' to more scenes.")
    for (t1, _), (t2, n) in zip(marks, marks[1:]):
        if t2 - t1 < 10:
            issues.append(f"A chapter before '{n}' is shorter than 10 seconds (YouTube's minimum).")
    return marks, total, issues


def credit_lines(project):
    seen, lines = set(), []
    for s in project["scenes"]:
        for m in s.get("media", []):
            k = (m["source"], m["id"])
            if k in seen:
                continue
            seen.add(k)
            name = SRC_NAMES.get(m["source"], m["source"])
            who = m.get("creator") or ""
            kind = "Video" if m["kind"] == "video" else "Photo"
            bits = [f"{kind}{' by ' + who if who else ''}{' on ' + name if name else ''}".strip()]
            if m.get("license") and m["source"] in ("commons", "archive", "local"):
                bits.append(f"licence: {m['license']}")
            if m.get("page_url"):
                bits.append(m["page_url"])
            lines.append(" - ".join(bits))
    mu = project.get("music") or {}
    if mu.get("attribution_text"):
        lines.append(f"Music: {mu['attribution_text']}")
    return lines


# Pexels and Pixabay licences do not require attribution, so their per-file lines can be shortened when the
# description is too long. Commons, Internet Archive and local files may carry attribution duties: always kept in full.
OPTIONAL_CREDIT = ("pexels", "pixabay")


def compact_credits(project, level):
    """level 1: one line per source listing creators; level 2: one summary line per source."""
    keep, groups = [], {}
    seen = set()
    for s in project["scenes"]:
        for m in s.get("media", []):
            k = (m["source"], m["id"])
            if k in seen:
                continue
            seen.add(k)
            if m["source"] in OPTIONAL_CREDIT:
                groups.setdefault(m["source"], []).append(m.get("creator") or "")
            else:
                keep.append(m)
    lines = []
    for src, creators in groups.items():
        name = SRC_NAMES.get(src, src)
        if level == 1:
            who = ", ".join(sorted({x for x in creators if x}))
            lines.append(f"{len(creators)} files from {name}" + (f" by {who}" if who else ""))
        else:
            lines.append(f"{len(creators)} files from {name}; full list with links: see the pinned comment")
    sub = dict(project, scenes=[{"media": keep}])
    return lines + credit_lines(dict(sub, music={})) + [x for x in credit_lines(dict(project, scenes=[]))]


def build_description(yt, ch_txt, sources, cred):
    parts = [yt.get("description", "").strip()]
    if ch_txt:
        parts.append("Chapters\n" + ch_txt)
    if sources:
        parts.append("Sources\n" + "\n".join(f"- {x}" for x in sources))
    if cred:
        parts.append("Credits\n" + "\n".join(f"- {x}" for x in cred))
    if yt.get("disclosure"):
        parts.append(yt["disclosure"].strip())
    return "\n\n".join(p for p in parts if p)


def cmd_credits(a):
    project = c.load_project(a.dir)
    d = Path(a.dir)
    marks, total, issues = chapters(project)
    ch_txt = "\n".join(f"{c.fmt_clock(t)} {n}" for t, n in marks)
    cred = credit_lines(project)
    yt = project.get("youtube") or {}
    unchecked = [m for s in project["scenes"] for m in s.get("media", []) if m.get("license_status") != "ok"]
    desc = build_description(yt, ch_txt, project.get("sources"), cred)
    for level in (1, 2):  # shorten optional (Pexels/Pixabay) credits until the description fits YouTube's limit
        if len(desc.encode("utf-8")) <= 5000:
            break
        desc = build_description(yt, ch_txt, project.get("sources"), compact_credits(project, level))
        issues.append(f"Description was over 5000 bytes; Pexels/Pixabay credits shortened (level {level}). "
                      "Post out/credits.txt as a pinned comment so every file stays credited.")
    (d / "out").mkdir(exist_ok=True)
    (d / "out" / "chapters.txt").write_text(ch_txt + "\n", encoding="utf-8")
    (d / "out" / "credits.txt").write_text("\n".join(cred) + "\n", encoding="utf-8")
    (d / "out" / "description.txt").write_text(desc + "\n", encoding="utf-8")
    title = yt.get("title", "")
    tags = yt.get("tags") or []
    if not title:
        issues.append("youtube.title is empty.")
    if len(title) > 100:
        issues.append(f"Title is {len(title)} characters (limit 100).")
    elif len(title) > 70:
        issues.append(f"Title is {len(title)} characters; the end may be cut off in search results.")
    if len(desc.encode("utf-8")) > 5000:
        issues.append(f"Description is {len(desc.encode('utf-8'))} bytes (limit 5000); shorten credits or sources.")
    if sum(len(t) + 1 for t in tags) > 500:
        issues.append("Tags exceed 500 characters in total.")
    if "<" in desc or ">" in desc:
        issues.append("Description contains < or >, which YouTube does not allow.")
    if unchecked:
        issues.append(f"{len(unchecked)} media file(s) still have license_status != 'ok' (verify before publishing).")
    if not yt.get("disclosure"):
        issues.append("youtube.disclosure is empty. Decide about the 'altered or synthetic content' setting in YouTube "
                      "Studio and add a plain line if the voice is synthetic.")
    if not (project.get("review") or {}).get("human_checked"):
        issues.append("review.human_checked is false: watch and fact-check the whole video first.")
    print(f"Wrote out/chapters.txt, out/credits.txt, out/description.txt ({len(cred)} credit lines, {len(marks)} chapters).")
    for i in issues:
        print(f"[CHECK] {i}")
    return 0


def cmd_thumbnail(a):
    project = c.load_project(a.dir)
    d = Path(a.dir)
    src = Path(a.source) if a.source else None
    if not src:
        for s in project["scenes"]:
            for m in s.get("media", []):
                if (d / m["file"]).exists():
                    src = d / m["file"]
                    break
            if src:
                break
    if not src or not src.exists():
        raise c.Fail("No source image or video found; pass --source FILE.")
    font = c.find_font(a.font)
    if not font:
        raise c.Fail("No font file found; pass --font PATH.")
    text = a.text.strip().upper()
    if not text or len(text.split()) > 6:
        raise c.Fail("Use 1 to 6 words of thumbnail text; short text reads on a phone.")
    tf = d / "build" / "thumb.txt"
    tf.parent.mkdir(parents=True, exist_ok=True)
    tf.write_text("\n".join(textwrap.wrap(text, 16)), encoding="utf-8")
    out = Path(a.out) if a.out else d / "out" / "thumbnail.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    info = c.probe(str(src))
    seek = ["-ss", f"{min(2.0, info['duration'] / 2):.2f}"] if info["has_video"] and info["duration"] > 0.5 else []
    vf = ("scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=contrast=1.1:saturation=1.2,"
          "drawbox=x=0:y=ih*0.45:w=iw:h=ih*0.55:color=black@0.35:t=fill,"
          f"drawtext=fontfile='{c.esc_filter_path(font)}':textfile='{c.esc_filter_path(tf)}':fontsize=96:"
          "fontcolor=white:borderw=8:bordercolor=black:line_spacing=10:x=60:y=h-text_h-60")
    for q in (3, 6, 10, 15):
        c.ffmpeg(seek + ["-i", src, "-vf", vf, "-frames:v", "1", "-q:v", str(q), out])
        if out.stat().st_size < 2 * 1024 * 1024:
            break
    size = out.stat().st_size / 1024
    print(f"Wrote {out} ({size:.0f} KB, 1280x720). YouTube accepts JPG/PNG up to 2 MB.")
    print("Check: text readable at phone size, one clear focal point, no misleading promise, no third-party logos.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    cr = sub.add_parser("credits")
    cr.add_argument("dir")
    cr.set_defaults(fn=cmd_credits)
    t = sub.add_parser("thumbnail")
    t.add_argument("dir")
    t.add_argument("--text", required=True)
    t.add_argument("--source")
    t.add_argument("--font")
    t.add_argument("--out")
    t.set_defaults(fn=cmd_thumbnail)
    a = p.parse_args(argv)
    try:
        return a.fn(a) or 0
    except c.Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
