#!/usr/bin/env python3
"""Fetch podcast episodes from configured RSS feeds."""

import json
import sys
import argparse
import hashlib
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import List, Dict, Optional

import feedparser

from utils import Episode


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch podcast episodes from RSS feeds"
    )
    parser.add_argument(
        '--config',
        type=Path,
        help='Path to feeds.yaml configuration file'
    )
    parser.add_argument(
        '--feed-url',
        type=str,
        help='Fetch from a single feed URL instead of config'
    )
    parser.add_argument(
        '--hours',
        type=int,
        default=168,
        help='Look back this many hours for new episodes (default: 168 = 7 days)'
    )
    return parser.parse_args()


def generate_episode_id(audio_url: str) -> str:
    """Generate episode ID from audio URL."""
    return hashlib.sha256(audio_url.encode()).hexdigest()[:12]


def parse_iso_date(date_str: str) -> Optional[datetime]:
    """Parse ISO 8601 date string."""
    try:
        parsed = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        try:
            parsed = parsedate_to_datetime(date_str)
        except (TypeError, ValueError):
            return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def fetch_feed(feed_url: str, feed_name: str, hours: int) -> List[Episode]:
    """Fetch episodes from a single RSS feed."""
    episodes = []
    lookback_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    
    try:
        feed = feedparser.parse(feed_url)
        
        if feed.bozo:
            print(f"Warning: Feed parsing error for {feed_name}: {feed.bozo_exception}", 
                  file=sys.stderr)
        
        for entry in feed.entries:
            # Extract publish date
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            elif hasattr(entry, 'published'):
                published = parse_iso_date(entry.published)
            
            if not published:
                continue
            
            # Filter by time window
            if published < lookback_time:
                continue
            
            # Extract audio URL
            audio_url = None
            if hasattr(entry, 'enclosures'):
                for enclosure in entry.enclosures:
                    content_type = str(getattr(enclosure, "type", "")).lower()
                    if 'audio' in content_type:
                        audio_url = enclosure.href
                        break
            
            if not audio_url:
                continue
            
            # Extract duration if available
            duration = 0
            if hasattr(entry, 'itunes_duration'):
                try:
                    # Handle various duration formats
                    dur_str = entry.itunes_duration
                    if ':' in dur_str:
                        # HH:MM:SS or MM:SS format
                        parts = dur_str.split(':')
                        if len(parts) == 3:
                            duration = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                        elif len(parts) == 2:
                            duration = int(parts[0]) * 60 + int(parts[1])
                    else:
                        duration = int(dur_str)  # Already in seconds
                except (ValueError, AttributeError):
                    pass
            
            # Create episode
            episode = Episode(
                id=generate_episode_id(audio_url),
                show=feed_name,
                title=entry.get('title', 'Untitled'),
                published=published,
                audio_url=audio_url,
                duration_seconds=duration,
                description=entry.get('summary', ''),
                feed_url=feed_url
            )
            
            episodes.append(episode)
    
    except Exception as e:
        print(f"Error fetching feed {feed_name}: {e}", file=sys.stderr)
    
    return episodes


def deduplicate_episodes(episodes: List[Episode]) -> List[Episode]:
    """Deduplicate episodes by audio_url, keeping most recent."""
    seen = {}
    for ep in episodes:
        if ep.audio_url not in seen or ep.published > seen[ep.audio_url].published:
            seen[ep.audio_url] = ep
    
    return list(seen.values())


def main():
    """Fetch episodes from feeds and output JSON."""
    args = parse_args()
    
    all_episodes = []
    
    if args.feed_url:
        # Fetch from single feed
        episodes = fetch_feed(args.feed_url, "Unknown Feed", args.hours)
        all_episodes.extend(episodes)
    else:
        # Load feeds from config
        try:
            from utils import load_feeds_config
            feeds = load_feeds_config(args.config)
        except Exception as e:
            print(f"Error loading feeds config: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Fetch from each feed
        for feed in feeds:
            episodes = fetch_feed(feed['url'], feed['name'], args.hours)
            all_episodes.extend(episodes)
    
    # Deduplicate
    all_episodes = deduplicate_episodes(all_episodes)
    
    # Sort by published descending
    all_episodes.sort(key=lambda e: e.published, reverse=True)
    
    # Convert to JSON-serializable format
    output = [
        {
            'id': ep.id,
            'show': ep.show,
            'title': ep.title,
            'published': ep.published.isoformat().replace('+00:00', 'Z'),
            'audio_url': ep.audio_url,
            'duration_seconds': ep.duration_seconds,
            'description': ep.description[:200] + '...' if len(ep.description) > 200 else ep.description,
            'feed_url': ep.feed_url
        }
        for ep in all_episodes
    ]
    
    # Output JSON
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
