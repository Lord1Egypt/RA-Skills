#!/usr/bin/env python3
"""
Generate RedNote (小红书) articles from GitHub repositories.
Main CLI entry point.
Uses OpenClaw's built-in agent capability for content generation.
"""

import argparse
import sys
import os
from typing import Optional

# Add script directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from github_api import GitHubAPI, GitHubAPIError
from llm_generator import OpenClawAgentClient, ArticleGenerator, AgentError
from formatters import RedNoteFormatter, format_rednote_article
from image_generator import generate_cover_image


def generate_fallback_article(repo_data: dict, article_type: str = 'intro') -> str:
    """Generate basic article without agent (fallback)."""
    formatter = RedNoteFormatter()
    
    # Build content parts
    parts = []
    
    # Title
    title = f"{repo_data['repo']} - {repo_data['description'] or '一个值得关注的开源项目'}"
    
    # Stats
    parts.append(formatter.format_repo_stats(
        repo_data['stars'],
        repo_data['forks'],
        repo_data['language']
    ))
    
    # Description section
    parts.append(formatter.format_section_header("项目简介"))
    if repo_data['description']:
        parts.append(repo_data['description'])
    else:
        parts.append(f"{repo_data['repo']} 是一个开源项目，值得关注！")
    
    # Features from topics
    if repo_data.get('topics'):
        parts.append(formatter.format_section_header("相关标签"))
        for topic in repo_data['topics'][:8]:
            parts.append(formatter.format_bullet(f"#{topic}"))
    
    # Languages
    if repo_data.get('languages'):
        parts.append(formatter.format_section_header("技术栈"))
        for lang, bytes_count in sorted(
            repo_data['languages'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]:
            parts.append(formatter.format_bullet(lang))
    
    # Links
    parts.append(formatter.format_section_header("相关链接"))
    parts.append(formatter.format_bullet(f"GitHub: {repo_data['url']}"))
    if repo_data.get('homepage'):
        parts.append(formatter.format_bullet(f"官网: {repo_data['homepage']}"))
    
    # Releases info
    releases = repo_data.get('releases', [])
    if releases:
        parts.append(formatter.format_section_header("最新版本"))
        for rel in releases[:3]:
            tag = rel.get('tag_name', 'N/A')
            name = rel.get('name', 'No name')
            parts.append(formatter.format_bullet(f"{tag}: {name}"))
    
    # Contributors
    contributors = repo_data.get('contributors', [])
    if contributors:
        parts.append(formatter.format_section_header("主要贡献者"))
        for c in contributors[:5]:
            parts.append(formatter.format_bullet(
                f"@{c['login']}: {c['contributions']} 次提交"
            ))
    
    # Build tags
    tags = [f"#{topic}" for topic in repo_data.get('topics', [])[:5]]
    tags.extend([f"#{repo_data['language']}", "#开源项目", "#GitHub"])
    tags = list(set(tags))  # Remove duplicates
    
    return format_rednote_article(
        content="\n".join(parts),
        title=title,
        tags=tags
    )


def generate_article(repo_data: dict, template: str = 'intro',
                     style: str = 'casual') -> str:
    """
    Generate RedNote article from repository data.
    Uses OpenClaw's built-in agent capability.
    
    Args:
        repo_data: Repository summary from GitHubAPI
        template: Article template (intro/review/tutorial/list/release)
        style: Writing style (casual/professional/enthusiastic/story/minimal)
    
    Returns:
        Formatted RedNote article
    """
    try:
        # Use OpenClaw agent for content generation
        client = OpenClawAgentClient()
        generator = ArticleGenerator(client)
        
        print(f"  Using OpenClaw agent for content generation", file=sys.stderr)
        return generator.generate(repo_data, template=template, style=style)
            
    except (AgentError, ValueError) as e:
        print(f"  Agent generation failed: {e}", file=sys.stderr)
        print("  Falling back to template generation...", file=sys.stderr)
        return generate_fallback_article(repo_data, template)


def main():
    parser = argparse.ArgumentParser(
        description="Generate RedNote article from GitHub repository using OpenClaw agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://github.com/pallets/flask
  %(prog)s https://github.com/torvalds/linux --template review --style professional
  %(prog)s https://github.com/microsoft/vscode --output vscode_article.txt

Environment Variables:
  GITHUB_TOKEN        Required for GitHub API access
        """
    )
    
    parser.add_argument(
        "url",
        nargs='?',
        default=None,
        help="GitHub repository URL"
    )
    
    parser.add_argument(
        "--template", "-t",
        choices=['intro', 'review', 'tutorial', 'list', 'release'],
        default="intro",
        help="Article template (default: intro)"
    )
    
    parser.add_argument(
        "--style", "-s",
        choices=['casual', 'professional', 'enthusiastic', 'story', 'minimal'],
        default="casual",
        help="Writing style (default: casual)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)"
    )
    
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable GitHub API caching"
    )
    
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List available article templates and exit"
    )
    
    parser.add_argument(
        "--list-styles",
        action="store_true",
        help="List available writing styles and exit"
    )
    
    parser.add_argument(
        "--clipboard", "-c",
        action="store_true",
        help="Copy output to clipboard"
    )
    
    parser.add_argument(
        "--with-image",
        action="store_true",
        help="Generate RedNote cover image (requires --output)"
    )
    
    parser.add_argument(
        "--image-output",
        help="Directory for cover image output (default: same as --output directory)"
    )
    
    args = parser.parse_args()
    
    # Handle list commands
    if args.list_templates:
        print("Available article templates:")
        for t in ArticleGenerator.list_templates():
            print(f"  {t['emoji']} {t['id']:12} - {t['name']}: {t['description']}")
        return 0
    
    if args.list_styles:
        print("Available writing styles:")
        for s in ArticleGenerator.list_styles():
            print(f"  {s['id']:12} - {s['name']}: {s['description']}")
        return 0
    
    # Validate URL argument
    if not args.url:
        parser.error("GitHub URL is required (unless using --list-templates or --list-styles)")
    
    try:
        # Initialize API with optional cache
        from github_api import GitHubCache
        cache = None if args.no_cache else GitHubCache()
        
        # Fetch repository data
        print(f"Fetching repository data...", file=sys.stderr)
        api = GitHubAPI(cache=cache)
        repo_data = api.get_repo_summary(args.url)
        print(f"✓ {repo_data['full_name']}: ⭐ {repo_data['stars']:,} stars", file=sys.stderr)
        
        # Generate article
        print(f"Generating {args.template} article ({args.style} style)...", file=sys.stderr)
        article = generate_article(
            repo_data,
            template=args.template,
            style=args.style
        )
        
        # Handle output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(article)
            print(f"✓ Article saved to: {args.output}", file=sys.stderr)
            
            # Generate cover image if requested
            if args.with_image:
                image_dir = args.image_output or os.path.dirname(args.output) or "."
                print(f"Generating cover image...", file=sys.stderr)
                image_path = generate_cover_image(repo_data, image_dir, article)
                if image_path:
                    print(f"✓ Cover image saved to: {image_path}", file=sys.stderr)
                else:
                    print(f"⚠ Cover image generation failed", file=sys.stderr)
        else:
            print(article)
            
            # Cannot generate image without output directory
            if args.with_image:
                print(f"⚠ --with-image requires --output to specify output directory", file=sys.stderr)
        
        # Copy to clipboard if requested
        if args.clipboard:
            try:
                import pyperclip
                pyperclip.copy(article)
                print(f"✓ Copied to clipboard", file=sys.stderr)
            except ImportError:
                print(f"⚠ Clipboard copy requires 'pyperclip'. Install with: pip install pyperclip", file=sys.stderr)
        
        return 0
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except GitHubAPIError as e:
        print(f"GitHub API Error: {e}", file=sys.stderr)
        if e.status_code:
            print(f"Status: {e.status_code}", file=sys.stderr)
            if e.status_code == 401:
                print("Check your GITHUB_TOKEN environment variable.", file=sys.stderr)
            elif e.status_code == 404:
                print("Repository not found. Check the URL.", file=sys.stderr)
            elif e.status_code == 403:
                print("API rate limit exceeded.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
