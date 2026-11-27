#!/usr/bin/env python3
"""Project setup and checks for the long-video pipeline.

Commands
  init DIR --title "..."   create a project folder with a project.json template
  validate DIR             lint the plan: length, scenes, originality, YouTube-policy risks
  estimate DIR             words, spoken minutes, scenes, clips needed
  status DIR               how far each scene is (media, files, audio, render)

Standard library only.
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402

SENSITIVE = {"health", "medical", "finance", "financial", "legal", "politics", "political", "news"}

TEMPLATE = {
    "title": "",
    "language": "en",
    "target_minutes": 10,
    "topic_category": "general",
    "angle": "",
    "sources": [],
    "fps": 30,
    "resolution": "1920x1080",
    "wpm": 150,
    "shot_seconds": 6,
    "voice": {"engine": "piper", "voice": "en_US-lessac-medium", "pad": 0.4},
    "music": {"file": "", "volume": 0.15, "duck": True, "license": "", "attribution_text": ""},
    "sfx": [],
    "review": {"human_checked": False, "notes": ""},
    "youtube": {"title": "", "description": "", "tags": [], "disclosure": ""},
    "scenes": [
        {"id": "s01", "title": "Hook", "chapter": "Intro",
         "narration": "Write the spoken text of this scene here. Keep one idea per scene.",
         "keywords": ["concrete noun phrase", "second visual idea"],
         "on_screen_text": "", "notes": ""},
    ],
}


def cmd_init(a):
    d = Path(a.dir)
    p = d / "project.json"
    if p.exists() and not a.force:
        raise c.Fail(f"{p} already exists (use --force to overwrite).")
    c.ensure_dirs(d)
    data = json.loads(json.dumps(TEMPLATE))
    data["title"] = a.title
    data["target_minutes"] = a.minutes
    data["language"] = a.language
    c.save_project(d, data)
    print(f"Created {p} and the working folders. Fill in 'angle', 'sources' and the scenes next.")


def lint(project):
    out = []  # (level, text)

    def warn(t):
        out.append(("WARN", t))

    def info(t):
        out.append(("INFO", t))

    scenes = project["scenes"]
    wpm = project.get("wpm", 150)
    if not project.get("title"):
        warn("No project title.")
    angle = (project.get("angle") or "").strip()
    if len(angle) < 40:
        warn("'angle' is empty or very short. Write the original point of view, analysis or insight the video "
             "adds; template-made videos without it risk YouTube's 'inauthentic content' rules.")
    if not project.get("sources"):
        warn("'sources' is empty. List the facts' sources (links) so claims can be checked and cited.")

    total_words, per = 0, []
    for s in scenes:
        n = len(c.words(s.get("narration", "")))
        per.append(n)
        total_words += n
        if n == 0:
            warn(f"Scene {s['id']} has no narration.")
        if n > 250:
            warn(f"Scene {s['id']} has {n} words (~{n * 60 / wpm / 60:.1f} min); split it so visuals can change with the topic.")
        if not s.get("keywords"):
            warn(f"Scene {s['id']} has no 'keywords' for finding visuals.")
        elif any(len(k.split()) > 5 for k in s["keywords"]):
            info(f"Scene {s['id']}: long keyword phrases search poorly; prefer 2 to 3 concrete words.")
    minutes = total_words / wpm
    target = project.get("target_minutes")
    info(f"{len(scenes)} scenes, {total_words} words, about {minutes:.1f} min at {wpm} wpm.")
    if isinstance(target, (int, float)) and target > 0:
        if abs(minutes - target) / target > 0.15:
            warn(f"Estimated {minutes:.1f} min vs target {target} min (more than 15% off).")
    if minutes < 5:
        warn("Under 5 minutes: this skill is meant for long-form; consider the short-form skill instead.")

    starts = Counter(" ".join(c.words(s.get("narration", ""))[:4]).lower() for s in scenes)
    repeated = [k for k, v in starts.items() if k and v >= 3 and v / len(scenes) >= 0.3]
    if repeated:
        warn(f"Many scenes start with the same words ({repeated[0]!r}); that reads as templated. Vary the structure.")
    sentences = [x.strip().lower() for s in scenes for x in re.split(r"(?<=[.!?])\s+", s.get("narration", "")) if len(x.split()) > 5]
    dup = [k for k, v in Counter(sentences).items() if v > 1]
    if dup:
        warn(f"{len(dup)} sentence(s) repeat verbatim (first: {dup[0][:60]!r}).")

    if sum(1 for s in scenes if s.get("chapter")) < 3 and minutes >= 8:
        info("Fewer than 3 scenes have a 'chapter' title; chapters help viewers and retention.")

    cat = str(project.get("topic_category", "general")).lower()
    engine = (project.get("voice") or {}).get("engine", "")
    if cat in SENSITIVE and engine in ("piper", "elevenlabs", "silent"):
        warn(f"Topic category '{cat}' with a synthetic voice: YouTube's July 2026 guidance targets AI personas "
             "presented as human experts on health, legal, finance or politics. Do not present the voice or an avatar "
             "as a real expert, cite sources on screen, and consider a human narrator.")
    if not (project.get("review") or {}).get("human_checked"):
        info("Human review is not recorded yet. Watch the whole video and fact-check it before publishing, then set "
             "review.human_checked to true.")
    return out


def cmd_validate(a):
    project = c.load_project(a.dir)
    results = lint(project)
    for lvl, t in results:
        print(f"[{lvl}] {t}")
    n = sum(1 for lvl, _ in results if lvl == "WARN")
    print(f"\n{n} warning(s). These are heuristics: they cannot prove a video is original or compliant.")
    return 1 if (a.strict and n) else 0


def cmd_estimate(a):
    project = c.load_project(a.dir)
    wpm = project.get("wpm", 150)
    shot = project.get("shot_seconds", 6)
    total_words = total_clips = 0
    print(f"{'scene':<8} {'words':>6} {'sec':>6} {'shots':>6}")
    for s in project["scenes"]:
        n = len(c.words(s.get("narration", "")))
        sec = n * 60 / wpm
        shots = max(1, math.ceil(sec / shot))
        total_words += n
        total_clips += shots
        print(f"{s['id']:<8} {n:>6} {sec:>6.1f} {shots:>6}")
    print(f"\nTotal: {total_words} words, {total_words / wpm:.1f} min, about {total_clips} shots at {shot}s each.")
    print("Stock APIs are rate-limited; plan roughly one search per keyword per source (see references/sources-and-licenses.md).")


def cmd_status(a):
    project = c.load_project(a.dir)
    d = Path(a.dir)
    print(f"{'scene':<8} {'media':>5} {'files':>5} {'audio':>6} {'render':>6}")
    for s in project["scenes"]:
        media = s.get("media", [])
        files = sum(1 for m in media if m.get("file") and (d / m["file"]).exists())
        audio = "yes" if s.get("audio_duration") else "no"
        rendered = "yes" if (d / "build" / "scenes" / f"{s['id']}.mp4").exists() else "no"
        print(f"{s['id']:<8} {len(media):>5} {files:>5} {audio:>6} {rendered:>6}")
    out = d / "out" / "video.mp4"
    print(f"\nFinal video: {'present' if out.exists() else 'not built yet'}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("dir")
    i.add_argument("--title", required=True)
    i.add_argument("--minutes", type=float, default=10)
    i.add_argument("--language", default="en")
    i.add_argument("--force", action="store_true")
    i.set_defaults(fn=cmd_init)
    v = sub.add_parser("validate")
    v.add_argument("dir")
    v.add_argument("--strict", action="store_true")
    v.set_defaults(fn=cmd_validate)
    e = sub.add_parser("estimate")
    e.add_argument("dir")
    e.set_defaults(fn=cmd_estimate)
    s = sub.add_parser("status")
    s.add_argument("dir")
    s.set_defaults(fn=cmd_status)
    a = p.parse_args(argv)
    try:
        return a.fn(a) or 0
    except c.Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
