#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", str(Path.home() / ".openclaw"))).expanduser()
PRIMARY_AGENT = os.environ.get("OPENCLAW_PRIMARY_AGENT", "taizi")
STATE_DIR = OPENCLAW_HOME / "openai-codex-accounts"
SNAPSHOT_DIR = STATE_DIR / "profiles"
META_FILE = STATE_DIR / "accounts.json"
MAIN_CFG = OPENCLAW_HOME / "openclaw.json"
AGENTS_DIR = OPENCLAW_HOME / "agents"
CANONICAL_PROFILE = "openai-codex:default"
DEFAULT_FALLBACK_MODEL = os.environ.get("OPENCLAW_FALLBACK_MODEL", "bailian/qwen3.5-plus")
CODEX_USAGE_URL = os.environ.get("OPENCLAW_CODEX_USAGE_URL", "https://chatgpt.com/backend-api/wham/usage")
WEEKLY_RESET_GAP_SECONDS = 4320 * 60


def atomic_write_text(path: Path, content: str, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=str(path.parent), delete=False) as tf:
        tf.write(content)
        tmp_name = tf.name
    tmp_path = Path(tmp_name)
    try:
        target_mode = mode
        if target_mode is None and path.exists():
            target_mode = path.stat().st_mode & 0o777
        if target_mode is not None:
            os.chmod(tmp_path, target_mode)
        os.replace(tmp_path, path)
        if target_mode is not None:
            try:
                os.chmod(path, target_mode)
            except Exception:
                pass
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass


def write_json_atomic(path: Path, data: object, mode: int | None = None) -> None:
    atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2), mode=mode)


def ensure_dirs() -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(SNAPSHOT_DIR, 0o700)
    except Exception:
        pass
    if not META_FILE.exists():
        write_json_atomic(META_FILE, {"accounts": {}, "active": None}, mode=0o600)


def load_meta() -> dict[str, Any]:
    ensure_dirs()
    try:
        return json.loads(META_FILE.read_text())
    except Exception:
        return {"accounts": {}, "active": None}


def save_meta(meta: dict[str, Any]) -> None:
    ensure_dirs()
    write_json_atomic(META_FILE, meta, mode=0o600)


def decode_jwt_payload(token: str) -> dict[str, Any]:
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return {}
        payload = parts[1] + '=' * (-len(parts[1]) % 4)
        return json.loads(base64.urlsafe_b64decode(payload))
    except Exception:
        return {}


def load_main_config() -> dict[str, Any]:
    if not MAIN_CFG.exists():
        return {}
    try:
        return json.loads(MAIN_CFG.read_text())
    except Exception:
        return {}


def save_main_config(cfg: dict[str, Any]) -> None:
    write_json_atomic(MAIN_CFG, cfg)


def current_selected_profile_id() -> str:
    cfg = load_main_config()
    order = (((cfg.get('auth') or {}).get('order') or {}).get('openai-codex')) or []
    if isinstance(order, list) and order:
        return str(order[0])
    return CANONICAL_PROFILE


def load_auth_store(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text())
        return raw if isinstance(raw, dict) else None
    except Exception:
        return None


def read_openclaw_profile(path: Path, profile_id: str | None = None) -> dict[str, Any] | None:
    obj = load_auth_store(path)
    if not obj:
        return None
    profiles = obj.get("profiles", {})
    if not isinstance(profiles, dict):
        return None
    pid = profile_id or current_selected_profile_id()
    return profiles.get(pid) or profiles.get(CANONICAL_PROFILE)


def canonical_auth_path() -> Path:
    return AGENTS_DIR / PRIMARY_AGENT / "agent" / "auth-profiles.json"


def current_live_profile_id(path: Path | None = None) -> str:
    auth_path = path or canonical_auth_path()
    obj = load_auth_store(auth_path)
    if not obj:
        return current_selected_profile_id()
    profiles = obj.get('profiles', {})
    if not isinstance(profiles, dict):
        return current_selected_profile_id()
    # Official openclaw models auth login for openai-codex keeps the live token in
    # openai-codex:default and preserves email-specific sibling profiles.
    if CANONICAL_PROFILE in profiles:
        return CANONICAL_PROFILE
    configured = current_selected_profile_id()
    if configured in profiles:
        return configured
    for profile_id, cred in profiles.items():
        if isinstance(cred, dict) and cred.get('provider') == 'openai-codex':
            return str(profile_id)
    return current_selected_profile_id()


def current_profile() -> dict[str, Any] | None:
    return read_openclaw_profile(canonical_auth_path(), current_live_profile_id())


def current_identity(profile: dict[str, Any] | None) -> dict[str, Any]:
    if not profile:
        return {}
    payload = decode_jwt_payload(profile.get("access", "")) if profile.get("access") else {}
    openai_profile = payload.get("https://api.openai.com/profile", {}) if isinstance(payload, dict) else {}
    auth = payload.get("https://api.openai.com/auth", {}) if isinstance(payload, dict) else {}
    return {
        "email": openai_profile.get("email"),
        "accountId": profile.get("accountId") or auth.get("chatgpt_account_id"),
        "userId": auth.get("user_id"),
        "planType": auth.get("chatgpt_plan_type"),
        "expires": profile.get("expires"),
    }


def configured_agents() -> list[str]:
    ids = []
    if MAIN_CFG.exists():
        try:
            cfg = json.loads(MAIN_CFG.read_text())
            for agent in cfg.get("agents", {}).get("list", []):
                aid = agent.get("id")
                if isinstance(aid, str) and aid:
                    ids.append(aid)
        except Exception:
            pass
    # Match official sibling-agent sync semantics more closely: also include
    # every on-disk agent workspace under ~/.openclaw/agents.
    if AGENTS_DIR.exists():
        for p in AGENTS_DIR.iterdir():
            if p.is_dir() and (p / 'agent').exists():
                ids.append(p.name)
    if PRIMARY_AGENT not in ids:
        ids.insert(0, PRIMARY_AGENT)
    return sorted(set(ids))


def auth_file_for_agent(agent_id: str) -> Path:
    return AGENTS_DIR / agent_id / "agent" / "auth-profiles.json"


