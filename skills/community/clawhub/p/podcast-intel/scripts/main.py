#!/usr/bin/env python3
"""
Podcast-intel main orchestrator.

Orchestrates the full intelligence pipeline:
1. Fetch new episodes from configured feeds
2. Transcribe audio (with caching)
3. Segment transcripts by topic (with caching)
4. Analyze and score against user interests + diary
5. Output recommendations and update diary
"""

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils import (
    get_segmentation_cache_path,
    get_transcript_cache_path,
)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Podcast-intel main orchestrator")
    parser.add_argument(
        "--hours",
        type=int,
        default=168,
        help="Look back this many hours (default: 168 = 7 days)",
    )
    parser.add_argument("--show", type=str, help="Filter to single show by name")
    parser.add_argument("--episode-url", type=str, help="Analyze single episode by URL")
    parser.add_argument(
        "--recommend-only",
        action="store_true",
        help="Skip transcription, use cached data only",
    )
    parser.add_argument("--top", type=int, default=10, help="Return only top N recommendations")
    parser.add_argument(
        "--output",
        choices=["json", "markdown", "tts"],
        default="markdown",
        help="Output format",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze but do not write to diary",
    )
    return parser.parse_args()


def run_script(
    script_name: str,
    args: List[str],
    timeout: int = 1200,
    expect_json: bool = True,
) -> Optional[Any]:
    """Run a pipeline script, optionally parsing JSON output."""
    script_path = Path(__file__).parent / f"{script_name}.py"
    cmd = ["python3", str(script_path)] + args

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"Error running {script_name}: timeout after {timeout}s", file=sys.stderr)
        return None
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        print(f"Error running {script_name}: {exc}", file=sys.stderr)
        return None

    if result.returncode != 0:
        stderr = result.stderr.strip()
        if stderr:
            print(f"Error running {script_name}: {stderr}", file=sys.stderr)
        else:
            print(f"Error running {script_name}: exit code {result.returncode}", file=sys.stderr)
        return None

    if not expect_json:
        return {"ok": True}

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        preview = result.stdout[:250].strip().replace("\n", " ")
        print(f"Invalid JSON from {script_name}: {preview}", file=sys.stderr)
        return None


def load_json_file(path: Path) -> Optional[Dict[str, Any]]:
    """Load JSON file and return dict, returning None on failure."""
    if not path.exists():
        return None
    try:
        with open(path, "r") as handle:
            return json.load(handle)
    except Exception as exc:
        print(f"Warning: failed to load cache {path}: {exc}", file=sys.stderr)
        return None


