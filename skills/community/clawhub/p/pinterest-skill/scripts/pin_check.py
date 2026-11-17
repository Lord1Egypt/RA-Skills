#!/usr/bin/env python3
"""Check every pin in plan.json against Pinterest's published limits and the spam patterns
practitioners report, before anything is uploaded. Fix what can be fixed safely, as new files.

    python3 scripts/pin_check.py plan.json
    python3 scripts/pin_check.py plan.json --fix          # converted copies in fixed/, plan updated
    python3 scripts/pin_check.py plan.json --log pins-log.jsonl

Checks, per pin:
- media: JPEG/PNG up to 20 MB, 2:3 recommended (taller than 1:2.1 gets cut in the feed); video
  MP4/MOV/M4V, H.264/H.265, 4 s to 15 min, up to 2 GB, 1:1, 2:3, 4:5 or 9:16;
- text: title up to 100 characters with the keyword in the first 40 (what the feed shows),
  description up to 800 (warning above 500), alt text up to 500, no hashtags (they do nothing on
  Pinterest), the same title or description reused on another pin;
- link: a full https:// address or a key in links, up to 2,048 characters, no shorteners, no
  redirects (from page.json), and the pin matching its page (shares words with its title and headings);
- board: chosen, and one of the account's boards;
- freshness: two pins with the same picture, or built from the same source photo, for one link;
  a picture already pinned to the same page (from the log; tracking parameters don't make it new);
  one page sent to several boards on one day;
- pace: pins per account per day (counting the log), new pins for one page about a week apart,
  times already in the past;
- the image text: readable at feed size, and only characters the font can draw (render manifest).
Exit code 0 means nothing blocks; warnings are worth reading. Run it until it passes.
"""
import argparse, json, os, re, shutil, subprocess, sys
from collections import defaultdict
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pinlib as P  # noqa: E402

UPLOAD_VIDEO = (".mp4", ".mov", ".m4v")


class Report:
    def __init__(self):
        self.items = []

    def error(self, pid, msg):
        self.items.append(("error", pid, msg))

    def warn(self, pid, msg):
        self.items.append(("warning", pid, msg))

    def fixed(self, pid, msg):
        self.items.append(("fixed", pid, msg))

    def errors(self):
        return [i for i in self.items if i[0] == "error"]


def fixed_path(base, pin, ext):
    return os.path.join(base, "fixed", f"{pin['id']}{ext}")


def check_image(pin, path, rep, fix, base):
    from PIL import Image
    pid = pin["id"]
    try:
        with Image.open(path) as im:
            fmt, (w, h), mode = im.format, im.size, im.mode
    except Exception:
        if path.lower().endswith((".heic", ".heif")):
            fmt, w, h, mode = "HEIC", 0, 0, ""
        else:
            rep.error(pid, f"{pin.get('file')} can't be opened as an image")
            return
    mb = os.path.getsize(path) / 1e6
    problems = []
    if fmt not in P.IMAGE_TYPES:
        problems.append(f"{fmt} isn't accepted (JPEG or PNG)")
    if mb > P.IMAGE_MAX_MB:
        problems.append(f"{mb:.1f} MB is over Pinterest's {P.IMAGE_MAX_MB} MB")
    if mode in ("CMYK", "I;16", "I;16B", "I", "LAB"):
        problems.append(f"{mode} colours don't show right on screens (needs RGB)")
    if problems:
        if fix:
            out = fixed_path(base, pin, ".jpg")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            im = P.open_image(path)
            if max(im.size) > 3000:
                im.thumbnail((3000, 3000))
            im.save(out, "JPEG", quality=88, optimize=True)
            pin["file"] = P.rel(out, base)
            rep.fixed(pid, "; ".join(problems) + f": saved an RGB JPEG copy as {pin['file']}")
            return check_image(pin, out, rep, False, base)
        for p in problems:
            rep.error(pid, p + " (run with --fix)")
        if not w:
            return
    r = w / h
    if abs(r - 2 / 3) <= 0.02:
        pass
    elif r < 1 / 2.1:
        rep.error(pid, f"{w}x{h} is taller than 1:2.1; Pinterest cuts it off in the feed. Re-render it at 1000x1500")
    elif r > 1:
        rep.warn(pid, f"{w}x{h} is landscape: it shows as a small tile in a feed of tall pins. 2:3 (1000x1500) works best")
    else:
        rep.warn(pid, f"{w}x{h} isn't 2:3; Pinterest recommends 1000x1500")
    if w < 600:
        rep.warn(pid, f"only {w} px wide: it will look soft on large screens (1000 px recommended)")


