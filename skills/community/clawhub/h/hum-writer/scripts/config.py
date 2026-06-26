#!/usr/bin/env python3
from __future__ import annotations
"""
Shared config loader for hum scripts.

Resolution order for data_dir:
  1. HUM_DATA_DIR env var
  2. openclaw.json → skills.entries.hum.config.hum_data_dir (if running inside OpenClaw)
  3. openclaw.json → skills.entries.hum.config.data_dir (legacy fallback)
  4. ~/Documents/hum (default)
"""
import json
import os
import re
from pathlib import Path

DEFAULT_DATA_DIR = Path.home() / "Documents" / "hum"


def _find_openclaw_json() -> Path | None:
    """Look for openclaw.json in parent directories and ~/.openclaw/."""
    # Walk up from script location (may be symlinked)
    candidate = Path(__file__).resolve().parent.parent
    for _ in range(6):
        candidate = candidate.parent
        oc = candidate / "openclaw.json"
        if oc.exists():
            return oc
    # Fallback: check ~/.openclaw/ directly
    home_oc = Path.home() / ".openclaw" / "openclaw.json"
    if home_oc.exists():
        return home_oc
    return None


def load_config() -> dict:
    """Load hum config with env var → openclaw.json → default fallback."""
    oc_path = _find_openclaw_json()
    oc_data = {}
    if oc_path:
        try:
            with open(oc_path) as f:
                oc_data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            pass

    # 1. Env var takes priority for data_dir
    env_dir = os.environ.get("HUM_DATA_DIR")
    if env_dir:
        data_dir = Path(os.path.expanduser(env_dir))
    else:
        # 2. Try openclaw.json (hum_data_dir preferred, data_dir for legacy compat)
        data_dir = DEFAULT_DATA_DIR
        hum_cfg = oc_data.get("skills", {}).get("entries", {}).get("hum", {}).get("config", {})
        raw = hum_cfg.get("hum_data_dir") or hum_cfg.get("data_dir")
        if raw:
            data_dir = Path(os.path.expanduser(raw))

    # Image model: env var → openclaw.json → default
    image_model = os.environ.get("HUM_IMAGE_MODEL")
    if not image_model:
        image_model = oc_data.get("skills", {}).get("entries", {}).get("hum", {}).get("config", {}).get("image_model")
    image_model = image_model or "gemini"

    # Digest delivery target: env var → openclaw.json → None
    hum_cfg = oc_data.get("skills", {}).get("entries", {}).get("hum", {}).get("config", {})
    digest_target = os.environ.get("HUM_DIGEST_TARGET") or hum_cfg.get("hum_digest_target") or None

    return {
        "data_dir": data_dir,
        "image_model": image_model,
        "digest_target": digest_target,
        "feed_dir": data_dir / "feed",
        "feeds_file": data_dir / "feed" / "feeds.json",
        "feed_raw": data_dir / "feed" / "raw",
        "feed_assets": data_dir / "feed" / "assets",
        "sources_file": data_dir / "feed" / "sources.json",
        "knowledge_dir": data_dir / "knowledge",
        "content_samples_dir": data_dir / "content-samples",
        "ideas_dir": data_dir / "ideas",
        "content_dir": data_dir / "content",
        "content_drafts_dir": data_dir / "content" / "drafts",
        "content_published_dir": data_dir / "content" / "published",
        "content_images_dir": data_dir / "content" / "images",
        "loop_dir": data_dir / "loop",
    }


def load_visual_style(data_dir: Path | None = None) -> str | None:
    """Parse VOICE.md for the '## Visual Style' section.

    Returns the section content as a string, or None if absent/empty.
    """
    if data_dir is None:
        data_dir = load_config()["data_dir"]

    voice_md = data_dir / "VOICE.md"
    if not voice_md.exists():
        return None

    lines: list[str] = []
    in_section = False

    with voice_md.open(encoding="utf-8") as f:
        for line in f:
            stripped = line.rstrip("\n")
            if re.match(r"^##\s+Visual Style", stripped):
                in_section = True
                continue
            if in_section:
                if re.match(r"^##\s+", stripped):
                    break
                lines.append(stripped)

    text = "\n".join(lines).strip()
    # Strip HTML comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()
    return text or None


def load_topics(data_dir: Path | None = None) -> dict[str, list[str]]:
    """Parse CONTENT.md into {pillar_name: [keywords]}.

    Falls back to feed/assets/topics.json if CONTENT.md has no pillars.
    """
    if data_dir is None:
        data_dir = load_config()["data_dir"]

    content_md = data_dir / "CONTENT.md"
    topics: dict[str, list[str]] = {}

    if content_md.exists():
        current_pillar = None
        with content_md.open(encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                # H2 heading = pillar name (skip template placeholders)
                h2 = re.match(r"^##\s+(.+)$", line)
                if h2:
                    name = h2.group(1).strip()
                    if name.startswith("[") or name.lower() == "example pillar":
                        current_pillar = None
                        continue
                    current_pillar = name
                    topics[current_pillar] = []
                    continue
                # Keywords line under a pillar
                kw_match = re.match(r"^Keywords:\s*(.+)$", line, re.IGNORECASE)
                if kw_match and current_pillar:
                    raw = kw_match.group(1).strip()
                    keywords = [k.strip().lower() for k in raw.split(",") if k.strip()]
                    topics[current_pillar] = keywords

    # Fallback: load from cached topics.json
    if not topics:
        topics_json = data_dir / "feed" / "assets" / "topics.json"
        if topics_json.exists():
            with topics_json.open() as f:
                topics = json.load(f)

    return topics


def load_x_credentials() -> dict[str, str | None]:
    """Load X/Twitter session credentials for Bird-based scraping.

    Priority order:
      1. HUM_X_AUTH_TOKEN / HUM_X_CT0 env vars
      2. ~/.hum/credentials/x.json → "auth_token" / "ct0"
      3. AUTH_TOKEN / CT0 env vars (shared with last30days)

    Returns dict with keys: auth_token, ct0 (either may be None).
    """
    auth_token = os.environ.get("HUM_X_AUTH_TOKEN")
    ct0 = os.environ.get("HUM_X_CT0")

    if not (auth_token and ct0):
        creds_file = Path.home() / ".hum" / "credentials" / "x.json"
        if creds_file.exists():
            try:
                with open(creds_file) as f:
                    data = json.load(f)
                auth_token = auth_token or data.get("auth_token")
                ct0 = ct0 or data.get("ct0")
            except (json.JSONDecodeError, OSError):
                pass

    if not (auth_token and ct0):
        auth_token = auth_token or os.environ.get("AUTH_TOKEN")
        ct0 = ct0 or os.environ.get("CT0")

    return {"auth_token": auth_token, "ct0": ct0}


if __name__ == "__main__":
    cfg = load_config()
    for k, v in cfg.items():
        if isinstance(v, Path):
            exists = "✓" if v.exists() else "✗"
            print(f"  {exists} {k}: {v}")
        else:
            val = f"{v[:4]}..." if isinstance(v, str) and len(v) > 8 else v
            print(f"    {k}: {val}")

    topics = load_topics(cfg["data_dir"])
    print(f"\n  Topics ({len(topics)} pillars):")
    for name, kws in topics.items():
        print(f"    {name}: {', '.join(kws[:5])}{'...' if len(kws) > 5 else ''}")
