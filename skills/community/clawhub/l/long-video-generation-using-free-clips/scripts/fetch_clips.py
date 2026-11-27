#!/usr/bin/env python3
"""Pick candidates per scene and download only the chosen files (no bulk downloading).

Commands
  pick     PROJECT_DIR [--prefer video|image|mixed] [--scene ID[,ID]] [--redo | --fill] [--allow-offtopic]
           [--max-per-scene N] [--max-downloads N] [--dry-run]
           choose the best unused candidates for each scene, download them, record them in scene['media'].
           Candidates whose tags match their keyword weakly (relevance < 0.3) are skipped unless --allow-offtopic.
           --redo replaces the media of the selected scenes; --fill only tops up scenes that are short of shots.
  reject   PROJECT_DIR SCENE_ID MEDIA_ID [MEDIA_ID ...]
           remove shots you rejected in review and block them from being picked again (then: pick --scene ID --fill)
  review   PROJECT_DIR [--out review.html]
           grab one frame per attached shot and write an HTML contact sheet: look at every shot before rendering
  add-local PROJECT_DIR SCENE_ID FILE --license "..." [--creator ..] [--page-url ..] [--kind video|image]
           register a file you downloaded by hand (Mixkit, your own footage, a licence-checked archive item)
  list     PROJECT_DIR     show what is attached to every scene
"""
import html
import argparse
import math
import shutil
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402

MIN_SHOT = 3.0
WEAK = 0.3  # keep in step with stock_search.WEAK


def needed_shots(scene, project):
    shot = project.get("shot_seconds", 6)
    sec = scene.get("audio_duration") or c.est_seconds(scene.get("narration", ""), project.get("wpm", 150))
    return max(1, math.ceil(sec / shot)), sec


def order(cands, prefer):
    def key(x):
        bonus = 0
        if prefer == "video" and x["kind"] == "video":
            bonus = 3
        elif prefer == "image" and x["kind"] == "image":
            bonus = 3
        return -(x.get("score", 0) + bonus)
    return sorted(cands, key=key)


def resolve_archive(cd):
    meta, _ = c.http_json(f"https://archive.org/metadata/{urllib.parse.quote(cd['id'])}", ttl=86400)
    files = meta.get("files") or []
    pref = [f for f in files if str(f.get("format", "")).lower() in ("h.264", "mpeg4", "h.264 hd") and
            str(f.get("name", "")).lower().endswith(".mp4")]
    if not pref:
        raise c.Fail(f"archive.org/{cd['id']}: no MP4 file found; choose a file by hand and use add-local.")
    pref.sort(key=lambda f: int(f.get("size") or 0))
    name = pref[0]["name"]
    return f"https://archive.org/download/{urllib.parse.quote(cd['id'])}/{urllib.parse.quote(name)}"


def ext_of(url, kind):
    e = Path(urllib.parse.urlsplit(url).path).suffix.lower()
    if e in (".mp4", ".webm", ".mov", ".ogv", ".jpg", ".jpeg", ".png", ".webp"):
        return e
    return ".mp4" if kind == "video" else ".jpg"


def media_entry(cd, rel, info):
    return {"source": cd["source"], "id": cd["id"], "kind": cd["kind"], "file": rel, "page_url": cd.get("page_url", ""),
            "creator": cd.get("creator", ""), "creator_url": cd.get("creator_url", ""), "license": cd.get("license", ""),
            "license_status": cd.get("license_status", "ok"), "attribution_required": cd.get("attribution_required", True),
            "width": info.get("width") or cd.get("width"), "height": info.get("height") or cd.get("height"),
            "duration": round(info.get("duration") or 0, 2) if cd["kind"] == "video" else 0}


