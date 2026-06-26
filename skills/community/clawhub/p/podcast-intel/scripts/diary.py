#!/usr/bin/env python3
"""Manage podcast consumption diary."""

import json
import sys
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Optional

from utils import save_diary_entry, save_markdown_note, get_diary_path, load_diary


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Manage podcast consumption diary"
    )
    parser.add_argument(
        '--analysis',
        type=str,
        help='Path or JSON string containing analysis data to log'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='Display diary entries'
    )
    parser.add_argument(
        '--last',
        type=int,
        default=7,
        help='Show entries from the last N days'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'markdown'],
        default='markdown',
        help='Output format for diary display'
    )
    parser.add_argument(
        '--diary-path',
        type=Path,
        help='Custom path to diary file'
    )
    return parser.parse_args()


def append_to_diary(analysis: Dict, diary_path: Optional[Path] = None) -> None:
    """Append an analyzed episode to the diary."""
    now = datetime.now(timezone.utc)
    
    # Create diary entry
    entry = {
        'briefed_at': now.isoformat().replace("+00:00", "Z"),
        'episode_id': analysis.get('episode_id', 'unknown'),
        'show': analysis.get('show', 'Unknown'),
        'title': analysis.get('title', 'Untitled'),
        'topics_exposed': [
            s['label'] for s in analysis.get('segments_ranked', [])
        ],
        'topic_embeddings_hash': 'na',  # Placeholder
        'wyt_score': analysis.get('worth_your_time_score', 0),
        'novel_minutes': analysis.get('novel_minutes', 0),
        'total_minutes': analysis.get('total_minutes', 0),
        'segments_recommended': [
            s['topic_id'] for s in analysis.get('segments_ranked', [])
            if 'LISTEN' in s.get('listen_recommendation', '')
        ],
        'segments_skipped': [
            s['topic_id'] for s in analysis.get('segments_ranked', [])
            if 'SKIP' in s.get('listen_recommendation', '')
        ],
        'overlap_flags': [
            o.get('topic', '') for o in analysis.get('overlaps', [])
        ]
    }
    
    # Save to JSONL diary
    if diary_path:
        # Write to custom path
        diary_path.parent.mkdir(parents=True, exist_ok=True)
        with open(diary_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    else:
        # Use default
        save_diary_entry(entry)
    
    # Also write to markdown memory file
    wyt_percent = int(entry['wyt_score'] * 100)
    novel_text = f"{entry['novel_minutes']:.0f} min of {entry['total_minutes']:.0f} min total"
    
    markdown = f"""
### {entry['show']}: {entry['title']} (WYT: {wyt_percent}%)
- **Worth listening:** {novel_text}
- **Key topics:** {', '.join(entry['topics_exposed'][:3])}
- **Recommended segments:** {len(entry['segments_recommended'])} / {len(entry['segments_recommended']) + len(entry['segments_skipped'])}
"""
    
    if entry['overlap_flags']:
        markdown += f"- **Note:** Overlaps with {', '.join(entry['overlap_flags'][:2])}\n"
    
    markdown += "\n"
    
    save_markdown_note(markdown)


def parse_briefed_at(value: str) -> Optional[datetime]:
    """Parse diary briefed_at field into timezone-aware datetime."""
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def filter_entries_last_days(diary: List[Dict], last_n_days: int) -> List[Dict]:
    """Filter entries to the last N days by briefed_at."""
    if last_n_days <= 0:
        return diary

    cutoff = datetime.now(timezone.utc) - timedelta(days=last_n_days)
    filtered = []
    for entry in diary:
        briefed_at = parse_briefed_at(entry.get("briefed_at", ""))
        if briefed_at is None or briefed_at >= cutoff:
            filtered.append(entry)
    return filtered


def display_diary_entries(diary: List[Dict], last_n_days: int = 7, format_type: str = 'markdown') -> str:
    """Display diary entries."""
    diary = filter_entries_last_days(diary, last_n_days)
    diary = sorted(
        diary,
        key=lambda entry: parse_briefed_at(entry.get("briefed_at", "")) or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )

    if format_type == 'json':
        return json.dumps(diary, indent=2)
    
    # Markdown format
    output = "## 🎧 Podcast Consumption Diary\n\n"
    
    for entry in diary[-20:]:  # Show last 20 entries
        briefed_at = entry.get('briefed_at', '?')
        show = entry.get('show', '?')
        title = entry.get('title', '?')
        wyt = int(entry.get('wyt_score', 0) * 100)
        novel_mins = entry.get('novel_minutes', 0)
        total_mins = entry.get('total_minutes', 0)
        
        output += f"### {show}: {title} (WYT: {wyt}%)\n"
        output += f"- **Briefed:** {briefed_at}\n"
        output += f"- **Content:** {novel_mins:.0f}m novel / {total_mins:.0f}m total\n"
        
        topics = entry.get('topics_exposed', [])
        if topics:
            output += f"- **Topics:** {', '.join(topics[:3])}\n"
        
        output += "\n"
    
    return output


def main():
    """Main diary entry point."""
    args = parse_args()
    
    if args.show:
        # Display diary
        try:
            diary = load_diary()
            output = display_diary_entries(diary, args.last, args.format)
            print(output)
        except Exception as e:
            print(f"Error displaying diary: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.analysis:
        # Append analysis to diary
        try:
            analysis_data = json.loads(args.analysis)
        except json.JSONDecodeError:
            try:
                with open(args.analysis, 'r') as f:
                    analysis_data = json.load(f)
            except Exception as e:
                print(f"Error loading analysis data: {e}", file=sys.stderr)
                sys.exit(1)
        
        # Handle list of analyses
        if isinstance(analysis_data, list):
            for analysis in analysis_data:
                append_to_diary(analysis, args.diary_path)
        else:
            append_to_diary(analysis_data, args.diary_path)
        
        print("Diary updated", file=sys.stderr)
    
    else:
        # Default: show diary
        try:
            diary = load_diary()
            output = display_diary_entries(diary, args.last, args.format)
            print(output)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
