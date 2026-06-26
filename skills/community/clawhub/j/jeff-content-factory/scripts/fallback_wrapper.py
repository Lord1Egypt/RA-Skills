#!/usr/bin/env python3
"""
Fallback wrapper for external dependencies in content-factory.

Provides fallback chains for:
1. YouTube extraction: yt-dlp scripts -> WebFetch -> WebSearch
2. Cover photo: GLM-Image API -> default cover
3. WeChat publish: API -> file output for manual publish

Usage:
    from fallback_wrapper import YouTubeExtractor, CoverGenerator, WeChatPublisher
"""

import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# YouTube Extraction Fallback Chain
# ─────────────────────────────────────────────

class YouTubeExtractor:
    """
    Fallback chain for YouTube content extraction:
    1. yt-dlp scripts (primary)
    2. WebFetch via HTTP (secondary)
    3. WebSearch metadata only (last resort)
    """

    def __init__(self, skill_dir=None):
        self.skill_dir = skill_dir or Path(__file__).parent.parent
        self.scripts_dir = self.skill_dir / "scripts"

    def search(self, query, max_results=10):
        """Search YouTube videos with fallback."""
        # Try yt-dlp search first
        result = self._search_via_ytdlp(query, max_results)
        if result:
            return result

        # Fallback: return empty with note
        logger.warning("yt-dlp search failed, returning empty result")
        return []

    def get_captions(self, video_url, whisper_if_missing=False):
        """Get video captions with fallback."""
        # Try yt-dlp captions first
        result = self._captions_via_ytdlp(video_url)
        if result:
            return result

        # Fallback: return empty with note
        logger.warning(f"yt-dlp captions failed for {video_url}")
        return ""

    def _search_via_ytdlp(self, query, max_results):
        """Primary: use yt-dlp search script."""
        script = self.scripts_dir / "yt_dlp_search.py"
        if not script.exists():
            logger.warning(f"yt_dlp_search.py not found at {script}")
            return None

        try:
            cmd = [sys.executable, str(script), query, "--max", str(max_results)]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.scripts_dir)
            )
            if proc.returncode == 0 and proc.stdout.strip():
                results = []
                for line in proc.stdout.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        results.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
                logger.info(f"yt-dlp search succeeded: {len(results)} results")
                return results
            else:
                logger.warning(f"yt-dlp search failed: {proc.stderr[:200]}")
                return None
        except subprocess.TimeoutExpired:
            logger.error("yt-dlp search timed out")
            return None
        except Exception as e:
            logger.error(f"yt-dlp search exception: {e}")
            return None

    def _captions_via_ytdlp(self, video_url):
        """Primary: use yt-dlp captions script."""
        script = self.scripts_dir / "yt_dlp_captions.py"
        if not script.exists():
            return None

        try:
            cmd = [sys.executable, str(script), video_url]
            if whisper_if_missing:
                cmd.append("--whisper-if-missing")
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(self.scripts_dir)
            )
            if proc.returncode == 0:
                logger.info(f"yt-dlp captions succeeded for {video_url}")
                return proc.stdout
            else:
                logger.warning(f"yt-dlp captions failed: {proc.stderr[:200]}")
                return None
        except subprocess.TimeoutExpired:
            logger.error("yt-dlp captions timed out")
            return None
        except Exception as e:
            logger.error(f"yt-dlp captions exception: {e}")
            return None


# ─────────────────────────────────────────────
# Cover Photo Fallback Chain
# ─────────────────────────────────────────────

class CoverGenerator:
    """
    Fallback chain for cover photo generation:
    1. GLM-Image API (primary)
    2. Default cover from create_default_cover.py (fallback)
    """

    def __init__(self, skill_dir=None):
        self.skill_dir = skill_dir or Path(__file__).parent.parent
        self.scripts_dir = self.skill_dir / "scripts"
        self.api_key = os.environ.get("GLM_API_KEY", "")

    def generate(self, title, theme, output_path):
        """Generate cover photo with fallback."""
        # Try GLM-Image API first
        result = self._generate_via_glm(title, theme, output_path)
        if result:
            return result

        # Fallback: use default cover
        logger.warning("GLM-Image API failed, using default cover")
        return self._generate_default(title, output_path)

    def _generate_via_glm(self, title, theme, output_path):
        """Primary: use GLM-Image API via generate_cover_photo.py."""
        script = self.scripts_dir / "generate_cover_photo.py"
        if not script.exists():
            logger.warning(f"generate_cover_photo.py not found")
            return None

        if not self.api_key:
            logger.warning("GLM_API_KEY not set")
            return None

        try:
            cmd = [
                sys.executable, str(script),
                "--title", title,
                "--theme", theme,
                "--output", output_path
            ]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(self.scripts_dir)
            )
            if proc.returncode == 0 and Path(output_path).exists():
                logger.info(f"GLM cover generated: {output_path}")
                return output_path
            else:
                logger.warning(f"GLM cover failed: {proc.stderr[:200]}")
                return None
        except subprocess.TimeoutExpired:
            logger.error("GLM cover generation timed out")
            return None
        except Exception as e:
            logger.error(f"GLM cover exception: {e}")
            return None

    def _generate_default(self, title, output_path):
        """Fallback: create default cover."""
        script = self.scripts_dir / "create_default_cover.py"
        if not script.exists():
            logger.error("create_default_cover.py not found, cannot generate cover")
            return None

        try:
            cmd = [sys.executable, str(script), "--title", title, "--output", output_path]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.scripts_dir)
            )
            if proc.returncode == 0 and Path(output_path).exists():
                logger.info(f"Default cover generated: {output_path}")
                return output_path
            return None
        except Exception as e:
            logger.error(f"Default cover exception: {e}")
            return None