def download_candidate(d, cd, key_env):
    url = cd.get("url", "")
    if cd["source"] == "archive":
        url = resolve_archive(cd)
    if not url:
        raise c.Fail(f"{cd['source']}/{cd['id']}: no download URL.")
    rel = f"assets/{cd['source']}_{c.slug(cd['id'])}{ext_of(url, cd['kind'])}"
    dest = Path(d) / rel
    if not dest.exists():
        if cd["source"] == "unsplash" and cd.get("extra", {}).get("download_location") and key_env:
            try:  # Unsplash API guideline: report the download
                c.http_json(cd["extra"]["download_location"], headers={"Authorization": f"Client-ID {key_env}"}, ttl=0)
            except c.Fail as e:
                print(f"  ! unsplash download ping failed: {e}", file=sys.stderr)
        c.download(url, dest)
        time.sleep(0.4)
    info = c.probe(str(dest))
    if not info["has_video"] and cd["kind"] == "video":
        dest.unlink(missing_ok=True)
        raise c.Fail(f"{cd['source']}/{cd['id']}: downloaded file has no video stream.")
    return rel, info


def selected_scenes(project, scene_arg):
    if not scene_arg:
        return project["scenes"]
    ids = {s.strip() for s in scene_arg.split(",") if s.strip()}
    missing = ids - {s["id"] for s in project["scenes"]}
    if missing:
        raise c.Fail(f"No scene with id: {', '.join(sorted(missing))}")
    return [s for s in project["scenes"] if s["id"] in ids]


def cmd_pick(a):
    import os
    if a.redo and a.fill:
        raise c.Fail("Use either --redo (replace) or --fill (top up), not both.")
    project = c.load_project(a.dir)
    scenes = selected_scenes(project, a.scene)
    if a.redo:  # media being replaced must not block their own scene's re-pick
        for sc in scenes:
            sc["media"] = []
    used = {(m["source"], m["id"]) for s in project["scenes"] for m in s.get("media", [])}
    n_down = 0
    for sc in scenes:
        want, sec = needed_shots(sc, project)
        want = min(want, a.max_per_scene)
        have = list(sc.get("media", []))
        if have and not a.fill:
            continue
        if a.fill and len(have) >= want:
            continue
        rejected = {str(x) for x in sc.get("rejected", [])}
        pool = [x for x in sc.get("candidates", []) if f"{x['source']}/{x['id']}" not in rejected]
        off = [x for x in pool if x.get("relevance") is not None and x["relevance"] < WEAK]
        if not a.allow_offtopic:
            pool = [x for x in pool if x not in off]
        cands = [x for x in order(pool, a.prefer) if (x["source"], x["id"]) not in used]
        if not cands:
            print(f"{sc['id']}: no usable candidates"
                  + (f" ({len(off)} skipped as off-topic by tags; change keywords or pass --allow-offtopic)" if off and not a.allow_offtopic else "")
                  + " (run stock_search.py with other keywords, or add-local)")
            continue
        picked, imgs = [], sum(1 for m in have if m.get("kind") == "image")
        need = want - len(have)
        for x in cands:
            if len(picked) >= need:
                break
            if x["kind"] == "image":
                if a.prefer == "mixed" and imgs >= math.ceil(want / 2):
                    continue
                imgs += 1
            picked.append(x)
        print(f"{sc['id']}: need ~{want} shot(s) for {sec:.0f}s, have {len(have)}, picked {len(picked)}"
              + (f" ({len(off)} off-topic skipped)" if off and not a.allow_offtopic else ""))
        if a.dry_run:
            for x in picked:
                rel = x.get("relevance")
                print(f"   - {x['source']}/{x['id']} {x['kind']} {x['width']}x{x['height']} [{x['license']}] "
                      f"relevance={'?' if rel is None else rel} tags='{str(x.get('tags', ''))[:50]}'")
            continue
        media = have
        for x in picked:
            if n_down >= a.max_downloads:
                print(f"Reached --max-downloads {a.max_downloads}; rerun to continue.")
                break
            try:
                rel, info = download_candidate(a.dir, x, os.environ.get("UNSPLASH_ACCESS_KEY", ""))
            except c.Fail as e:
                print(f"   ! {e}", file=sys.stderr)
                continue
            n_down += 1
            used.add((x["source"], x["id"]))
            media.append(media_entry(x, rel, info))
        sc["media"] = media
        c.save_project(a.dir, project)
        if len(media) < want:
            print(f"   note: only {len(media)} of {want}; shots will be longer. Add keywords or use add-local.")
    check = [m for s in project["scenes"] for m in s.get("media", []) if m.get("license_status") != "ok"]
    if check:
        print(f"\n{len(check)} file(s) need a licence check before publishing (commons/archive/unsplash): "
              "open each page_url, confirm the licence and attribution, then set license_status to 'ok'.")
    if not a.dry_run:
        print("\nNext: fetch_clips.py review DIR, and look at every shot. Tags can still mislead; "
              "reject wrong shots with fetch_clips.py reject DIR SCENE ID, then pick --scene ID --fill.")
    return 0


