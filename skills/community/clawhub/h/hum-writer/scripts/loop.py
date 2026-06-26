#!/usr/bin/env python3
"""
loop.py — Daily hum automation loop.

Runs at 6am daily. Orchestrates the full morning workflow:
  1. Feed digest — scrape, rank, format, send via Telegram
  2. Engage — suggest accounts to follow + draft replies for approval
  3. Brainstorm — surface top ideas and ask which topics to add / posts to work on
  4. Learn (Sundays only) — analyze feed trends, research algorithms, update context files

Usage:
    python3 scripts/loop.py                     # full daily loop
    python3 scripts/loop.py --step digest       # just the digest
    python3 scripts/loop.py --step engage       # just engagement suggestions
    python3 scripts/loop.py --step brainstorm   # just brainstorm
    python3 scripts/loop.py --step learn        # just strategy refresh (normally Sunday only)
    python3 scripts/loop.py --dry-run           # format output but don't send
    python3 scripts/loop.py --max-posts 15      # override digest size
"""

import argparse
import json
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config

_CFG = load_config()


def _loop_run_dir() -> Path:
    """Return today's loop output directory: data_dir/loop/YYYY-MM-DD/."""
    d = _CFG["loop_dir"] / datetime.now().strftime("%Y-%m-%d")
    d.mkdir(parents=True, exist_ok=True)
    return d


def _save_step_output(step_name: str, text: str) -> None:
    """Write a step's output to the loop run directory."""
    if not text.strip():
        return
    out_file = _loop_run_dir() / f"{step_name}.md"
    out_file.write_text(text, encoding="utf-8")
    print(f"[loop] Saved {step_name} output → {out_file}", file=sys.stderr)


def run_step(label: str, cmd: list[str], *, allow_fail: bool = False) -> tuple[int, str]:
    """Run a subprocess step, printing status and returning captured stdout."""
    print(f"\n{'─' * 50}")
    print(f"▶ {label}")
    print(f"  {' '.join(cmd)}")
    print(f"{'─' * 50}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0 and not allow_fail:
        print(f"✗ {label} failed (exit {result.returncode})", file=sys.stderr)
    return result.returncode, result.stdout or ""


def _write_run_summary(data_dir: Path, summary: dict) -> None:
    """Write run summary to run_log.json (latest), runs.jsonl (history), and loop dir."""
    feed_dir = data_dir / "feed"
    feed_dir.mkdir(parents=True, exist_ok=True)

    run_log = feed_dir / "run_log.json"
    runs_jsonl = feed_dir / "runs.jsonl"

    try:
        run_log.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"[loop] Could not write run_log.json: {exc}", file=sys.stderr)

    try:
        with runs_jsonl.open("a", encoding="utf-8") as f:
            f.write(json.dumps(summary) + "\n")
    except OSError as exc:
        print(f"[loop] Could not append to runs.jsonl: {exc}", file=sys.stderr)

    # Also save summary to the loop run directory
    try:
        loop_summary = _loop_run_dir() / "summary.json"
        loop_summary.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"[loop] Could not write loop summary: {exc}", file=sys.stderr)


# ── Step 1: Feed Digest ────────────────────────────────────────────────────


