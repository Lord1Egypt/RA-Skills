"""
Plan variable shot durations from Korean subtitle reading time.

Input:
  subs.json: {"S01": "subtitle text", "S02": "..."}

Output:
  durations.json:
  {
    "S01": {"subtitle": "...", "read_chars": 12, "duration_s": 2.55, "frames_16fps": 41},
    ...
  }

Optionally updates shotlist/shotlist.json duration_s so the writer script,
video renderer, and final compose share the same timing.
"""
import argparse
import json
import math
import re
from pathlib import Path


PUNCT_RE = re.compile(r"[\s\.,!?;:()\[\]{}\"'`~\-_/\\|+=*#@<>，。！？、；：]+")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def clean_text(text):
    return " ".join(str(text).replace("\\n", " ").replace("\r", " ").replace("\n", " ").split())


def reading_chars(text):
    compact = PUNCT_RE.sub("", clean_text(text))
    return len(compact)


def duration_for(text, cps, min_s, max_s, lead_s, tail_s):
    chars = reading_chars(text)
    raw = chars / cps + lead_s + tail_s
    dur = max(min_s, raw)
    if max_s > 0:
        dur = min(max_s, dur)
    return round(dur, 2), chars


def load_order(project, subs):
    shotlist_path = project / "shotlist" / "shotlist.json"
    if shotlist_path.exists():
        shotlist = read_json(shotlist_path)
        ids = [s["shot_id"] for s in shotlist if s.get("shot_id") in subs]
        ids.extend(sid for sid in subs if sid not in ids)
        return ids, shotlist, shotlist_path
    return sorted(subs), None, shotlist_path


def update_shotlist(shotlist, durations):
    if not shotlist:
        return None
    by_id = {sid: data["duration_s"] for sid, data in durations.items()}
    for shot in shotlist:
        sid = shot.get("shot_id")
        if sid in by_id:
            shot["duration_s"] = by_id[sid]
            shot["duration_source"] = "subtitle_reading_time"
    return shotlist


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--subs", required=True, help="JSON file: {sid: subtitle text}")
    ap.add_argument("--out", help="Default: <project>/durations.json")
    ap.add_argument("--cps", type=float, default=5.5, help="Korean reading speed in visible chars per second")
    ap.add_argument("--min", dest="min_s", type=float, default=1.6, help="Minimum shot duration")
    ap.add_argument("--max", dest="max_s", type=float, default=5.0, help="Maximum shot duration; <=0 disables cap")
    ap.add_argument("--lead", dest="lead_s", type=float, default=0.25, help="Subtitle lead-in / breath time")
    ap.add_argument("--tail", dest="tail_s", type=float, default=0.35, help="Subtitle tail / reaction time")
    ap.add_argument("--final-tail", type=float, default=0.75, help="Extra tail added to the final subtitle")
    ap.add_argument("--fps", type=float, default=16.0, help="Wan native FPS estimate for frame planning")
    ap.add_argument("--update-shotlist", action="store_true")
    args = ap.parse_args()

    project = Path(args.project)
    subs = read_json(args.subs)
    order, shotlist, shotlist_path = load_order(project, subs)
    durations = {}
    last_sid = order[-1] if order else None

    for sid in order:
        text = clean_text(subs[sid])
        tail = args.tail_s + (args.final_tail if sid == last_sid else 0.0)
        dur, chars = duration_for(text, args.cps, args.min_s, args.max_s, args.lead_s, tail)
        durations[sid] = {
            "subtitle": text,
            "read_chars": chars,
            "duration_s": dur,
            "frames_16fps": int(math.ceil(dur * args.fps)),
        }

    total = round(sum(item["duration_s"] for item in durations.values()), 2)
    payload = {
        "schema": "local-video-subtitle-durations-v1",
        "reading_speed_cps": args.cps,
        "total_duration_s": total,
        "items": durations,
    }

    out = Path(args.out) if args.out else project / "durations.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (project / "meta").mkdir(parents=True, exist_ok=True)
    (project / "meta" / "subtitle_durations.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    if args.update_shotlist and shotlist:
        updated = update_shotlist(shotlist, durations)
        shotlist_path.write_text(json.dumps(updated, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"durations -> {out}")
    print(f"total_duration_s={total}")


if __name__ == "__main__":
    main()