def cmd_reject(a):
    project = c.load_project(a.dir)
    sc = next((s for s in project["scenes"] if s["id"] == a.scene), None)
    if not sc:
        raise c.Fail(f"No scene '{a.scene}'.")
    ids = {str(x) for x in a.ids}
    keep, gone = [], []
    for m in sc.get("media", []):
        (gone if str(m["id"]) in ids or f"{m['source']}/{m['id']}" in ids else keep).append(m)
    if not gone:
        raise c.Fail(f"None of {', '.join(sorted(ids))} is attached to {a.scene}. See: fetch_clips.py list DIR")
    sc["media"] = keep
    rej = set(sc.get("rejected", []))
    rej.update(f"{m['source']}/{m['id']}" for m in gone)
    sc["rejected"] = sorted(rej)
    c.save_project(a.dir, project)
    print(f"{a.scene}: removed {len(gone)} shot(s), {len(keep)} left; they will not be picked again.\n"
          f"Top up with: fetch_clips.py pick DIR --scene {a.scene} --fill")
    return 0


def cmd_review(a):
    c.need_tool("ffmpeg")
    project = c.load_project(a.dir)
    d = Path(a.dir)
    outdir = d / "build" / "review"
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for s in project["scenes"]:
        cells = []
        for m in s.get("media", []):
            src = d / m["file"]
            jpg = outdir / f"{s['id']}_{c.slug(m['source'] + '_' + str(m['id']))}.jpg"
            if src.exists() and not jpg.exists():
                seek = ["-ss", str(min(2.0, (m.get("duration") or 0) / 2))] if m.get("kind") == "video" else []
                try:
                    c.ffmpeg(["-y", *seek, "-i", str(src), "-frames:v", "1", "-vf", "scale=320:-2", str(jpg)])
                except c.Fail as e:
                    print(f"  ! {s['id']} {m['id']}: {e}", file=sys.stderr)
            label = html.escape(f"{m['source']}/{m['id']} ({m.get('kind')})")
            img = f'<img src="{html.escape(jpg.relative_to(d / "build").as_posix())}">' if jpg.exists() else "<i>missing</i>"
            cells.append(f"<figure>{img}<figcaption>{label}</figcaption></figure>")
        kw = html.escape(", ".join(s.get("keywords", [])))
        text = html.escape((s.get("narration") or "")[:160])
        rows.append(f"<section><h2>{html.escape(s['id'])} <small>{kw}</small></h2><p dir=auto>{text}</p>"
                    f"<div class=g>{''.join(cells) or '<i>no media</i>'}</div></section>")
    out = Path(a.out) if a.out else d / "build" / "review.html"
    out.write_text("<!doctype html><meta charset=utf-8><title>Shot review</title><style>body{font:14px sans-serif;"
                   "background:#111;color:#eee;margin:16px}section{margin:0 0 24px}.g{display:flex;flex-wrap:wrap;gap:8px}"
                   "figure{margin:0}img{width:320px;display:block}figcaption{font-size:12px;color:#aaa}"
                   "small{color:#8ab}</style><h1>Shot review: does every shot show what the narration says?</h1>"
                   + "".join(rows), encoding="utf-8")
    print(f"Wrote {out}. Open it in a browser; reject wrong shots with: fetch_clips.py reject DIR SCENE ID")
    return 0