def run_digest(max_posts: int = 12, days: int = 7, skip_youtube: bool = False):
    """Fetch feeds, rank, format digest.

    All sources fetch directly via API/subprocess — no browser automation.
      - HN: Algolia API (step 1a)
      - X profiles: Bird API (from:handle) (step 1b)
      - X home feed: Bird API (filter:follows) (step 1c)
      - YouTube: yt-dlp (step 1d)
    """
    feed_raw = _CFG["feed_raw"]
    feeds_file = str(_CFG["feeds_file"])
    youtube_feed = str(feed_raw / "youtube_feed.json")
    hn_feed = str(feed_raw / "hn_feed.json")
    ranked_feed = str(feed_raw / "feed_ranked.json")
    sources_file = str(_CFG["sources_file"])
    feed_dir = _SCRIPTS_ROOT / "feed"

    # Step 1a: Fetch Hacker News stories directly (Algolia API — no browser needed).
    # HN posts are merged into feeds_file so they appear in digest alongside X/PH.
    _, _ = run_step(
        "Fetch Hacker News stories (Algolia API)",
        [sys.executable, str(feed_dir / "source" / "hn.py"),
         "--days", str(days), "--output", hn_feed],
        allow_fail=True,
    )
    hn_path = Path(hn_feed)
    if hn_path.exists():
        try:
            hn_items = json.loads(hn_path.read_text())
            existing = []
            if Path(feeds_file).exists():
                existing = json.loads(Path(feeds_file).read_text())
            seen_urls = {p.get("url") for p in existing if p.get("url")}
            merged = list(existing)
            for item in hn_items:
                if item.get("url") and item["url"] not in seen_urls:
                    seen_urls.add(item["url"])
                    merged.append(item)
            Path(feeds_file).write_text(json.dumps(merged, indent=2))
            print(f"[loop] Merged {len(hn_items)} HN posts → feeds_file ({len(merged)} total)", file=sys.stderr)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[loop] Could not merge HN feed: {exc}", file=sys.stderr)

    # Step 1b: Crawl X profile sources via Bird API (direct, no browser needed).
    # Falls back silently to browser instructions if credentials are absent.
    _, _ = run_step(
        "X profiles — Bird API (incremental)",
        [sys.executable, str(feed_dir / "refresh.py"),
         "--type", "x_profile", "--output", feeds_file],
        allow_fail=True,
    )

    # Step 1c: Fetch X home feed via Bird (filter:follows). Direct, no browser.
    _, _ = run_step(
        "X home feed — Bird filter:follows",
        [sys.executable, str(feed_dir / "refresh.py"), "--type", "x_feed"],
        allow_fail=True,
    )

    # Step 1d: Fetch YouTube creator updates (direct via yt-dlp).
    if not skip_youtube:
        _, _ = run_step(
            "Fetch YouTube creator updates",
            [sys.executable, str(feed_dir / "source" / "youtube.py"),
             "--file", sources_file, "--days", str(days),
             "--output", youtube_feed],
            allow_fail=True,
        )

    # Steps below depend on feeds_file being fully populated by the agent (X + PH).
    _, _ = run_step(
        "Rank and score posts",
        [sys.executable, str(feed_dir / "ranker.py"),
         "--input", feeds_file, "--output", ranked_feed],
        allow_fail=True,
    )

    _, digest_output = run_step(
        "Format digest",
        [sys.executable, str(feed_dir / "digest.py"),
         "--input", feeds_file, "--youtube-input", youtube_feed,
         "--max-posts", str(max_posts)],
    )

    _save_step_output("digest", digest_output)


# ── Step 2: Engage ─────────────────────────────────────────────────────────


def run_engage():
    """Suggest accounts to follow and draft replies for approval.

    Outputs structured suggestions for the agent to present to the user.
    """
    lines = [
        "",
        "═" * 50,
        "💬 ENGAGEMENT SUGGESTIONS",
        "═" * 50,
        "",
        "Review your recent posts on X and LinkedIn for new comments/replies.",
        "Check feed sources for high-value accounts to follow.",
        "",
        "Actions for the agent:",
        "  1. Open X and LinkedIn in browser",
        "  2. Check recent posts for unanswered comments",
        "  3. Draft reply suggestions for user approval",
        "  4. Suggest 3-5 new accounts to follow based on feed sources",
        "",
        "Present all suggestions and wait for user approval before acting.",
    ]
    text = "\n".join(lines)
    print(text)
    _save_step_output("engage", text)


# ── Step 3: Brainstorm ─────────────────────────────────────────────────────


def run_brainstorm():
    """Surface top ideas from feed and ask about topics/posts.

    Outputs prompts for the agent to present to the user.
    """
    create_dir = _SCRIPTS_ROOT / "create"

    _, brainstorm_output = run_step(
        "Filter feed for brainstorm ideas",
        [sys.executable, str(create_dir / "brainstorm.py"), "--max", "8"],
        allow_fail=True,
    )

    lines = [
        "",
        "═" * 50,
        "💡 CONTENT BRAINSTORM",
        "═" * 50,
        "",
        "Actions for the agent:",
        "  1. Present the top feed items above as inspiration",
        "  2. Ask: 'Any topics you want to add to the pipeline?'",
        "  3. Ask: 'Want to work on any posts today?'",
        "  4. If yes, run /hum create for the chosen idea",
    ]
    text = "\n".join(lines)
    print(text)
    _save_step_output("brainstorm", brainstorm_output + text)


# ── Step 4: Learn (Sundays only) ──────────────────────────────────────────