def profile_id_for_identity(email: str | None) -> str:
    email = (email or '').strip()
    return f"openai-codex:{email}" if email else CANONICAL_PROFILE


def profile_id_for_profile(profile: dict[str, Any] | None) -> str:
    ident = current_identity(profile)
    return profile_id_for_identity(ident.get('email'))


def email_profile_id_for_snapshot(info: dict[str, Any] | None, profile: dict[str, Any] | None) -> str:
    candidate = (info or {}).get('profileId')
    if isinstance(candidate, str) and candidate.strip() and candidate != CANONICAL_PROFILE:
        return candidate.strip()
    derived = profile_id_for_profile(profile)
    if derived != CANONICAL_PROFILE:
        return derived
    return profile_id_for_identity((info or {}).get('email'))


def apply_auth_profile_selection(email_profile_id: str, email: str | None = None) -> None:
    cfg = load_main_config()
    auth = cfg.setdefault('auth', {})
    profiles = auth.setdefault('profiles', {})
    order = auth.setdefault('order', {})
    # Official login behavior observed in this environment: current active
    # selection stays on openai-codex:default, while the email-specific profile
    # remains present as a named historical entry.
    profiles[CANONICAL_PROFILE] = {
        'provider': 'openai-codex',
        'mode': 'oauth'
    }
    if email_profile_id and email_profile_id != CANONICAL_PROFILE:
        profiles[email_profile_id] = {
            'provider': 'openai-codex',
            'mode': 'oauth',
            **({'email': email} if email else {}),
        }
    existing = order.get('openai-codex') or []
    if not isinstance(existing, list):
        existing = []
    desired = [CANONICAL_PROFILE]
    if email_profile_id and email_profile_id != CANONICAL_PROFILE:
        desired.append(email_profile_id)
    remainder = [pid for pid in existing if pid not in desired]
    order['openai-codex'] = [*desired, *remainder]
    save_main_config(cfg)


def update_profile_file(path: Path, profile: dict[str, Any], email_profile_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    obj = {"version": 1, "profiles": {}}
    if path.exists():
        try:
            obj = json.loads(path.read_text())
        except Exception:
            pass
    profiles = obj.setdefault("profiles", {})
    if not isinstance(profiles, dict):
        profiles = {}
        obj["profiles"] = profiles
    # Mirror official auth login behavior actually observed here: the live
    # account token is written into openai-codex:default, while email-specific
    # profiles are retained as named records for the same credential set.
    profiles[CANONICAL_PROFILE] = profile
    if email_profile_id and email_profile_id != CANONICAL_PROFILE:
        profiles[email_profile_id] = profile
    # Important for parity with official `openclaw models auth login`:
    # do NOT rewrite usageStats or lastGood here. The built-in login path only
    # upserts credentials and preserves existing metadata objects.
    write_json_atomic(path, obj, mode=0o600)


def propagate_profile(profile: dict[str, Any], email_profile_id: str) -> None:
    for aid in configured_agents():
        update_profile_file(auth_file_for_agent(aid), profile, email_profile_id)


def snapshot_path(name: str) -> Path:
    return SNAPSHOT_DIR / f"{name}.json"


def profile_identity(profile: dict[str, Any] | None) -> tuple[str | None, str | None]:
    ident = current_identity(profile)
    return ident.get("email"), ident.get("accountId")


def snapshot_profile(name: str) -> dict[str, Any] | None:
    sp = snapshot_path(name)
    if not sp.exists():
        return None
    try:
        return json.loads(sp.read_text())
    except Exception:
        return None


def account_identity_from_info(name: str, info: dict[str, Any] | None) -> tuple[str | None, str | None, str | None]:
    prof = snapshot_profile(name)
    email = (info or {}).get('email')
    account = (info or {}).get('accountId')
    access = None
    if prof:
        access = prof.get('access')
        prof_email, prof_account = profile_identity(prof)
        email = prof_email or email
        account = prof_account or account
    return email, account, access


def find_account_name_by_email(meta: dict[str, Any], email: str | None) -> str | None:
    if not email:
        return None
    candidates: list[tuple[int, str]] = []
    for name, info in sorted((meta.get('accounts') or {}).items()):
        candidate_email, _, _ = account_identity_from_info(name, info)
        if candidate_email == email:
            saved_at = int((info or {}).get('savedAt') or 0)
            candidates.append((saved_at, name))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def upsert_account_snapshot(meta: dict[str, Any], name: str, profile: dict[str, Any], *, saved_at: int | None = None, auto_discovered: bool | None = None) -> dict[str, Any]:
    accounts = meta.setdefault('accounts', {})
    identity = current_identity(profile)
    sp = snapshot_path(name)
    write_json_atomic(sp, profile, mode=0o600)
    existing = dict(accounts.get(name, {}))
    entry = {
        **existing,
        **identity,
        'savedAt': int(existing.get('savedAt') or saved_at or time.time()),
        'snapshot': str(sp),
        'profileId': profile_id_for_profile(profile),
    }
    if auto_discovered is not None:
        entry['autoDiscovered'] = auto_discovered
    accounts[name] = entry
    return entry


def sync_profile_into_list(meta: dict[str, Any], profile: dict[str, Any], *, preferred_name: str | None = None, set_active: bool = True, auto_discovered: bool | None = None) -> dict[str, Any]:
    identity = current_identity(profile)
    email = identity.get('email')
    existing_name = find_account_name_by_email(meta, email)

    if existing_name:
        target_name = existing_name
        action = 'updated-existing'
    else:
        target_name = preferred_name or next_account_name(meta)
        info = meta.get('accounts', {}).get(target_name, {})
        existing_email = (info or {}).get('email')
        if existing_email and email and existing_email != email:
            raise SystemExit(f"❌ 账号名已被其他邮箱占用: {target_name} ({existing_email})")
        action = 'created-new'

    upsert_account_snapshot(meta, target_name, profile, auto_discovered=auto_discovered)
    if set_active:
        meta['active'] = target_name
    reconcile_related_auth_state(meta, live_profile=profile)
    return {
        'name': target_name,
        'email': email,
        'action': action,
        'isNew': action == 'created-new',
    }


def resolve_actual_active_name() -> str | None:
    actual = current_profile()
    if not actual:
        return None
    meta = load_meta()
    actual_email, _ = profile_identity(actual)
    actual_access = actual.get('access')
    candidates: list[tuple[int, int, str]] = []

    for name, info in sorted((meta.get('accounts') or {}).items()):
        email, _, access = account_identity_from_info(name, info)

        score = -1
        # Account identity is keyed by email. accountId can change when the same
        # human moves to a new workspace/team, so accountId-only matches must
        # never collapse distinct emails into one saved account.
        if actual_email and email == actual_email and actual_access and access == actual_access:
            score = 400
        elif actual_email and email == actual_email:
            score = 300
        elif (not actual_email) and actual_access and access == actual_access:
            score = 200

        if score >= 0:
            saved_at = int((info or {}).get('savedAt') or 0)
            candidates.append((score, saved_at, name))

    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][2]