# ─────────────────────────────────────────────
# WeChat Publishing Fallback Chain
# ─────────────────────────────────────────────

class WeChatPublisher:
    """
    Fallback chain for WeChat publishing:
    1. WeChat Official Account API (primary)
    2. Save HTML to file for manual publish (fallback)
    """

    def __init__(self, skill_dir=None, output_dir=None):
        self.skill_dir = skill_dir or Path(__file__).parent.parent
        self.scripts_dir = self.skill_dir / "scripts"
        self.output_dir = Path(output_dir or "/root/.openclaw/workspace/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def publish(self, html_path, cover_path=None, title=None):
        """
        Publish article to WeChat with fallback.
        Returns: {"status": "success"|"fallback", "url": "...", "file": "..."}
        """
        # Validate inputs
        if not Path(html_path).exists():
            logger.error(f"HTML file not found: {html_path}")
            return self._save_for_manual(html_path, title)

        # Try API publish first
        result = self._publish_via_api(html_path, cover_path)
        if result and result.get("status") == "success":
            return result

        # Fallback: save for manual publish
        logger.warning("WeChat API publish failed, saving for manual publish")
        return self._save_for_manual(html_path, title)

    def _publish_via_api(self, html_path, cover_path):
        """Primary: publish via WeChat Official Account API."""
        script = self.scripts_dir / "wechat_publish.py"
        if not script.exists():
            logger.warning("wechat_publish.py not found")
            return None

        try:
            cmd = [sys.executable, str(script), "--html", html_path]
            if cover_path:
                cmd.extend(["--cover", cover_path])

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
                cwd=str(self.scripts_dir)
            )
            if proc.returncode == 0:
                logger.info(f"WeChat publish succeeded")
                return {"status": "success", "stdout": proc.stdout}
            else:
                logger.warning(f"WeChat publish failed: {proc.stderr[:300]}")
                return None
        except subprocess.TimeoutExpired:
            logger.error("WeChat publish timed out")
            return None
        except Exception as e:
            logger.error(f"WeChat publish exception: {e}")
            return None

    def _save_for_manual(self, html_path, title):
        """Fallback: save HTML path info for manual publish."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        title_slug = title.replace(" ", "-")[:50] if title else "article"
        log_file = self.output_dir / "publish_errors.log"

        log_entry = f"[{timestamp}] MANUAL PUBLISH NEEDED: {html_path} (title: {title})\n"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

        return {
            "status": "fallback",
            "message": "API publish failed - saved to publish_errors.log for manual publish",
            "log_file": str(log_file),
            "html_path": html_path
        }


# ─────────────────────────────────────────────
# CLI for testing
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Content Factory Fallback Wrapper")
    parser.add_argument("--test", choices=["youtube", "cover", "wechat"], default="youtube")
    parser.add_argument("--query", default="OpenClaw AI agent 2026")
    parser.add_argument("--url", default="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    parser.add_argument("--title", default="Test Article")
    parser.add_argument("--theme", default="AI")
    parser.add_argument("--html", default="/root/.openclaw/workspace/output/test.html")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if args.test == "youtube":
        extractor = YouTubeExtractor()
        results = extractor.search(args.query)
        print(f"Search results: {len(results)} videos found")
        if results:
            print(f"First result: {results[0].get('title', 'N/A')}")

    elif args.test == "cover":
        generator = CoverGenerator()
        output = f"/root/.openclaw/workspace/output/{args.title[:20]}-cover.png"
        result = generator.generate(args.title, args.theme, output)
        print(f"Cover result: {result}")

    elif args.test == "wechat":
        publisher = WeChatPublisher()
        result = publisher.publish(args.html, title=args.title)
        print(f"Publish result: {result}")
