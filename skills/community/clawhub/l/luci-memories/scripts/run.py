#!/usr/bin/env python3
"""Luci-memory skill — unified client for personal media + portrait APIs.

Usage:
    python run.py --query "cooking" --type search_video
    python run.py --type query_audio --video-ids VI123,VI456
    python run.py --type traits --person "Alice"
    python run.py --query "meeting" --type search_events --person "Bob" --after 2025-12-01
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import UTC, datetime

API_HOST = "https://skills.memories.ai/luci-memory"
API_PERSONAL = API_HOST + "/personal"
API_PORTRAIT = API_HOST + "/portrait"
USERINFO_API = "https://mavi-backend.memories.ai/serve/api/userinfo"
ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")

def _load_env():
    """Load MEMORIES_AI_KEY from .env file next to the skill root."""
    if not os.path.exists(ENV_FILE):
        return None
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line.startswith("MEMORIES_AI_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def resolve_user_id():
    """Resolve USER_ID from MEMORIES_AI_KEY"""
    api_key = os.environ.get("MEMORIES_AI_KEY", "").strip() or _load_env()
    if not api_key:
        print("Error: MEMORIES_AI_KEY not found.", file=sys.stderr)
        print(f"Please create {ENV_FILE} with:", file=sys.stderr)
        print('  MEMORIES_AI_KEY=sk-your-key-here', file=sys.stderr)
        sys.exit(1)
    req = urllib.request.Request(USERINFO_API, headers={"authorization": api_key, "User-Agent": "LuciMemory/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"Error: Failed to resolve user from API key: {e}", file=sys.stderr)
        sys.exit(1)
    infra_user_id = data.get("data", {}).get("infraUserId")
    if not infra_user_id:
        print("Error: Could not resolve infraUserId from API key. Is your key valid?", file=sys.stderr)
        sys.exit(1)
    return infra_user_id


USER_ID = resolve_user_id()
# ---------------------------------------------------------------------------
# Type definitions
# ---------------------------------------------------------------------------

# Personal media types: (api_base, endpoint, needs_query)
PERSONAL_TYPE_MAP = {
    "search_video":    (API_PERSONAL, "/search/videos",             True),
    "query_video":     (API_PERSONAL, "/query/videos",              False),
    "search_image":    (API_PERSONAL, "/search/images",             True),
    "query_image":     (API_PERSONAL, "/query/images",              False),
    "search_audio":    (API_PERSONAL, "/search/audio-transcripts",  True),
    "query_audio":     (API_PERSONAL, "/query/audio-transcripts",   False),
    "search_visual":   (API_PERSONAL, "/search/visual-transcripts", True),
    "query_visual":    (API_PERSONAL, "/query/video-transcripts",   False),
    "search_keyframe": (API_PERSONAL, "/search/keyframes",          True),
    "query_keyframe":  (API_PERSONAL, "/query/keyframes",           False),
    "search_recording":(API_PERSONAL, "/search/recordings",         True),
    "query_recording": (API_PERSONAL, "/query/recordings",          False),
}

# Portrait types handled with custom logic
PORTRAIT_TYPES = [
    "traits", "events", "relationships", "speeches",
    "search_events", "search_traits",
]

ALL_TYPES = list(PERSONAL_TYPE_MAP.keys()) + PORTRAIT_TYPES

# Per-type top_k defaults. query_audio/query_visual default high so that
# fetching a full transcript with --video-ids "just works" without -k.
DEFAULT_TOP_K = {
    "query_audio": 5000,
    "query_visual": 5000,
    "query_recording": 100,
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_date(s):
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=UTC)
        except ValueError:
            continue
    raise argparse.ArgumentTypeError(f"Invalid date: {s}. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS")


def api_post(url, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "User-Agent": "LuciMemory/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"Error: HTTP {e.code} from {url}\n{error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _person_label(p):
    """Return display name, annotating the owner with '(you)'."""
    name = p.get("name", "")
    if p.get("uuid") == USER_ID:
        return f"{name} (you)"
    return name


def _fmt_time(time_str):
    """Format an ISO timestamp as 'YYYY-MM-DD HH:MM UTC'. All stored times are UTC."""
    if not time_str or time_str == "unknown time":
        return "unknown time"
    return time_str[:16].replace("T", " ") + " UTC"

# ---------------------------------------------------------------------------
# Formatters — personal media
# ---------------------------------------------------------------------------

def format_videos(videos):
    if not videos:
        return "No videos found."
    lines = []
    for v in videos:
        time_str = _fmt_time(v.get("captured_time"))
        sim = v.get("similarity", 1)
        sim_str = f" (similarity: {sim:.2f})" if sim < 1 else ""
        vid = v.get("video_id", "?")
        lines.append(f"- **{vid}** [{time_str}]{sim_str}")
        lines.append(f"  {v.get('summary') or 'No summary'}")
        if v.get("location"):
            lines.append(f"  Location: {v['location']}")
    return "\n".join(lines)


def format_images(images):
    if not images:
        return "No images found."
    lines = []
    for img in images:
        time_str = _fmt_time(img.get("captured_time"))
        sim = img.get("similarity", 1)
        sim_str = f" (similarity: {sim:.2f})" if sim < 1 else ""
        lines.append(f"- **{img.get('id', '?')}** [{time_str}]{sim_str}")
        if img.get("text"):
            lines.append(f"  {img['text']}")
        lines.append(f"  bucket: {img.get('bucket')}, blob: {img.get('blob')}")
        if img.get("location"):
            lines.append(f"  Location: {img['location']}")
        if img.get("camera_model"):
            lines.append(f"  Camera: {img['camera_model']}")
    return "\n".join(lines)


def format_audio_ts(records):
    if not records:
        return "No audio transcripts found."
    records = sorted(records, key=lambda r: (r.get("video_id", ""), r.get("start_time") or 0))
    lines = []
    for r in records:
        time_str = _fmt_time(r.get("captured_time"))
        sim = r.get("similarity", 1)
        sim_str = f" (similarity: {sim:.2f})" if sim < 1 else ""
        lines.append(f"- **{r.get('video_id', '?')}** [{time_str}] {r.get('start_time', 0):.1f}s-{r.get('end_time', 0):.1f}s{sim_str}")
        lines.append(f'  "{r.get("text", "")}"')
    return "\n".join(lines)


def format_visual_ts(records):
    if not records:
        return "No visual transcripts found."
    records = sorted(records, key=lambda r: (r.get("video_id", ""), r.get("start_time") or 0))
    lines = []
    for r in records:
        time_str = _fmt_time(r.get("captured_time"))
        sim = r.get("similarity")
        sim_str = f" (similarity: {sim:.2f})" if sim is not None and sim < 1 else ""
        lines.append(f"- **{r.get('video_id', '?')}** [{time_str}] {r.get('start_time', 0):.1f}s-{r.get('end_time', 0):.1f}s{sim_str}")
        lines.append(f'  "{r.get("text", "")}"')
    return "\n".join(lines)


def format_keyframes(records):
    if not records:
        return "No keyframes found."
    lines = []
    for r in records:
        sim = r.get("similarity", 1)
        sim_str = f" (similarity: {sim:.2f})" if sim < 1 else ""
        lines.append(f"- **{r.get('id', '?')}** frame #{r.get('frame_id')} @ {r.get('frame_time', 0):.1f}s{sim_str}")
        lines.append(f"  bucket: {r.get('bucket')}, blob: {r.get('blob')}")
    return "\n".join(lines)


def format_recordings(records):
    if not records:
        return "No recordings found."
    records = sorted(records, key=lambda r: r.get("captured_time") or "")
    lines = []
    for r in records:
        time_str = _fmt_time(r.get("captured_time"))
        sim = r.get("similarity", 1)
        sim_str = f" (similarity: {sim:.2f})" if sim is not None and sim < 1 else ""
        rid = r.get("recording_id", "?")
        dur = r.get("duration")
        dur_str = f" {dur:.0f}s" if dur else ""
        lines.append(f"- **{rid}** [{time_str}]{dur_str}{sim_str}")
        lines.append(f'  "{r.get("transcript", "")}"')
    return "\n".join(lines)


PERSONAL_FORMATTERS = {
    "search_video": ("Video Search", format_videos),
    "query_video": ("Recent Videos", format_videos),
    "search_image": ("Image Search", format_images),
    "query_image": ("Recent Images", format_images),
    "search_audio": ("Audio Transcript Search", format_audio_ts),
    "query_audio": ("Audio Transcripts", format_audio_ts),
    "search_visual": ("Visual Transcript Search", format_visual_ts),
    "query_visual": ("Visual Transcripts", format_visual_ts),
    "search_keyframe": ("Keyframe Search", format_keyframes),
    "query_keyframe": ("Keyframes", format_keyframes),
    "search_recording": ("Recording Search", format_recordings),
    "query_recording": ("Recent Recordings", format_recordings),
}

# ---------------------------------------------------------------------------
# Formatters — portrait
# ---------------------------------------------------------------------------

def format_traits(traits):
    if not traits:
        return "No traits found."
    lines = []
    for t in traits:
        lines.append(f"- **{t['trait']}** ({t['category']}) — strength: {t['strength']:.2f}")
        evidence = t.get("evidence_facts", [])
        if evidence:
            lines.append(f"  Evidence: {', '.join(evidence[:3])}")
    return "\n".join(lines)


def format_events(events):
    if not events:
        return "No events found."
    lines = []
    for e in events:
        time_str = _fmt_time(e.get("capture_time"))
        people = e.get("people", [])
        people_str = ", ".join(_person_label(p) for p in people) if people else "no people"
        lines.append(f"- **{e.get('event_name', '')}** [{time_str}] (event_id: {e.get('event_id', '?')})")
        lines.append(f"  {e.get('event_description', '')}")
        lines.append(f"  People: {people_str}")
    return "\n".join(lines)


def format_relationships(relationships):
    if not relationships:
        return "No relationships found."
    lines = []
    for r in relationships:
        name = r.get("person_name") or r.get("person_id")
        rel = r.get("relationship") or "unknown"
        lines.append(f"- **{name}**: {rel}")
    return "\n".join(lines)


def format_speeches(speeches):
    if not speeches:
        return "No speeches found."
    lines = []
    for s in speeches:
        speaker = s.get("person_name") or s.get("person_id") or "unknown"
        if s.get("person_id") == USER_ID:
            speaker = f"{speaker} (you)"
        lines.append(f"- [{speaker}]: {s.get('text', '')}")
    return "\n".join(lines)


def format_search_traits(results):
    if not results:
        return "No matching traits found."
    lines = []
    for r in results:
        t = r.get("trait", {})
        pid = r.get("person_id", "?")
        lines.append(f"- **{t.get('trait', '')}** ({t.get('category', '')}) — strength: {t.get('strength', 0):.2f} [person: {pid}]")
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Luci-memory: search personal media and portrait data")
    parser.add_argument("--query", "-q", default=None, help="Search term (required for search_* types)")
    parser.add_argument("--type", "-t", default="search_video", choices=ALL_TYPES,
                        help="Operation type (default: search_video)")
    parser.add_argument("--top-k", "-k", type=int, default=None,
                        help="Max results (default: 10, or 5000 for query_audio/query_visual)")
    # Personal-specific filters
    parser.add_argument("--location", "-l", default=None, help="Filter by location name (e.g. 'Suzhou', 'Heze')")
    parser.add_argument("--video-ids", default=None, help="Comma-separated video IDs to filter by")
    parser.add_argument("--recording-ids", default=None, help="Comma-separated recording IDs to filter by")
    # Portrait-specific filters
    parser.add_argument("--person", "-p", default=None, help="Filter by person name(s), comma-separated. Use 'user' for self.")
    parser.add_argument("--event-ids", default=None, help="Comma-separated event IDs to filter by")
    # Shared filters
    parser.add_argument("--after", type=parse_date, default=None, help="Filter: only results after this date (YYYY-MM-DD)")
    parser.add_argument("--before", type=parse_date, default=None, help="Filter: only results before this date (YYYY-MM-DD)")
    args = parser.parse_args()

    if args.top_k is None:
        args.top_k = DEFAULT_TOP_K.get(args.type, 10)

    person_names = args.person.split(",") if args.person else None
    event_ids = args.event_ids.split(",") if args.event_ids else None

    # -----------------------------------------------------------------------
    # Personal media types
    # -----------------------------------------------------------------------
    if args.type in PERSONAL_TYPE_MAP:
        api_base, endpoint, needs_query = PERSONAL_TYPE_MAP[args.type]

        if needs_query and not args.query:
            print(f"Error: --query is required for {args.type}", file=sys.stderr)
            sys.exit(1)

        query_types_need_video_ids = {"query_audio", "query_visual", "query_keyframe"}
        if args.type == "query_recording" and not args.recording_ids:
            print(f"Error: --recording-ids is required for {args.type}", file=sys.stderr)
            sys.exit(1)
        elif args.type in query_types_need_video_ids and not args.video_ids:
            print(f"Error: --video-ids is required for {args.type}", file=sys.stderr)
            sys.exit(1)

        body = {"user_id": USER_ID, "top_k": args.top_k}

        if args.query:
            body["question"] = args.query
        if args.after:
            body["start_time"] = args.after.isoformat()
        if args.before:
            body["end_time"] = args.before.isoformat()
        if args.location:
            body["location"] = args.location
        if args.video_ids:
            video_ids = args.video_ids.split(",")
            if args.type == "query_image":
                body["image_ids"] = video_ids
            else:
                body["video_ids"] = video_ids
        if args.recording_ids:
            body["recording_ids"] = args.recording_ids.split(",")

        results = api_post(api_base + endpoint, body)

        label, formatter = PERSONAL_FORMATTERS[args.type]
        if args.query:
            print(f"## {label}: '{args.query}'\n")
        else:
            print(f"## {label}\n")
        print(formatter(results))
        return

    # -----------------------------------------------------------------------
    # Portrait types
    # -----------------------------------------------------------------------
    search_types = {"search_events", "search_traits"}
    if args.type in search_types and not args.query:
        print(f"Error: --query is required for {args.type}", file=sys.stderr)
        sys.exit(1)

    if args.type == "traits":
        person_name = person_names[0] if person_names else "user"
        body = {"user_id": USER_ID, "person_name": person_name, "top_k": args.top_k}
        results = api_post(API_PORTRAIT + "/query/traits", body)
        print(f"## Traits for '{person_name}'\n")
        print(format_traits(results))

    elif args.type == "search_traits":
        body = {"user_id": USER_ID, "search_text": args.query, "top_k": args.top_k}
        results = api_post(API_PORTRAIT + "/search/traits", body)
        print(f"## Trait Search: '{args.query}'\n")
        print(format_search_traits(results))

    elif args.type == "events":
        names = person_names or ([args.query] if args.query else None)
        body = {"user_id": USER_ID, "top_k": args.top_k}
        if names:
            body["person_names"] = names
        if event_ids:
            body["event_ids"] = event_ids
        if args.after:
            body["start_time"] = args.after.isoformat()
        if args.before:
            body["end_time"] = args.before.isoformat()
        results = api_post(API_PORTRAIT + "/query/events", body)
        label = f" for {','.join(names)}" if names else ""
        print(f"## Events{label}\n")
        print(format_events(results))

    elif args.type == "search_events":
        body = {"user_id": USER_ID, "search_text": args.query, "top_k": args.top_k}
        if person_names:
            body["person_names"] = person_names
        if args.after:
            body["start_time"] = args.after.isoformat()
        if args.before:
            body["end_time"] = args.before.isoformat()
        results = api_post(API_PORTRAIT + "/search/events", body)
        label = f" (person: {','.join(person_names)})" if person_names else ""
        print(f"## Event Search: '{args.query}'{label}\n")
        print(format_events(results))

    elif args.type == "relationships":
        names = person_names or ([args.query] if args.query else None)
        body = {"user_id": USER_ID}
        if names:
            body["person_names"] = names
        results = api_post(API_PORTRAIT + "/query/relationships", body)
        label = f" for {','.join(names)}" if names else ""
        print(f"## Relationships{label}\n")
        print(format_relationships(results))

    elif args.type == "speeches":
        names = person_names or ([args.query] if args.query else None)
        body = {"user_id": USER_ID}
        if names:
            body["person_names"] = names
        if event_ids:
            body["event_ids"] = event_ids
        results = api_post(API_PORTRAIT + "/query/speeches", body)
        label = f" by {','.join(names)}" if names else ""
        print(f"## Speeches{label}\n")
        print(format_speeches(results))


if __name__ == "__main__":
    main()