def next_account_name(meta: dict[str, Any]) -> str:
    accounts = meta.get('accounts', {})
    nums = []
    for name in accounts.keys():
        if isinstance(name, str) and name.startswith('account'):
            try:
                nums.append(int(name.replace('account', '', 1)))
            except Exception:
                pass
    n = max(nums) + 1 if nums else 1
    while f'account{n}' in accounts:
        n += 1
    return f'account{n}'


def repair_meta_metadata(meta: dict[str, Any]) -> dict[str, Any]:
    accounts = meta.setdefault('accounts', {})
    # Repair snapshot path fields and migrate old ambiguous profileId=default
    # metadata to stable email-specific profile ids.
    for name, info in list(accounts.items()):
        sp = snapshot_path(name)
        info['snapshot'] = str(sp)
        prof = snapshot_profile(name)
        ident = current_identity(prof) if prof else {}
        if ident.get('email') and not info.get('email'):
            info['email'] = ident.get('email')
        if ident.get('accountId') and not info.get('accountId'):
            info['accountId'] = ident.get('accountId')
        info['profileId'] = email_profile_id_for_snapshot(info, prof)
    return meta


def desired_openai_email_profiles(meta: dict[str, Any], live_profile: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    desired: dict[str, dict[str, Any]] = {}
    for name, info in sorted((meta.get('accounts') or {}).items()):
        prof = snapshot_profile(name)
        email = (info or {}).get('email') or current_identity(prof).get('email')
        profile_id = email_profile_id_for_snapshot(info, prof)
        if profile_id != CANONICAL_PROFILE and email:
            desired[profile_id] = {
                'email': email,
                'profile': prof,
                'accountName': name,
                'savedAt': int((info or {}).get('savedAt') or 0),
            }
    if live_profile:
        live_ident = current_identity(live_profile)
        live_email = live_ident.get('email')
        live_profile_id = profile_id_for_profile(live_profile)
        if live_profile_id != CANONICAL_PROFILE and live_email:
            desired[live_profile_id] = {
                'email': live_email,
                'profile': live_profile,
                'accountName': meta.get('active'),
                'savedAt': int(time.time()),
            }
    return desired


def desired_openai_profile_order(meta: dict[str, Any], desired: dict[str, dict[str, Any]], existing_order: list[str] | None = None) -> list[str]:
    desired_ids = list(desired.keys())
    if not desired_ids:
        return [CANONICAL_PROFILE]

    active_alias = None
    active_name = meta.get('active')
    active_info = (meta.get('accounts', {}) or {}).get(active_name or '', {}) if active_name else {}
    if active_info:
        active_alias = email_profile_id_for_snapshot(active_info, snapshot_profile(active_name))
        if active_alias == CANONICAL_PROFILE:
            active_alias = None

    ordered = [CANONICAL_PROFILE]
    if active_alias and active_alias in desired and active_alias not in ordered:
        ordered.append(active_alias)

    for pid in (existing_order or []):
        if pid in desired and pid not in ordered:
            ordered.append(pid)

    remaining = [
        (int((desired.get(pid) or {}).get('savedAt') or 0), pid)
        for pid in desired_ids
        if pid not in ordered
    ]
    for _, pid in sorted(remaining, key=lambda item: (item[0], item[1])):
        ordered.append(pid)
    return ordered


def reconcile_main_auth_config(meta: dict[str, Any], live_profile: dict[str, Any] | None = None) -> None:
    cfg = load_main_config()
    auth = cfg.setdefault('auth', {})
    profiles = auth.setdefault('profiles', {})
    if not isinstance(profiles, dict):
        profiles = {}
        auth['profiles'] = profiles
    desired = desired_openai_email_profiles(meta, live_profile=live_profile)
    desired_ids = set(desired.keys())

    profiles[CANONICAL_PROFILE] = {
        'provider': 'openai-codex',
        'mode': 'oauth',
    }
    for profile_id, entry in desired.items():
        profiles[profile_id] = {
            'provider': 'openai-codex',
            'mode': 'oauth',
            'email': entry.get('email'),
        }

    for profile_id in list(profiles.keys()):
        if not isinstance(profile_id, str):
            continue
        if not profile_id.startswith('openai-codex:'):
            continue
        if profile_id == CANONICAL_PROFILE:
            continue
        if profile_id not in desired_ids:
            del profiles[profile_id]

    order = auth.setdefault('order', {})
    if not isinstance(order, dict):
        order = {}
        auth['order'] = order
    existing_order = order.get('openai-codex') if isinstance(order.get('openai-codex'), list) else []
    order['openai-codex'] = desired_openai_profile_order(meta, desired, existing_order=existing_order)
    save_main_config(cfg)


def reconcile_agent_auth_store(path: Path, meta: dict[str, Any], live_profile: dict[str, Any] | None = None) -> None:
    obj = load_auth_store(path) or {'version': 1, 'profiles': {}}
    profiles = obj.setdefault('profiles', {})
    if not isinstance(profiles, dict):
        profiles = {}
        obj['profiles'] = profiles

    desired = desired_openai_email_profiles(meta, live_profile=live_profile)
    desired_ids = set(desired.keys())

    if live_profile:
        profiles[CANONICAL_PROFILE] = live_profile

    for profile_id, entry in desired.items():
        prof = entry.get('profile')
        if isinstance(prof, dict):
            profiles[profile_id] = prof

    for profile_id in list(profiles.keys()):
        if not isinstance(profile_id, str):
            continue
        if not profile_id.startswith('openai-codex:'):
            continue
        if profile_id == CANONICAL_PROFILE:
            continue
        if profile_id not in desired_ids:
            del profiles[profile_id]

    write_json_atomic(path, obj, mode=0o600)


def reconcile_related_auth_state(meta: dict[str, Any], live_profile: dict[str, Any] | None = None) -> dict[str, Any]:
    meta = repair_meta_metadata(meta)
    save_meta(meta)
    reconcile_main_auth_config(meta, live_profile=live_profile)
    for aid in configured_agents():
        reconcile_agent_auth_store(auth_file_for_agent(aid), meta, live_profile=live_profile)
    return meta


def sync_meta_with_reality() -> dict[str, Any]:
    meta = repair_meta_metadata(load_meta())

    actual = current_profile()
    if not actual:
        return reconcile_related_auth_state(meta)

    actual_name = resolve_actual_active_name()
    if actual_name:
        upsert_account_snapshot(meta, actual_name, actual)
        meta['active'] = actual_name
        return reconcile_related_auth_state(meta, live_profile=actual)

    # Real auth exists but is not in list yet: sync the current live login into
    # the list. Only a brand-new email should allocate a new account slot.
    sync_profile_into_list(meta, actual, auto_discovered=True)
    return repair_meta_metadata(load_meta())


def quota_cache_file(name: str) -> Path:
    return SNAPSHOT_DIR / f".{name}.quota.json"


def read_codex_quota(name: str) -> dict[str, Any] | None:
    quota_file = quota_cache_file(name)
    if not quota_file.exists():
        return None
    try:
        data = json.loads(quota_file.read_text())
        rate_limits = data.get("rate_limits", {})
        primary = rate_limits.get("primary", {})
        secondary = rate_limits.get("secondary", {})
        result = {
            "fiveHourUsedPct": primary.get("used_percent"),
            "weeklyUsedPct": secondary.get("used_percent"),
            "primary": primary,
            "secondary": secondary,
            "cachedAt": data.get("cached_at") or data.get("collected_at"),
        }
        if isinstance(data.get("health"), dict):
            result["health"] = data["health"]
        elif result["fiveHourUsedPct"] is not None and result["weeklyUsedPct"] is not None:
            result["health"] = {"status": "healthy", "reason": "cached-rate-limits"}
        return result
    except Exception:
        return None


def save_quota_cache(name: str, rate_limits: dict[str, Any], health: dict[str, Any] | None = None) -> None:
    payload = {
        "rate_limits": rate_limits,
        "cached_at": int(time.time()),
    }
    if health is not None:
        payload["health"] = health
    write_json_atomic(quota_cache_file(name), payload, mode=0o600)


def clamp_percent(value: Any) -> float | None:
    try:
        num = float(value)
    except Exception:
        return None
    if num < 0:
        return 0.0
    if num > 100:
        return 100.0
    return round(num, 1)


def resolve_secondary_window_label(window_seconds: Any, primary_reset_at: Any, secondary_reset_at: Any) -> str:
    try:
        window_hours = round((float(window_seconds) or 86400) / 3600)
    except Exception:
        window_hours = 24
    if window_hours >= 168:
        return 'Week'
    if window_hours < 24:
        return f'{window_hours}h'
    try:
        if primary_reset_at is not None and secondary_reset_at is not None and float(secondary_reset_at) - float(primary_reset_at) >= WEEKLY_RESET_GAP_SECONDS:
            return 'Week'
    except Exception:
        pass
    return 'Day'


def classify_usage_http_error(status: int, body_text: str = '') -> dict[str, Any]:
    low = (body_text or '').lower()
    if status in (401, 403):
        if 'workspace' in low or 'not enabled' in low or 'plan' in low:
            return {'status': 'plan-unavailable', 'reason': f'http-{status}-workspace-or-plan'}
        return {'status': 'auth-invalid', 'reason': f'http-{status}-token-invalid'}
    if status == 429:
        return {'status': 'rate-limited', 'reason': 'http-429-rate-limited'}
    return {'status': 'quota-unknown', 'reason': f'http-{status}'}


def fetch_codex_usage_snapshot(profile: dict[str, Any], timeout_sec: int = 30) -> tuple[dict[str, Any], dict[str, Any]]:
    token = profile.get('access')
    account_id = profile.get('accountId') or current_identity(profile).get('accountId')
    if not token:
        return {}, {'status': 'auth-invalid', 'reason': 'missing-access-token'}

    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'CodexBar',
        'Accept': 'application/json',
    }
    if account_id:
        headers['ChatGPT-Account-Id'] = str(account_id)

    req = urllib.request.Request(CODEX_USAGE_URL, headers=headers, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            raw = resp.read().decode('utf-8', errors='ignore')
            data = json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore') if hasattr(e, 'read') else ''
        return {}, classify_usage_http_error(e.code, body)
    except Exception as e:
        return {}, {'status': 'quota-unknown', 'reason': f'usage-fetch-error:{type(e).__name__}'}

    primary = {}
    secondary = {}
    rate_limit = data.get('rate_limit') or {}
    if isinstance(rate_limit.get('primary_window'), dict):
        pw = rate_limit['primary_window']
        primary = {
            'used_percent': clamp_percent(pw.get('used_percent') or 0),
            'window_minutes': round((float(pw.get('limit_window_seconds') or 10800) / 60)),
            'resets_at': pw.get('reset_at'),
        }
    if isinstance(rate_limit.get('secondary_window'), dict):
        sw = rate_limit['secondary_window']
        secondary = {
            'used_percent': clamp_percent(sw.get('used_percent') or 0),
            'window_minutes': round((float(sw.get('limit_window_seconds') or 86400) / 60)),
            'resets_at': sw.get('reset_at'),
            'label': resolve_secondary_window_label(sw.get('limit_window_seconds'), (rate_limit.get('primary_window') or {}).get('reset_at'), sw.get('reset_at')),
        }

    rate_limits = {'primary': primary, 'secondary': secondary}
    health = {'status': 'healthy', 'reason': 'live-usage-api'} if primary or secondary else {'status': 'quota-unknown', 'reason': 'usage-api-empty'}
    plan = data.get('plan_type')
    credits = data.get('credits') or {}
    if credits.get('balance') is not None:
        try:
            balance = float(credits.get('balance'))
            health['plan'] = f'{plan} (${balance:.2f})' if plan else f'${balance:.2f}'
        except Exception:
            if plan:
                health['plan'] = plan
    elif plan:
        health['plan'] = plan
    return rate_limits, health


def probe_quota_with_codex(name: str, profile: dict[str, Any], timeout_sec: int = 30) -> dict[str, Any] | None:
    cached_quota = read_codex_quota(name)
    try:
        rate_limits, health = fetch_codex_usage_snapshot(profile, timeout_sec=timeout_sec)
        if rate_limits.get('primary') or rate_limits.get('secondary'):
            save_quota_cache(name, rate_limits, health=health)
            return read_codex_quota(name)
        if cached_quota and cached_quota.get('fiveHourUsedPct') is not None:
            stale_health = {'status': 'stale', 'reason': 'cached-after-empty-usage-api'}
            save_quota_cache(name, {
                'primary': cached_quota.get('primary', {}),
                'secondary': cached_quota.get('secondary', {}),
            }, health=stale_health)
            return read_codex_quota(name)
        save_quota_cache(name, {}, health=health)
    except Exception as e:
        health = {'status': 'quota-unknown', 'reason': f'probe-error:{type(e).__name__}'}
        if cached_quota and cached_quota.get('fiveHourUsedPct') is not None:
            stale_health = {'status': 'stale', 'reason': f'cached-after-{type(e).__name__}'}
            save_quota_cache(name, {
                'primary': cached_quota.get('primary', {}),
                'secondary': cached_quota.get('secondary', {}),
            }, health=stale_health)
            return read_codex_quota(name)
        save_quota_cache(name, {}, health=health)
    return read_codex_quota(name)


def best_effort_quota_for_identity(name: str, email: str | None, profile: dict[str, Any] | None = None, probe: bool = False) -> dict[str, Any] | None:
    # `--probe` must mean a real fresh Codex CLI probe, not "return whatever was
    # cached before". The previous implementation short-circuited on cache hits,
    # which made list/status/auto appear frozen forever once .account*.quota.json
    # existed. Force a live probe first when requested, then fall back to cache
    # only if probing is not requested or cannot run.
    if probe and profile is not None:
        fresh = probe_quota_with_codex(name, profile)
        if fresh:
            return fresh
    quota = read_codex_quota(name)
    if quota:
        return quota
    if email:
        local = email.split('@', 1)[0]
        quota = read_codex_quota(local)
        if quota:
            return quota
    return None


def cmd_list(verbose: bool = False, json_mode: bool = False, probe: bool = False) -> None:
    meta = sync_meta_with_reality()
    accounts = meta.get("accounts", {})
    active = meta.get("active")
    rows = []
    for name, info in sorted(accounts.items()):
        profile = None
        sp = snapshot_path(name)
        if sp.exists():
            try:
                profile = json.loads(sp.read_text())
            except Exception:
                profile = None
        quota = best_effort_quota_for_identity(name, info.get("email"), profile=profile, probe=probe)
        row = {
            "name": name,
            "active": name == active,
            "email": info.get("email"),
            "accountId": info.get("accountId"),
            "planType": info.get("planType"),
            "expires": info.get("expires"),
            "quota": quota,
            "health": (quota or {}).get("health", {"status": "quota-unknown", "reason": "no-cache"}),
        }
        rows.append(row)
    if json_mode:
        print(json.dumps({"active": active, "accounts": rows}, ensure_ascii=False, indent=2))
        return
    if not rows:
        print("(no accounts saved)")
        return
    for row in rows:
        mark = "ACTIVE" if row["active"] else ""
        parts = [f"- {row['name']}", row.get("email") or "unknown"]
        if verbose:
            q = row.get("quota")
            if q:
                parts.append(f"5h_left={format_left_pct(q.get('fiveHourUsedPct'))}")
                parts.append(f"week_left={format_left_pct(q.get('weeklyUsedPct'))}")
            else:
                parts.append("5h_left=unknown")
                parts.append("week_left=unknown")
            h = row.get('health', {})
            reason = h.get('reason', '')
            if reason == 'stale-cached-rate-limits':
                parts.append(f"status=stale")
            else:
                parts.append(f"status={h.get('status', 'quota-unknown')}")
        if mark:
            parts.append(mark)
        print(" | ".join(parts))


def capture_current(name: str, set_active: bool = True, emit: bool = True) -> dict[str, Any]:
    profile = current_profile()
    if not profile:
        raise SystemExit("❌ 当前没有可保存的 OpenClaw OpenAI Codex OAuth profile")
    meta = repair_meta_metadata(load_meta())
    result = sync_profile_into_list(meta, profile, preferred_name=name, set_active=set_active, auto_discovered=False)
    if emit:
        if result.get('action') == 'updated-existing':
            print(f"✅ 邮箱 {result.get('email') or 'unknown'} 已存在，已更新现有账号快照: {result.get('name')}")
        else:
            print(f"✅ 已保存账号快照: {result.get('name')} ({result.get('email') or 'unknown'})")
    return result


def cmd_add(name: str | None, set_default_model: str | None) -> None:
    cmd = ["openclaw", "models", "auth", "login", "--provider", "openai-codex"]
    if set_default_model:
        cmd.append("--set-default")
    subprocess.run(cmd, check=True)
    profile = current_profile()
    ident = current_identity(profile)
    guessed = name or ((ident.get("email") or "account").split('@', 1)[0])
    result = capture_current(guessed, set_active=True, emit=False)
    if result.get('action') == 'updated-existing':
        print(f"✅ 已检测到当前登录账号 {result.get('email') or 'unknown'}，并更新现有账号 {result.get('name')}（沿用官方 auth login 产生的 profile 选择）")
    else:
        print(f"✅ 已检测到当前登录账号 {result.get('email') or 'unknown'}，并新增账号 {result.get('name')}（沿用官方 auth login 产生的 profile 选择）")


def cmd_use(name: str, model: str = "openai-codex/gpt-5.4", verify: bool = True, emit: bool = True) -> dict[str, Any]:
    snap = snapshot_path(name)
    if not snap.exists():
        raise SystemExit(f"❌ 账号不存在: {name}")
    profile = json.loads(snap.read_text())
    meta = sync_meta_with_reality()
    info = meta.get("accounts", {}).get(name, {})
    identity = current_identity(profile)
    email_profile_id = email_profile_id_for_snapshot(info, profile)
    email = info.get('email') or identity.get('email')
    apply_auth_profile_selection(email_profile_id, email=email)
    propagate_profile(profile, email_profile_id)
    meta = sync_meta_with_reality()
    meta.setdefault('accounts', {}).setdefault(name, {}).update({
        **identity,
        'savedAt': int((meta.get('accounts', {}).get(name, {}) or {}).get('savedAt') or time.time()),
        'snapshot': str(snap),
        'profileId': email_profile_id,
    })
    meta["active"] = name
    reconcile_related_auth_state(meta, live_profile=profile)
    set_model_silently(model)
    quota = best_effort_quota_for_identity(name, email, profile=profile)
    msg = f"✅ 已切换到 {name} ({email}) | selected_profile={CANONICAL_PROFILE} | email_profile={email_profile_id} | {quota_summary_text(quota)} | model={model}"
    verify_status = None
    if verify:
        verify_status = build_status(model=model, probe=True)
        if verify_status.get('health', {}).get('status') in {'auth-invalid', 'plan-unavailable'}:
            msg += f" | verify={verify_status.get('health', {}).get('status')}，可能仍需重新执行 openclaw models auth login --provider openai-codex"
    result = {
        'account': name,
        'email': email,
        'selectedProfile': CANONICAL_PROFILE,
        'emailProfile': email_profile_id,
        'model': model,
        'quota': quota,
        'message': msg,
        'verify': verify_status,
    }
    if emit:
        print(msg)
    return result


def build_status(model: str = "openai-codex/gpt-5.4", probe: bool = False) -> dict[str, Any]:
    meta = sync_meta_with_reality()
    active = meta.get("active")
    if not active:
        return {"error": "no-active-account", "model": model}
    info = meta.get("accounts", {}).get(active, {})
    profile = None
    sp = snapshot_path(active)
    if sp.exists():
        try:
            profile = json.loads(sp.read_text())
        except Exception:
            profile = None
    quota = best_effort_quota_for_identity(active, info.get("email"), profile=profile, probe=probe)
    data = {
        "active": active,
        "email": info.get("email"),
        "accountId": info.get("accountId"),
        "planType": info.get("planType"),
        "model": model,
        "health": (quota or {}).get("health", {"status": "quota-unknown", "reason": "no-cache"}),
    }
    if quota and quota.get('fiveHourUsedPct') is not None and quota.get('weeklyUsedPct') is not None:
        data["fiveHourUsedPct"] = quota.get("fiveHourUsedPct")
        data["weeklyUsedPct"] = quota.get("weeklyUsedPct")
        data["fiveHourLeftPct"] = quota_left_pct(quota.get("fiveHourUsedPct"))
        data["weeklyLeftPct"] = quota_left_pct(quota.get("weeklyUsedPct"))
    else:
        data["quota"] = "unknown"
    return data


def cmd_status(model: str = "openai-codex/gpt-5.4", probe: bool = False) -> None:
    print(json.dumps(build_status(model=model, probe=probe), ensure_ascii=False, indent=2))


def score_account(info: dict[str, Any], quota: dict[str, Any] | None) -> tuple[int, int]:
    if not quota:
        return (10_000, 10_000)
    five = quota.get("fiveHourUsedPct")
    week = quota.get("weeklyUsedPct")
    five = 10_000 if five is None else int(float(five))
    week = 10_000 if week is None else int(float(week))
    return (five, week)


def quota_is_usable(quota: dict[str, Any] | None, five_hour_switch_at: float, weekly_switch_at: float) -> bool:
    if not quota:
        return False
    health = quota.get('health', {}) if isinstance(quota, dict) else {}
    if health.get('status') in {'auth-invalid', 'plan-unavailable'}:
        return False
    five = quota.get("fiveHourUsedPct")
    week = quota.get("weeklyUsedPct")
    if five is None or week is None:
        return False
    return float(five) < float(five_hour_switch_at) and float(week) < float(weekly_switch_at)


def quota_hits_hard_five_hour_limit(quota: dict[str, Any] | None, hard_five_hour_switch_at: float) -> bool:
    if not quota:
        return False
    health = quota.get('health', {}) if isinstance(quota, dict) else {}
    if health.get('status') in {'auth-invalid', 'plan-unavailable'}:
        return False
    five = quota.get('fiveHourUsedPct')
    if five is None:
        return False
    try:
        return float(five) >= float(hard_five_hour_switch_at)
    except Exception:
        return False


def quota_hits_hard_weekly_limit(quota: dict[str, Any] | None, hard_weekly_switch_at: float) -> bool:
    if not quota:
        return False
    health = quota.get('health', {}) if isinstance(quota, dict) else {}
    if health.get('status') in {'auth-invalid', 'plan-unavailable'}:
        return False
    week = quota.get('weeklyUsedPct')
    if week is None:
        return False
    try:
        return float(week) >= float(hard_weekly_switch_at)
    except Exception:
        return False


def quota_left_pct(value: Any) -> Any:
    if value is None:
        return 'unknown'
    try:
        return round(100.0 - float(value), 1)
    except Exception:
        return 'unknown'


def format_left_pct(value: Any) -> str:
    left = quota_left_pct(value)
    return f"{left}%" if isinstance(left, (int, float)) else str(left)


def quota_summary_text(quota: dict[str, Any] | None) -> str:
    if not quota:
        return "5h_left=unknown | week_left=unknown"
    return f"5h_left={format_left_pct(quota.get('fiveHourUsedPct'))} | week_left={format_left_pct(quota.get('weeklyUsedPct'))}"


def set_model_silently(model: str) -> int:
    cp = subprocess.run(
        ["openclaw", "models", "set", model],
        check=False,
        capture_output=True,
        text=True,
    )
    return int(cp.returncode)


def list_recent_active_sessions(active_minutes: float) -> list[dict[str, Any]]:
    if active_minutes <= 0:
        return []
    now_ms = int(time.time() * 1000)
    threshold_ms = int(float(active_minutes) * 60 * 1000)
    rows: list[dict[str, Any]] = []
    for aid in configured_agents():
        store_path = AGENTS_DIR / aid / 'sessions' / 'sessions.json'
        if not store_path.exists():
            continue
        try:
            store = json.loads(store_path.read_text())
        except Exception:
            continue
        if not isinstance(store, dict):
            continue
        for key, info in store.items():
            if not isinstance(info, dict):
                continue
            key_str = str(key)
            # Ignore automation lanes; the guard is meant to protect human/user
            # conversations from mid-flight model/account switches.
            if ':cron:' in key_str or key_str.startswith('cron:'):
                continue
            updated_at = info.get('updatedAt')
            try:
                updated_at_ms = int(updated_at)
            except Exception:
                continue
            age_ms = now_ms - updated_at_ms
            if age_ms < 0:
                age_ms = 0
            if age_ms <= threshold_ms:
                rows.append({
                    'agentId': aid,
                    'key': key_str,
                    'updatedAt': updated_at_ms,
                    'ageMs': age_ms,
                    'model': info.get('model'),
                })
    rows.sort(key=lambda row: row.get('updatedAt', 0), reverse=True)
    return rows


def summarize_active_sessions(rows: list[dict[str, Any]], limit: int = 3) -> str:
    if not rows:
        return 'none'
    parts = []
    for row in rows[:limit]:
        age_min = round(float(row.get('ageMs', 0)) / 60000.0, 1)
        parts.append(f"{row.get('key')}({age_min}m)")
    extra = len(rows) - len(parts)
    if extra > 0:
        parts.append(f"+{extra} more")
    return ', '.join(parts)


def cmd_auto(primary_model: str = "openai-codex/gpt-5.4", fallback_model: str = DEFAULT_FALLBACK_MODEL, json_mode: bool = False, notify_mode: bool = False, five_hour_switch_at: float = 80.0, hard_five_hour_switch_at: float = 90.0, weekly_switch_at: float = 90.0, hard_weekly_switch_at: float = 95.0, inactive_minutes: float = 3.0) -> dict[str, Any]:
    meta = sync_meta_with_reality()
    accounts = meta.get("accounts", {})
    if not accounts:
        raise SystemExit("❌ 没有可切换账号")

    scored = []
    for name, info in accounts.items():
        profile = None
        sp = snapshot_path(name)
        if sp.exists():
            try:
                profile = json.loads(sp.read_text())
            except Exception:
                profile = None
        quota = best_effort_quota_for_identity(name, info.get("email"), profile=profile, probe=True)
        scored.append((score_account(info, quota), name, info, quota))

    active_name = meta.get("active")
    active_entry = next((x for x in scored if x[1] == active_name), None)
    current_quota = active_entry[3] if active_entry else None
    current_info = active_entry[2] if active_entry else {}
    hard_five_hour_required = quota_hits_hard_five_hour_limit(current_quota, hard_five_hour_switch_at)
    hard_weekly_required = quota_hits_hard_weekly_limit(current_quota, hard_weekly_switch_at)
    hard_switch_required = hard_five_hour_required or hard_weekly_required

    if active_entry is not None:
        _, name, info, quota = active_entry
        if quota_is_usable(quota, five_hour_switch_at, weekly_switch_at):
            set_model_silently(primary_model)
            result = {
                "mode": "keep-current",
                "activeAccount": name,
                "email": info.get("email"),
                "fiveHourUsedPct": quota.get("fiveHourUsedPct") if quota else None,
                "weeklyUsedPct": quota.get("weeklyUsedPct") if quota else None,
                "model": primary_model,
                "softFiveHourSwitchAt": five_hour_switch_at,
                "hardFiveHourSwitchAt": hard_five_hour_switch_at,
                "softWeeklySwitchAt": weekly_switch_at,
                "hardWeeklySwitchAt": hard_weekly_switch_at,
                "message": f"当前账号 {name} ({info.get('email')}) 仍可用，{quota_summary_text(quota)}，继续使用 {primary_model}",
            }
            if json_mode:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            elif notify_mode:
                print(result["message"])
            return result

    recent_active_sessions = list_recent_active_sessions(inactive_minutes)
    if recent_active_sessions and not hard_switch_required:
        result = {
            "mode": "blocked-active-sessions",
            "activeAccount": active_name,
            "email": current_info.get("email") if isinstance(current_info, dict) else None,
            "fiveHourUsedPct": current_quota.get("fiveHourUsedPct") if current_quota else None,
            "weeklyUsedPct": current_quota.get("weeklyUsedPct") if current_quota else None,
            "inactiveMinutesRequired": inactive_minutes,
            "softFiveHourSwitchAt": five_hour_switch_at,
            "hardFiveHourSwitchAt": hard_five_hour_switch_at,
            "softWeeklySwitchAt": weekly_switch_at,
            "hardWeeklySwitchAt": hard_weekly_switch_at,
            "activeSessionCount": len(recent_active_sessions),
            "activeSessionExamples": recent_active_sessions[:3],
            "message": f"检测到最近 {inactive_minutes:g} 分钟内仍有 {len(recent_active_sessions)} 个活跃 session（{summarize_active_sessions(recent_active_sessions)}），当前仅达到软切换条件（5小时或每周额度），为避免打断对话，本次暂不切换账号/模型。",
        }
        if json_mode:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif notify_mode:
            print(result["message"])
        return result

    usable = [x for x in scored if quota_is_usable(x[3], five_hour_switch_at, weekly_switch_at)]
    if usable:
        usable.sort(key=lambda x: x[0])
        _, name, info, quota = usable[0]
        cmd_use(name, model=primary_model, emit=False)
        result = {
            "mode": "account",
            "activeAccount": name,
            "email": info.get("email"),
            "fiveHourUsedPct": quota.get("fiveHourUsedPct"),
            "weeklyUsedPct": quota.get("weeklyUsedPct"),
            "model": primary_model,
            "inactiveMinutesRequired": inactive_minutes,
            "softFiveHourSwitchAt": five_hour_switch_at,
            "hardFiveHourSwitchAt": hard_five_hour_switch_at,
            "softWeeklySwitchAt": weekly_switch_at,
            "hardWeeklySwitchAt": hard_weekly_switch_at,
            "forcedImmediate": hard_switch_required,
            "forcedBy": (
                "five-hour"
                if hard_five_hour_required
                else "weekly"
                if hard_weekly_required
                else None
            ),
            "message": f"已切换到账号 {name} ({info.get('email')})，{quota_summary_text(quota)}，当前模型 {primary_model}",
        }
        if json_mode:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif notify_mode:
            print(result["message"])
        return result

    set_model_silently(fallback_model)
    reason = "all accounts exhausted or quota unknown"
    hard_reason_label = None
    if hard_five_hour_required:
        reason = "hard-five-hour-threshold-reached"
        hard_reason_label = f"5 小时用量已触发硬切换阈值（>= {hard_five_hour_switch_at:g}%）"
    elif hard_weekly_required:
        reason = "hard-weekly-threshold-reached"
        hard_reason_label = f"每周用量已触发硬切换阈值（>= {hard_weekly_switch_at:g}%）"
    result = {
        "mode": "fallback-model",
        "reason": reason,
        "fallbackModel": fallback_model,
        "inactiveMinutesRequired": inactive_minutes,
        "softFiveHourSwitchAt": five_hour_switch_at,
        "hardFiveHourSwitchAt": hard_five_hour_switch_at,
        "softWeeklySwitchAt": weekly_switch_at,
        "hardWeeklySwitchAt": hard_weekly_switch_at,
        "forcedImmediate": hard_switch_required,
        "forcedBy": (
            "five-hour"
            if hard_five_hour_required
            else "weekly"
            if hard_weekly_required
            else None
        ),
        "message": (
            f"当前账号{hard_reason_label}，已立即切换到备选模型 {fallback_model}"
            if hard_switch_required and hard_reason_label
            else f"所有 OpenAI 账号都不适合继续使用（达到阈值或额度未知），且最近 {inactive_minutes:g} 分钟无活跃 session，已切换到备选模型 {fallback_model}"
        ),
    }
    if json_mode:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["message"])
    return result