def run_learn():
    """Weekly strategy refresh — feed trends, algorithm research, context updates.

    Outputs instructions for the agent to execute the /learn command.
    """
    lines = [
        "",
        "═" * 50,
        "📚 WEEKLY LEARN (Sunday)",
        "═" * 50,
        "",
        "Actions for the agent:",
        "  1. Run the /hum learn command as defined in COMMANDS.md",
        "  2. Analyze feed trends and top-performing content",
        "  3. Research what X and LinkedIn algorithms currently favor",
        "  4. Update context files based on findings",
        "  5. Share key findings and recommended actions with the user",
    ]
    text = "\n".join(lines)
    print(text)
    _save_step_output("learn", text)


# ── Main ───────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Daily hum automation loop")
    parser.add_argument("--step", choices=["digest", "engage", "brainstorm", "learn"],
                        help="Run a single step instead of the full loop")
    parser.add_argument("--dry-run", action="store_true",
                        help="Format output but don't send")
    parser.add_argument("--max-posts", type=int, default=12,
                        help="Max posts in digest (default: 12)")
    parser.add_argument("--days", type=int, default=7,
                        help="YouTube lookback days (default: 7)")
    parser.add_argument("--skip-youtube", action="store_true",
                        help="Skip YouTube fetch in digest step")
    args = parser.parse_args()

    is_sunday = datetime.now().weekday() == 6

    if args.step:
        # Run a single step
        if args.step == "digest":
            run_digest(args.max_posts, args.days, args.skip_youtube)
        elif args.step == "engage":
            run_engage()
        elif args.step == "brainstorm":
            run_brainstorm()
        elif args.step == "learn":
            run_learn()
        return

    # Full daily loop
    print("🌅 Hum Daily Loop")
    print(f"   {datetime.now().strftime('%A, %d %B %Y %H:%M')}")
    if is_sunday:
        print("   📚 Sunday — includes weekly strategy refresh")
    print()

    run_ts = datetime.now(timezone.utc).astimezone().isoformat()
    steps: dict = {}
    errors: list[str] = []

    # Step 1: Digest
    t0 = time.time()
    try:
        run_digest(args.max_posts, args.days, args.skip_youtube)
        steps["digest"] = {"status": "ok", "duration_s": round(time.time() - t0, 1)}
    except Exception as exc:
        msg = f"[loop] digest failed: {exc}"
        print(msg, file=sys.stderr)
        steps["digest"] = {"status": "error", "duration_s": round(time.time() - t0, 1)}
        errors.append(msg)

    # Step 2: Engage
    t0 = time.time()
    try:
        run_engage()
        steps["engage"] = {"status": "ok", "duration_s": round(time.time() - t0, 1)}
    except Exception as exc:
        msg = f"[loop] engage failed: {exc}"
        print(msg, file=sys.stderr)
        steps["engage"] = {"status": "error", "duration_s": round(time.time() - t0, 1)}
        errors.append(msg)

    # Step 3: Brainstorm
    t0 = time.time()
    try:
        run_brainstorm()
        steps["brainstorm"] = {"status": "ok", "duration_s": round(time.time() - t0, 1)}
    except Exception as exc:
        msg = f"[loop] brainstorm failed: {exc}"
        print(msg, file=sys.stderr)
        steps["brainstorm"] = {"status": "error", "duration_s": round(time.time() - t0, 1)}
        errors.append(msg)

    # Step 4: Learn (Sundays only)
    if is_sunday:
        t0 = time.time()
        try:
            run_learn()
            steps["learn"] = {"status": "ok", "duration_s": round(time.time() - t0, 1)}
        except Exception as exc:
            msg = f"[loop] learn failed: {exc}"
            print(msg, file=sys.stderr)
            steps["learn"] = {"status": "error", "duration_s": round(time.time() - t0, 1)}
            errors.append(msg)

    summary = {
        "timestamp": run_ts,
        "status": "error" if errors else "ok",
        "steps": steps,
        "errors": errors,
    }
    data_dir = _CFG.get("data_dir")
    if data_dir:
        _write_run_summary(Path(data_dir), summary)

    print("\n" + "═" * 50)
    print("✓ Daily loop complete.")
    if is_sunday:
        print("  Includes: digest + engage + brainstorm + learn")
    else:
        print("  Includes: digest + engage + brainstorm")
    print("═" * 50)


if __name__ == "__main__":
    main()