def check_video(pin, path, rep, fix, base):
    pid = pin["id"]
    info = P.ffprobe(path)
    if info is None:
        rep.warn(pid, "ffprobe isn't installed, so the video wasn't checked (python3 scripts/check_setup.py)")
        return
    v = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    if not v:
        rep.error(pid, "no video stream found")
        return
    dur = P.duration(info)
    mb = os.path.getsize(path) / 1e6
    w, h = int(v.get("width", 0) or 0), int(v.get("height", 0) or 0)
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        try:
            rot = abs(int(float(sd.get("rotation", 0) or 0)))
        except (TypeError, ValueError):
            pass
    try:
        rot = rot or abs(int((v.get("tags") or {}).get("rotate", 0)))
    except (TypeError, ValueError):
        pass
    if rot % 180 == 90:
        w, h = h, w
    problems = []
    if not path.lower().endswith(UPLOAD_VIDEO):
        problems.append("the file type isn't MP4, MOV or M4V")
    if v.get("codec_name") not in ("h264", "hevc"):
        problems.append(f"the video codec is {v.get('codec_name')} (H.264 or H.265 needed)")
    if v.get("pix_fmt", "yuv420p") not in ("yuv420p", "yuvj420p"):
        problems.append(f"the pixel format is {v.get('pix_fmt')} (8-bit 4:2:0 plays everywhere)")
    if problems and fix and shutil.which("ffmpeg"):
        out = fixed_path(base, pin, ".mp4")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
        pin["file"] = P.rel(out, base)
        rep.fixed(pid, "; ".join(problems) + f": re-encoded as {pin['file']}")
        return check_video(pin, out, rep, False, base)
    for p in problems:
        rep.error(pid, p + " (run with --fix)")
    if not dur:
        rep.warn(pid, "couldn't read the video's length")
    elif dur < P.VIDEO_MIN_S:
        rep.error(pid, f"{dur:.1f} s is shorter than Pinterest's 4 s minimum")
    elif dur > P.VIDEO_MAX_S:
        rep.error(pid, f"{dur / 60:.1f} min is longer than Pinterest's 15 min maximum")
    elif dur > 60:
        rep.warn(pid, f"{dur:.0f} s: Pinterest recommends short videos (6 to 15 s); cut it down if the point comes late")
    if mb > P.VIDEO_MAX_MB:
        rep.error(pid, f"{mb:.0f} MB is over 2 GB")
    r = w / h if h else 0
    near = min(P.VIDEO_RATIOS.items(), key=lambda kv: abs(kv[1] - r))
    if abs(near[1] - r) > 0.02:
        rep.warn(pid, f"{w}x{h} isn't 1:1, 2:3, 4:5 or 9:16; fit it with video.py fit")
    elif r > 1:
        rep.warn(pid, "landscape video shows as a small tile; 2:3 or 9:16 fills the feed")
    if min(w, h) < 720:
        rep.warn(pid, f"{w}x{h} is under 720p; Pinterest recommends 720p or higher")