def cmd_import_codex(name: str) -> None:
    src = CODEX_ACCOUNTS_DIR / f"{name}.json"
    if not src.exists():
        raise SystemExit(f"❌ 未找到 Codex 账号快照: {src}")
    raise SystemExit("❌ 该版本暂不支持直接把 ~/.codex/accounts/*.json 转换为 OpenClaw OAuth profile；请先用 openclaw models auth login 登录，再用 add/capture 保存。")


def main() -> int:
    ensure_dirs()
    parser = argparse.ArgumentParser(description="OpenClaw OpenAI Codex multi-account switcher")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("list")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--probe", action="store_true")

    p = sub.add_parser("capture")
    p.add_argument("name")

    p = sub.add_parser("add")
    p.add_argument("--name")
    p.add_argument("--set-default", action="store_true")

    p = sub.add_parser("use")
    p.add_argument("name")
    p.add_argument("--model", default="openai-codex/gpt-5.4")

    p = sub.add_parser("status")
    p.add_argument("--model", default="openai-codex/gpt-5.4")
    p.add_argument("--probe", action="store_true")

    p = sub.add_parser("auto")
    p.add_argument("--model", default="openai-codex/gpt-5.4")
    p.add_argument("--fallback-model", default=DEFAULT_FALLBACK_MODEL)
    p.add_argument("--json", action="store_true")
    p.add_argument("--notify", action="store_true")
    p.add_argument("--five-hour-switch-at", type=float, default=80.0)
    p.add_argument("--five-hour-hard-switch-at", type=float, default=90.0)
    p.add_argument("--weekly-switch-at", type=float, default=90.0)
    p.add_argument("--weekly-hard-switch-at", type=float, default=95.0)
    p.add_argument("--inactive-minutes", type=float, default=3.0)

    p = sub.add_parser("cron-check")
    p.add_argument("--model", default="openai-codex/gpt-5.4")
    p.add_argument("--fallback-model", default=DEFAULT_FALLBACK_MODEL)
    p.add_argument("--json", action="store_true")
    p.add_argument("--five-hour-switch-at", type=float, default=80.0)
    p.add_argument("--five-hour-hard-switch-at", type=float, default=90.0)
    p.add_argument("--weekly-switch-at", type=float, default=90.0)
    p.add_argument("--weekly-hard-switch-at", type=float, default=95.0)
    p.add_argument("--inactive-minutes", type=float, default=3.0)

    p = sub.add_parser("import-codex")
    p.add_argument("name")

    args = parser.parse_args()

    if args.cmd == "list" or not args.cmd:
        cmd_list(verbose=getattr(args, "verbose", False), json_mode=getattr(args, "json", False), probe=getattr(args, "probe", False))
    elif args.cmd == "capture":
        capture_current(args.name)
    elif args.cmd == "add":
        cmd_add(args.name, set_default_model="1" if args.set_default else None)
    elif args.cmd == "use":
        cmd_use(args.name, model=args.model)
    elif args.cmd == "status":
        cmd_status(model=args.model, probe=args.probe)
    elif args.cmd == "auto":
        cmd_auto(primary_model=args.model, fallback_model=args.fallback_model, json_mode=args.json, notify_mode=args.notify, five_hour_switch_at=args.five_hour_switch_at, hard_five_hour_switch_at=args.five_hour_hard_switch_at, weekly_switch_at=args.weekly_switch_at, hard_weekly_switch_at=args.weekly_hard_switch_at, inactive_minutes=args.inactive_minutes)
    elif args.cmd == "cron-check":
        result = cmd_auto(primary_model=args.model, fallback_model=args.fallback_model, json_mode=args.json, notify_mode=not args.json, five_hour_switch_at=args.five_hour_switch_at, hard_five_hour_switch_at=args.five_hour_hard_switch_at, weekly_switch_at=args.weekly_switch_at, hard_weekly_switch_at=args.weekly_hard_switch_at, inactive_minutes=args.inactive_minutes)
        if args.json:
            return 0
        # human-readable single line for cron/system events
        if isinstance(result, dict) and result.get('message'):
            print(result['message'])
    elif args.cmd == "import-codex":
        cmd_import_codex(args.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