def cmd_add_local(a):
    project = c.load_project(a.dir)
    sc = next((s for s in project["scenes"] if s["id"] == a.scene), None)
    if not sc:
        raise c.Fail(f"No scene '{a.scene}'.")
    src = Path(a.file)
    if not src.exists():
        raise c.Fail(f"File not found: {src}")
    info = c.probe(str(src))
    kind = a.kind or ("video" if info["has_video"] and info["duration"] > 0.2 else "image")
    c.ensure_dirs(a.dir)
    rel = f"assets/local_{c.slug(src.stem)}{src.suffix.lower()}"
    shutil.copy2(src, Path(a.dir) / rel)
    entry = {"source": "local", "id": c.slug(src.stem), "kind": kind, "file": rel, "page_url": a.page_url or "",
             "creator": a.creator or "", "creator_url": "", "license": a.license,
             "license_status": "ok" if a.confirmed else "check", "attribution_required": bool(a.creator),
             "width": info.get("width"), "height": info.get("height"),
             "duration": round(info["duration"], 2) if kind == "video" else 0}
    sc.setdefault("media", []).append(entry)
    c.save_project(a.dir, project)
    print(f"Added {rel} ({kind}) to {a.scene}. Licence status: {entry['license_status']}"
          + ("" if a.confirmed else " (pass --confirmed once you checked the licence terms)"))
    return 0


def cmd_list(a):
    project = c.load_project(a.dir)
    for s in project["scenes"]:
        print(f"{s['id']}: {len(s.get('media', []))} media, {len(s.get('candidates', []))} candidates")
        for m in s.get("media", []):
            print(f"   {m['kind']:<5} {m['source']}/{m['id']}  {m.get('width')}x{m.get('height')}  "
                  f"[{m['license']}] {m['license_status']}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    k = sub.add_parser("pick")
    k.add_argument("dir")
    k.add_argument("--prefer", choices=["video", "image", "mixed"], default="video")
    k.add_argument("--max-per-scene", type=int, default=8)
    k.add_argument("--max-downloads", type=int, default=150)
    k.add_argument("--dry-run", action="store_true")
    k.add_argument("--scene", help="only these scene ids (comma-separated)")
    k.add_argument("--redo", action="store_true", help="replace media already attached (selected scenes only)")
    k.add_argument("--fill", action="store_true", help="top up scenes that have fewer shots than needed")
    k.add_argument("--allow-offtopic", action="store_true",
                   help="also pick candidates whose tags match their keyword weakly (relevance < 0.3)")
    k.set_defaults(fn=cmd_pick)
    r = sub.add_parser("reject")
    r.add_argument("dir")
    r.add_argument("scene")
    r.add_argument("ids", nargs="+")
    r.set_defaults(fn=cmd_reject)
    v = sub.add_parser("review")
    v.add_argument("dir")
    v.add_argument("--out")
    v.set_defaults(fn=cmd_review)
    l = sub.add_parser("add-local")
    l.add_argument("dir")
    l.add_argument("scene")
    l.add_argument("file")
    l.add_argument("--license", required=True)
    l.add_argument("--creator")
    l.add_argument("--page-url")
    l.add_argument("--kind", choices=["video", "image"])
    l.add_argument("--confirmed", action="store_true", help="I checked this file's licence terms")
    l.set_defaults(fn=cmd_add_local)
    s = sub.add_parser("list")
    s.add_argument("dir")
    s.set_defaults(fn=cmd_list)
    a = p.parse_args(argv)
    try:
        return a.fn(a) or 0
    except c.Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
