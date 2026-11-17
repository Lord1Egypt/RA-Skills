# -*- coding: utf-8 -*-
"""
omnipub-content-engine Unified CLI
====================================
Single entry point for all content engine operations.

Commands:
  topic         Search and score hot topics
  fact-check     Verify data claims in article
  infographic   Generate AI infographic prompts
  footer         Build article footer from config
  geo-check      Check GEO readiness of article
  convert        Convert HTML to WeChat-compatible format
  preview        Preview article with theme in browser
  gallery        Show all themes side-by-side
  themes         List available themes
  publish        Publish article to WeChat draft box
  toutiao        Prepare/publish article to Toutiao
  analytics      Analyze post-publish data

Usage:
  python cli.py <command> [args]
  python cli.py publish article.md --cover cover.png --theme xinming-lab
  python cli.py gallery
  python cli.py geo-check article.md
"""
import argparse
import os
import sys
import subprocess
import webbrowser
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
PYTHON = sys.executable

# Import theme and converter modules
sys.path.insert(0, str(SCRIPT_DIR))
try:
    from theme import load_theme, list_themes
    from converter import WeChatConverter, ConvertResult
    from wechat_publish import create_draft, verify_draft, push_loop, detect_mmbiz_images, republish_with_images
    from wechat_api import get_access_token, upload_image, upload_thumb, delete_draft
    _MODULES_OK = True
except ImportError:
    _MODULES_OK = False


def cmd_topic(args):
    """Search and score hot topics."""
    cmd = [PYTHON, str(SCRIPT_DIR / "topic_research.py"), args.query]
    if args.redfox_key:
        cmd += ["--redfox-key", args.redfox_key]
    if args.days:
        cmd += ["--days", str(args.days)]
    if args.output:
        cmd += ["--output", args.output]
    if args.verbose:
        cmd += ["--verbose"]
    subprocess.run(cmd)


def cmd_fact_check(args):
    """Verify data claims in article."""
    cmd = [PYTHON, str(SCRIPT_DIR / "fact_check.py"), args.input]
    if args.output:
        cmd += ["--output", args.output]
    if args.verbose:
        cmd += ["--verbose"]
    subprocess.run(cmd)


def cmd_infographic(args):
    """Generate AI infographic prompts."""
    cmd = [PYTHON, str(SCRIPT_DIR / "infographic.py"), args.title,
           "--engine", args.engine]
    if args.subtitle:
        cmd += ["--subtitle", args.subtitle]
    if args.data:
        cmd += ["--data", args.data]
    if args.source:
        cmd += ["--source", args.source]
    if args.brand:
        cmd += ["--brand", args.brand]
    if args.output:
        cmd += ["--output", args.output]
    subprocess.run(cmd)


def cmd_footer(args):
    """Build article footer from config."""
    cmd = [PYTHON, str(SCRIPT_DIR / "footer_builder.py"),
           "--config", args.config, "--format", args.format]
    if args.output:
        cmd += ["--output", args.output]
    subprocess.run(cmd)


def cmd_geo_check(args):
    """Check GEO readiness of article."""
    cmd = [PYTHON, str(SCRIPT_DIR / "geo_check.py"), "--file", args.input]
    if args.keyword:
        cmd += ["--keyword", args.keyword]
    if args.brand:
        cmd += ["--brand", args.brand]
    subprocess.run(cmd)


def cmd_convert(args):
    """Convert HTML to WeChat-compatible format."""
    cmd = [PYTHON, str(SCRIPT_DIR / "wechat_compat.py"),
           "--src", args.src, "--dst", args.dst]
    if args.verbose:
        cmd += ["--verbose"]
    subprocess.run(cmd)


