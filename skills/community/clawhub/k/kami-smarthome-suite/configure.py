#!/usr/bin/env python3
"""
Kami SmartHome Suite - Centralized Configuration Distributor
=============================================================

Reads kami_config.json (the single source of truth) and distributes settings
to each skill's local config file. Also caches credentials to ~/.kami/ for
env-based skills.

Usage:
  python3 configure.py                                # interactive (fills kami_config.json then distributes)
  python3 configure.py --distribute                   # distribute existing kami_config.json to all skills
  python3 configure.py --api-key sk_xxx               # set API key and distribute
  python3 configure.py --add-camera rtsp://...           # add a camera with auto-assigned name (cam1/cam2/...)
  python3 configure.py --add-camera front=rtsp://...     # add/update a camera with explicit name
  python3 configure.py --remove-camera front             # remove a camera by name (repeatable)
  python3 configure.py --show                         # show current centralized config

Exit codes:
  0  success
  1  partial failure (some configs could not be updated)
  2  no API key available / config missing
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import quote

# ---------------------------------------------------------------------------
# Included-skills capability summary
#
# Printed to stdout after every successful distribution so the user (and
# the calling agent) immediately see what skills are now usable. The text
# mirrors the Included Skills table in SKILL.md and MUST stay in sync.
# ---------------------------------------------------------------------------

SKILL_SUMMARY: List[tuple] = [
    ("kami-package-detection",  "\U0001f4e6",
     "Continuous package/parcel monitoring on RTSP streams (YOLO-World ONNX) with smart notification",
     "Doorstep delivery alerts"),
    ("kami-image-search",       "\U0001f50d",
     "Periodic frame capture + VLM captioning + FAISS index for natural-language image search",
     "Search historical frames"),
    ("kami-video-search",       "\U0001f4f9",
     "Continuous video segmentation + VLM scene description + natural-language clip search",
     "Search historical clips"),
    ("kami-fall-detection",     "\U0001f6a8",
     "Frame-difference detection + KamiClaw cloud inference for fall events",
     "Elder / lone-resident care"),
    ("kami-conflict-detection", "\U0001f94a",
     "Multi-person physical conflict (fight/shove) detection with event-driven alarm JSON",
     "Security alerting"),
    ("kami-suspicious-person",  "\U0001f575\ufe0f",
     "Stranger recognition via SCRFD + ArcFace, detects unregistered face loitering",
     "Doorway / stranger-loiter alerts"),
]


def print_skill_summary() -> None:
    """Print the Included Skills capability table to stdout.

    Called after a successful --distribute so the user always sees what is
    now available. SKILL.md mandates the calling agent relay this verbatim.
    """
    bar = "=" * 72
    print()
    print(bar)
    print("  Kami SmartHome Suite \u2014 Installed Skills (ready to use)")
    print(bar)
    for slug, emoji, desc, use_case in SKILL_SUMMARY:
        print(f"  {emoji}  {slug}")
        print(f"      {desc}")
        print(f"      Use case: {use_case}")
    print(bar)
    print("  Tip: ask the agent things like 'detect packages at the front door'")
    print("       or 'search recent frames for a red car' to trigger a skill.")
    print(bar)
    print()

# ---------------------------------------------------------------------------
# Common-brand RTSP URL templates
#
# Each entry maps a short brand key to:
#   - label   : human-readable name (shown in menus)
#   - url     : RTSP URL pattern with named placeholders
#   - defaults: default value for each placeholder (Enter = keep)
#   - fields  : ordered list of (placeholder, prompt) used by the wizard
#
# The wizard URL-encodes `user` and `password` automatically so that special
# characters (e.g. '@' / ':' / '#') do not break the URL.
# ---------------------------------------------------------------------------

RTSP_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "hikvision": {
        "label": "Hikvision",
        "url": "rtsp://{user}:{password}@{ip}:{port}/Streaming/Channels/{channel_code}",
        "defaults": {"port": "554", "channel_code": "101"},
        "fields": [
            ("ip", "Camera IP"),
            ("user", "Username"),
            ("password", "Password"),
            ("port", "Port [554]"),
            ("channel_code", "Channel code (101=ch1 main, 102=ch1 sub) [101]"),
        ],
    },
    "dahua": {
        "label": "Dahua",
        "url": "rtsp://{user}:{password}@{ip}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}",
        "defaults": {"port": "554", "channel": "1", "subtype": "0"},
        "fields": [
            ("ip", "Camera IP"),
            ("user", "Username"),
            ("password", "Password"),
            ("port", "Port [554]"),
            ("channel", "Channel [1]"),
            ("subtype", "Subtype (0=main, 1=sub) [0]"),
        ],
    },
    "tplink": {
        "label": "TP-Link",
        "url": "rtsp://{user}:{password}@{ip}:{port}/stream{stream}",
        "defaults": {"port": "554", "stream": "1"},
        "fields": [
            ("ip", "Camera IP"),
            ("user", "Username"),
            ("password", "Password"),
            ("port", "Port [554]"),
            ("stream", "Stream (1=main, 2=sub) [1]"),
        ],
    },
    "ezviz": {
        "label": "EZVIZ",
        "url": "rtsp://{user}:{password}@{ip}:{port}/H264/ch{channel}/{stream}/av_stream",
        "defaults": {"port": "554", "channel": "1", "stream": "main"},
        "fields": [
            ("ip", "Camera IP"),
            ("user", "Username (usually 'admin')"),
            ("password", "Verification code from device label"),
            ("port", "Port [554]"),
            ("channel", "Channel [1]"),
            ("stream", "Stream (main/sub) [main]"),
        ],
    },
    "uniview": {
        "label": "Uniview",
        "url": "rtsp://{user}:{password}@{ip}:{port}/media/video{stream}",
        "defaults": {"port": "554", "stream": "1"},
        "fields": [
            ("ip", "Camera IP"),
            ("user", "Username"),
            ("password", "Password"),
            ("port", "Port [554]"),
            ("stream", "Stream (1=main, 2=sub) [1]"),
        ],
    },
    "reolink": {
        "label": "Reolink",
        "url": "rtsp://{user}:{password}@{ip}:{port}/h264Preview_01_{stream}",
        "defaults": {"port": "554", "stream": "main"},
        "fields": [
            ("ip", "Camera IP"),
            ("user", "Username"),
            ("password", "Password"),
            ("port", "Port [554]"),
            ("stream", "Stream (main/sub) [main]"),
        ],
    },
}


def list_rtsp_templates() -> None:
    """Print all known brand templates with their URL pattern."""
    print("Common brand RTSP templates:")
    print("-" * 60)
    for key, tpl in RTSP_TEMPLATES.items():
        print(f"  [{key:9s}] {tpl['label']}")
        print(f"             {tpl['url']}")
    print()
    print("Use them in the interactive wizard ([t]emplate action) or")
    print("render manually and pass via --add-camera NAME=<rendered_url>.")


def build_rtsp_from_template(brand_key: str) -> str:
    """Prompt the user for placeholder values of a brand template and return
    the rendered RTSP URL. Returns empty string on incomplete input."""
    tpl = RTSP_TEMPLATES.get(brand_key)
    if not tpl:
        warn(f"Unknown brand: {brand_key}")
        return ""
    print(f"    Template: {tpl['label']}")
    print(f"    Pattern : {tpl['url']}")
    values: Dict[str, str] = dict(tpl.get("defaults", {}))
    for fkey, prompt in tpl["fields"]:
        v = input(f"    {prompt}: ").strip()
        if v:
            values[fkey] = v
    # Required fields: ip, user, password (all templates share these)
    for required in ("ip", "user", "password"):
        if not values.get(required):
            warn(f"Missing required field '{required}', aborting template.")
            return ""
    # URL-encode credentials so special chars (@ : # / etc.) survive.
    safe_values = dict(values)
    safe_values["user"] = quote(values["user"], safe="")
    safe_values["password"] = quote(values["password"], safe="")
    try:
        return tpl["url"].format(**safe_values)
    except KeyError as exc:
        warn(f"Template missing field: {exc}")
        return ""

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SUITE_DIR = Path(__file__).resolve().parent
SKILLS_ROOT = SUITE_DIR.parent
CONFIG_FILE = SUITE_DIR / "kami_config.json"

CRED_DIR = Path.home() / ".kami"
CRED_FILE = CRED_DIR / "credentials.json"
CAMERAS_FILE = CRED_DIR / "cameras.json"

# ---------------------------------------------------------------------------
# Skill config mapping
# Maps: (skill_slug, local_config_file, field_mappings)
# field_mappings: list of (central_path, local_field_name)
# ---------------------------------------------------------------------------

SKILL_CONFIGS: List[Dict[str, Any]] = [
    {
        "slug": "kami-image-search",
        "config_file": "image_config.json",
        "multi_camera": True,
        # Per-camera fields written into each cameras[] entry.
        "camera_fields": [
            ("stream_url", "STREAM_URL"),
            ("device_id", "DEVICE_ID"),
        ],
        # Global fields written at top level.
        "mappings": [
            ("kamiclaw_api_key", "KAMIVISION_API_KEY"),
            ("skills.kami-image-search.capture_interval", "CAPTURE_INTERVAL"),
            ("skills.kami-image-search.retention_days", "RETENTION_DAYS"),
        ],
    },
    {
        "slug": "kami-video-search",
        "config_file": "stream_config.json",
        "multi_camera": True,
        # Per-camera fields written into each cameras[] entry.
        "camera_fields": [
            ("stream_url", "STREAM_URL"),
            ("device_id", "DEVICE_ID"),
        ],
        # Global fields written at top level.
        "mappings": [
            ("kamiclaw_api_key", "KAMI_API_KEY"),
            ("skills.kami-video-search.segment_duration", "SEGMENT_DURATION"),
            ("skills.kami-video-search.retention_days", "RETENTION_DAYS"),
        ],
    },
    {
        "slug": "kami-fall-detection",
        "config_file": "config.json",
        "multi_camera": True,
        # Per-camera fields written into each cameras[] entry.
        "camera_fields": [
            ("stream_url", "rtsp_url"),
            ("device_id", "name"),
        ],
        # Global fields written at top level.
        "mappings": [
            ("kamiclaw_api_key", "api_key"),
            # Notifications: fall-detection supports Feishu / Telegram / Discord (webhook + bot)
            ("notifications.feishu_webhook_url", "feishu_webhook_url"),
            ("notifications.feishu_app_id", "feishu_app_id"),
            ("notifications.feishu_app_secret", "feishu_app_secret"),
            ("notifications.telegram_bot_token", "telegram_bot_token"),
            ("notifications.telegram_chat_id", "telegram_chat_id"),
            ("notifications.discord_webhook_url", "discord_webhook_url"),
            ("notifications.discord_bot_token", "discord_bot_token"),
            ("notifications.discord_channel_id", "discord_channel_id"),
            ("skills.kami-fall-detection.pre_seconds", "pre_seconds"),
            ("skills.kami-fall-detection.post_seconds", "post_seconds"),
            ("skills.kami-fall-detection.save_alarm_clips", "save_alarm_clips"),
        ],
    },
    {
        "slug": "kami-package-detection",
        "config_file": "config.json",
        "multi_camera": True,
        # Per-camera fields written into each cameras[] entry.
        "camera_fields": [
            ("stream_url", "rtsp_url"),
            ("device_id", "device_id"),
        ],
        # Global fields written at top level.
        # Pure local inference: no API key. Supports Feishu / Telegram / Discord notifications.
        # class_names is intentionally NOT distributed (kept as per-skill default).
        "mappings": [
            ("skills.kami-package-detection.conf_threshold", "conf_threshold"),
            ("skills.kami-package-detection.run_time", "run_time"),
            ("skills.kami-package-detection.alarm_cooldown", "alarm_cooldown"),
            # Notifications: package-detection supports Feishu / Telegram / Discord (webhook)
            ("notifications.feishu_webhook_url", "feishu_webhook_url"),
            ("notifications.feishu_app_id", "feishu_app_id"),
            ("notifications.feishu_app_secret", "feishu_app_secret"),
            ("notifications.telegram_bot_token", "telegram_bot_token"),
            ("notifications.telegram_chat_id", "telegram_chat_id"),
            ("notifications.discord_webhook_url", "discord_webhook_url"),
            ("notifications.discord_bot_token", "discord_bot_token"),
            ("notifications.discord_channel_id", "discord_channel_id"),
        ],
    },
    {
        "slug": "kami-conflict-detection",
        "config_file": "config.json",
        "multi_camera": True,
        # Per-camera fields written into each cameras[] entry.
        "camera_fields": [
            ("stream_url", "rtsp_url"),
            ("device_id", "name"),
        ],
        # Global fields written at top level.
        "mappings": [
            # Local YOLO + cloud conflict analysis. Reads credentials from config.json
            # (preferred) or env vars / CLI as fallback. Note: skill uses short field
            # names `feishu_webhook` / `discord_webhook` (no `_url` suffix).
            ("kamiclaw_api_key", "kami_api_key"),
            ("notifications.feishu_webhook_url", "feishu_webhook"),
            ("notifications.feishu_app_id", "feishu_app_id"),
            ("notifications.feishu_app_secret", "feishu_app_secret"),
            ("notifications.telegram_bot_token", "telegram_bot_token"),
            ("notifications.telegram_chat_id", "telegram_chat_id"),
            ("notifications.discord_webhook_url", "discord_webhook"),
        ],
    },
    {
        "slug": "kami-suspicious-person",
        "config_file": "config.json",
        "multi_camera": True,
        # Per-camera fields written into each cameras[] entry.
        "camera_fields": [
            ("stream_url", "rtsp_url"),
            ("device_id", "name"),
        ],
        # Global fields written at top level.
        "mappings": [
            # Pure local inference (SCRFD + ArcFace). No API key needed; only camera
            # URL + push channels are distributed. Field names match the skill's
            # argparse: `feishu_webhook` / `discord_webhook` (no `_url` suffix).
            ("notifications.feishu_webhook_url", "feishu_webhook"),
            ("notifications.feishu_app_id", "feishu_app_id"),
            ("notifications.feishu_app_secret", "feishu_app_secret"),
            ("notifications.telegram_bot_token", "telegram_bot_token"),
            ("notifications.telegram_chat_id", "telegram_chat_id"),
            ("notifications.discord_webhook_url", "discord_webhook"),
        ],
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def info(msg: str) -> None:
    print(f"[i] {msg}")

def ok(msg: str) -> None:
    print(f"[\u2713] {msg}")

def warn(msg: str) -> None:
    print(f"[!] {msg}")

def err(msg: str) -> None:
    print(f"[\u2717] {msg}", file=sys.stderr)


def load_central_config() -> Dict[str, Any]:
    if not CONFIG_FILE.is_file():
        warn(f"Central config not found: {CONFIG_FILE}")
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        err(f"Failed to parse {CONFIG_FILE}: {exc}")
        return {}


def save_central_config(config: Dict[str, Any]) -> None:
    CONFIG_FILE.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    ok(f"Central config saved: {CONFIG_FILE}")


def resolve_path(config: Dict[str, Any], path: str, skill_cfg: Dict[str, Any] = None,
                 override_camera: str = None) -> Any:
    """Resolve a dotted path like 'cameras.{camera}.stream_url' from config.

    override_camera: when set, replaces {camera} placeholder regardless of skill_cfg.
    """
    # Replace {camera} placeholder
    if "{camera}" in path:
        camera_name = override_camera
        if camera_name is None and skill_cfg:
            skill_settings = config.get("skills", {}).get(skill_cfg.get("slug", ""), {})
            # New format: cameras list (use first); legacy: camera string
            cams_list = skill_settings.get("cameras")
            if cams_list:
                camera_name = cams_list[0]
            elif cams_list == [] or cams_list is None:
                camera_name = skill_settings.get("camera", "default")
        if camera_name is None:
            camera_name = "default"
        path = path.replace("{camera}", camera_name)

    parts = path.split(".")
    current = config
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
        if current is None:
            # Special-case: legacy mapping `cameras.<name>.device_id` falls back
            # to <name> itself when the field is absent.
            if (len(parts) == 3 and parts[0] == "cameras"
                    and parts[2] == "device_id"
                    and parts[1] in config.get("cameras", {})):
                return parts[1]
            return None
    return current


def _auto_camera_name(cams_dict: Dict[str, Any]) -> str:
    """Return the smallest cam<N> name not yet used in cams_dict."""
    if not isinstance(cams_dict, dict):
        return "cam1"
    i = 1
    while f"cam{i}" in cams_dict:
        i += 1
    return f"cam{i}"


def _camera_with_default_id(name: str, c: Any) -> Dict[str, Any]:
    """Return a shallow copy of camera dict with device_id forced to the dict key.

    The suite treats the dict key as the canonical camera identifier (the user-
    facing "name"). To keep alarm messages and logs human-readable, we ALWAYS
    overwrite any inner `device_id` field with the dict key, so the value users
    see in notifications matches what they typed in `kami_config.json`.
    """
    if not isinstance(c, dict):
        return {"device_id": name}
    out = dict(c)
    out["device_id"] = name
    return out


def select_cameras_for_skill(config: Dict[str, Any], slug: str) -> List[tuple]:
    """Return ordered list of (name, camera_dict) tuples for a skill.

    Resolution rules:
    - skills.{slug}.cameras = []      -> all cameras with non-empty stream_url
    - skills.{slug}.cameras = [a, b]  -> only listed names (preserving order)
    - skills.{slug}.camera = "name"   -> legacy single-camera fallback
    - none of the above               -> ["default"] if present

    The returned camera dict always has a `device_id` field, defaulting to the
    dict key when not explicitly set in kami_config.json.
    """
    skill_cfg = config.get("skills", {}).get(slug, {})
    all_cams = config.get("cameras", {})
    if not isinstance(all_cams, dict):
        return []

    selected = skill_cfg.get("cameras")
    if isinstance(selected, list):
        if not selected:
            return [(n, _camera_with_default_id(n, all_cams[n]))
                    for n in all_cams
                    if isinstance(all_cams.get(n), dict)
                    and all_cams[n].get("stream_url")]
        return [(n, _camera_with_default_id(n, all_cams[n]))
                for n in selected
                if n in all_cams and isinstance(all_cams[n], dict)]

    legacy = skill_cfg.get("camera")
    if legacy and legacy in all_cams:
        return [(legacy, _camera_with_default_id(legacy, all_cams[legacy]))]

    if "default" in all_cams:
        return [("default", _camera_with_default_id("default", all_cams["default"]))]
    return []


def _merge_cameras_array(existing: list, incoming: list) -> tuple:
    """Merge incoming cameras list into existing by device_id (case-insensitive lookup
    over both 'device_id' and 'DEVICE_ID' keys).

    For each incoming entry:
    - If a matching device_id exists, update overlapping keys; preserve other keys.
    - Otherwise, append.
    Existing entries with no match in incoming are preserved as-is.

    Returns (merged_list, changed_bool).
    """
    def _dev_id(entry):
        if not isinstance(entry, dict):
            return None
        return entry.get("device_id") or entry.get("DEVICE_ID")

    if not isinstance(existing, list):
        existing = []
    merged = [dict(e) if isinstance(e, dict) else e for e in existing]
    changed = False

    for inc in incoming:
        if not isinstance(inc, dict):
            continue
        inc_id = _dev_id(inc)
        target_idx = None
        if inc_id:
            for i, e in enumerate(merged):
                if _dev_id(e) == inc_id:
                    target_idx = i
                    break
        if target_idx is not None:
            for k, v in inc.items():
                if merged[target_idx].get(k) != v:
                    merged[target_idx][k] = v
                    changed = True
        else:
            merged.append(dict(inc))
            changed = True

    return merged, changed


def patch_json_file(path: Path, updates: Dict[str, Any]) -> bool:
    """Update multiple fields in a JSON config file.

    Special handling for `cameras` field: completely REPLACE the array from central
    config (Single Source of Truth), rather than merging. This prevents duplicate
    cameras when running --distribute multiple times.
    """
    try:
        if not path.is_file():
            warn(f"Skip (not found): {path}")
            return False
        original = path.read_text(encoding="utf-8")
        data = json.loads(original) if original.strip() else {}
        if not isinstance(data, dict):
            err(f"Top-level is not object: {path}")
            return False

        changed = False
        for field, value in updates.items():
            if value is None or value == "":
                continue
            if field == "cameras" and isinstance(value, list):
                # REPLACE cameras array entirely (Single Source of Truth)
                # Do not merge — this prevents duplicates on repeated --distribute
                if data.get("cameras") != value:
                    data["cameras"] = value
                    changed = True
                continue
            if data.get(field) != value:
                data[field] = value
                changed = True

        if changed:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
            ok(f"{path.relative_to(SKILLS_ROOT)} updated")
        else:
            ok(f"{path.relative_to(SKILLS_ROOT)} already up-to-date")
        return True
    except Exception as exc:
        err(f"Failed to patch {path}: {exc}")
        return False


def save_credentials(api_key: str) -> None:
    """Cache API key to ~/.kami/credentials.json."""
    try:
        CRED_DIR.mkdir(parents=True, exist_ok=True)
        data = {}
        if CRED_FILE.is_file():
            try:
                data = json.loads(CRED_FILE.read_text(encoding="utf-8")) or {}
            except Exception:
                data = {}
        data["kamiclaw_api_key"] = api_key
        CRED_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        try:
            os.chmod(CRED_FILE, 0o600)
        except Exception:
            pass
        ok(f"Credentials cached: {CRED_FILE}")
    except Exception as exc:
        warn(f"Could not cache credentials: {exc}")


def save_cameras(cameras: Dict[str, Any]) -> None:
    """Cache cameras to ~/.kami/cameras.json so any skill can read them."""
    try:
        CRED_DIR.mkdir(parents=True, exist_ok=True)
        CAMERAS_FILE.write_text(
            json.dumps(cameras, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        try:
            os.chmod(CAMERAS_FILE, 0o600)
        except Exception:
            pass
        ok(f"Cameras cached: {CAMERAS_FILE}")
    except Exception as exc:
        warn(f"Could not cache cameras: {exc}")


# ---------------------------------------------------------------------------
# Distribution logic
# ---------------------------------------------------------------------------

def distribute(config: Dict[str, Any]) -> int:
    """Distribute centralized config to all skill local configs. Returns failure count."""
    api_key = config.get("kamiclaw_api_key", "")
    failed = 0

    for skill_cfg in SKILL_CONFIGS:
        slug = skill_cfg["slug"]
        cfg_file = skill_cfg["config_file"]
        cfg_path = SKILLS_ROOT / slug / cfg_file

        if not cfg_path.is_file():
            warn(f"Skip {slug} (not installed)")
            continue

        cams = select_cameras_for_skill(config, slug)
        updates: Dict[str, Any] = {}

        if skill_cfg.get("multi_camera"):
            # Build cameras: [...] array from per-camera fields
            cam_entries = []
            for _, c in cams:
                entry = {}
                for src, dst in skill_cfg.get("camera_fields", []):
                    val = c.get(src)
                    if val not in (None, ""):
                        entry[dst] = val
                if entry:
                    cam_entries.append(entry)
            if cam_entries:
                updates["cameras"] = cam_entries
            # Global mappings (no {camera} placeholder expected)
            for path, field in skill_cfg.get("mappings", []):
                v = resolve_path(config, path)
                if v not in (None, ""):
                    updates[field] = v
        else:
            # Legacy single-camera skill: take FIRST selected camera
            first_name = cams[0][0] if cams else None
            if len(cams) > 1:
                others = [n for n, _ in cams[1:]]
                warn(f"{slug}: only supports single camera, using '{first_name}' "
                     f"(others ignored: {others})")
            for path, field in skill_cfg.get("mappings", []):
                v = resolve_path(config, path, skill_cfg, override_camera=first_name)
                if v not in (None, ""):
                    updates[field] = v

        if updates:
            if not patch_json_file(cfg_path, updates):
                failed += 1
        else:
            info(f"{slug}: nothing to distribute (config values empty)")

    # Cache API key and cameras to ~/.kami/ so any skill can reuse them.
    if api_key:
        save_credentials(api_key)

    cams = config.get("cameras", {})
    if isinstance(cams, dict) and cams:
        save_cameras(cams)

    return failed


# ---------------------------------------------------------------------------
# Interactive setup
# ---------------------------------------------------------------------------

def interactive_setup() -> Dict[str, Any]:
    """Guide user through filling kami_config.json interactively."""
    config = load_central_config()
    if not config:
        config = {}

    print()
    print("=" * 60)
    print("  🏠 Kami SmartHome Suite - Configuration")
    print("=" * 60)
    print()

    # API Key
    current_key = config.get("kamiclaw_api_key", "")
    if current_key:
        masked = current_key[:8] + "..." + current_key[-4:] if len(current_key) > 12 else "***"
        print(f"  Current API Key: {masked}")
        inp = input("  Enter new key (or press Enter to keep): ").strip()
        if inp:
            config["kamiclaw_api_key"] = inp
    else:
        print("  KamiClaw API Key is required for 4 out of 6 skills.")
        print("  Register at: https://kamiclaw-skill.kamihome.com (free 200 credits)")
        print()
        inp = input("  Enter your KamiClaw API Key (or press Enter to skip): ").strip()
        if inp:
            config["kamiclaw_api_key"] = inp

    # Cameras (multi-camera management)
    print()
    print("  --- Cameras ---")
    print("  image-search and package-detection run all cameras in parallel.")
    print("  Other skills (fall / video-search / conflict / suspicious) use the FIRST camera only.")
    cams_dict = config.setdefault("cameras", {})
    if not isinstance(cams_dict, dict):
        cams_dict = {}
        config["cameras"] = cams_dict

    while True:
        # Show current cameras
        if cams_dict:
            print("  Current cameras:")
            for name, c in cams_dict.items():
                if isinstance(c, dict):
                    url = c.get("stream_url", "") or "<empty>"
                    print(f"    [{name}] {url}")
        else:
            print("  No cameras configured yet.")

        print("  Actions: [a]dd  [t]emplate-add  [d]elete  [e]dit  [Enter] done")
        action = input("  Choice: ").strip().lower()
        if not action:
            break
        if action == "a":
            name = input("    Camera name (press Enter to auto-assign, e.g., front, back, garage): ").strip()
            if not name:
                name = _auto_camera_name(cams_dict)
                print(f"    Auto-assigned name: '{name}'")
            if name in cams_dict:
                print(f"    Camera '{name}' already exists, use [e] to edit.")
                continue
            url = input("    RTSP URL: ").strip()
            cams_dict[name] = {"stream_url": url, "device_id": name}
        elif action == "t":
            print("    Available brand templates:")
            keys = list(RTSP_TEMPLATES.keys())
            for i, k in enumerate(keys, 1):
                print(f"      {i}. {k:9s} {RTSP_TEMPLATES[k]['label']}")
            sel = input("    Pick a number or brand key: ").strip().lower()
            brand = None
            if sel.isdigit() and 1 <= int(sel) <= len(keys):
                brand = keys[int(sel) - 1]
            elif sel in RTSP_TEMPLATES:
                brand = sel
            if not brand:
                print("    Unknown selection, aborting template.")
                continue
            url = build_rtsp_from_template(brand)
            if not url:
                continue
            print(f"    Built URL: {url}")
            name = input("    Camera name (Enter to auto-assign): ").strip()
            if not name:
                name = _auto_camera_name(cams_dict)
                print(f"    Auto-assigned name: '{name}'")
            if name in cams_dict:
                print(f"    Camera '{name}' already exists, use [e] to edit.")
                continue
            cams_dict[name] = {"stream_url": url, "device_id": name}
        elif action == "d":
            name = input("    Camera name to delete: ").strip()
            if name in cams_dict:
                del cams_dict[name]
                print(f"    Deleted '{name}'.")
            else:
                print(f"    Not found: '{name}'.")
        elif action == "e":
            name = input("    Camera name to edit: ").strip()
            if name not in cams_dict:
                print(f"    Not found: '{name}'.")
                continue
            entry = cams_dict[name]
            cur_url = entry.get("stream_url", "")
            new_url = input(f"    RTSP URL [{cur_url or '<empty>'}]: ").strip()
            if new_url:
                entry["stream_url"] = new_url
            # Keep device_id in sync with name (rename = delete + add)
            entry["device_id"] = name
        else:
            print("    Unknown action.")

    # Notification channels (all optional, any combination)
    print()
    print("  --- Notification Channels (all optional) ---")
    print("  Alarm skills (fall / package / conflict / suspicious-person) can push via:")
    print("    - Feishu Webhook  (all 4 alarm skills)")
    print("    - Telegram Bot    (all 4 alarm skills)")
    print("    - Discord Webhook (all 4 alarm skills)")
    print("    - Discord Bot     (fall-detection & package-detection, two-way)")
    print("  Press Enter to skip any channel you don't need.")
    notif = config.setdefault("notifications", {})

    # Feishu
    current_webhook = notif.get("feishu_webhook_url", "")
    if current_webhook:
        print(f"  Current Feishu webhook: {current_webhook[:40]}...")
    inp = input("  Feishu webhook URL (Enter to skip): ").strip()
    if inp:
        notif["feishu_webhook_url"] = inp
        inp2 = input("  Feishu webhook secret (Enter if not signed): ").strip()
        if inp2:
            notif["feishu_webhook_secret"] = inp2
        # Self-built app credentials (optional, enables inline snapshot rendering
        # inside the Feishu card via OpenAPI image_key upload). Used by all
        # 4 alarm skills (fall / package / conflict / suspicious-person).
        # Without them, the snapshot falls back to a clickable image-host URL.
        print("  --- Optional: Feishu self-built app for inline snapshot images ---")
        print("  Provide app_id + app_secret to render alarm snapshots INSIDE the card.")
        print("  Without them, snapshots are pushed as clickable URLs.")
        inp3 = input("  Feishu app_id (Enter to skip): ").strip()
        if inp3:
            notif["feishu_app_id"] = inp3
            inp4 = input("  Feishu app_secret: ").strip()
            if inp4:
                notif["feishu_app_secret"] = inp4

    # Telegram
    current_tg = notif.get("telegram_bot_token", "")
    if current_tg:
        print(f"  Current Telegram bot token: {current_tg[:8]}...")
    inp = input("  Telegram bot token (Enter to skip): ").strip()
    if inp:
        notif["telegram_bot_token"] = inp
        inp2 = input("  Telegram chat ID: ").strip()
        if inp2:
            notif["telegram_chat_id"] = inp2

    # Discord
    current_dc = notif.get("discord_webhook_url", "")
    if current_dc:
        print(f"  Current Discord webhook: {current_dc[:40]}...")
    inp = input("  Discord webhook URL (push-only, Enter to skip): ").strip()
    if inp:
        notif["discord_webhook_url"] = inp
    # Discord Bot (fall-detection only)
    inp = input("  Discord bot token for fall-detection two-way (Enter to skip): ").strip()
    if inp:
        notif["discord_bot_token"] = inp
        inp2 = input("  Discord channel ID: ").strip()
        if inp2:
            notif["discord_channel_id"] = inp2

    # Proxy reminder (NOT managed by suite)
    print()
    print("  \u2139\ufe0f  Note: To access Discord / Telegram from mainland China,")
    print("     set HTTPS_PROXY in your shell rc (e.g. ~/.bashrc) yourself.")
    print("     Suite intentionally does NOT manage proxy configuration.")

    # Save
    save_central_config(config)
    return config


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Kami SmartHome Suite - Centralized config distributor."
    )
    parser.add_argument("--api-key", default="",
                        help="Set API key in kami_config.json and distribute.")
    parser.add_argument("--stream-url", default="",
                        help="Set default camera URL and distribute.")
    parser.add_argument("--add-camera", action="append", default=[],
                        metavar="[NAME=]URL",
                        help="Add or update a camera. NAME is optional (auto-assigned as cam1/cam2/...). Repeatable.")
    parser.add_argument("--remove-camera", action="append", default=[],
                        metavar="NAME",
                        help="Remove a camera by name. Repeatable.")
    parser.add_argument("--distribute", action="store_true",
                        help="Distribute existing kami_config.json to all skills.")
    parser.add_argument("--show", action="store_true",
                        help="Show current centralized config and exit.")
    parser.add_argument("--list-templates", action="store_true",
                        help="Print common-brand RTSP URL templates and exit.")
    parser.add_argument("--no-prompt", action="store_true",
                        help="Non-interactive mode.")
    args = parser.parse_args()

    # List templates and exit
    if args.list_templates:
        list_rtsp_templates()
        return 0

    # Show mode
    if args.show:
        config = load_central_config()
        if config:
            # Mask API key for display
            display = dict(config)
            key = display.get("kamiclaw_api_key", "")
            if key and len(key) > 12:
                display["kamiclaw_api_key"] = key[:8] + "..." + key[-4:]
            print(json.dumps(display, indent=2, ensure_ascii=False))
        else:
            err("No config found.")
        return 0

    # Set values from CLI args
    config = load_central_config()
    modified = False

    if args.api_key:
        config["kamiclaw_api_key"] = args.api_key
        modified = True
    if args.stream_url:
        config.setdefault("cameras", {}).setdefault("default", {})["stream_url"] = args.stream_url
        modified = True

    # --add-camera [NAME=]URL  (NAME optional, auto-assigned when omitted)
    for spec in args.add_camera:
        cams_dict = config.setdefault("cameras", {})
        if not isinstance(cams_dict, dict):
            cams_dict = {}
            config["cameras"] = cams_dict
        if "=" in spec:
            name, rest = spec.split("=", 1)
            name, url = name.strip(), rest.strip()
            if not name:
                name = _auto_camera_name(cams_dict)
        else:
            url = spec.strip()
            name = _auto_camera_name(cams_dict)
        if not url:
            warn(f"Invalid --add-camera spec (empty URL): {spec}")
            continue
        cams_dict[name] = {"stream_url": url, "device_id": name}
        ok(f"Camera '{name}' added/updated")
        modified = True

    # --remove-camera NAME
    for name in args.remove_camera:
        cams_dict = config.get("cameras", {})
        if isinstance(cams_dict, dict) and name in cams_dict:
            del cams_dict[name]
            ok(f"Camera '{name}' removed")
            modified = True
        else:
            warn(f"Camera '{name}' not found")

    if modified:
        save_central_config(config)

    # Interactive mode
    if not args.distribute and not args.no_prompt and not modified:
        if sys.stdin.isatty():
            config = interactive_setup()
        else:
            info("Non-interactive mode, distributing existing config.")

    # Distribute
    if not config.get("kamiclaw_api_key") and not any(
        isinstance(c, dict) and c.get("stream_url")
        for c in (config.get("cameras") or {}).values()
    ):
        if args.no_prompt:
            warn("No config values set. Skipping distribution.")
            return 2
        warn("Config is mostly empty. Distribution will be limited.")

    print()
    info("Distributing configuration to skills...")
    print()
    failed = distribute(config)

    print()
    if failed == 0:
        ok("All configurations distributed successfully!")
        print_skill_summary()
    else:
        warn(f"{failed} skill(s) had errors during distribution.")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