def load_manifests(plan, base):
    """file path -> render manifest entry (with its source photos resolved to absolute paths)."""
    out = {}
    for mf in plan.get("manifests", []) or []:
        mp = P.resolve(base, mf)
        if not os.path.exists(mp):
            continue
        try:
            entries = json.load(open(mp, encoding="utf-8")).get("pins", [])
        except Exception:
            continue
        mdir = os.path.dirname(mp)
        for m in entries:
            spec_dir = os.path.normpath(os.path.join(mdir, m.get("spec_dir") or ".."))
            m = dict(m, sources=[os.path.normpath(P.resolve(spec_dir, s)) for s in m.get("images", [])])
            out[os.path.normpath(P.resolve(spec_dir, m["file"]))] = m
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("plan")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--log", help="pins already posted (default: pins-log.jsonl next to plan.json)")
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.plan))
    plan = P.load_plan(a.plan)
    log_path = a.log or os.path.join(base, "pins-log.jsonl")
    posted = P.read_log(log_path)
    rep = Report()
    accounts, links, pins = plan["accounts"], plan["links"], plan["pins"]
    rules = dict({"max_per_day": 5, "link_gap_days": 7}, **(plan.get("rules") or {}))
    if not pins:
        sys.exit("plan.json has no pins")
    if not accounts:
        sys.exit("plan.json has no accounts: add one with its boards (references/plan-json.md)")
    P.check_ids(pins)

    manifest = load_manifests(plan, base)
    prints, sources, urls, src_prints = {}, {}, {}, {}
    tz_of = lambda k: (accounts.get(k) or {}).get("timezone") or plan.get("timezone")
    now = datetime.now()

    for pin in pins:
        pid = pin["id"]
        acc = accounts.get(pin.get("account"))
        if not acc:
            rep.error(pid, f"account '{pin.get('account')}' isn't in accounts ({', '.join(accounts)})")
        # media
        path = P.resolve(base, pin.get("file"))
        if not path or not os.path.exists(path):
            rep.error(pid, f"media file not found: {pin.get('file')}")
            continue
        video = path.lower().endswith(P.VIDEO_EXT)
        (check_video if video else check_image)(pin, path, rep, a.fix, base)
        path = P.resolve(base, pin.get("file"))
        prints[pid] = P.media_fingerprint(path)
        m = manifest.get(os.path.normpath(path))
        explicit = {os.path.normpath(P.resolve(base, s)) if ("/" in s or "." in s) else s
                    for s in (pin.get("sources") or []) if isinstance(s, str)}
        sources[pid] = set(m.get("sources", [])) | explicit if m else explicit
        src_prints[pid] = [f for f in (P.media_fingerprint(s) for s in sources[pid] if os.path.exists(s)) if f]
        if m:
            for w in m.get("warnings", []):
                if "can't draw" in w:
                    rep.error(pid, "render: " + w)
                else:
                    rep.warn(pid, "render: " + w)
            if m.get("headline_px_in_feed") and m["headline_px_in_feed"] < 14:
                rep.warn(pid, f"the headline is {m['headline_px_in_feed']} px tall in the feed: too small to read on a phone. Fewer words, bigger type")

        # text
        link = links.get(pin.get("link")) if isinstance(pin.get("link"), str) else None
        link = link if isinstance(link, dict) else {}
        keywords = [k for k in (pin.get("keywords") or link.get("keywords") or []) if isinstance(k, str)]
        title, desc, alt = pin.get("title", ""), pin.get("description", ""), pin.get("alt", "")
        if not title.strip():
            rep.error(pid, "no title: the title is the pin's first search signal and what the feed shows")
        elif len(title) > P.TITLE_MAX:
            rep.error(pid, f"title is {len(title)} characters (max {P.TITLE_MAX})")
        if title and keywords and not any(P.has_phrase(title[:P.TITLE_FEED], k) for k in keywords):
            rep.warn(pid, f"none of the keywords ({', '.join(keywords[:3])}) is in the first {P.TITLE_FEED} characters of the title, which is all the feed shows")
        if not desc.strip():
            rep.warn(pid, "no description: write 1 to 3 sentences that say what's on the page, keywords first")
        elif len(desc) > P.DESC_MAX:
            rep.error(pid, f"description is {len(desc)} characters (max {P.DESC_MAX})")
        elif len(desc) > P.DESC_SOFT:
            rep.warn(pid, f"description is {len(desc)} characters; some Pinterest screens cut at {P.DESC_SOFT}, so keep the point in the first {P.DESC_SOFT}")
        if desc and keywords and not any(P.has_phrase(desc, k) for k in keywords):
            rep.warn(pid, "the description doesn't use any of the link's keywords")
        tags = re.findall(r"(?<![\w&])#[^\W\d_][\w]*", title + " " + desc)
        if tags:
            rep.warn(pid, f"hashtags ({' '.join(tags[:4])}) do nothing on Pinterest any more; use the words themselves in the text")
        if alt and len(alt) > P.ALT_MAX:
            rep.error(pid, f"alt text is {len(alt)} characters (max {P.ALT_MAX})")
        if re.search(r"https?://", title + " " + desc):
            rep.warn(pid, "a URL in the text isn't clickable on Pinterest; the pin's link is the one that counts")

        # link
        url, err = P.link_of(pin, links)
        if err:
            rep.error(pid, err)
        elif not url:
            rep.warn(pid, "no link: the pin can't send anyone to the site. Add the page's URL unless that's intended")
        else:
            urls[pid] = P.canonical(url)
            if len(url) > P.LINK_MAX:
                rep.error(pid, f"link is {len(url)} characters (max {P.LINK_MAX})")
            if P.domain(url) in P.SHORTENERS:
                rep.error(pid, f"{P.domain(url)} is a link shortener; Pinterest can block them as spam. Use the page's own URL")
            if url.startswith("http://"):
                rep.warn(pid, "the link is http://; use https:// if the site has it")
            page = None
            if link.get("page") and os.path.exists(P.resolve(base, link["page"])):
                try:
                    page = json.load(open(P.resolve(base, link["page"]), encoding="utf-8"))
                except Exception:
                    page = None
            if page:
                if page.get("final_url") and P.canonical(page["final_url"]) != P.canonical(url):
                    rep.warn(pid, f"the link redirects to {page['final_url']}; Pinterest flags redirects. Pin the final URL")
                if (page.get("status") or 200) >= 400:
                    rep.error(pid, f"the page answers HTTP {page['status']}")
                page_words = set(P.words(" ".join([page.get("title", ""), page.get("description", "")] + page.get("headings", []))))
                if page_words and not (set(P.words(title + " " + desc)) & page_words):
                    rep.warn(pid, "the pin shares no words with its page's title and headings; Pinterest wants the pin to match where it leads")
            else:
                rep.warn(pid, "the link's page wasn't read (page.py), so the redirect and match checks were skipped")

        # board
        board = pin.get("board")
        boards = (acc or {}).get("boards") or {}
        if not board:
            rep.error(pid, "no board chosen")
        elif not boards:
            rep.warn(pid, "the account's boards aren't in the plan (social_accounts_get_platform_inputs), so the board wasn't checked")
        elif board not in boards:
            rep.error(pid, f"board '{board}' isn't one of the account's boards ({', '.join(list(boards)[:6])})")

        at = P.parse_local(pin.get("at"), (acc or {}).get("timezone") or plan.get("timezone"))
        if pin.get("at") and not at:
            rep.error(pid, f"'at' must be a local time like 2026-11-16T20:30, not {pin.get('at')!r}")
        elif at and at < now and not pin.get("postId"):
            rep.warn(pid, f"{pin['at']} is in the past; schedule.py will move it (remove 'at' and run it again)")

        if pin.get("ai"):
            rep.warn(pid, "made with AI: Pinterest labels AI images from their file metadata, which re-rendering removes. "
                          "Upload the generator's original file, or say so in the description ('Image made with AI')")

    # duplicates within the batch
    by_text = defaultdict(list)
    for pin in pins:
        for field in ("title", "description"):
            t = (pin.get(field) or "").strip().lower()
            if t:
                by_text[(field, t)].append(pin["id"])
    for (field, _), group in by_text.items():
        if len(group) > 1:
            rep.warn(group[1], f"same {field} as {group[0]}: give each pin its own words")
    ids = [p["id"] for p in pins]
    byid = {p["id"]: p for p in pins}
    for i, pid in enumerate(ids):
        for qid in ids[:i]:
            if byid[pid].get("account") != byid[qid].get("account"):
                continue
            if P.same_picture(prints.get(pid), prints.get(qid)):
                rep.error(pid, f"looks the same as {qid}: each pin needs its own picture or design, not a copy")
            elif urls.get(pid) and urls.get(pid) == urls.get(qid) and sources.get(pid, set()) & sources.get(qid, set()):
                shared = sorted(sources[pid] & sources[qid])[0]
                rep.error(pid, f"uses the same photo as {qid} ({os.path.basename(shared)}) for the same page; give each pin its own picture")

    # against the posted log
    for pid in ids:
        for old in posted:
            if old.get("account") != byid[pid].get("account") or not urls.get(pid):
                continue
            if P.canonical(old.get("url")) == urls[pid] and any(
                    P.same_picture(a, b) for a in src_prints.get(pid, []) for b in old.get("sources") or []):
                rep.error(pid, f"uses a photo already pinned to this page on {str(old.get('at') or '?')[:10]} ({old.get('id')}); give it a new picture")
                break
        if not prints.get(pid):
            continue
        for old in posted:
            if old.get("account") != byid[pid].get("account") or not old.get("print"):
                continue
            if P.same_picture(prints[pid], old["print"]):
                if urls.get(pid) and P.canonical(old.get("url")) == urls[pid]:
                    rep.error(pid, f"this picture was already pinned to this page on {str(old.get('at') or '?')[:10]} ({old.get('id')}). "
                                   "Pinterest treats re-uploading the same content as spam: make a new design")
                else:
                    rep.warn(pid, f"this picture was already pinned on {str(old.get('at') or '?')[:10]} ({old.get('id')}), to another page")

    # pace
    per_day = defaultdict(list)
    page_events = defaultdict(list)
    for p in pins:
        d = P.parse_local(p.get("at"), tz_of(p.get("account")))
        if d:
            per_day[(p.get("account"), d.date())].append(p["id"])
            if urls.get(p["id"]):
                page_events[(p.get("account"), urls[p["id"]])].append((d, p["id"], p.get("board")))
    plan_posts = {p.get("postId") for p in pins if p.get("postId")}
    for old in posted:
        d = P.parse_local(old.get("at"), tz_of(old.get("account")))
        if d and old.get("postId") not in plan_posts:
            per_day[(old.get("account"), d.date())].append(f"{old.get('id')} (posted)")
            page_events[(old.get("account"), P.canonical(old.get("url")))].append((d, f"{old.get('id')} (posted)", old.get("board")))
    for (acc, day), group in per_day.items():
        cap = (accounts.get(acc) or {}).get("max_per_day") or rules["max_per_day"]
        fresh = [g for g in group if not g.endswith("(posted)")]
        if len(group) > cap and fresh:
            rep.error(fresh[-1], f"{len(group)} pins on {day} for {acc}: more than {cap} a day reads as a burst. Spread them out (schedule.py)")
    for (acc, url), events in page_events.items():
        events.sort(key=lambda e: e[0])
        for i in range(1, len(events)):
            if events[i][1].endswith("(posted)"):
                continue
            gap = events[i][0] - events[i - 1][0]
            if events[i][0].date() == events[i - 1][0].date() and events[i][2] != events[i - 1][2]:
                rep.error(events[i][1], f"same page as {events[i - 1][1]} to another board on the same day: one page across many boards at once is a spam signal")
            elif gap < timedelta(days=rules["link_gap_days"]):
                rep.warn(events[i][1], f"only {gap.days} day(s) after {events[i - 1][1]} for the same page; space new pins for one page about {rules['link_gap_days']} days apart")

    if a.fix:
        P.save_plan(a.plan, plan)

    order = {"error": 0, "fixed": 1, "warning": 2}
    for kind, pid, msg in sorted(rep.items, key=lambda i: (order[i[0]], str(i[1]))):
        print(f"[{kind}] {pid}: {msg}")
    n_err = len(rep.errors())
    n_warn = sum(1 for i in rep.items if i[0] == "warning")
    print(f"\n{len(pins)} pins checked: {n_err} error(s), {n_warn} warning(s)"
          + (". Nothing blocks." if not n_err else ". Fix the errors and run again."))
    report = {"errors": n_err, "warnings": n_warn,
              "items": [{"kind": k, "pin": p, "message": m} for k, p, m in rep.items]}
    with open(os.path.join(base, "check.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
