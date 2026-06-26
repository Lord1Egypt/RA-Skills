#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import feedparser  # type: ignore
except ImportError:
    feedparser = None


DEFAULT_USER_AGENT = "hn-podcast-archive/1.0 (+OpenClaw skill)"


@dataclass
class Episode:
    title: str
    guid: str
    published: str
    link: str
    audio_url: str
    audio_type: str
    slug: str


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "episode"


def ensure_dirs(output_dir: Path) -> dict[str, Path]:
    paths = {
        "root": output_dir,
        "audio": output_dir / "audio",
        "transcripts": output_dir / "transcripts",
        "episodes": output_dir / "episodes",
    }
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
    return paths


def load_state(path: Path) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"processed": {}, "runs": []}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_log(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def dependency_check() -> list[str]:
    missing = []
    if feedparser is None:
        missing.append("python module: feedparser")
    for binary in ("ffmpeg", "whisper"):
        if shutil.which(binary) is None:
            missing.append(f"binary: {binary}")
    return missing


def parse_feed(feed_url: str) -> list[Episode]:
    parsed = feedparser.parse(feed_url, agent=DEFAULT_USER_AGENT)
    episodes: list[Episode] = []
    for entry in parsed.entries:
        enclosures = getattr(entry, "enclosures", []) or []
        audio_url = ""
        audio_type = ""
        for enc in enclosures:
            href = enc.get("href") or ""
            enc_type = enc.get("type") or ""
            if href:
                audio_url = href
                audio_type = enc_type
                break
        if not audio_url:
            links = getattr(entry, "links", []) or []
            for link in links:
                href = link.get("href") or ""
                rel = link.get("rel") or ""
                link_type = link.get("type") or ""
                if href and (rel == "enclosure" or str(link_type).startswith("audio/")):
                    audio_url = href
                    audio_type = link_type
                    break
        if not audio_url:
            continue
        title = getattr(entry, "title", "Untitled episode")
        guid = getattr(entry, "id", "") or getattr(entry, "guid", "") or audio_url
        published = getattr(entry, "published", "") or getattr(entry, "updated", "") or ""
        link = getattr(entry, "link", "") or audio_url
        slug = slugify(title)
        episodes.append(Episode(title=title, guid=guid, published=published, link=link, audio_url=audio_url, audio_type=audio_type, slug=slug))
    return episodes


def file_ext_from_url(url: str, fallback: str = ".mp3") -> str:
    base = url.split("?")[0].split("#")[0]
    ext = os.path.splitext(base)[1].lower()
    if ext and len(ext) <= 8:
        return ext
    return fallback


def download_file(url: str, dest: Path, dry_run: bool) -> None:
    if dry_run:
        return
    req = urllib.request.Request(url, headers={"User-Agent": DEFAULT_USER_AGENT})
    with urllib.request.urlopen(req) as resp, dest.open("wb") as out:
        shutil.copyfileobj(resp, out)


def transcribe(audio_path: Path, transcripts_dir: Path, model: str, dry_run: bool) -> Path:
    expected = transcripts_dir / f"{audio_path.stem}.txt"
    if dry_run:
        return expected
    cmd = [
        "whisper",
        str(audio_path),
        "--model",
        model,
        "--output_format",
        "txt",
        "--output_dir",
        str(transcripts_dir),
    ]
    subprocess.run(cmd, check=True)
    if not expected.exists():
        raise FileNotFoundError(f"Whisper did not produce expected transcript: {expected}")
    return expected


def render_episode_markdown(ep: Episode, audio_rel: str, transcript_rel: str, transcript_text: str) -> str:
    return textwrap.dedent(
        f"""\
        # {ep.title}

        - Published: {ep.published or 'unknown'}
        - GUID: {ep.guid}
        - Link: {ep.link}
        - Audio URL: {ep.audio_url}
        - Audio File: `{audio_rel}`
        - Transcript File: `{transcript_rel}`

        ## Transcript

        {transcript_text}
        """
    )


def update_index(index_path: Path, episodes_dir: Path) -> None:
    files = sorted(episodes_dir.glob("*.md"), reverse=True)
    lines = ["# Hacker News Podcast Archive", ""]
    for file in files:
        title = file.stem
        with file.open("r", encoding="utf-8") as f:
            first = f.readline().strip()
        if first.startswith("# "):
            title = first[2:]
        lines.append(f"- [{title}](episodes/{file.name})")
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def process_episode(ep: Episode, output_dir: Path, whisper_model: str, state: dict[str, Any], dry_run: bool, force: bool, log_path: Path) -> dict[str, Any]:
    paths = ensure_dirs(output_dir)
    key = ep.guid or ep.audio_url
    already = state.get("processed", {}).get(key)
    if already and not force:
        record = {"ts": now_iso(), "status": "skipped", "guid": key, "title": ep.title, "reason": "already-processed"}
        append_log(log_path, record)
        return record

    ext = file_ext_from_url(ep.audio_url)
    audio_path = paths["audio"] / f"{ep.slug}{ext}"
    transcript_path = paths["transcripts"] / f"{ep.slug}.txt"
    episode_md_path = paths["episodes"] / f"{ep.slug}.md"

    try:
        if not audio_path.exists() or force:
            download_file(ep.audio_url, audio_path, dry_run=dry_run)
        transcript_generated = transcribe(audio_path, paths["transcripts"], whisper_model, dry_run=dry_run)
        if transcript_generated != transcript_path and not dry_run and transcript_generated.exists():
            transcript_generated.replace(transcript_path)
        transcript_text = "[dry-run: transcript not generated]"
        if transcript_path.exists():
            transcript_text = transcript_path.read_text(encoding="utf-8", errors="replace")
        audio_rel = os.path.relpath(audio_path, output_dir)
        transcript_rel = os.path.relpath(transcript_path, output_dir)
        if not dry_run:
            episode_md_path.write_text(render_episode_markdown(ep, audio_rel, transcript_rel, transcript_text), encoding="utf-8")
        state.setdefault("processed", {})[key] = {
            "title": ep.title,
            "slug": ep.slug,
            "published": ep.published,
            "audio_url": ep.audio_url,
            "audio_file": audio_rel,
            "transcript_file": transcript_rel,
            "episode_file": os.path.relpath(episode_md_path, output_dir),
            "processed_at": now_iso(),
        }
        record = {"ts": now_iso(), "status": "processed", "guid": key, "title": ep.title, "audio": str(audio_path), "transcript": str(transcript_path)}
        append_log(log_path, record)
        return record
    except Exception as exc:
        record = {"ts": now_iso(), "status": "failed", "guid": key, "title": ep.title, "error": str(exc)}
        append_log(log_path, record)
        return record


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive podcast episodes from RSS and transcribe them with Whisper.")
    parser.add_argument("--feed-url", required=True, help="RSS feed URL")
    parser.add_argument("--output-dir", required=True, help="Archive output directory")
    parser.add_argument("--whisper-model", default="turbo", help="Whisper model name")
    parser.add_argument("--limit", type=int, default=0, help="Only process first N feed items")
    parser.add_argument("--force", action="store_true", help="Reprocess already-seen episodes")
    parser.add_argument("--dry-run", action="store_true", help="Print intent without writing files")
    args = parser.parse_args()

    missing = dependency_check()
    if missing:
        print("Missing dependencies:", file=sys.stderr)
        for item in missing:
            print(f"- {item}", file=sys.stderr)
        print("Install the missing dependencies, then rerun.", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir).expanduser().resolve()
    ensure_dirs(output_dir)
    state_path = output_dir / "state.json"
    log_path = output_dir / "run-log.jsonl"
    index_path = output_dir / "index.md"
    state = load_state(state_path)

    episodes = parse_feed(args.feed_url)
    if args.limit and args.limit > 0:
        episodes = episodes[: args.limit]

    results = []
    for ep in episodes:
        results.append(process_episode(ep, output_dir, args.whisper_model, state, args.dry_run, args.force, log_path))

    if not args.dry_run:
        save_state(state_path, state)
        update_index(index_path, output_dir / "episodes")

    processed = sum(1 for r in results if r["status"] == "processed")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    failed = sum(1 for r in results if r["status"] == "failed")
    print(json.dumps({
        "feed_url": args.feed_url,
        "output_dir": str(output_dir),
        "episodes_seen": len(episodes),
        "processed": processed,
        "skipped": skipped,
        "failed": failed,
        "dry_run": args.dry_run,
    }, ensure_ascii=False, indent=2))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