def cmd_themes(args):
    """List available themes."""
    themes_dir = SKILL_DIR / "themes"
    if not themes_dir.exists():
        print("No themes directory found.")
        return
    yaml_files = list(themes_dir.glob("*.yaml"))
    if not yaml_files:
        print("No themes found.")
        return
    print(f"Available themes ({len(yaml_files)}):")
    print()
    for f in sorted(yaml_files):
        try:
            import yaml
            with open(f, encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            name = data.get("name", f.stem)
            desc = data.get("description", "")
            colors = data.get("colors", {})
            color_str = " / ".join(f"{k}:{v}" for k, v in colors.items()) if colors else ""
            print(f"  {f.stem}")
            print(f"    Name: {name}")
            print(f"    Desc: {desc}")
            if color_str:
                print(f"    Colors: {color_str}")
            print()
        except Exception as e:
            print(f"  {f.stem} (error reading: {e})")


def cmd_gallery(args):
    """Show all themes side-by-side in browser."""
    if not _MODULES_OK:
        print("Modules not available. Run from the skill directory.")
        return

    themes_dir = str(SKILL_DIR / "themes")
    theme_names = list_themes(themes_dir)
    if not theme_names:
        print("No themes found.")
        return

    sample_md = """# Sample Article

## Section One

This is a sample paragraph to demonstrate theme styling. The quick brown fox jumps over the lazy dog. Lorem ipsum dolor sit amet.

## Section Two

- Bullet point one
- Bullet point two
- Bullet point three

> This is a blockquote with important insight.

## Data Section

| Metric | Value | Change |
|--------|-------|--------|
| Users | 1.2M | +15% |
| Revenue | 3.5B | +8% |
"""

    html_parts = ['<!DOCTYPE html><html><head><meta charset="utf-8">',
                  '<title>Theme Gallery</title>',
                  '<style>body{margin:0;padding:20px;background:#f5f5f5;}'
                  '.gallery{display:flex;gap:20px;flex-wrap:wrap;}'
                  '.theme-card{flex:1;min-width:400px;max-width:600px;}'
                  '.theme-card h2{background:#333;color:#fff;padding:10px;margin:0 0 0;}'
                  '.theme-card .content{background:#fff;padding:16px;min-height:400px;}</style>'
                  '</head><body><div class="gallery">']

    for theme_name in theme_names:
        try:
            theme = load_theme(theme_name, themes_dir)
            converter = WeChatConverter(theme=theme)
            result = converter.convert(sample_md)
            html_parts.append(
                f'<div class="theme-card"><h2>{theme_name}</h2>'
                f'<div class="content">{result.html}</div></div>'
            )
        except Exception as e:
            html_parts.append(
                f'<div class="theme-card"><h2>{theme_name}</h2>'
                f'<div class="content">Error: {e}</div></div>'
            )

    html_parts.append('</div></body></html>')
    html = "\n".join(html_parts)

    output = args.output or os.path.join(SKILL_DIR, "gallery.html")
    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Gallery saved: {output}")
    if not args.no_open:
        webbrowser.open(f"file:///{os.path.abspath(output)}")


def cmd_preview(args):
    """Preview article with selected theme."""
    if not _MODULES_OK:
        print("Modules not available. Run from the skill directory.")
        return

    themes_dir = str(SKILL_DIR / "themes")
    with open(args.input, encoding="utf-8") as f:
        md = f.read()

    theme = load_theme(args.theme, themes_dir)
    converter = WeChatConverter(theme=theme)
    result = converter.convert(md)

    full = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Preview - {args.theme}</title>
<style>body{{max-width:680px;margin:0 auto;padding:20px;background:#fff;}}</style>
</head><body>{result.html}</body></html>"""

    output = args.output or os.path.join(SKILL_DIR, "preview.html")
    with open(output, "w", encoding="utf-8") as f:
        f.write(full)

    print(f"Preview saved: {output}")
    if not args.no_open:
        webbrowser.open(f"file:///{os.path.abspath(output)}")


def cmd_publish(args):
    """Publish article to WeChat draft box."""
    if not _MODULES_OK:
        print("Modules not available. Run from the skill directory.")
        return

    # Load config
    config_path = SKILL_DIR / "config.yaml"
    if not config_path.exists():
        config_path = SKILL_DIR / "config.example.yaml"
        print("Warning: config.yaml not found, using example config")

    try:
        import yaml
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Config error: {e}")
        return

    wechat_cfg = config.get("publish", {}).get("wechat", {})
    appid = args.appid or wechat_cfg.get("appid", "")
    secret = args.secret or wechat_cfg.get("secret", "")

    if not appid or not secret:
        print("Error: WeChat appid and secret required. Use --appid and --secret or set in config.yaml")
        return

    # Get access token (with retry if --retry is set)
    print("Getting access token...")
    token = None
    if args.retry:
        loop_result = push_loop(appid, secret, get_token_fn=get_access_token)
        if loop_result["token"]:
            token = loop_result["token"]
            print(f"  Token acquired after {loop_result['attempts']} attempts")
            if loop_result["seen_ips"]:
                print(f"  Seen IPs during retry: {', '.join(loop_result['seen_ips'])}")
        else:
            print(f"Error: All {loop_result['attempts']} attempts failed.")
            print(f"  Seen IPs: {', '.join(loop_result['seen_ips'])}")
            print("  Please add all these IPs to WeChat MP IP whitelist, then retry.")
            return
    else:
        token = get_access_token(appid, secret)

    if not token:
        print("Error: Failed to get access token. Check appid/secret.")
        return
    print(f"  Token: {token[:20]}...")

    # Read markdown
    with open(args.input, encoding="utf-8") as f:
        md = f.read()

    # Upload images (local + optionally force re-upload https/mmbiz)
    import re
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    image_uploads = {}

    # Detect stale mmbiz links (from deleted drafts)
    stale_images = detect_mmbiz_images(md) if not args.force_upload else []
    if stale_images:
        print(f"  WARNING: Found {len(stale_images)} mmbiz.qpic.cn URLs that may be stale.")
        for img in stale_images:
            print(f"    - {img['alt']}: {img['url'][:60]}...")

    def replace_image(match):
        alt, src = match.group(1), match.group(2)
        if src.startswith("http") and not args.force_upload:
            # Skip https URLs unless --force-upload is set
            # But warn if it's an mmbiz link (likely stale from deleted draft)
            if "mmbiz.qpic.cn" in src:
                print(f"  WARNING: Skipping stale mmbiz URL (use --force-upload to re-upload): {src[:60]}...")
            return match.group(0)
        # Resolve relative paths against the markdown file's directory
        if not os.path.exists(src):
            md_dir = os.path.dirname(os.path.abspath(args.input))
            src_abs = os.path.join(md_dir, src)
            if os.path.exists(src_abs):
                src = src_abs
        if os.path.exists(src):
            print(f"  Uploading image: {src}")
            try:
                new_url = upload_image(token, src)
                image_uploads[src] = new_url
                print(f"    -> {new_url}")
                return f"![{alt}]({new_url})"
            except Exception as e:
                print(f"    Error: {e}")
                return match.group(0)
        return match.group(0)

    md = re.sub(image_pattern, replace_image, md)

    # Convert markdown to HTML with theme
    themes_dir = str(SKILL_DIR / "themes")
    theme = load_theme(args.theme, themes_dir)
    converter = WeChatConverter(theme=theme)
    result = converter.convert(md)

    # Use converted title/digest
    title = args.title or result.title or Path(args.input).stem
    digest = result.digest or ""

    # Upload cover
    thumb_media_id = None
    if args.cover:
        print(f"Uploading cover: {args.cover}")
        try:
            thumb_media_id = upload_thumb(token, args.cover)
            print(f"  -> media_id: {thumb_media_id}")
        except Exception as e:
            print(f"  Warning: Cover upload failed: {e}")
            print("  Continuing without cover. Note: WeChat draft/add requires thumb_media_id.")
            return

    # Delete old draft if specified
    if args.delete_old:
        print(f"Deleting old draft: {args.delete_old[:30]}...")
        try:
            result_del = delete_draft(token, args.delete_old)
            print(f"  -> {result_del}")
        except Exception as e:
            print(f"  Warning: Delete failed: {e}")

    # Create draft
    print(f"Creating draft: {title}")
    author = wechat_cfg.get("author", config.get("brand", {}).get("author", ""))
    try:
        draft_result = create_draft(token, title, result.html, digest, thumb_media_id, author=author)
        media_id = draft_result.media_id if hasattr(draft_result, 'media_id') else ""
        if media_id:
            print(f"\nSuccess! Draft created.")
            print(f"  Media ID: {media_id}")
            print(f"  Title: {title}")
            print(f"  Theme: {args.theme}")
            print(f"  Images uploaded: {len(image_uploads)}")

            # Verify draft if --verify is set
            if args.verify:
                print("\nVerifying draft (draft/get)...")
                try:
                    v = verify_draft(token, media_id)
                    print(f"  Title verified: {v.title}")
                    print(f"  Content length: {v.content_length}")
                    print(f"  Images in draft: {v.image_count}")
                    print(f"  Style stats (should be 0 for safe props):")
                    for k, count in v.style_stats.items():
                        flag = "⚠️" if count > 0 and k in ("border_radius", "box_shadow", "linear_gradient", "letter_spacing", "opacity", "text_shadow", "flex", "grid") else "  "
                        print(f"    {flag} {k}: {count}")
                    print(f"\n  Verification complete. Media ID: {media_id}")
                except Exception as e:
                    print(f"  Warning: Verification failed: {e}")
        else:
            print(f"Error: No media_id returned")
    except Exception as e:
        print(f"Error creating draft: {e}")


def cmd_toutiao(args):
    """Prepare/publish article to Toutiao."""
    cmd = [PYTHON, str(SCRIPT_DIR / "toutiao_publish.py")]
    if args.subcommand == "prepare":
        cmd += ["prepare", args.input, "--output", args.output]
    elif args.subcommand == "publish":
        cmd += ["publish", "--title", args.title, "--inject", args.inject, "--images", args.images]
    else:
        cmd += ["--help"]
    subprocess.run(cmd)


def cmd_analytics(args):
    """Analyze post-publish data."""
    cmd = [PYTHON, str(SCRIPT_DIR / "analyze_article_data.py")]
    if args.csv:
        cmd += ["--csv", args.csv]
    elif args.demo:
        cmd += ["--demo"]
    if args.output:
        cmd += ["--out", args.output]
    subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(
        prog="omnipub",
        description="omnipub-content-engine: Full-cycle content publishing pipeline"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # topic
    p = subparsers.add_parser("topic", help="Search and score hot topics")
    p.add_argument("query", help="Search keyword")
    p.add_argument("--platforms", default="all")
    p.add_argument("--redfox-key", default=os.environ.get("REDFOX_API_KEY", ""))
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--output", "-o")
    p.add_argument("--verbose", "-v", action="store_true")
    p.set_defaults(func=cmd_topic)

    # fact-check
    p = subparsers.add_parser("fact-check", help="Verify data claims")
    p.add_argument("input", help="Article file path")
    p.add_argument("--output", "-o")
    p.add_argument("--verbose", "-v", action="store_true")
    p.set_defaults(func=cmd_fact_check)

    # infographic
    p = subparsers.add_parser("infographic", help="Generate AI infographic prompts")
    p.add_argument("title", help="Main title (Chinese)")
    p.add_argument("--subtitle", default="")
    p.add_argument("--data", default="")
    p.add_argument("--source", default="公开数据整理")
    p.add_argument("--brand", default="心明增长实验室")
    p.add_argument("--engine", default="all", choices=["jimeng", "lovart", "chatgpt", "midjourney", "all"])
    p.add_argument("--output", "-o")
    p.set_defaults(func=cmd_infographic)

    # footer
    p = subparsers.add_parser("footer", help="Build article footer")
    p.add_argument("--config", default=str(SKILL_DIR / "config.yaml"))
    p.add_argument("--format", choices=["html", "markdown"], default="html")
    p.add_argument("--output", "-o")
    p.set_defaults(func=cmd_footer)

    # geo-check
    p = subparsers.add_parser("geo-check", help="Check GEO readiness")
    p.add_argument("input", help="Article file path")
    p.add_argument("--keyword", help="Target keyword for GEO check")
    p.add_argument("--brand", help="Brand name for attribution check")
    p.set_defaults(func=cmd_geo_check)

    # convert
    p = subparsers.add_parser("convert", help="Convert HTML to WeChat format")
    p.add_argument("--src", required=True, help="Source HTML file")
    p.add_argument("--dst", required=True, help="Destination HTML file")
    p.add_argument("--verbose", "-v", action="store_true")
    p.set_defaults(func=cmd_convert)

    # themes
    p = subparsers.add_parser("themes", help="List available themes")
    p.set_defaults(func=cmd_themes)

    # gallery
    p = subparsers.add_parser("gallery", help="Show theme gallery")
    p.add_argument("--output", "-o")
    p.add_argument("--no-open", action="store_true")
    p.set_defaults(func=cmd_gallery)

    # preview
    p = subparsers.add_parser("preview", help="Preview article with theme")
    p.add_argument("input", help="Markdown article path")
    p.add_argument("--theme", "-t", default="xinming-lab")
    p.add_argument("--output", "-o")
    p.add_argument("--no-open", action="store_true")
    p.set_defaults(func=cmd_preview)

    # publish
    p = subparsers.add_parser("publish", help="Publish to WeChat draft box")
    p.add_argument("input", help="Markdown article path")
    p.add_argument("--cover", help="Cover image path (required: draft/add needs thumb_media_id)")
    p.add_argument("--theme", "-t", default="xinming-lab")
    p.add_argument("--title", help="Override article title")
    p.add_argument("--appid", help="WeChat AppID")
    p.add_argument("--secret", help="WeChat AppSecret")
    p.add_argument("--delete-old", help="Old draft media_id to delete")
    p.add_argument("--verify", action="store_true", help="Verify draft after creation (draft/get)")
    p.add_argument("--force-upload", action="store_true", help="Force re-upload all images including https URLs")
    p.add_argument("--retry", action="store_true", help="Auto-retry on IP whitelist errors (China Mobile)")
    p.set_defaults(func=cmd_publish)

    # toutiao
    p = subparsers.add_parser("toutiao", help="Publish to Toutiao")
    p.add_argument("subcommand", choices=["prepare", "publish"])
    p.add_argument("--input", help="Markdown file (for prepare)")
    p.add_argument("--output", default="./toutiao-prep", help="Output directory for prepare")
    p.add_argument("--images", "-i", default="", help="Images directory (for prepare)")
    p.add_argument("--title", help="Article title (for publish)")
    p.add_argument("--inject", help="Inject script path (for publish)")
    p.set_defaults(func=cmd_toutiao)

    # analytics
    p = subparsers.add_parser("analytics", help="Analyze post-publish data")
    p.add_argument("--csv", help="CSV data file path")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--output", "-o")
    p.set_defaults(func=cmd_analytics)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