def fetch_episodes(hours: int, show_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch new episodes from configured feeds."""
    print("📡 Fetching episodes...", file=sys.stderr)
    episodes = run_script("fetch_feeds", ["--hours", str(hours)])

    if not episodes:
        print("No episodes fetched", file=sys.stderr)
        return []

    if show_filter:
        lowered = show_filter.lower()
        episodes = [episode for episode in episodes if lowered in episode.get("show", "").lower()]

    print(f"✓ Fetched {len(episodes)} episodes", file=sys.stderr)
    return episodes


def build_manual_episode(episode_url: str) -> Dict[str, Any]:
    """Build episode metadata for a manually provided audio URL."""
    episode_id = hashlib.sha256(episode_url.encode("utf-8")).hexdigest()[:12]
    return {
        "id": episode_id,
        "show": "Manual Episode",
        "title": episode_url,
        "published": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "audio_url": episode_url,
        "duration_seconds": 0,
        "description": "",
        "feed_url": "manual",
    }


def get_transcript_for_episode(
    episode: Dict[str, Any],
    recommend_only: bool,
) -> Optional[Dict[str, Any]]:
    """Get transcript from cache or by transcribing the episode."""
    episode_id = episode["id"]
    cache_path = get_transcript_cache_path(episode_id)

    if cache_path.exists():
        cached = load_json_file(cache_path)
        if cached:
            print(f"  ⚡ {episode.get('show', 'Unknown')}: Using cached transcript", file=sys.stderr)
            return cached

    if recommend_only:
        print(
            f"  ⏭️  {episode.get('show', 'Unknown')}: no cached transcript, skipping",
            file=sys.stderr,
        )
        return None

    print(f"  🔄 {episode.get('show', 'Unknown')}: transcribing", file=sys.stderr)
    return run_script("transcribe", ["--episode", json.dumps(episode)], timeout=3600)


def get_segmentation_for_episode(
    episode: Dict[str, Any],
    transcript: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Get segmentation from cache or by running the segment stage."""
    episode_id = episode["id"]
    cache_path = get_segmentation_cache_path(episode_id)

    if cache_path.exists():
        cached = load_json_file(cache_path)
        if cached:
            print(f"  ⚡ {episode.get('show', 'Unknown')}: Using cached segmentation", file=sys.stderr)
            segmentation = cached
        else:
            segmentation = None
    else:
        segmentation = None

    if segmentation is None:
        segmentation = run_script(
            "segment",
            ["--method", "llm", "--transcript", json.dumps(transcript)],
        )

    if not segmentation:
        return None

    return attach_episode_metadata(segmentation, episode)


def attach_episode_metadata(
    segmentation: Dict[str, Any],
    episode: Dict[str, Any],
) -> Dict[str, Any]:
    """Attach episode metadata required by analysis/recommendation steps."""
    episode_id = episode["id"]
    segmentation["episode_id"] = episode_id
    segmentation["show"] = episode.get("show", "Unknown")
    segmentation["title"] = episode.get("title", "Untitled")
    segmentation["published"] = episode.get("published")
    segmentation["audio_url"] = episode.get("audio_url")
    segmentation["duration_seconds"] = episode.get("duration_seconds", 0)
    segmentation["feed_url"] = episode.get("feed_url", "")
    return segmentation


def analyze_segmented_episodes(segmented_episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze episodes for relevance, novelty, and overlap."""
    print("🧠 Analyzing episodes...", file=sys.stderr)
    analyses = run_script("analyze", ["--episodes", json.dumps(segmented_episodes)])

    if not analyses:
        return []

    analyses.sort(key=lambda item: item.get("worth_your_time_score", 0.0), reverse=True)
    print(f"✓ Analyzed {len(analyses)} episodes", file=sys.stderr)
    return analyses


def format_output(analyses: List[Dict[str, Any]], output_format: str, top_n: int) -> str:
    """Format analyses for output."""
    top_analyses = analyses[:top_n]
    if output_format == "json":
        return json.dumps(top_analyses, indent=2)

    if output_format == "markdown":
        from utils.tts_output import format_markdown_briefing

        return format_markdown_briefing(top_analyses, top_n)

    if output_format == "tts":
        from utils.tts_output import format_tts_briefing

        return format_tts_briefing(top_analyses, top_n)

    return json.dumps(top_analyses, indent=2)


def update_diary(analyses: List[Dict[str, Any]], dry_run: bool) -> None:
    """Append analyses to diary unless dry-run is active."""
    if dry_run:
        print("(Dry run: not updating diary)", file=sys.stderr)
        return

    print("📝 Updating diary...", file=sys.stderr)
    updated = 0
    for analysis in analyses:
        result = run_script(
            "diary",
            ["--analysis", json.dumps(analysis)],
            expect_json=False,
        )
        if result is not None:
            updated += 1
    print(f"✓ Updated diary with {updated} entries", file=sys.stderr)


def main() -> None:
    """Main orchestration entry point."""
    args = parse_args()

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"🎧 Podcast-Intel v1.0 — {now_utc}", file=sys.stderr)
    print(f"   Hours: {args.hours}, Top: {args.top}, Format: {args.output}", file=sys.stderr)

    if args.episode_url:
        episodes = [build_manual_episode(args.episode_url)]
    else:
        episodes = fetch_episodes(args.hours, args.show)
        if not episodes:
            print("No episodes to process", file=sys.stderr)
            sys.exit(0)

    print("🎤 Building transcripts and segmentations...", file=sys.stderr)
    segmented_episodes: List[Dict[str, Any]] = []

    for episode in episodes:
        # Fast path: if segmentation is already cached we can skip upstream stages.
        cached_segmentation = load_json_file(get_segmentation_cache_path(episode["id"]))
        if cached_segmentation:
            print(
                f"  ⚡ {episode.get('show', 'Unknown')}: using fully cached segmentation",
                file=sys.stderr,
            )
            segmented_episodes.append(attach_episode_metadata(cached_segmentation, episode))
            continue

        transcript = get_transcript_for_episode(episode, args.recommend_only)
        if not transcript:
            continue

        segmentation = get_segmentation_for_episode(episode, transcript)
        if not segmentation:
            print(f"Warning: segmentation failed for {episode.get('id')}", file=sys.stderr)
            continue

        segmented_episodes.append(segmentation)

    if not segmented_episodes:
        print("No segmentations generated", file=sys.stderr)
        sys.exit(1)

    analyses = analyze_segmented_episodes(segmented_episodes)
    if not analyses:
        print("No analyses generated", file=sys.stderr)
        sys.exit(1)

    output_text = format_output(analyses, args.output, args.top)
    print(output_text)

    update_diary(analyses[: args.top], args.dry_run)
    print("✨ Done", file=sys.stderr)


if __name__ == "__main__":
    main()
