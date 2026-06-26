#!/usr/bin/env python3
"""
Image Breaker - Convert documents, PDFs, and images to structured markdown notes.

Usage:
    python3 break_image.py <url_or_path> [--title "Title"] [--tags tag1,tag2] [--output-dir path] [--sync]

Examples:
    python3 break_image.py https://labcorp.com/document.pdf --title "NMR Panel Reference" --sync
    python3 break_image.py /path/to/image.jpg --title "Research Notes" --tags research,bloodwork --sync
"""

import sys
import os
import argparse
import subprocess
import re
from datetime import datetime
from pathlib import Path

# Add workspace to path for imports
WORKSPACE_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_DIR))


def slugify(text):
    """Convert text to filesystem-safe slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def extract_url_content(url):
    """
    Extract content from URL using OpenClaw's web_fetch.
    Returns markdown content.
    """
    # For now, return placeholder - Cortana will use web_fetch directly
    return f"<!-- Content extracted from: {url} -->\n\n"


def create_markdown_note(content, title, tags=None, source=None):
    """
    Convert content to structured markdown with YAML frontmatter.
    
    Args:
        content: Raw content text
        title: Note title
        tags: List of tags
        source: Source URL or path
    
    Returns:
        Formatted markdown string
    """
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Build frontmatter
    frontmatter = ["---"]
    frontmatter.append(f"date: {date}")
    
    if tags:
        frontmatter.append("tags:")
        for tag in tags:
            frontmatter.append(f"  - {tag}")
    
    if source:
        frontmatter.append(f"source: {source}")
    
    frontmatter.append("type: image-breaker-note")
    frontmatter.append("---")
    
    # Build full note
    note = "\n".join(frontmatter)
    note += f"\n\n# {title}\n\n"
    note += content
    
    return note


def save_note(content, title, output_dir):
    """
    Save markdown note to workspace.
    
    Args:
        content: Markdown content
        title: Note title
        output_dir: Output directory path
    
    Returns:
        Path to saved file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(title)
    filename = f"{date}-{slug}.md"
    filepath = output_path / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


def sync_to_obsidian(filepath, subfolder="ImageBreaker"):
    """
    Sync file to Obsidian using obsidian-sync skill.
    
    Args:
        filepath: Path to markdown file
        subfolder: Obsidian subfolder name
    """
    obsidian_sync_script = WORKSPACE_DIR / "skills/obsidian-sync/scripts/sync_to_obsidian.py"
    obsidian_vault = "/Users/biohacker/Desktop/Connections"
    
    cmd = [
        "python3",
        str(obsidian_sync_script),
        str(filepath),
        obsidian_vault,
        subfolder
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"\n✅ Synced to Obsidian: {subfolder}/{filepath.name}")
    else:
        print(f"\n⚠️  Obsidian sync failed: {result.stderr}")


def main():
    parser = argparse.ArgumentParser(
        description="Break down documents/images into structured markdown notes"
    )
    parser.add_argument(
        "source",
        help="URL or file path to process"
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Note title"
    )
    parser.add_argument(
        "--tags",
        help="Comma-separated tags"
    )
    parser.add_argument(
        "--output-dir",
        default=str(WORKSPACE_DIR / "research/image-breaker-notes"),
        help="Output directory (default: research/image-breaker-notes)"
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Automatically sync to Obsidian after saving"
    )
    
    args = parser.parse_args()
    
    # Parse tags
    tags = []
    if args.tags:
        tags = [t.strip() for t in args.tags.split(",")]
    
    # This is a helper script - Cortana will provide the actual content
    # via the content parameter when calling this programmatically
    print(f"📝 Creating note: {args.title}")
    print(f"📂 Output: {args.output_dir}")
    
    if args.sync:
        print(f"🔄 Will sync to Obsidian after saving")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
