#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Daily report generator for Health-Mate."""

import sys
import json
import re
import os
import glob
import shutil
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime


def console_print(*args, sep=" ", end="\n", file=sys.stdout, flush=False):
    """Print safely even when the active terminal encoding cannot render CJK text."""
    text = sep.join(str(arg) for arg in args) + end
    try:
        file.write(text)
    except UnicodeEncodeError:
        encoding = getattr(file, "encoding", None) or "utf-8"
        buffer = getattr(file, "buffer", None)
        if buffer is not None:
            buffer.write(text.encode(encoding, errors="replace"))
        else:
            file.write(text.encode("ascii", errors="backslashreplace").decode("ascii"))
    if flush:
        file.flush()


print = console_print

# ==================== Environment validation ====================
def validate_environment():
    """Validate required runtime settings before execution."""
    errors = []
    warnings = []

    memory_dir = os.environ.get('MEMORY_DIR', '')
    if not memory_dir:
        errors.append(t(None, "env_missing_memory_dir"))
        errors.append(t(None, "env_set_memory_dir"))
    elif not os.path.exists(memory_dir):
        errors.append(t(None, "env_memory_dir_missing", path=memory_dir))
    elif not os.access(memory_dir, os.R_OK):
        errors.append(t(None, "env_memory_dir_unreadable", path=memory_dir))

    webhooks = {
        'DINGTALK_WEBHOOK': os.environ.get('DINGTALK_WEBHOOK', ''),
        'FEISHU_WEBHOOK': os.environ.get('FEISHU_WEBHOOK', ''),
        'TELEGRAM_BOT_TOKEN': os.environ.get('TELEGRAM_BOT_TOKEN', ''),
    }
    configured_webhooks = [k for k, v in webhooks.items() if v]

    if not configured_webhooks:
        warnings.append(t(None, "env_no_webhooks"))
        warnings.append(t(None, "env_webhook_hint"))

    if warnings:
        print("=" * 60)
        print(t(None, "security_warning_title"))
        print("=" * 60)
        for w in warnings:
            print(w)
        print("=" * 60)

    if errors:
        print("=" * 60)
        print(t(None, "env_validation_failed"))
        print("=" * 60)
        for e in errors:
            print(e)
        print("=" * 60)
        print(f"\n{t(None, 'program_exit')}")
        sys.exit(1)

    return True

# ==================== Path setup ====================
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.resolve()
CONFIG_DIR = PROJECT_ROOT / 'config'
ASSETS_DIR = PROJECT_ROOT / 'assets'
LOGS_DIR = PROJECT_ROOT / 'logs'
REPORTS_DIR = PROJECT_ROOT / 'reports'
REPORTS_DIR.mkdir(exist_ok=True)
sys.path.insert(0, str(SCRIPT_DIR))


def load_project_env_file():
    """Load project-local config/.env without overriding already exported variables."""
    env_path = CONFIG_DIR / '.env'
    if not env_path.exists():
        return

    try:
        for raw_line in env_path.read_text(encoding='utf-8').splitlines():
            line = raw_line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('export '):
                line = line[7:].strip()
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            if not key or key in os.environ:
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            os.environ[key] = value
    except OSError:
        return


load_project_env_file()

from constants import DEFAULT_PORTIONS, FOOD_CALORIES, FOOD_NAME_ALIASES
from i18n import (
    CALORIE_BURN_ALIASES,
    CALORIE_UNIT_PATTERN,
    CUMULATIVE_ALIASES,
    DISTANCE_ALIASES,
    DISTANCE_UNIT_PATTERN,
    DURATION_ALIASES,
    EXERCISE_ALIASES,
    MEAL_ALIASES,
    MEAL_SKIP_KEYWORDS,
    MINUTE_UNIT_PATTERN,
    OVEREATING_PATTERN,
    PLACEHOLDER_TOKENS,
    PORTION_UNIT_PATTERN,
    STEP_LABEL_ALIASES,
    STEP_UNIT_PATTERN,
    SYMPTOM_KEYWORDS,
    SYMPTOM_SECTION_ALIASES,
    TIME_APPROX_PATTERN,
    WATER_AMOUNT_ALIASES,
    WATER_PERIOD_ALIASES,
    WEIGHT_MORNING_ALIASES,
    WEIGHT_UNIT_PATTERN,
    and_more,
    alias_pattern,
    build_ai_comment_prompt,
    build_ai_comment_system_prompt,
    build_ai_plan_prompt,
    build_ai_plan_system_prompt,
    build_condition_tip,
    build_delivery_message,
    build_fallback_plan,
    condition_key,
    condition_name,
    convert_weight_to_kg,
    exercise_key,
    exercise_name,
    extract_time_token,
    format_weight,
    gender_key,
    has_excluded_section_keyword,
    list_separator,
    localized_exercise_query,
    localized_recipe_query,
    localize_free_text,
    meal_key,
    meal_name,
    resolve_locale,
    strip_parenthetical_details,
    t,
    inline_localize,
    water_period_key,
    water_period_name,
    weight_unit,
)
from daily_pdf_generator import generate_pdf_report as generate_pdf_report_impl, has_local_cjk_font

validate_environment()

# ==================== Tavily configuration ====================
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY', '')
FONT_DOWNLOAD_HELP_URL = "https://github.com/tankeito/Health-Mate"

DEFAULT_AI_GENERATION = {
    "expert_commentary": {"mode": "hybrid", "max_attempts": 3, "timeout_seconds": 90},
    "next_day_plan": {"mode": "hybrid", "max_attempts": 3, "timeout_seconds": 90},
    "risk_alerts": {"mode": "local"},
}

ENGLISH_MEMORY_HEADER_HINTS = (
    "health log",
    "weight record",
    "water record",
    "meal record",
    "exercise record",
    "symptoms / discomfort",
    "medication record",
    "daily targets",
    "today steps",
    "breakfast",
    "lunch",
    "dinner",
    "snack",
    "wake-up",
    "morning",
    "noon",
    "afternoon",
    "evening",
)
CHINESE_MEMORY_HEADER_HINTS = (
    "健康记录",
    "体重记录",
    "饮水记录",
    "饮食记录",
    "运动记录",
    "症状/不适",
    "用药记录",
    "今日目标",
    "今日步数",
    "早餐",
    "午餐",
    "晚餐",
    "加餐",
    "晨起",
    "上午",
    "中午",
    "下午",
    "晚上",
)
JAPANESE_MEMORY_HEADER_HINTS = (
    "健康記録",
    "体重記録",
    "飲水記録",
    "食事記録",
    "運動記録",
    "症状 / 不調",
    "服薬記録",
    "今日の歩数",
    "朝食",
    "昼食",
    "夕食",
    "間食",
    "起床後",
    "午前",
    "正午",
    "午後",
    "夜",
)
PROFILE_ITEM_TRANSLATIONS = {
    "苹果": "apple",
    "耙耙柑": "ponkan orange",
    "香蕉": "banana",
    "梨": "pear",
    "鱼": "fish",
    "蛙": "frog",
    "海鲜": "seafood",
}
PROFILE_ITEM_TRANSLATIONS_JA = {
    "苹果": "りんご",
    "耙耙柑": "ポンカン",
    "香蕉": "バナナ",
    "梨": "梨",
    "鱼": "魚",
    "蛙": "カエル",
    "海鲜": "海鮮",
}

BUILTIN_MODULE_IDS = {"diet", "water", "weight", "symptom", "exercise", "adherence", "medication"}
MEDICATION_SECTION_ALIASES = {
    "\u7528\u836f",
    "\u7528\u836f\u60c5\u51b5",
    "\u7528\u836f\u8bb0\u5f55",
    "\u670d\u836f",
    "\u670d\u836f\u8bb0\u5f55",
    "\u670d\u85ac",
    "\u670d\u85ac\u8a18\u9332",
    "medication",
    "medications",
    "medicine",
    "medicines",
}


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def deep_merge_dict(defaults, overrides):
    merged = dict(defaults)
    for key, value in (overrides or {}).items():
        if isinstance(merged.get(key), dict) and isinstance(value, dict):
            merged[key] = deep_merge_dict(merged[key], value)
        else:
            merged[key] = value
    return merged


def normalize_section_name(value):
    return re.sub(r'[\s:：\-_()/（）\[\]·,.，、]+', '', str(value or '').strip().lower())


def default_module_title(locale, module_id):
    label_keys = {
        "diet": "diet_label",
        "water": "water_label",
        "weight": "weight_label",
        "symptom": "symptom_label",
        "exercise": "exercise_label",
        "adherence": "adherence_label",
    }
    if module_id in label_keys:
        return t(locale, label_keys[module_id])
    extra_titles = {
        "medication": {"zh-CN": "用药情况", "en-US": "Medication", "ja-JP": "服薬状況"},
    }
    locale = resolve_locale(locale=locale)
    titles = extra_titles.get(module_id, {})
    return titles.get(locale, titles.get("en-US", module_id))


def localize_profile_item(locale, value):
    text = str(value or "").strip()
    resolved = resolve_locale(locale=locale)
    if not text:
        return text
    if resolved == "en-US":
        return PROFILE_ITEM_TRANSLATIONS.get(text, text)
    if resolved == "ja-JP":
        return localize_free_text(locale, PROFILE_ITEM_TRANSLATIONS_JA.get(text, text))
    return text


def localize_profile_list(locale, values):
    return [localize_profile_item(locale, item) for item in (values or []) if str(item or "").strip()]


def build_default_scoring_modules(locale):
    return [
        {"id": "diet", "type": "builtin", "title": default_module_title(locale, "diet"), "enabled": True, "weight": 20},
        {"id": "water", "type": "builtin", "title": default_module_title(locale, "water"), "enabled": True, "weight": 15},
        {"id": "weight", "type": "builtin", "title": default_module_title(locale, "weight"), "enabled": True, "weight": 15},
        {"id": "symptom", "type": "builtin", "title": default_module_title(locale, "symptom"), "enabled": True, "weight": 15},
        {"id": "exercise", "type": "builtin", "title": default_module_title(locale, "exercise"), "enabled": True, "weight": 20},
        {"id": "adherence", "type": "builtin", "title": default_module_title(locale, "adherence"), "enabled": True, "weight": 15},
        {
            "id": "medication",
            "type": "section_presence",
            "title": default_module_title(locale, "medication"),
            "section_title": default_module_title(locale, "medication"),
            "enabled": False,
            "weight": 0,
            "score_when_present": 100,
            "score_when_missing": 0,
        },
    ]


def clone_ai_generation_defaults():
    return {
        key: dict(value)
        for key, value in DEFAULT_AI_GENERATION.items()
    }


def normalize_scoring_module(module, locale):
    if not isinstance(module, dict):
        return None
    module_id = str(module.get("id", "")).strip()
    if not module_id:
        return None

    module_type = str(module.get("type") or ("builtin" if module_id in BUILTIN_MODULE_IDS else "section_presence")).strip()
    if module_id in BUILTIN_MODULE_IDS:
        title = default_module_title(locale, module_id)
    else:
        title = str(module.get("title") or default_module_title(locale, module_id)).strip() or module_id
    if module_id == "medication" and (not title or "逕" in title or "闕" in title):
        title = default_module_title(locale, module_id)
    enabled = bool(module.get("enabled", True))
    weight = safe_float(module.get("weight", 0), 0)
    normalized = {
        "id": module_id,
        "type": module_type,
        "title": title,
        "enabled": enabled,
        "weight": weight,
    }

    if module_type == "section_presence":
        section_title = str(
            module.get("section_title")
            or module.get("section_name")
            or module.get("match_section")
            or title
        ).strip()
        if module_id == "medication" and (not section_title or "逕" in section_title or "闕" in section_title):
            section_title = default_module_title(locale, module_id)
        normalized["section_title"] = section_title
        normalized["score_when_present"] = safe_float(module.get("score_when_present", 100), 100)
        normalized["score_when_missing"] = safe_float(module.get("score_when_missing", 0), 0)

    return normalized


def normalize_scoring_modules(raw_config, locale):
    scoring = raw_config.get("scoring", {}) if isinstance(raw_config, dict) else {}
    modules = scoring.get("modules") if isinstance(scoring, dict) else None
    if isinstance(modules, list) and modules:
        normalized_modules = []
        seen_ids = set()
        for module in modules:
            normalized = normalize_scoring_module(module, locale)
            if not normalized or normalized["id"] in seen_ids:
                continue
            normalized_modules.append(normalized)
            seen_ids.add(normalized["id"])

        for default_module in build_default_scoring_modules(locale):
            if default_module["id"] not in seen_ids:
                normalized_modules.append(default_module)
        return normalized_modules

    return build_default_scoring_modules(locale)


def normalize_user_config(raw_config):
    base = _get_default_config()
    if not isinstance(raw_config, dict):
        return base

    merged = deep_merge_dict(base, raw_config)
    locale = resolve_locale(merged)
    user_profile = merged.setdefault("user_profile", {})
    raw_profile = raw_config.get("user_profile", {}) if isinstance(raw_config.get("user_profile"), dict) else {}
    raw_conditions = raw_profile.get("conditions")
    if isinstance(raw_conditions, list) and raw_conditions:
        normalized_conditions = []
        seen_conditions = set()
        for item in raw_conditions:
            canonical = condition_key(item)
            if canonical and canonical not in seen_conditions:
                normalized_conditions.append(canonical)
                seen_conditions.add(canonical)
    else:
        normalized_conditions = [condition_key(raw_profile.get("condition", user_profile.get("condition", "balanced")))]
    normalized_conditions = [item for item in normalized_conditions if item]
    if not normalized_conditions:
        normalized_conditions = ["balanced"]
    primary_source = raw_profile.get("primary_condition") or raw_profile.get("condition") or normalized_conditions[0]
    primary_condition = condition_key(primary_source) or normalized_conditions[0]
    if primary_condition not in normalized_conditions:
        normalized_conditions.insert(0, primary_condition)
    user_profile["conditions"] = normalized_conditions
    user_profile["primary_condition"] = primary_condition
    user_profile["condition"] = primary_condition
    raw_condition_standards = merged.get("condition_standards", {})
    normalized_condition_standards = {}
    for key, value in (raw_condition_standards or {}).items():
        if not isinstance(value, dict):
            continue
        canonical_key = condition_key(key)
        existing = normalized_condition_standards.get(canonical_key, {})
        normalized_condition_standards[canonical_key] = deep_merge_dict(existing, value)
    merged["condition_standards"] = deep_merge_dict(base.get("condition_standards", {}), normalized_condition_standards)
    merged["_version"] = "1.5.3"
    merged["config_version"] = "1.5.3"
    merged["ai_generation"] = deep_merge_dict(clone_ai_generation_defaults(), raw_config.get("ai_generation", {}))
    merged["scoring"] = {"modules": normalize_scoring_modules(raw_config, locale)}
    merged.setdefault("integrations", {"tavily_api_key": ""})
    merged["integrations"] = deep_merge_dict({"tavily_api_key": ""}, merged.get("integrations", {}))
    merged.setdefault("report_preferences", {"append_custom_sections": True, "population_branch": "lifestyle"})
    merged["report_preferences"] = deep_merge_dict(
        {"append_custom_sections": True, "population_branch": "lifestyle"},
        merged.get("report_preferences", {}),
    )
    merged["report_preferences"]["population_branch"] = normalize_population_branch(
        merged.get("report_preferences", {}).get("population_branch")
    ) or infer_population_branch(primary_condition)
    return merged


def get_scoring_modules(config):
    locale = resolve_locale(config)
    modules = config.get("scoring", {}).get("modules", [])
    if not isinstance(modules, list) or not modules:
        return build_default_scoring_modules(locale)
    normalized_modules = []
    seen_ids = set()
    for module in modules:
        normalized = normalize_scoring_module(module, locale)
        if not normalized or normalized["id"] in seen_ids:
            continue
        normalized_modules.append(normalized)
        seen_ids.add(normalized["id"])
    return normalized_modules or build_default_scoring_modules(locale)


def module_is_enabled(config, module_id):
    return any(module.get("id") == module_id and module.get("enabled", True) for module in get_scoring_modules(config))


def get_generation_settings(config, key):
    return deep_merge_dict(clone_ai_generation_defaults().get(key, {}), config.get("ai_generation", {}).get(key, {}))


def get_tavily_api_key(config=None):
    env_key = str(os.environ.get("TAVILY_API_KEY", "") or "").strip()
    if env_key:
        return env_key

    runtime_config = config
    if runtime_config is None:
        try:
            runtime_config = load_user_config()
        except Exception:
            runtime_config = {}

    integrations = runtime_config.get("integrations", {}) if isinstance(runtime_config, dict) else {}
    return str(integrations.get("tavily_api_key") or "").strip()


def has_tavily_api_key(config=None):
    return bool(get_tavily_api_key(config))


def generation_source_label(locale, source):
    locale = resolve_locale(locale=locale)
    labels = {
        "llm": {"zh-CN": "\u6765\u6e90\uff1aLLM \u52a8\u6001\u751f\u6210", "en-US": "Source: dynamically generated by LLM", "ja-JP": "出典: LLM 動的生成"},
        "fallback": {"zh-CN": "\u6765\u6e90\uff1a\u672c\u5730\u89c4\u5219", "en-US": "Source: local rules", "ja-JP": "出典: ローカルルール"},
        "fallback_tavily": {"zh-CN": "\u6765\u6e90\uff1aTavily \u68c0\u7d22 + \u672c\u5730\u89c4\u5219", "en-US": "Source: Tavily retrieval + local rules", "ja-JP": "出典: Tavily 検索 + ローカルルール"},
        "local": {"zh-CN": "\u6765\u6e90\uff1a\u672c\u5730\u89c4\u5219", "en-US": "Source: local rules", "ja-JP": "出典: ローカルルール"},
    }
    selected = labels.get(source, labels["local"])
    return selected.get(locale, selected.get("en-US", labels["local"]["en-US"]))

# ==================== Config loading ====================
def load_user_config(config_path=None):
    if config_path is None:
        config_path = CONFIG_DIR / 'user_config.json'
    if not os.path.exists(config_path):
        return _get_default_config()
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return normalize_user_config(json.load(f))
    except Exception as e:
        print(t(None, "config_load_failed", error=e), file=sys.stderr)
        return _get_default_config()


def infer_memory_locale_from_text(content):
    """Infer locale from visible markdown headings and text density."""
    text = str(content or "")
    if not text.strip():
        return None

    headings = re.findall(r'(?m)^#{1,3}\s+(.+?)\s*$', text)
    sample = '\n'.join(headings) if headings else text[:4000]
    sample_lower = sample.lower()

    en_score = sum(sample_lower.count(hint) for hint in ENGLISH_MEMORY_HEADER_HINTS)
    zh_score = sum(sample.count(hint) for hint in CHINESE_MEMORY_HEADER_HINTS)
    ja_score = sum(sample.count(hint) for hint in JAPANESE_MEMORY_HEADER_HINTS)

    if en_score >= max(2, zh_score + 1, ja_score + 1):
        return "en-US"
    if zh_score >= max(2, en_score + 1, ja_score + 1):
        return "zh-CN"
    if ja_score >= max(2, en_score + 1, zh_score + 1):
        return "ja-JP"

    latin_chars = len(re.findall(r'[A-Za-z]', sample))
    cjk_chars = len(re.findall(r'[\u4e00-\u9fff]', sample))
    kana_chars = len(re.findall(r'[\u3040-\u30ff]', sample))
    if latin_chars >= max(20, cjk_chars * 2):
        return "en-US"
    if kana_chars >= max(6, latin_chars // 2):
        return "ja-JP"
    if cjk_chars >= max(10, latin_chars):
        return "zh-CN"
    return None


def infer_memory_locale(memory_file):
    """Infer locale from one memory file if it exists."""
    try:
        with open(memory_file, 'r', encoding='utf-8') as f:
            return infer_memory_locale_from_text(f.read())
    except OSError:
        return None


def resolve_report_locale(config=None, memory_files=None, locale=None):
    """Resolve report locale with env override first, then memory inference."""
    if locale or os.environ.get("HEALTH_MATE_LANG"):
        return resolve_locale(config, locale=locale)

    base_locale = resolve_locale(config)
    detected_counts = {}
    for memory_file in memory_files or []:
        detected = infer_memory_locale(memory_file)
        if not detected:
            continue
        detected_counts[detected] = detected_counts.get(detected, 0) + 1

    if not detected_counts:
        return base_locale

    ranked = sorted(detected_counts.items(), key=lambda item: item[1], reverse=True)
    top_locale, top_count = ranked[0]
    if len(ranked) == 1 or top_count > ranked[1][1]:
        return top_locale
    return base_locale


def force_config_locale(config, locale):
    """Clone config and pin locale for downstream localized generation."""
    pinned_locale = resolve_locale(config, locale=locale)
    cloned = json.loads(json.dumps(config, ensure_ascii=False))
    cloned["language"] = pinned_locale
    cloned["locale"] = pinned_locale
    profile = cloned.setdefault("user_profile", {})
    profile["language"] = pinned_locale
    profile["locale"] = pinned_locale
    if pinned_locale == "ja-JP":
        if profile.get("name"):
            profile["name"] = localize_free_text(pinned_locale, profile.get("name"))
        residence = profile.get("residence", {})
        for field in ("country", "province", "city", "district", "display_name"):
            if residence.get(field):
                residence[field] = localize_free_text(pinned_locale, residence.get(field))
        preferences = profile.get("dietary_preferences", {})
        for field in ("dislike", "allergies", "favorite_fruits"):
            values = preferences.get(field)
            if isinstance(values, list):
                preferences[field] = [localize_free_text(pinned_locale, item) for item in values]
    return cloned


def build_font_render_notice(locale):
    font_path = "assets/NotoSansJP-VF.ttf" if resolve_locale(locale=locale) == "ja-JP" else "assets/NotoSansSC-VF.ttf"
    return t(
        locale,
        "font_missing_english_fallback",
        path=font_path,
        url=FONT_DOWNLOAD_HELP_URL,
    )


def export_memory_dir_to_english(source_dir):
    """Build a temporary English memory mirror using the export helper script."""
    temp_dir = tempfile.TemporaryDirectory(prefix="health_mate_memory_en_")
    command = [
        sys.executable,
        str(SCRIPT_DIR / "export_memory_en.py"),
        str(Path(source_dir).resolve()),
        temp_dir.name,
    ]
    env = {**os.environ, "MEMORY_DIR": str(Path(source_dir).resolve()), "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=180)
    if result.returncode != 0:
        temp_dir.cleanup()
        raise RuntimeError((result.stderr or result.stdout or "english memory export failed").strip())
    return temp_dir


def prepare_font_compatible_memory(requested_locale, source_dir, default_memory_file=None):
    """Switch to an English memory mirror when the bundled local CJK font is missing."""
    resolved_source_dir = str(Path(source_dir).resolve())
    result = {
        "locale": requested_locale,
        "render_notice": "",
        "temp_dir": None,
        "memory_dir": resolved_source_dir,
        "memory_file": default_memory_file,
    }

    if requested_locale not in {"zh-CN", "ja-JP"} or has_local_cjk_font(requested_locale):
        return result

    try:
        temp_dir = export_memory_dir_to_english(resolved_source_dir)
    except Exception as exc:
        print(f"WARNING: English fallback export failed: {exc}", file=sys.stderr)
        return result

    result["locale"] = "en-US"
    result["render_notice"] = build_font_render_notice("en-US")
    result["temp_dir"] = temp_dir
    result["memory_dir"] = temp_dir.name

    if default_memory_file:
        candidate = Path(temp_dir.name) / Path(default_memory_file).name
        if candidate.exists():
            result["memory_file"] = str(candidate)

    return result

def _get_default_config():
    locale = "zh-CN"
    return {
        "_version": "1.5.3",
        "config_version": "1.5.3",
        "language": "zh-CN",
        "user_profile": {
            "name": "Demo User",
            "gender": "male",
            "age": 34,
            "height_cm": 172,
            "current_weight_kg": 65,
            "target_weight_kg": 64,
            "condition": "fat_loss",
            "primary_condition": "fat_loss",
            "conditions": ["fat_loss"],
            "activity_level": 1.2,
            "water_target_ml": 2000,
            "step_target": 8000,
            "residence": {
                "country": "China",
                "province": "",
                "city": "",
                "district": "",
                "display_name": "",
            },
            "dietary_preferences": {
                "dislike": ["seafood"],
                "allergies": ["seafood"],
                "favorite_fruits": ["apple", "banana", "pear"],
            },
        },
        "condition_standards": {
            "gallstones": {"fat_min_g": 40, "fat_max_g": 50, "fiber_min_g": 25, "water_min_ml": 2000},
            "diabetes": {"fat_min_g": 40, "fat_max_g": 55, "fiber_min_g": 30, "water_min_ml": 2000},
            "hypertension": {"fat_min_g": 40, "fat_max_g": 55, "fiber_min_g": 25, "water_min_ml": 2000, "sodium_max_mg": 2000},
            "fat_loss": {"fat_min_g": 30, "fat_max_g": 50, "fiber_min_g": 25, "water_min_ml": 2000},
            "balanced": {"fat_min_g": 40, "fat_max_g": 60, "fiber_min_g": 25, "water_min_ml": 2000},
        },
        "scoring": {
            "modules": build_default_scoring_modules(locale),
        },
        "exercise_standards": {"weekly_target_minutes": 150},
        "ai_generation": clone_ai_generation_defaults(),
        "integrations": {"tavily_api_key": ""},
        "report_preferences": {"append_custom_sections": True, "population_branch": "lifestyle"},
    }

def get_profile_conditions(user_profile):
    if not isinstance(user_profile, dict):
        return ["balanced"]
    raw_conditions = user_profile.get("conditions")
    if isinstance(raw_conditions, list) and raw_conditions:
        conditions = [condition_key(item) for item in raw_conditions if condition_key(item)]
    else:
        conditions = [condition_key(user_profile.get("condition", "balanced"))]
    conditions = [item for item in conditions if item]
    return conditions or ["balanced"]


def get_primary_condition(user_profile):
    conditions = get_profile_conditions(user_profile)
    primary = condition_key((user_profile or {}).get("primary_condition", conditions[0])) or conditions[0]
    return primary if primary in conditions else conditions[0]


def normalize_population_branch(value):
    normalized = str(value or "").strip().lower().replace("-", "_")
    if normalized in {"lifestyle", "health", "healthy", "balanced", "fat_loss", "wellness"}:
        return "lifestyle"
    if normalized in {"disease", "medical", "condition", "illness"}:
        return "disease"
    return ""


def infer_population_branch(primary_condition=None):
    return "lifestyle" if condition_key(primary_condition) in {"balanced", "fat_loss"} else "disease"


def get_population_branch(config=None, user_profile=None, primary_condition=None):
    runtime_config = config if isinstance(config, dict) else {}
    explicit = normalize_population_branch(runtime_config.get("report_preferences", {}).get("population_branch"))
    if explicit:
        return explicit

    profile = user_profile if isinstance(user_profile, dict) else runtime_config.get("user_profile", {})
    resolved_primary = condition_key(primary_condition) or get_primary_condition(profile)
    return infer_population_branch(resolved_primary)


def is_lifestyle_branch(config=None, user_profile=None, primary_condition=None):
    return get_population_branch(config=config, user_profile=user_profile, primary_condition=primary_condition) == "lifestyle"


def get_conditions_display_name(locale, conditions):
    resolved = [condition_name(locale, item) for item in conditions if item]
    if not resolved:
        return condition_name(locale, "balanced")
    separator = "、" if resolve_locale(locale=locale) in {"zh-CN", "ja-JP"} else ", "
    return separator.join(resolved)


def build_multi_condition_tip(locale, conditions, standards):
    if not conditions:
        conditions = ["balanced"]
    tips = []
    for condition in conditions:
        tips.append(
            build_condition_tip(
                locale,
                condition,
                standards.get("fat_min_g", 40),
                standards.get("fat_max_g", 60),
                standards.get("fiber_min_g", 25),
            )
        )
    unique_tips = []
    for tip in tips:
        if tip not in unique_tips:
            unique_tips.append(tip)
    joiner = "；" if resolve_locale(locale=locale) in {"zh-CN", "ja-JP"} else "; "
    return joiner.join(unique_tips)


def get_condition_standards(config, condition_name):
    standards = config.get('condition_standards', {})
    if isinstance(condition_name, (list, tuple, set)):
        merged = {}
        for item in condition_name:
            current = get_condition_standards(config, item)
            for key, value in current.items():
                if not isinstance(value, (int, float)):
                    continue
                if key not in merged:
                    merged[key] = value
                elif key.endswith("_max_g") or key.endswith("_max_ml") or key.endswith("_max_mg"):
                    merged[key] = min(merged[key], value)
                elif key.endswith("_min_g") or key.endswith("_min_ml") or key.endswith("_min_mg"):
                    merged[key] = max(merged[key], value)
                else:
                    merged[key] = value
        return merged or standards.get('fat_loss', standards.get('balanced', {}))
    canonical = condition_key(condition_name)
    if canonical in standards:
        return standards[canonical]
    for key, value in standards.items():
        if condition_key(key) == canonical:
            return value
    return standards.get('fat_loss', standards.get('balanced', {}))

def get_scoring_weights(config):
    modules = [module for module in get_scoring_modules(config) if module.get("enabled", True)]
    if not modules:
        return {}

    positive_modules = [module for module in modules if safe_float(module.get("weight", 0), 0) > 0]
    if positive_modules:
        total = sum(safe_float(module.get("weight", 0), 0) for module in positive_modules)
        return {
            module["id"]: safe_float(module.get("weight", 0), 0) / total
            for module in positive_modules
        } if total > 0 else {}

    equal_weight = 1 / len(modules)
    return {module["id"]: equal_weight for module in modules}

def get_exercise_bonus_weight(config):
    return 0

# ==================== Core calculations ====================
def calculate_bmi(weight_kg, height_cm):
    if not weight_kg or not height_cm: return 0
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

def calculate_bmr(weight_kg, height_cm, age, gender):
    if gender_key(gender) == 'male':
        return round(10 * weight_kg + 6.25 * height_cm - 5 * age + 5, 1)
    return round(10 * weight_kg + 6.25 * height_cm - 5 * age - 161, 1)

def calculate_tdee(bmr, activity_level):
    return round(bmr * activity_level, 1)

# ==================== Food parsing ====================
SERVING_NUMBER_PATTERN = r"(?:一|两|半|\d+(?:\.\d+)?)"
SERVING_UNIT_PATTERN = r"(?:大个|大碗|个|碗|份|片|根|杯|盒|粒|块|条|瓶|袋|slice|cup|serving|piece)"
COUNTABLE_UNIT_PATTERN = r"(?:个|碗|份|片|根|杯|盒|粒|块|条|瓶|袋|slice|cup|serving|piece)"
DECLARED_CALORIE_PATTERN = rf'(?:→|->|=>)\s*(?:约\s*|approx\.?\s*)?(\d+(?:\.\d+)?)\s*{CALORIE_UNIT_PATTERN}'


def strip_serving_descriptors(value):
    text = strip_parenthetical_details(value)
    text = re.sub(rf'^\s*{SERVING_NUMBER_PATTERN}\s*{SERVING_UNIT_PATTERN}\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(rf'\s*{SERVING_NUMBER_PATTERN}\s*{SERVING_UNIT_PATTERN}\s*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+\d+(?:\.\d+)?\s*(?:g|ml)\s*$', '', text, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', text).strip()


def normalize_food_name(value):
    text = re.sub(r'\s+', ' ', str(value or '')).strip()
    alias_key = text.lower()
    if alias_key in FOOD_NAME_ALIASES:
        return FOOD_NAME_ALIASES[alias_key]

    best_target = None
    best_len = 0
    for alias, target in FOOD_NAME_ALIASES.items():
        if alias == alias_key or alias in alias_key or alias_key in alias:
            if len(alias) > best_len:
                best_target = target
                best_len = len(alias)
    return best_target or text


def extract_explicit_portion(entry_text):
    entry = str(entry_text or "")
    for paren_content in re.findall(r'[\(（]([^()（）]*)[\)）]', entry):
        if '+' in paren_content or '/' in paren_content:
            continue
        match = re.search(r'(\d+(?:\.\d+)?)\s*(ml|g)\b', paren_content, re.IGNORECASE)
        if match:
            return float(match.group(1))

    trailing = re.search(r'(\d+(?:\.\d+)?)\s*(ml|g)\b', strip_parenthetical_details(entry), re.IGNORECASE)
    if trailing:
        return float(trailing.group(1))
    return None


def lookup_default_unit_portion(food_name):
    canonical_name = normalize_food_name(strip_serving_descriptors(food_name))
    best_match = None
    for portion_key, grams in DEFAULT_PORTIONS.items():
        base_name = normalize_food_name(strip_serving_descriptors(portion_key))
        if not base_name:
            continue
        if base_name == canonical_name or base_name in canonical_name or canonical_name in base_name:
            if best_match is None or len(base_name) > best_match[0]:
                best_match = (len(base_name), grams)
    return best_match[1] if best_match else None


def extract_declared_calories(line_text):
    match = re.search(DECLARED_CALORIE_PATTERN, str(line_text or ""), re.IGNORECASE)
    return round(float(match.group(1)), 1) if match else None


def parse_food_entry(entry_text):
    entry = str(entry_text or '').strip()
    explicit_portion = extract_explicit_portion(entry)
    entry_without_notes = re.sub(r'[\(（][^()（）]*[\)）]', '', entry).strip()
    entry_without_notes = re.sub(r'\s+', ' ', entry_without_notes)

    alias_key = entry_without_notes.lower().strip()
    if alias_key in FOOD_NAME_ALIASES:
        entry_without_notes = FOOD_NAME_ALIASES[alias_key]

    for portion_prefix, portion_grams in DEFAULT_PORTIONS.items():
        if entry_without_notes.startswith(portion_prefix):
            food_name = entry_without_notes[len(portion_prefix):].strip()
            food_name = normalize_food_name(strip_serving_descriptors(food_name or portion_prefix))
            return food_name, explicit_portion or portion_grams

    food_name = normalize_food_name(strip_serving_descriptors(entry_without_notes))

    if explicit_portion:
        return food_name or normalize_food_name(entry_without_notes), explicit_portion

    count_match = re.search(rf'(.+?)\s*(\d+(?:\.\d+)?)\s*{COUNTABLE_UNIT_PATTERN}\s*$', entry_without_notes, re.IGNORECASE)
    if count_match:
        counted_name = normalize_food_name(strip_serving_descriptors(count_match.group(1)))
        per_unit_grams = lookup_default_unit_portion(counted_name)
        if per_unit_grams:
            return counted_name, round(float(count_match.group(2)) * per_unit_grams, 1)

    return food_name or normalize_food_name(entry_without_notes), 100


def estimate_composite_nutrition(food_name, calories_db):
    text = str(food_name or "")
    match = re.search(r'[\(（]([^()（）]*)[\)）]', text)
    if not match:
        return None

    ingredient_text = match.group(1)
    if '+' not in ingredient_text and '/' not in ingredient_text:
        return None

    total = {'calories': 0.0, 'protein': 0.0, 'fat': 0.0, 'carb': 0.0, 'fiber': 0.0}
    matched_items = 0
    for part in re.split(r'[+/]', ingredient_text):
        item_match = re.search(r'(.+?)\s*(\d+(?:\.\d+)?)\s*(g|ml)\b', part.strip(), re.IGNORECASE)
        if not item_match:
            continue
        item_name = normalize_food_name(strip_serving_descriptors(item_match.group(1)))
        item_portion = float(item_match.group(2))
        item_nutrition = estimate_nutrition(item_name, item_portion, calories_db, allow_composite=False)
        if not item_nutrition:
            continue
        matched_items += 1
        for key in total:
            total[key] += item_nutrition.get(key, 0)

    if matched_items >= 2:
        return {key: round(value, 1) for key, value in total.items()}
    return None


def estimate_nutrition(food_name, portion_grams, calories_db, allow_composite=True):
    if allow_composite:
        composite_nutrition = estimate_composite_nutrition(food_name, calories_db)
        if composite_nutrition:
            return composite_nutrition

    nutrition = None
    lookup_name = normalize_food_name(strip_serving_descriptors(food_name))
    if lookup_name in calories_db:
        nutrition = calories_db[lookup_name]
    else:
        candidate_matches = []
        for db_name, db_nutrition in calories_db.items():
            if db_name in lookup_name or lookup_name in db_name:
                candidate_matches.append((len(db_name), db_nutrition))
        if candidate_matches:
            nutrition = max(candidate_matches, key=lambda item: item[0])[1]
    if nutrition is None:
        nutrition = {"calories": 100, "protein": 10, "fat": 5, "carb": 10, "fiber": 2}
    scale = portion_grams / 100.0
    return {k: round(nutrition.get(k, 0) * scale, 1) for k in ['calories', 'protein', 'fat', 'carb', 'fiber']}

# ==================== Scoring ====================
def calculate_diet_score(daily_data, standards, scoring_standards):
    diet_weights = scoring_standards.get('diet', {'fat_score_weight': 0.30, 'protein_score_weight': 0.25, 'fiber_score_weight': 0.25, 'avoid_food_penalty': 0.20})
    total_fat = daily_data.get('total_fat', 0)
    fat_min, fat_max = standards.get('fat_min_g', 40), standards.get('fat_max_g', 50)
    fat_score = 100 if fat_min <= total_fat <= fat_max else max(0, 100 - (fat_min - total_fat) * 5 if total_fat < fat_min else (total_fat - fat_max) * 8)
    total_fiber = daily_data.get('total_fiber', 0)
    fiber_min = standards.get('fiber_min_g', 25)
    fiber_score = 100 if total_fiber >= fiber_min else max(0, 100 - (fiber_min - total_fiber) * 4)
    avoid_count = len(daily_data.get('avoid_foods', []))
    avoid_penalty = min(100, avoid_count * 25)
    score = (fat_score * diet_weights.get('fat_score_weight', 0.30) + fiber_score * diet_weights.get('fiber_score_weight', 0.25) + (100 - avoid_penalty) * diet_weights.get('avoid_food_penalty', 0.20) + 100 * diet_weights.get('protein_score_weight', 0.25))
    return max(0, min(100, round(score, 1)))

def calculate_water_score(water_total, water_target):
    if water_total >= water_target: return 100
    percentage = water_total / water_target
    if percentage >= 0.8: return round(80 + (percentage - 0.8) * 100, 1)
    elif percentage >= 0.5: return round(50 + (percentage - 0.5) * 60, 1)
    else: return round(percentage * 100, 1)

def calculate_weight_score(weight_recorded, target_weight, current_weight):
    score = 50 if weight_recorded else 0
    if current_weight and target_weight:
        diff = abs(current_weight - target_weight)
        score += 50 if diff <= 1 else (30 if diff <= 3 else (15 if diff <= 5 else 0))
    return max(0, min(100, score))

def calculate_exercise_score(exercise_data, steps, exercise_standards, scoring_standards):
    try:
        exercise_weights = scoring_standards.get('exercise', {'duration_score_weight': 0.40, 'frequency_score_weight': 0.30, 'calorie_score_weight': 0.30, 'daily_calorie_target': 300})
        total_minutes = sum(e.get('duration_min', 0) for e in exercise_data if isinstance(e, dict)) if exercise_data else 0
        daily_target = exercise_standards.get('weekly_target_minutes', 150) / 7
        duration_score = 100 if total_minutes >= daily_target else round((total_minutes / daily_target) * 100, 1) if daily_target > 0 else 0

        frequency_score = 100 if (exercise_data and len(exercise_data) > 0) or steps > 3000 else 0

        total_calories = sum(e.get('calories', 0) for e in exercise_data if isinstance(e, dict)) if exercise_data else 0
        total_calories += int(steps * 0.035)
        calorie_target = exercise_weights.get('daily_calorie_target', 300)
        calorie_score = 100 if total_calories >= calorie_target else round((total_calories / calorie_target) * 100, 1) if calorie_target > 0 else 0
        score = duration_score * exercise_weights.get('duration_score_weight', 0.40) + frequency_score * exercise_weights.get('frequency_score_weight', 0.30) + calorie_score * exercise_weights.get('calorie_score_weight', 0.30)
        return max(0, min(100, round(score, 1)))
    except Exception as e:
        print(t(None, "exercise_score_failed", error=e), file=sys.stderr)
        return 0


def calculate_symptom_score(symptom_keywords):
    symptom_penalty = len(symptom_keywords or []) * 20
    return max(0, 100 - symptom_penalty)


def calculate_adherence_score(health_data, water_target):
    meal_count = len(health_data.get('meals', []))
    meal_score = min(100, round(meal_count / 3 * 100, 1)) if meal_count > 0 else 0
    hydration_score = calculate_water_score(health_data.get('water_total', 0), max(1, water_target))
    tracking_checks = [
        100 if health_data.get('weight_morning') is not None else 0,
        100 if health_data.get('water_records') or health_data.get('water_total', 0) > 0 else 0,
        100 if health_data.get('exercise_records') or health_data.get('steps', 0) > 0 else 0,
    ]
    tracking_score = round(sum(tracking_checks) / len(tracking_checks), 1)
    return max(0, min(100, round(meal_score * 0.45 + hydration_score * 0.35 + tracking_score * 0.20, 1)))


def calculate_section_presence_score(lines, present_score=100, missing_score=0):
    return present_score if lines else missing_score

def parse_memory_file(file_path):
    """Parse one markdown memory file with bilingual heading support."""
    data = {
        'date': '', 'weight_morning': None, 'weight_evening': None,
        'water_records': [], 'meals': [], 'exercise_records': [],
        'medication_records': [],
        'symptoms': [], 'symptom_keywords': [], 'risks': [], 'plan': {}, 'ai_comment': '',
        'water_total': 0, 'water_target': 2000,
        'total_calories': 0, 'total_protein': 0, 'total_fat': 0, 'total_carb': 0, 'total_fiber': 0,
        'steps': 0, 'overeating_factor': 1.0,
        'custom_sections': {}
    }
    if not os.path.exists(file_path):
        return data

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def strip_markdown_emphasis(value):
        return re.sub(r'[*_`]+', '', str(value or '')).strip()

    def clean_heading(value):
        text = strip_markdown_emphasis(value)
        text = re.sub(r'^[^A-Za-z0-9\u4e00-\u9fff\u3040-\u30ff]+', '', text)
        return text.strip()

    def build_alias_lookup(mapping):
        lookup = {}
        for canonical, aliases in mapping.items():
            for alias in {canonical, *(aliases or [])}:
                normalized = normalize_section_name(alias)
                if normalized:
                    lookup[normalized] = canonical
        return lookup

    def build_fuzzy_aliases(mapping):
        values = []
        for canonical, aliases in mapping.items():
            for alias in {canonical, *(aliases or [])}:
                normalized = normalize_section_name(alias)
                if normalized:
                    values.append((canonical, normalized))
        values.sort(key=lambda item: len(item[1]), reverse=True)
        return values

    def classify_level3_heading(title):
        title_without_time = re.sub(TIME_APPROX_PATTERN, '', clean_heading(title), flags=re.IGNORECASE).strip()
        normalized = normalize_section_name(title_without_time)
        if normalized in meal_heading_lookup:
            return "meal"
        if normalized in water_heading_lookup:
            return "water"
        if normalized in medication_heading_lookup:
            return "medication"
        if detect_exercise_type(title_without_time):
            return "exercise"
        return None

    def iter_meaningful_lines(block_text):
        for raw_line in str(block_text or '').splitlines():
            line = raw_line.strip()
            if not line or line in PLACEHOLDER_TOKENS or line.startswith('_'):
                continue
            yield line

    def parse_custom_section_items(block_text):
        items = []
        current_subheading = ""
        skipping_builtin_subblock = False
        for line in iter_meaningful_lines(block_text):
            heading_match = re.match(r'^###\s+(.+)$', line)
            if heading_match:
                subheading = clean_heading(heading_match.group(1))
                if classify_level3_heading(subheading):
                    current_subheading = ""
                    skipping_builtin_subblock = True
                else:
                    current_subheading = subheading
                    skipping_builtin_subblock = False
                continue

            if skipping_builtin_subblock:
                continue

            item_text = strip_markdown_emphasis(re.sub(r'^\s*[-*]\s*', '', line)).strip()
            if not item_text:
                continue
            if current_subheading:
                separator = "：" if re.search(r'[\u4e00-\u9fff]', current_subheading) else ": "
                item_text = f"{current_subheading}{separator}{item_text}"
            items.append(item_text)
        return items

    def append_unique(target, values):
        seen = {
            normalize_section_name(strip_markdown_emphasis(re.sub(r'^\s*[-*]\s*', '', item)))
            for item in target
            if str(item or '').strip()
        }
        for item in values:
            cleaned_item = strip_markdown_emphasis(re.sub(r'^\s*[-*]\s*', '', str(item or ''))).strip()
            if not cleaned_item:
                continue
            dedupe_key = normalize_section_name(cleaned_item)
            if dedupe_key in seen:
                continue
            target.append(cleaned_item)
            seen.add(dedupe_key)

    def clean_food_line(value):
        text = strip_markdown_emphasis(re.sub(r'^\s*[-*]\s*', '', str(value or ''))).strip()
        text = re.sub(
            r'\s*(?:→|->|=>)\s*(?:约\s*|approx\.?\s*)?\d+(?:\.\d+)?\s*(?:千卡|kcal|calories?|卡路里)\s*$',
            '',
            text,
            flags=re.IGNORECASE,
        )
        return re.sub(r'\s+', ' ', text).strip(' -–—>')

    def is_meal_summary_or_assessment(line_text):
        text = strip_markdown_emphasis(str(line_text or '')).strip()
        normalized = normalize_section_name(text)
        if not text:
            return True
        if text.startswith('**') and ('评估' in text or 'assessment' in text.lower()):
            return True
        if any(marker in text for marker in ('总计', 'meal total', '评估', 'assessment')):
            return True
        if re.match(r'^(?:蛋白质|脂肪|碳水|膳食纤维|热量|protein|fat|carb|carbs|fiber)\s*[:：]', text, re.IGNORECASE):
            return True
        if re.match(r'^(?:✅|⚠️|⚠|❌|✔|✘)', text):
            return True
        if re.match(r'^(?:用药提醒|备注|说明|状态)\s*[:：]', text, re.IGNORECASE):
            return True
        lowered = text.lower()
        if any(keyword.lower() in lowered for keyword in MEAL_SKIP_KEYWORDS):
            return True
        return normalized.startswith(normalize_section_name('评估'))

    def detect_exercise_type(title):
        normalized = normalize_section_name(title)
        for canonical, alias in exercise_heading_aliases:
            if alias in normalized:
                return canonical
        return None

    def extract_duration_minutes(block_text):
        hour_minute_match = re.search(
            r'(?:耗时|时长|duration|time)\s*[:：]\s*(?:(\d+)\s*(?:小时|hr|hrs|hour|hours))?\s*(\d+)\s*(?:分|分钟|min|minutes?)\s*(?:(\d+)\s*(?:秒|sec|secs|seconds?))?',
            block_text,
            re.IGNORECASE,
        )
        if hour_minute_match:
            hours = int(hour_minute_match.group(1) or 0)
            minutes = int(hour_minute_match.group(2) or 0)
            seconds = int(hour_minute_match.group(3) or 0)
            total_minutes = hours * 60 + minutes + (1 if seconds >= 30 else 0)
            return total_minutes
        minute_only_match = re.search(
            rf'(?:{alias_pattern(DURATION_ALIASES)})\s*[:：]\s*(\d+)\s*{MINUTE_UNIT_PATTERN}',
            block_text,
            re.IGNORECASE,
        )
        return int(minute_only_match.group(1)) if minute_only_match else 0

    meal_heading_lookup = build_alias_lookup(MEAL_ALIASES)
    water_heading_lookup = build_alias_lookup(WATER_PERIOD_ALIASES)
    medication_heading_lookup = {normalize_section_name(alias) for alias in MEDICATION_SECTION_ALIASES}
    symptom_heading_lookup = {
        normalize_section_name(alias)
        for aliases in SYMPTOM_SECTION_ALIASES.values()
        for alias in aliases
    }
    exercise_heading_aliases = build_fuzzy_aliases(EXERCISE_ALIASES)

    date_match = re.search(r'#\s+(\d{4}-\d{2}-\d{2})', content)
    if date_match:
        data['date'] = date_match.group(1)

    weight_match = re.search(
        rf'(?:\*\*)?\s*(?:{alias_pattern(WEIGHT_MORNING_ALIASES)})\s*(?:\*\*)?\s*[:：]\s*([\d.]+)\s*(斤|kg|公斤|jin|lbs?|pounds?)?',
        content,
        re.IGNORECASE,
    )
    if weight_match:
        raw_value = float(weight_match.group(1))
        raw_unit = weight_match.group(2)
        assume_jin = raw_unit in {'斤', 'jin'} or (raw_unit is None and '晨起' in content)
        unit = raw_unit or (weight_unit("zh-CN") if assume_jin else weight_unit("en-US"))
        data['weight_morning'] = convert_weight_to_kg(raw_value, unit, assume_jin=assume_jin)

    section_blocks = re.finditer(r'(?ms)^##\s+([^\n]+)\n(.*?)(?=^##\s+|\Z)', content)
    for match in section_blocks:
        header_raw = clean_heading(match.group(1))
        items = parse_custom_section_items(match.group(2))
        if not items:
            continue

        normalized_header = normalize_section_name(header_raw)
        if normalized_header in medication_heading_lookup:
            append_unique(data['medication_records'], items)
            continue

        if any(alias and alias in normalized_header for alias in symptom_heading_lookup):
            data['symptoms'] = items
            continue

        if not has_excluded_section_keyword(header_raw):
            data['custom_sections'][header_raw] = items

    level3_blocks = list(re.finditer(r'(?ms)^###\s+([^\n]+)\n(.*?)(?=^###\s+|^##\s+|\Z)', content))
    for match in level3_blocks:
        title = clean_heading(match.group(1))
        block_text = match.group(2)
        title_without_time = re.sub(TIME_APPROX_PATTERN, '', title, flags=re.IGNORECASE).strip()
        title_key = normalize_section_name(title_without_time)
        exact_time = extract_time_token(title)

        water_key = water_heading_lookup.get(title_key)
        if water_key:
            amount_match = re.search(
                rf'^[*-]?\s*(?:{alias_pattern(WATER_AMOUNT_ALIASES)})\s*[:：]\s*(\d+(?:\.\d+)?)\s*ml\b',
                block_text,
                re.IGNORECASE | re.MULTILINE,
            )
            cumulative_match = re.search(
                rf'^[*-]?\s*(?:{alias_pattern(CUMULATIVE_ALIASES)})\s*[:：]\s*(\d+(?:\.\d+)?)\s*ml\s*/\s*(\d+(?:\.\d+)?)\s*ml',
                block_text,
                re.IGNORECASE | re.MULTILINE,
            )
            if amount_match and cumulative_match:
                data['water_records'].append({
                    'time_label': water_key,
                    'exact_time': exact_time,
                    'time': exact_time or water_key,
                    'amount_ml': int(float(amount_match.group(1))),
                    'cumulative_ml': int(float(cumulative_match.group(1))),
                })
                data['water_target'] = int(float(cumulative_match.group(2)))
            continue

        meal_type = meal_heading_lookup.get(title_key)
        if meal_type:
            meal_overeating = 1.25 if re.search(OVEREATING_PATTERN, block_text, re.IGNORECASE) else 1.0
            meal_data = {
                'type': meal_type,
                'time': exact_time,
                'foods': [],
                'food_nutrition': [],
                'total_calories': 0,
                'total_protein': 0,
                'total_fat': 0,
                'total_carb': 0,
                'total_fiber': 0,
                'overeating_factor': meal_overeating,
            }
            in_assessment_block = False
            for line in iter_meaningful_lines(block_text):
                if re.match(r'^###\s+', line):
                    break

                line_text = strip_markdown_emphasis(line)
                if line_text in {'评估', 'Assessment'} or re.match(r'^\*\*(?:评估|Assessment)', line, re.IGNORECASE):
                    in_assessment_block = True
                    continue
                if in_assessment_block:
                    continue
                if is_meal_summary_or_assessment(line_text):
                    continue

                clean_line = clean_food_line(line_text)
                if not clean_line:
                    continue

                food_name, portion = parse_food_entry(clean_line)
                nutrition = estimate_nutrition(food_name, portion, FOOD_CALORIES)
                if meal_overeating > 1.0:
                    nutrition = {k: v * meal_overeating for k, v in nutrition.items()}
                declared_calories = extract_declared_calories(line_text)
                if declared_calories is not None:
                    nutrition['calories'] = declared_calories
                meal_data['foods'].append(clean_line)
                meal_data['food_nutrition'].append({'name': clean_line, 'portion_grams': portion, **nutrition})
                for key in ['calories', 'protein', 'fat', 'carb', 'fiber']:
                    meal_data[f'total_{key}'] += nutrition[key]

            if meal_data['foods']:
                data['meals'].append(meal_data)
            continue

        if title_key in medication_heading_lookup:
            medication_lines = []
            for line in iter_meaningful_lines(block_text):
                item_text = strip_markdown_emphasis(re.sub(r'^\s*[-*]\s*', '', line)).strip()
                if not item_text:
                    continue
                if exact_time and not re.match(r'^\d{1,2}:\d{2}\b', item_text):
                    item_text = f"{exact_time} {item_text}"
                medication_lines.append(item_text)
            append_unique(data['medication_records'], medication_lines)
            continue

        exercise_type = detect_exercise_type(title_without_time)
        if exercise_type:
            distance_match = re.search(
                r'(?:距离|路程|距離|distance)\s*[:：]\s*([\d.]+)\s*(?:公里|km)',
                block_text,
                re.IGNORECASE,
            )
            calories_match = re.search(
                rf'(?:{alias_pattern(CALORIE_BURN_ALIASES)})\s*[:：]\s*(?:约\s*|approx\.?\s*)?(\d+(?:\.\d+)?)\s*{CALORIE_UNIT_PATTERN}',
                block_text,
                re.IGNORECASE,
            )
            duration_minutes = extract_duration_minutes(block_text)
            if distance_match or calories_match or duration_minutes:
                data['exercise_records'].append({
                    'type': exercise_type,
                    'time': exact_time,
                    'distance_km': float(distance_match.group(1)) if distance_match else 0,
                    'duration_min': duration_minutes,
                    'calories': round(float(calories_match.group(1)), 1) if calories_match else 0,
                })

    if data['water_records']:
        data['water_total'] = max(record.get('cumulative_ml', 0) for record in data['water_records'])

    overeating_matches = re.findall(OVEREATING_PATTERN, content, re.IGNORECASE)
    data['overeating_factor'] = 1.25 if overeating_matches else 1.0

    steps_match = re.search(
        rf'(?:{alias_pattern(STEP_LABEL_ALIASES)})\s*[:：]\s*([\d,]+)\s*{STEP_UNIT_PATTERN}?',
        content,
        re.IGNORECASE,
    )
    if steps_match:
        data['steps'] = int(steps_match.group(1).replace(',', ''))

    symptom_source = '\n'.join(data['symptoms'])
    data['symptom_keywords'] = [keyword for keyword in SYMPTOM_KEYWORDS if keyword.lower() in symptom_source.lower()]

    data['total_calories'] = sum(m.get('total_calories', 0) for m in data['meals'])
    data['total_protein'] = sum(m.get('total_protein', 0) for m in data['meals'])
    data['total_fat'] = sum(m.get('total_fat', 0) for m in data['meals'])
    data['total_carb'] = sum(m.get('total_carb', 0) for m in data['meals'])
    data['total_fiber'] = sum(m.get('total_fiber', 0) for m in data['meals'])

    return data

# ==================== AI insight generation ====================
def resolve_openclaw_binary():
    """Resolve the OpenClaw executable even in cron-like shells with a minimal PATH."""
    candidates = []

    configured = str(os.environ.get("OPENCLAW_BIN", "") or "").strip()
    if configured:
        candidates.append(configured)

    for binary_name in ("openclaw", "openclaw.cmd", "openclaw.exe"):
        resolved = shutil.which(binary_name)
        if resolved:
            candidates.append(resolved)

    home_dir = str(Path.home())
    fallback_patterns = [
        "/root/.nvm/versions/node/*/bin/openclaw",
        "/home/*/.nvm/versions/node/*/bin/openclaw",
        f"{home_dir}/.nvm/versions/node/*/bin/openclaw",
        "/usr/local/bin/openclaw",
        "/usr/bin/openclaw",
        "C:/Program Files/nodejs/openclaw.cmd",
        "C:/Program Files/nodejs/openclaw.exe",
    ]
    for pattern in fallback_patterns:
        for match in sorted(glob.glob(pattern), reverse=True):
            candidates.append(match)

    seen = set()
    for candidate in candidates:
        normalized = str(candidate or "").strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        if os.path.isfile(normalized):
            return normalized
    return None


LOCAL_LLM_LOG_PREFIXES = ("[plugins]", "[adp-", "[qqbot-", "[openclaw")
LOCAL_LLM_LOG_PHRASES = (
    "register() called - starting plugin registration",
    "registering tool factory:",
    "tool adp_upload_file registered successfully",
    "plugin registration complete",
    "no qqbot accounts configured, skipping",
    "registered qqbot remind tool",
)
LOCAL_LLM_INLINE_LOG_PATTERNS = (
    r"\[adp-openclaw\]\s*register\(\)\s*called\s*-\s*starting plugin registration",
    r"\[adp-openclaw\]\s*registering tool factory:\s*adp_upload_file",
    r"\[adp-openclaw\]\s*tool adp_upload_file registered successfully",
    r"\[adp-openclaw\]\s*plugin registration complete",
    r"\[qqbot-channel-api\]\s*no qqbot accounts configured,\s*skipping",
    r"\[qqbot-remind\]\s*registered qqbot remind tool",
)
LOCAL_LLM_SECTION_MARKERS = (
    "【做得很好的地方】",
    "【需要关注的隐患】",
    "【核心发现】",
    "【体态与习惯预警】",
    "【次月高阶干预清单】",
    "【下周调整】",
    "【下周干预方案】",
    "【主要な発見】",
    "【注意点】",
    "【次月アクションチェックリスト】",
    "[What Went Well]",
    "[Watchouts]",
    "[Core Findings]",
    "[Body & Habit Alerts]",
    "[Advanced Next-Month Checklist]",
)


def sanitize_local_llm_output(text):
    raw = str(text or "")
    if not raw:
        return ""

    cleaned = raw.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", cleaned)

    for pattern in LOCAL_LLM_INLINE_LOG_PATTERNS:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)

    cleaned = re.sub(
        r"(?<!\n)(\[(?:plugins|adp-[^\]]+|qqbot-[^\]]+|openclaw[^\]]*)\])",
        r"\n\1",
        cleaned,
        flags=re.IGNORECASE,
    )
    for marker in LOCAL_LLM_SECTION_MARKERS:
        cleaned = cleaned.replace(marker, f"\n{marker}")
    cleaned = re.sub(r"([】\]])\s*-\s*", r"\1\n- ", cleaned)
    cleaned = re.sub(
        r"(?<!\n)\s+-\s+(?=(?:\d+[.)]\s*)?[A-Za-z\u4e00-\u9fff])",
        "\n- ",
        cleaned,
    )

    lines = []
    for raw_line in cleaned.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        if lowered.startswith(LOCAL_LLM_LOG_PREFIXES):
            continue
        if any(phrase in lowered for phrase in LOCAL_LLM_LOG_PHRASES):
            continue
        lines.append(line)

    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned).strip()
    return cleaned


def run_local_llm(prompt, system_prompt, settings, locale, timeout_key, failure_key):
    mode = str(settings.get("mode", "hybrid")).strip().lower()
    if mode == "local_only":
        return None

    openclaw_bin = resolve_openclaw_binary()
    if not openclaw_bin:
        return None

    max_attempts = max(1, int(safe_float(settings.get("max_attempts", 3), 3)))
    timeout_seconds = max(30, int(safe_float(settings.get("timeout_seconds", 90), 90)))

    for attempt in range(max_attempts):
        try:
            result = subprocess.run(
                [openclaw_bin, 'agent', '--local', '--to', '+860000000000', '--message', prompt],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env={**os.environ, 'SYSTEM_PROMPT': system_prompt},
            )
            if result.returncode == 0 and result.stdout.strip():
                output = sanitize_local_llm_output(result.stdout)
                if output:
                    return output
        except subprocess.TimeoutExpired:
            print(t(locale, timeout_key, attempt=attempt + 1), file=sys.stderr)
        except Exception as e:
            print(t(locale, failure_key, attempt=attempt + 1, error=e), file=sys.stderr)
        if attempt < max_attempts - 1:
            import time
            time.sleep(2)

    return None


SEARCH_NOISE_TERMS = (
    "返回顶部按钮",
    "返回顶部",
    "倍速",
    "播放",
    "收藏",
    "分享",
    "关注",
    "交流",
    "视频",
    "门诊好评",
    "累计挂号",
    "精选内容",
    "点击展开",
    "展开全文",
    "阅读全文",
    "相关推荐",
    "立即预约",
    "在线问诊",
    "广告",
)
SEARCH_BAD_PATTERNS = (
    r"(?:\[\d+\]){2,}",
    r"(?:表|图)\s*\d",
    r"(?:Table|Figure)\s*\d",
    r"注释[:：]",
    r"\bDOI\b",
    r"\bet al\.\b",
    r"[Α-Ωα-ω]",
    r"[Ѐ-ӿ]",
)


def strip_search_noise(text):
    raw = str(text or "")
    if not raw:
        return ""
    raw = re.sub(r"https?://\S+|www\.\S+", "", raw)
    raw = re.sub(r"(?:\b\d+:\d+\b\s*){1,3}", " ", raw)
    raw = re.sub(r"^\s*(?:\d+[.)、]\s*)+", "", raw)
    raw = re.sub(r"^\s*\d+\s+", "", raw)
    raw = re.sub(r"\[\d+\]", "", raw)
    raw = re.sub(r"(?:表|图|Table|Figure)\s*[-\d.]+", " ", raw, flags=re.IGNORECASE)
    raw = re.sub("|".join(re.escape(term) for term in SEARCH_NOISE_TERMS), " ", raw, flags=re.IGNORECASE)
    raw = re.sub(r"[|<>#@]+", " ", raw)
    raw = re.sub(r"[•·]{2,}", " ", raw)
    raw = re.sub(r"[.。…]{4,}", "…", raw)
    raw = re.sub(r"\s+", " ", raw).strip(" |，,.;；、-")
    return raw


def matches_search_locale(text, locale):
    cleaned = str(text or "").strip()
    if not cleaned:
        return False
    locale = resolve_locale(locale=locale)
    if locale == "zh-CN":
        return len(re.findall(r"[\u4e00-\u9fff]", cleaned)) >= 8
    if locale == "ja-JP":
        return bool(re.search(r"[\u3040-\u30ff]", cleaned)) or len(re.findall(r"[\u4e00-\u9fff]", cleaned)) >= 6
    return len(re.findall(r"[A-Za-z]{3,}", cleaned)) >= 5


def has_actionable_health_keywords(text, locale):
    cleaned = str(text or "")
    zh_keywords = ("低脂", "脂肪", "纤维", "饮水", "补水", "运动", "步行", "步数", "症状", "用药", "体重", "血压", "血糖", "胆", "蔬菜", "豆类", "粗粮")
    ja_keywords = ("低脂質", "脂質", "食物繊維", "飲水", "補水", "運動", "散歩", "歩数", "症状", "服薬", "体重", "血圧", "血糖", "胆", "野菜", "豆類", "全粒穀物")
    en_keywords = ("low-fat", "fat", "fiber", "hydration", "water", "exercise", "walk", "steps", "symptom", "medication", "weight", "blood pressure", "glucose", "vegetable", "whole grain")
    resolved = resolve_locale(locale=locale)
    if resolved == "zh-CN":
        return any(keyword in cleaned for keyword in zh_keywords)
    if resolved == "ja-JP":
        return any(keyword in cleaned for keyword in ja_keywords)
    lowered = cleaned.lower()
    return any(keyword in lowered for keyword in en_keywords)


def has_recipe_guidance_keywords(text, locale):
    cleaned = str(text or "")
    zh_keywords = ("低脂", "纤维", "蔬菜", "豆类", "粗粮", "蛋白", "清蒸", "少油", "饱腹")
    ja_keywords = ("低脂質", "食物繊維", "野菜", "豆類", "全粒穀物", "たんぱく質", "蒸し", "油控えめ", "満腹感")
    en_keywords = ("low-fat", "fiber", "vegetable", "beans", "whole grain", "protein", "steam", "low oil", "satiety")
    resolved = resolve_locale(locale=locale)
    if resolved == "zh-CN":
        return any(keyword in cleaned for keyword in zh_keywords)
    if resolved == "ja-JP":
        return any(keyword in cleaned for keyword in ja_keywords)
    lowered = cleaned.lower()
    return any(keyword in lowered for keyword in en_keywords)


def has_exercise_guidance_keywords(text, locale):
    cleaned = str(text or "")
    zh_keywords = ("步行", "快走", "运动", "活动", "骑行", "拉伸", "饭后")
    ja_keywords = ("散歩", "早歩き", "運動", "活動", "サイクリング", "ストレッチ", "食後")
    en_keywords = ("walk", "exercise", "activity", "cycling", "stretch", "after dinner")
    resolved = resolve_locale(locale=locale)
    if resolved == "zh-CN":
        return any(keyword in cleaned for keyword in zh_keywords)
    if resolved == "ja-JP":
        return any(keyword in cleaned for keyword in ja_keywords)
    lowered = cleaned.lower()
    return any(keyword in lowered for keyword in en_keywords)


def is_readable_search_excerpt(text, locale):
    cleaned_text = strip_search_noise(text)
    if not cleaned_text:
        return False
    if cleaned_text.lstrip().startswith(("+", "•")):
        return False
    if cleaned_text.rstrip().endswith(("e.g.", "e.g", "for example", "for exampl…")):
        return False
    compact = re.sub(r"\s+", "", cleaned_text)
    if len(compact) < 14:
        return False
    if any(re.search(pattern, cleaned_text, re.IGNORECASE) for pattern in SEARCH_BAD_PATTERNS):
        return False
    useful_chars = len(re.findall(r"[A-Za-z0-9\u4e00-\u9fff]", compact))
    weird_chars = len(re.findall(r"[^A-Za-z0-9\u4e00-\u9fff.,;:!?%()（）/+℃ \\-]", cleaned_text))
    if useful_chars / max(1, len(compact)) < 0.62:
        return False
    if weird_chars > max(3, len(compact) // 16):
        return False
    if re.search(r"(?:\b\d{2,3}\b[\s,.;]*){3,}", cleaned_text):
        return False
    if len(re.findall(r"[，、, ]", cleaned_text)) >= 6 and not re.search(r"[。！？.!?；;:：]", cleaned_text):
        return False
    if re.search(r"(好评率|接诊量|平均响应|福報購|人間福報|蔬食譜|蔬知識|蔬新聞|蔬視頻)", cleaned_text, re.IGNORECASE):
        return False
    if not has_actionable_health_keywords(cleaned_text, locale):
        return False
    return matches_search_locale(cleaned_text, locale)


def clean_search_excerpt(text, locale, max_length=140):
    raw = strip_search_noise(text)
    if not raw:
        return ""

    parts = []
    for sentence in re.split(r"(?<=[。！？!?])\s+|(?<=[.;；])\s+", raw):
        candidate = sentence.strip(" -")
        if not candidate:
            continue
        if is_readable_search_excerpt(candidate, locale):
            if len(candidate) <= max_length:
                return candidate
            parts.append(candidate)

    if is_readable_search_excerpt(raw, locale):
        parts.append(raw)

    if not parts:
        return ""
    clipped = parts[0][: max_length - 1].rstrip(" ,.;，；、")
    return clipped + ("…" if len(parts[0]) > max_length else "")


def generate_ai_comment(health_data, config):
    """Generate an AI insight, with a local fallback when LLM is unavailable."""
    locale = resolve_locale(config)
    user_profile = config.get('user_profile', {})
    conditions = get_profile_conditions(user_profile)
    primary_condition = get_primary_condition(user_profile)
    user_name = localize_free_text(locale, user_profile.get('name', t(locale, 'default_user')))
    condition_text = get_conditions_display_name(locale, conditions)
    standards = get_condition_standards(config, conditions)

    fat_min, fat_max = standards.get('fat_min_g', 40), standards.get('fat_max_g', 50)
    fiber_min = standards.get('fiber_min_g', 25)
    prompt_context = {
        'user_name': user_name,
        'condition_name': condition_text,
        'diet_principle': build_multi_condition_tip(locale, conditions, standards),
        'calories': health_data.get('total_calories', 0),
        'protein': health_data.get('total_protein', 0),
        'fat': health_data.get('total_fat', 0),
        'fat_min': fat_min,
        'fat_max': fat_max,
        'carb': health_data.get('total_carb', 0),
        'fiber': health_data.get('total_fiber', 0),
        'fiber_min': fiber_min,
        'water_total': health_data.get('water_total', 0),
        'water_target': health_data.get('water_target', user_profile.get('water_target_ml', 2000)),
        'exercise_count': len(health_data.get('exercise_records', [])),
        'steps': health_data.get('steps', 0),
        'overeating_factor': health_data.get('overeating_factor', 1.0),
        'symptom_keywords': health_data.get('symptom_keywords', []),
    }
    prompt = build_ai_comment_prompt(locale, prompt_context)
    if locale == "zh-CN":
        prompt += (
            "\n\n[排版要求]\n"
            "请优先使用下面的结构输出，不要写成一整段：\n"
            "【做得很好的地方】\n"
            "- xxx\n"
            "- xxx\n"
            "【需要关注的隐患】\n"
            "- xxx\n"
            "- xxx\n"
            "每条都要结合当天数据，避免空泛表述。"
        )
    elif locale == "ja-JP":
        prompt += (
            "\n\n[出力フォーマット]\n"
            "長い一段落ではなく、次の構成を優先してください:\n"
            "【良かった点】\n"
            "- xxx\n"
            "- xxx\n"
            "【注意点】\n"
            "- xxx\n"
            "- xxx\n"
            "各項目は必ず当日の実データに基づいてください。"
        )
    else:
        prompt += (
            "\n\n[Formatting requirement]\n"
            "Prefer this structure instead of a dense paragraph:\n"
            "[What Went Well]\n"
            "- xxx\n"
            "- xxx\n"
            "[Watchouts]\n"
            "- xxx\n"
            "- xxx\n"
            "Each bullet must be grounded in today's actual data."
        )
    settings = get_generation_settings(config, "expert_commentary")
    output = run_local_llm(
        prompt=prompt,
        system_prompt=build_ai_comment_system_prompt(locale, primary_condition),
        settings=settings,
        locale=locale,
        timeout_key="ai_comment_timeout",
        failure_key="ai_comment_failed",
    )
    if output:
        return output, "llm"

    comments = []
    fat_val = health_data.get('total_fat', 0)
    if fat_min <= fat_val <= fat_max:
        comments.append(t(locale, "fallback_comment_fat_ok", value=fat_val))
    elif fat_val < fat_min:
        comments.append(t(locale, "fallback_comment_fat_low", value=fat_val))
    else:
        comments.append(t(locale, "fallback_comment_fat_high", value=fat_val))

    fiber_val = health_data.get('total_fiber', 0)
    if fiber_val >= fiber_min:
        comments.append(t(locale, "fallback_comment_fiber_ok", value=fiber_val))
    else:
        comments.append(t(locale, "fallback_comment_fiber_low", value=fiber_val))

    water_val = health_data.get('water_total', 0)
    water_target = health_data.get('water_target', user_profile.get('water_target_ml', 2000))
    if water_val >= water_target:
        comments.append(t(locale, "fallback_comment_water_ok", value=water_val))
    else:
        comments.append(t(locale, "fallback_comment_water_low", value=water_val, target=water_target))

    steps = health_data.get('steps', 0)
    if steps >= 6000:
        comments.append(t(locale, "fallback_comment_steps_high", value=steps))
    elif steps >= 3000:
        comments.append(t(locale, "fallback_comment_steps_mid", value=steps))
    else:
        comments.append(t(locale, "fallback_comment_steps_low", value=steps))

    if has_tavily_api_key(config):
        if locale == "zh-CN":
            query = f"{condition_text} 患者教育 低脂 饮水 膳食纤维 运动 日常管理"
        elif locale == "ja-JP":
            query = f"{condition_text} 患者教育 低脂質 飲水 食物繊維 運動 日常管理"
        else:
            query = f"{condition_text} patient education low-fat hydration fiber activity daily care"
        tavily_results = tavily_search(query, max_results=2, config=config)
        references = []
        for result in tavily_results:
            content = clean_search_excerpt(str(result.get('content', '') or ''), locale, max_length=120)
            if locale == "ja-JP" and content and not re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", content):
                continue
            if content:
                references.append(content)
        if references:
            if locale == "zh-CN":
                lead = "外部资料补充："
            elif locale == "ja-JP":
                lead = "外部参考："
            else:
                lead = "External note: "
            comments.append(lead + " ".join(references[:2]))
            return " ".join(comments), "fallback_tavily"

    return " ".join(comments), "fallback"

# ==================== AI next-day planning ====================
def tavily_search(query, max_results=3, config=None):
    """Call Tavily for external context when the API key is available."""
    import urllib.request
    url = "https://api.tavily.com/search"
    api_key = get_tavily_api_key(config)
    if not api_key:
        return []

    for attempt in range(3):
        try:
            data = json.dumps({
                "api_key": api_key,
                "query": query,
                "search_depth": "basic",
                "max_results": max_results
            }).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            resp = urllib.request.urlopen(req, timeout=60)
            result = json.loads(resp.read().decode('utf-8'))
            return result.get('results', [])
        except Exception as e:
            print(t(None, "tavily_failed", attempt=attempt + 1, error=e), file=sys.stderr)
            if attempt < 2:
                import time
                time.sleep(2)
    return []

def generate_ai_plan(health_data, config):
    """Generate the next-day plan with bilingual prompts and a local fallback."""
    locale = resolve_locale(config)
    user_profile = config.get('user_profile', {})
    conditions = get_profile_conditions(user_profile)
    primary_condition = get_primary_condition(user_profile)
    condition_text = get_conditions_display_name(locale, conditions)
    standards = get_condition_standards(config, conditions)
    fat_min, fat_max = standards.get('fat_min_g', 40), standards.get('fat_max_g', 50)
    fiber_min = standards.get('fiber_min_g', 25)

    shortcomings = []
    fat_val = health_data.get('total_fat', 0)
    fiber_val = health_data.get('total_fiber', 0)
    water_val = health_data.get('water_total', 0)
    steps = health_data.get('steps', 0)

    if fat_val < fat_min * 0.8:
        shortcomings.append(t(locale, "shortcoming_fat_low"))
    elif fat_val > fat_max:
        shortcomings.append(t(locale, "shortcoming_fat_high"))
    if fiber_val < fiber_min * 0.8:
        shortcomings.append(t(locale, "shortcoming_fiber_low"))
    water_threshold = user_profile.get('water_target_ml', health_data.get('water_target', 2000)) * 0.75
    if water_val < water_threshold:
        shortcomings.append(t(locale, "shortcoming_water_low"))
    if steps < 3000:
        shortcomings.append(t(locale, "shortcoming_exercise_low"))

    recipes = []
    exercises = []

    if has_tavily_api_key(config) and any(item in shortcomings for item in [t(locale, "shortcoming_fat_low"), t(locale, "shortcoming_fat_high")]):
        if locale == "zh-CN":
            recipe_query = localized_recipe_query(locale, condition_text) + " 患者教育"
        elif locale == "ja-JP":
            recipe_query = localized_recipe_query(locale, condition_text) + " 患者教育"
        else:
            recipe_query = localized_recipe_query(locale, condition_text) + " patient education"
        recipe_results = tavily_search(recipe_query, max_results=2, config=config)
        recipes = [
            clean_search_excerpt(r.get('content', ''), locale, max_length=120)
            for r in recipe_results[:2]
        ]
        recipes = [item for item in recipes if item and has_recipe_guidance_keywords(item, locale)]

    if has_tavily_api_key(config) and t(locale, "shortcoming_exercise_low") in shortcomings:
        if locale == "zh-CN":
            exercise_query = localized_exercise_query(locale, condition_text) + " 患者教育"
        elif locale == "ja-JP":
            exercise_query = localized_exercise_query(locale, condition_text) + " 患者教育"
        else:
            exercise_query = localized_exercise_query(locale, condition_text) + " patient education"
        exercise_results = tavily_search(exercise_query, max_results=2, config=config)
        exercises = [
            clean_search_excerpt(r.get('content', ''), locale, max_length=120)
            for r in exercise_results[:2]
        ]
        exercises = [item for item in exercises if item and has_exercise_guidance_keywords(item, locale)]

    preferences = user_profile.get('dietary_preferences', {})
    localized_dislike = localize_profile_list(locale, preferences.get('dislike', []))
    localized_allergies = localize_profile_list(locale, preferences.get('allergies', []))
    localized_fruits = localize_profile_list(locale, preferences.get('favorite_fruits', []))
    prompt = build_ai_plan_prompt(
        locale,
        {
            'user_name': localize_free_text(locale, user_profile.get('name', t(locale, 'default_user'))),
            'condition_name': condition_text,
            'diet_principle': build_multi_condition_tip(locale, conditions, standards),
            'avoid_foods': ', '.join(localized_dislike + localized_allergies),
            'favorite_fruits': ', '.join(localized_fruits),
            'shortcomings': shortcomings,
            'recipe_reference': recipes[:1] if recipes else ('なし' if locale == "ja-JP" else 'none'),
            'exercise_reference': exercises[:1] if exercises else ('なし' if locale == "ja-JP" else 'none'),
        },
    )
    if locale == "zh-CN":
        prompt += (
            "\n\n[输出强化]\n"
            "diet、water、exercise 三个数组中的每个项目都尽量带明确时间段，"
            "适合第二天直接照着执行。"
        )
    elif locale == "ja-JP":
        prompt += (
            "\n\n[出力強化]\n"
            "diet・water・exercise の各項目には、できるだけ具体的な時間帯を入れてください。"
            "翌日にそのまま実行できるチェックリスト形式を優先します。"
        )
    else:
        prompt += (
            "\n\n[Output refinement]\n"
            "Each item in diet, water, and exercise should include a clear time block when possible,"
            " so it reads like a next-day checklist."
        )
    settings = get_generation_settings(config, "next_day_plan")
    output = run_local_llm(
        prompt=prompt,
        system_prompt=build_ai_plan_system_prompt(locale),
        settings=settings,
        locale=locale,
        timeout_key="ai_plan_timeout",
        failure_key="ai_plan_failed",
    )
    if output:
        try:
            json_match = re.search(r'\{.*\}', output, re.DOTALL)
            if json_match:
                return json.loads(json_match.group()), "llm"
        except Exception as e:
            print(t(locale, "ai_plan_failed", attempt=1, error=e), file=sys.stderr)

    target_water = int(user_profile.get('water_target_ml', health_data.get('water_target', 2000)) or 2000)
    favorite_fruits = localized_fruits
    is_zh = locale == "zh-CN"
    is_ja = locale == "ja-JP"
    fruit_text = favorite_fruits[0] if favorite_fruits else ("苹果" if is_zh else "りんご" if is_ja else "apple")
    avoid_foods = localized_dislike + localized_allergies
    avoid_text = "、".join(avoid_foods[:2]) if is_zh or is_ja else ", ".join(avoid_foods[:2])
    water_split = [max(200, round(target_water * ratio / 100 / 50) * 50) for ratio in [15, 20, 25, 20, 20]]
    breakfast_base = "燕麦粥 + 水煮蛋 + " + fruit_text if is_zh else f"オートミール + ゆで卵 + {fruit_text}" if is_ja else f"oatmeal + boiled egg + {fruit_text}"
    lunch_base = "杂粮饭 + 鸡胸肉 + 两份蔬菜" if is_zh else "雑穀ご飯 + 鶏むね肉 + 野菜2品" if is_ja else "mixed grains + chicken breast + two servings of vegetables"
    dinner_base = "豆腐/鱼肉 + 绿叶菜 + 少量主食" if is_zh else "豆腐または白身魚 + 葉物野菜 + 少量の主食" if is_ja else "tofu or fish + leafy vegetables + a small portion of carbs"
    if t(locale, "shortcoming_fat_low") in shortcomings:
        breakfast_base += " + 一小把坚果" if is_zh else " + 少量のナッツ" if is_ja else " + a small handful of nuts"
    if t(locale, "shortcoming_fat_high") in shortcomings:
        lunch_base = "清蒸蛋白质 + 焯蔬菜 + 少油主食" if is_zh else "蒸し調理のたんぱく質 + 温野菜 + 低脂質の主食" if is_ja else "lean steamed protein + blanched vegetables + low-oil carbs"
    if t(locale, "shortcoming_fiber_low") in shortcomings:
        dinner_base += "，并增加豆类或菌菇" if is_zh else "、豆類かきのこを追加" if is_ja else ", plus beans or mushrooms for extra fiber"
    if avoid_text:
        dinner_base += f"（避开 {avoid_text}）" if is_zh else f"（{avoid_text} は避ける）" if is_ja else f" (avoid {avoid_text})"

    plan = {
        "diet": [
            {"time": "07:30-08:30", "meal": "早餐" if is_zh else "朝食" if is_ja else "Breakfast", "menu": breakfast_base, "calories": 320, "fat": 8 if t(locale, "shortcoming_fat_low") in shortcomings else 6, "fiber": 7},
            {"time": "12:00-13:00", "meal": "午餐" if is_zh else "昼食" if is_ja else "Lunch", "menu": lunch_base, "calories": 480, "fat": 10 if t(locale, "shortcoming_fat_high") not in shortcomings else 7, "fiber": 8},
            {"time": "18:00-19:00", "meal": "晚餐" if is_zh else "夕食" if is_ja else "Dinner", "menu": dinner_base, "calories": 420, "fat": 9 if t(locale, "shortcoming_fat_low") in shortcomings else 6, "fiber": 9 if t(locale, "shortcoming_fiber_low") in shortcomings else 6},
        ],
        "water": [
            {"time": "07:00-08:00", "amount": f"{water_split[0]}ml", "note": "晨起先补水" if is_zh else "起床後にまず補水" if is_ja else "Hydrate after waking"},
            {"time": "10:00-11:00", "amount": f"{water_split[1]}ml", "note": "上午工作间隙" if is_zh else "午前の小休憩で補水" if is_ja else "Mid-morning refill"},
            {"time": "13:30-14:30", "amount": f"{water_split[2]}ml", "note": "午后补水" if is_zh else "午後の補水" if is_ja else "Afternoon hydration"},
            {"time": "17:00-18:00", "amount": f"{water_split[3]}ml", "note": "下班前完成一轮" if is_zh else "夕方までにもう1回" if is_ja else "Finish another round before evening"},
            {"time": "20:00-21:00", "amount": f"{water_split[4]}ml", "note": "睡前不过量" if is_zh else "就寝前は飲み過ぎない" if is_ja else "Top up without overdrinking before bed"},
        ],
        "exercise": [
            {
                "time": "晚饭后" if is_zh else "夕食後" if is_ja else "After dinner",
                "activity": "快走" if is_zh else "早歩き" if is_ja else "Brisk walk",
                "duration": "20-30分钟" if is_zh else "20-30分" if is_ja else "20-30 minutes",
                "details": "目标补足步数并帮助消化" if is_zh else "歩数を補い、消化を助ける目的" if is_ja else "Use it to recover steps and support digestion",
            }
        ],
        "notes": [
            ("今日重点围绕 " if is_zh else "明日の重点: " if is_ja else "Tomorrow should focus on ")
            + condition_text
        ],
    }
    if health_data.get('overeating_factor', 1.0) > 1.0:
        plan['notes'].append(t(locale, "fallback_note_overeat"))
    if t(locale, "shortcoming_fat_low") in shortcomings:
        plan['notes'].append(t(locale, "fallback_note_fat_low"))
    elif t(locale, "shortcoming_fat_high") in shortcomings:
        plan['notes'].append(t(locale, "fallback_note_fat_high"))
    if t(locale, "shortcoming_fiber_low") in shortcomings:
        plan['notes'].append(t(locale, "fallback_note_fiber_low"))
    if t(locale, "shortcoming_exercise_low") in shortcomings:
        plan['notes'].append(t(locale, "fallback_note_exercise_low"))
    if recipes:
        if locale == "zh-CN":
            note_prefix = "检索建议："
        elif locale == "ja-JP":
            note_prefix = "外部参考："
        else:
            note_prefix = "Search note: "
        plan['notes'].append(note_prefix + recipes[0])
    if exercises:
        if locale == "zh-CN":
            exercise_prefix = "运动参考："
        elif locale == "ja-JP":
            exercise_prefix = "運動メモ："
        else:
            exercise_prefix = "Exercise note: "
        plan['notes'].append(exercise_prefix + exercises[0])
    return plan, "fallback_tavily" if recipes or exercises else "fallback"

def get_star_string(score):
    stars_count = max(1, min(5, int(score / 20)))
    return "\u2605" * stars_count


def find_custom_section_items(custom_sections, section_title):
    target = normalize_section_name(section_title)
    for header, items in (custom_sections or {}).items():
        if normalize_section_name(header) == target:
            return items
    return []


def build_module_detail_text(locale, module_id, info):
    locale = resolve_locale(locale=locale)
    if module_id == "diet":
        return info.get("fat_status", "")
    if module_id == "water":
        return t(locale, 'completion_status', current=info.get('water_total', 0), target=info.get('water_target', 0), percent=info.get('water_percent', 0))
    if module_id == "weight":
        return t(locale, 'weight_status', weight=format_weight(locale, info.get('weight_value', info.get('weight'))), bmi=info.get('bmi', 0))
    if module_id == "symptom":
        symptoms = info.get("symptoms", [])
        return t(locale, "no_symptoms") if not symptoms else t(locale, "symptoms_prefix", symptoms='; '.join(symptoms))
    if module_id == "exercise":
        return info.get("exercise_summary", t(locale, 'no_record'))
    if module_id == "adherence":
        return info.get("adherence_status", "")
    if info.get("present"):
        if locale == "zh-CN":
            return "\u5df2\u8bb0\u5f55"
        if locale == "ja-JP":
            return "記録あり"
        return "Recorded"
    if locale == "zh-CN":
        return "\u672a\u8bb0\u5f55"
    if locale == "ja-JP":
        return "未記録"
    return "Not recorded"


def build_module_status(locale, module_id, info):
    locale = resolve_locale(locale=locale)
    if module_id == "diet":
        return t(locale, 'achieved') if info.get('raw', 0) >= 80 else t(locale, 'needs_improvement')
    if module_id == "water":
        return t(locale, 'achieved') if info.get('raw', 0) >= 100 else t(locale, 'under_target')
    if module_id == "weight":
        bmi = info.get('bmi', 0)
        return t(locale, 'normal') if bmi and 18.5 <= bmi < 24 else t(locale, 'attention')
    if module_id == "symptom":
        return t(locale, 'symptom_free') if not info.get('has_symptoms') else t(locale, 'has_symptoms')
    if module_id == "exercise":
        return t(locale, 'achieved') if info.get('raw', 0) >= 60 else t(locale, 'needs_boost')
    if module_id == "adherence":
        return t(locale, 'excellent') if info.get('raw', 0) >= 80 else t(locale, 'fair')
    if info.get("present"):
        return "\u5df2\u8bb0\u5f55" if locale == "zh-CN" else "Recorded"
    return "\u672a\u8bb0\u5f55" if locale == "zh-CN" else "Missing"


def build_score_report(health_data, config):
    locale = resolve_locale(config)
    user_profile = config.get('user_profile', {})
    conditions = get_profile_conditions(user_profile)
    standards = get_condition_standards(config, conditions)
    scoring_standards = config.get('scoring_standards', {})
    exercise_standards = config.get('exercise_standards', {})

    water_target = health_data.get('water_target', user_profile.get('water_target_ml', 2000))
    water_target = water_target if water_target > 0 else user_profile.get('water_target_ml', 2000) or 2000
    diet_score = calculate_diet_score(health_data, standards, scoring_standards)
    water_score = calculate_water_score(health_data.get('water_total', 0), water_target)
    weight_score = calculate_weight_score(
        health_data.get('weight_morning') is not None,
        user_profile.get('target_weight_kg', 64),
        health_data.get('weight_morning'),
    )
    exercise_score = calculate_exercise_score(
        health_data.get('exercise_records', []),
        health_data.get('steps', 0),
        exercise_standards,
        scoring_standards,
    )
    symptom_score = calculate_symptom_score(health_data.get('symptom_keywords', []))
    adherence_score = calculate_adherence_score(health_data, water_target)
    medication_score = calculate_section_presence_score(health_data.get('medication_records', []))

    weight_kg = health_data.get('weight_morning')
    bmi = calculate_bmi(weight_kg, user_profile.get('height_cm', 172)) if weight_kg else 0

    fat_min, fat_max = standards.get('fat_min_g', 40), standards.get('fat_max_g', 50)
    fat_val = health_data.get('total_fat', 0)
    if fat_val > fat_max:
        fat_status = t(locale, 'fat_high', value=fat_val)
    elif fat_val < fat_min:
        fat_status = t(locale, 'fat_low', value=fat_val)
    else:
        fat_status = t(locale, 'fat_in_range')

    builtin_info = {
        'diet': {
            'raw': diet_score,
            'fat_status': fat_status,
        },
        'water': {
            'raw': water_score,
            'water_total': health_data.get('water_total', 0),
            'water_target': water_target,
            'water_percent': int(health_data.get('water_total', 0) * 100 // max(1, water_target)),
        },
        'weight': {
            'raw': weight_score,
            'weight_value': health_data.get('weight_morning'),
            'bmi': bmi,
        },
        'symptom': {
            'raw': symptom_score,
            'symptoms': health_data.get('symptom_keywords', []),
            'has_symptoms': bool(health_data.get('symptom_keywords')),
        },
        'exercise': {
            'raw': exercise_score,
            'exercise_summary': generate_exercise_summary(health_data, locale),
        },
        'adherence': {
            'raw': adherence_score,
            'adherence_status': t(
                locale,
                'adherence_status',
                meals=len(health_data.get('meals', [])),
                water_status=t(locale, 'water_goal_met') if health_data.get('water_total', 0) >= water_target else t(locale, 'water_goal_not_met'),
            ),
        },
        'medication': {
            'raw': medication_score,
            'present': bool(health_data.get('medication_records')),
            'items': health_data.get('medication_records', []),
        },
    }

    score_modules = []
    for module in get_scoring_modules(config):
        if not module.get('enabled', True):
            continue

        if module.get('type') == 'builtin':
            module_info = dict(builtin_info.get(module['id'], {'raw': 0}))
        else:
            if module['id'] == 'medication':
                items = health_data.get('medication_records', [])
            else:
                items = find_custom_section_items(health_data.get('custom_sections', {}), module.get('section_title', module.get('title', '')))
            module_info = {
                'raw': calculate_section_presence_score(
                    items,
                    present_score=safe_float(module.get('score_when_present', 100), 100),
                    missing_score=safe_float(module.get('score_when_missing', 0), 0),
                ),
                'present': bool(items),
                'items': items,
            }

        module_info.update({
            'id': module['id'],
            'type': module.get('type', 'builtin'),
            'title': module.get('title') or default_module_title(locale, module['id']),
            'weight': safe_float(module.get('weight', 0), 0),
        })
        module_info['stars'] = get_star_string(module_info.get('raw', 0))
        module_info['status'] = build_module_status(locale, module['id'], module_info)
        module_info['detail_text'] = build_module_detail_text(locale, module['id'], module_info)
        score_modules.append(module_info)

    positive_modules = [module for module in score_modules if module.get('weight', 0) > 0]
    if positive_modules:
        weight_total = sum(module['weight'] for module in positive_modules)
        for module in score_modules:
            module['normalized_weight'] = round(module['weight'] / weight_total, 6) if module.get('weight', 0) > 0 else 0
        total_score = round(sum(module['raw'] * module['normalized_weight'] for module in positive_modules), 1)
    elif score_modules:
        equal_weight = round(1 / len(score_modules), 6)
        for module in score_modules:
            module['normalized_weight'] = equal_weight
        total_score = round(sum(module['raw'] * module['normalized_weight'] for module in score_modules), 1)
    else:
        total_score = 0

    return {
        'modules': score_modules,
        'module_map': {module['id']: module for module in score_modules},
        'total': min(100, total_score),
        'total_stars': get_star_string(total_score),
        'bmi': bmi,
        'conditions': conditions,
        'condition_text': get_conditions_display_name(locale, conditions),
    }


def generate_risk_alerts(health_data, config):
    locale = resolve_locale(config)
    user_profile = config.get('user_profile', {})
    conditions = get_profile_conditions(user_profile)
    condition_text = get_conditions_display_name(locale, conditions)
    standards = get_condition_standards(config, conditions)
    water_target = health_data.get('water_target', user_profile.get('water_target_ml', 2000))
    water_target = water_target if water_target > 0 else user_profile.get('water_target_ml', 2000) or 2000
    risks = []

    def localize(zh_text, en_text, ja_text=None):
        return inline_localize(locale, zh_text, en_text, ja_text)

    fat_val = health_data.get('total_fat', 0)
    fat_min, fat_max = standards.get('fat_min_g', 40), standards.get('fat_max_g', 50)
    if fat_val > fat_max:
        risks.append({
            'level': localize('\u9ad8', 'High', '高'),
            'item': localize('\u8102\u80aa\u6444\u5165\u504f\u9ad8', 'Fat intake high', '脂質摂取が高め'),
            'risk': localize(
                f"\u4eca\u65e5\u8102\u80aa {fat_val:.1f}g\uff0c\u9ad8\u4e8e\u5efa\u8bae\u4e0a\u9650 {fat_max}g\u3002",
                f"Fat reached {fat_val:.1f}g today, above the suggested ceiling of {fat_max}g.",
                f"本日の脂質は {fat_val:.1f}g で、推奨上限 {fat_max}g を上回りました。",
            ),
            'action': localize('\u660e\u65e5\u51cf\u5c11\u6cb9\u70b8\u3001\u80a5\u8089\u3001\u5976\u6cb9\u548c\u91cd\u6cb9\u9171\u6c41\u3002', 'Cut fried food, fatty meat, cream, and oily sauces tomorrow.', '明日は揚げ物、脂身、クリーム、油の多いソースを控えてください。'),
        })
    elif fat_val < fat_min * 0.7:
        risks.append({
            'level': localize('\u4e2d', 'Medium', '中'),
            'item': localize('\u8102\u80aa\u6444\u5165\u504f\u4f4e', 'Fat intake low', '脂質摂取が少なめ'),
            'risk': localize(
                f"\u4eca\u65e5\u8102\u80aa\u4ec5 {fat_val:.1f}g\uff0c\u660e\u663e\u4f4e\u4e8e\u5efa\u8bae\u4e0b\u9650 {fat_min}g\u3002",
                f"Fat was only {fat_val:.1f}g today, well below the suggested floor of {fat_min}g.",
                f"本日の脂質は {fat_val:.1f}g にとどまり、推奨下限 {fat_min}g を大きく下回りました。",
            ),
            'action': localize('\u53ef\u9002\u91cf\u8865\u5145\u575a\u679c\u3001\u725b\u6cb9\u679c\u6216\u6a44\u6984\u6cb9\u7b49\u5065\u5eb7\u8102\u80aa\u3002', 'Add a moderate amount of healthy fats such as nuts, avocado, or olive oil.', 'ナッツ、アボカド、オリーブオイルなどの良質な脂質を少量追加してください。'),
        })

    fiber_val = health_data.get('total_fiber', 0)
    fiber_min = standards.get('fiber_min_g', 25)
    if fiber_val < fiber_min:
        risks.append({
            'level': localize('\u4e2d', 'Medium', '中'),
            'item': localize('\u81b3\u98df\u7ea4\u7ef4\u4e0d\u8db3', 'Fiber intake low', '食物繊維が不足'),
            'risk': localize(
                f"\u4eca\u65e5\u81b3\u98df\u7ea4\u7ef4 {fiber_val:.1f}g\uff0c\u4f4e\u4e8e\u5efa\u8bae\u503c {fiber_min}g\u3002",
                f"Fiber was {fiber_val:.1f}g today, below the recommended {fiber_min}g.",
                f"本日の食物繊維は {fiber_val:.1f}g で、推奨量 {fiber_min}g を下回りました。",
            ),
            'action': localize('\u660e\u65e5\u589e\u52a0\u6df1\u8272\u852c\u83dc\u3001\u8c46\u7c7b\u548c\u7c97\u7cae\u3002', 'Increase vegetables, beans, and whole grains tomorrow.', '明日は野菜、豆類、全粒穀物を意識して増やしてください。'),
        })

    water_val = health_data.get('water_total', 0)
    if water_val < water_target * 0.75:
        risks.append({
            'level': localize('\u4e2d', 'Medium', '中'),
            'item': localize('\u996e\u6c34\u4e0d\u8db3', 'Hydration low', '飲水量が不足'),
            'risk': localize(
                f"\u4eca\u65e5\u996e\u6c34 {water_val}ml\uff0c\u4f4e\u4e8e\u76ee\u6807 {water_target}ml \u7684 75%\u3002",
                f"Hydration was {water_val}ml today, below 75% of the {water_target}ml target.",
                f"本日の飲水量は {water_val}ml で、目標 {water_target}ml の 75% 未満でした。",
            ),
            'action': localize('\u628a\u996e\u6c34\u62c6\u6210 4-6 \u6b21\u5b8c\u6210\uff0c\u4f18\u5148\u5b89\u6392\u6668\u8d77\u548c\u5348\u540e\u8865\u6c34\u3002', 'Split water into 4-6 sessions, especially after waking and in the afternoon.', '飲水を 4〜6 回に分け、起床後と午後の補水を優先してください。'),
        })

    symptoms = health_data.get('symptom_keywords', [])
    if symptoms:
        symptom_text = '\u3001'.join(symptoms) if locale == 'zh-CN' else ', '.join(symptoms)
        risks.append({
            'level': localize('\u9ad8', 'High', '高'),
            'item': localize('\u75c7\u72b6\u8bb0\u5f55\u5f02\u5e38', 'Symptoms recorded', '症状の記録あり'),
            'risk': localize(
                f"\u4eca\u65e5\u8bb0\u5f55\u5230\u75c7\u72b6\uff1a{symptom_text}\u3002",
                f"Symptoms were recorded today: {symptom_text}.",
                f"本日は次の症状が記録されました: {symptom_text}。",
            ),
            'action': localize('\u82e5\u6301\u7eed\u6216\u52a0\u91cd\uff0c\u8bf7\u4f18\u5148\u4f11\u606f\u5e76\u8003\u8651\u7ebf\u4e0b\u5c31\u533b\u3002', 'If symptoms persist or worsen, rest first and consider offline medical care.', '症状が続く、または悪化する場合は、まず休息を取り、対面受診を検討してください。'),
        })

    if health_data.get('steps', 0) < 3000 and not health_data.get('exercise_records'):
        risks.append({
            'level': localize('\u4e2d', 'Medium', '中'),
            'item': localize('\u6d3b\u52a8\u91cf\u504f\u4f4e', 'Activity low', '活動量が少なめ'),
            'risk': localize(
                f"\u4eca\u65e5\u6b65\u6570\u4ec5 {health_data.get('steps', 0)}\uff0c\u4e14\u6ca1\u6709\u989d\u5916\u8fd0\u52a8\u8bb0\u5f55\u3002",
                f"Only {health_data.get('steps', 0)} steps were logged today and no extra exercise was recorded.",
                f"本日の歩数は {health_data.get('steps', 0)} 歩にとどまり、追加の運動記録もありませんでした。",
            ),
            'action': localize('\u660e\u65e5\u5b89\u6392\u4e00\u6b21 15-20 \u5206\u949f\u8f7b\u4e2d\u5ea6\u6b65\u884c\u6216\u9a91\u884c\u3002', 'Plan one 15-20 minute light-to-moderate walk or ride tomorrow.', '明日は 15〜20 分の軽い散歩かサイクリングを 1 回入れてください。'),
        })

    if module_is_enabled(config, 'medication') and not health_data.get('medication_records'):
        risks.append({
            'level': localize('\u4e2d', 'Medium', '中'),
            'item': localize('\u7f3a\u5c11\u7528\u836f\u8bb0\u5f55', 'Medication record missing', '服薬記録が不足'),
            'risk': localize('\u5f53\u524d\u5df2\u542f\u7528\u7528\u836f\u8ffd\u8e2a\uff0c\u4f46\u4eca\u65e5\u6ca1\u6709\u8bb0\u5f55\u3002', 'Medication tracking is enabled, but no medication entry was recorded today.', '服薬トラッキングは有効ですが、本日の服薬記録がありません。'),
            'action': localize('\u5982\u4eca\u65e5\u6709\u670d\u836f\uff0c\u8bf7\u8865\u5145\u65f6\u95f4\u3001\u836f\u540d\u548c\u5242\u91cf\u3002', 'If medication was taken today, add time, medicine name, and dosage.', '本日服薬している場合は、時間・薬剤名・用量を追記してください。'),
        })

    if len(conditions) > 1:
        risks.append({
            'level': localize('\u63d0\u793a', 'Info', '参考'),
            'item': localize('\u591a\u75c5\u79cd\u8054\u5408\u7ba1\u7406', 'Multi-condition management', '複数疾患の併行管理'),
            'risk': localize(
                f"\u5f53\u524d\u5df2\u6309 {condition_text} \u8054\u5408\u7ba1\u7406\uff0c\u9884\u8b66\u9608\u503c\u5df2\u6309\u66f4\u4e25\u6807\u51c6\u5408\u5e76\u3002",
                f"The report is evaluating {condition_text} together and has merged thresholds using the stricter combined standards.",
                f"現在は {condition_text} を組み合わせて管理しており、警戒ラインはより厳しい基準で統合されています。",
            ),
            'action': localize(
                '\u5b89\u6392\u6b21\u65e5\u996e\u98df\u3001\u8fd0\u52a8\u548c\u7528\u836f\u65f6\uff0c\u8bf7\u4ee5\u4e3b\u8981\u76ee\u6807\u4e3a\u4e3b\uff0c\u540c\u65f6\u907f\u514d\u89e6\u53d1\u5176\u4ed6\u75c5\u79cd\u98ce\u9669\u3002',
                'Plan tomorrow around the primary goal while avoiding triggers that may worsen the other managed conditions.',
                '明日の食事・運動・服薬は主目標を優先しつつ、他の管理疾患を悪化させる誘因も避けてください。',
            ),
        })

    return risks


def render_risk_text(risks, locale):
    if not risks:
        return f"- {t(locale, 'no_risk')}"

    lines = []
    for risk in risks:
        resolved = resolve_locale(locale=locale)
        if resolved == 'zh-CN':
            advice_prefix = '\u5efa\u8bae'
        elif resolved == 'ja-JP':
            advice_prefix = '対応'
        else:
            advice_prefix = 'Action'
        lines.append(f"- [{risk.get('level', '')}] {risk.get('item', '')}: {risk.get('risk', '')} {advice_prefix}: {risk.get('action', '')}")
    return "\n".join(lines)


TEXT_REPORT_ICONS = {
    'daily_report_heading': '🌅',
    'overall_score_title': '🏆',
    'item_summary_title': '📊',
    'diet_label': '🍽',
    'water_label': '💧',
    'weight_label': '⚖',
    'symptom_label': '🩺',
    'exercise_label': '🏃',
    'adherence_label': '✅',
    'medication_label': '💊',
    'ai_comment_title': '🧠',
    'details_title': '📝',
    'meal_section': '🍱',
    'water_section': '🚰',
    'exercise_section': '🚴',
    'risk_alert_title': '⚠️',
    'next_day_plan_title': '🎯',
    'diet_plan': '🥗',
    'water_plan': '💦',
    'exercise_plan': '👟',
    'special_attention': '🔔',
}

TEXT_REPORT_MODULE_ICON_KEYS = {
    'diet': 'diet_label',
    'water': 'water_label',
    'weight': 'weight_label',
    'symptom': 'symptom_label',
    'exercise': 'exercise_label',
    'adherence': 'adherence_label',
    'medication': 'medication_label',
}


def with_text_icon(key, text):
    icon = TEXT_REPORT_ICONS.get(key, '')
    return f"{icon} {text}".strip() if icon else text


def compact_number(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value

def generate_text_report(health_data, config, date):
    """Generate the localized markdown text report."""
    locale = resolve_locale(config)
    score_report = build_score_report(health_data, config)
    render_notice = str(health_data.get('render_notice', '') or '').strip()

    ai_comment = health_data.get('ai_comment', '')
    ai_comment_source = health_data.get('generation_meta', {}).get('ai_comment')
    if not ai_comment:
        ai_comment, ai_comment_source = generate_ai_comment(health_data, config)

    ai_plan = health_data.get('plan', {})
    ai_plan_source = health_data.get('generation_meta', {}).get('next_day_plan')
    if not ai_plan:
        ai_plan, ai_plan_source = generate_ai_plan(health_data, config)

    risks = health_data.get('risks')
    if not risks:
        risks = generate_risk_alerts(health_data, config)
    risk_source = health_data.get('generation_meta', {}).get('risk_alerts', 'local')

    compact_ai_comment = re.sub(r'[\u2605\u2606]', '', ai_comment).replace('\n', ' ').strip()
    score_lines = []
    for module in score_report.get('modules', []):
        module_title = module.get('title', module.get('id', ''))
        icon_key = TEXT_REPORT_MODULE_ICON_KEYS.get(module.get('id'))
        score_lines.append(f"- {with_text_icon(icon_key, module_title) if icon_key else module_title}: {get_star_string(module.get('raw', 0))} {module.get('raw', 0)}/100")
        if module.get('detail_text'):
            score_lines.append(f"  {module['detail_text']}")
    score_summary = "\n".join(score_lines)

    medication_text = ''
    if module_is_enabled(config, 'medication'):
        medication_lines = health_data.get('medication_records', [])
        medication_title = with_text_icon('medication_label', default_module_title(locale, 'medication'))
        medication_body = '\n'.join(medication_lines) if medication_lines else t(locale, 'no_record')
        medication_text = f"\n\n**{medication_title}**\n{medication_body}"

    custom_text = ''
    if config.get('report_preferences', {}).get('append_custom_sections', True):
        for header, items in health_data.get('custom_sections', {}).items():
            custom_text += f"\n**{header}**\n" + '\n'.join(items) + "\n"

    notice_block = ""
    if render_notice:
        notice_block = f"""### {t(locale, 'render_notice_title')}
{render_notice}

"""

    report = f"""## {with_text_icon('daily_report_heading', t(locale, 'daily_report_heading', date=date))}
### {with_text_icon('overall_score_title', t(locale, 'overall_score_title', date=date))}
**{t(locale, 'score_total_label')}: {get_star_string(score_report.get('total', 0))} {score_report.get('total', 0)}/100**

### {with_text_icon('item_summary_title', t(locale, 'item_summary_title'))}
{score_summary}

{notice_block}### {with_text_icon('ai_comment_title', t(locale, 'ai_comment_title'))}
{compact_ai_comment}
_{generation_source_label(locale, ai_comment_source or 'fallback')}_

### {with_text_icon('details_title', t(locale, 'details_title'))}
**{with_text_icon('meal_section', t(locale, 'meal_section'))}**
{generate_meal_summary(health_data, locale)}

**{with_text_icon('water_section', t(locale, 'water_section'))}**
{generate_water_summary(health_data, locale)}

**{with_text_icon('exercise_section', t(locale, 'exercise_section'))}**
{generate_exercise_detail(health_data, locale)}{medication_text}{custom_text}

### {with_text_icon('risk_alert_title', t(locale, 'risk_alerts'))}
{render_risk_text(risks, locale)}
_{generation_source_label(locale, risk_source)}_

### {with_text_icon('next_day_plan_title', t(locale, 'next_day_plan_title'))}
{generate_plan_text(ai_plan, locale)}
_{generation_source_label(locale, ai_plan_source or 'fallback')}_"""
    if locale == "ja-JP":
        report = "\n".join(localize_free_text(locale, line) for line in report.splitlines())
    return report


def generate_meal_summary(health_data, locale):
    meals = health_data.get('meals', [])
    if not meals:
        return t(locale, 'no_record')
    lines = []
    for meal in meals:
        foods = list_separator(locale).join(meal.get('foods', []))
        time_suffix = f" ({meal.get('time', '')})" if meal.get('time') else ""
        lines.append(f"{meal_name(locale, meal.get('type', ''))}{time_suffix}: {foods} - {meal.get('total_calories', 0):.0f}kcal")
    return '\n'.join(lines)


def generate_water_summary(health_data, locale):
    water_target = health_data.get('water_target', 2000)
    water_target = water_target if water_target > 0 else 2000
    return t(locale, 'completion_status', current=health_data.get('water_total', 0), target=water_target, percent=int(health_data.get('water_total', 0) * 100 // water_target))


def generate_exercise_summary(health_data, locale):
    exercises = health_data.get('exercise_records', [])
    steps = health_data.get('steps', 0)
    if not exercises and steps == 0:
        return t(locale, 'no_record')
    parts = []
    for e in exercises:
        exercise_label = exercise_name(locale, e.get('type'))
        if e.get('time'):
            exercise_label = f"{exercise_label} ({e.get('time')})"
        details = []
        if e.get('distance_km', 0) > 0:
            details.append(t(locale, 'distance_unit_km', value=compact_number(e.get('distance_km', 0))))
        if e.get('duration_min', 0) > 0:
            details.append(t(locale, 'minutes_unit', value=compact_number(e.get('duration_min', 0))))
        if e.get('calories', 0) > 0:
            details.append(t(locale, 'calories_unit', value=compact_number(e.get('calories', 0))))
        parts.append(f"{exercise_label}: {' / '.join(details)}")
    if steps > 0:
        parts.append(f"{t(locale, 'today_steps')}: {t(locale, 'steps_unit', value=steps)}")
    return '; '.join(parts) if parts else t(locale, 'no_record')


def generate_exercise_detail(health_data, locale):
    exercises = health_data.get('exercise_records', [])
    steps = health_data.get('steps', 0)
    if not exercises and steps == 0:
        return t(locale, 'no_record')
    lines = []
    for exercise in exercises:
        exercise_label = exercise_name(locale, exercise.get('type'))
        if exercise.get('time'):
            exercise_label = f"{exercise_label} ({exercise.get('time')})"
        details = []
        if exercise.get('distance_km', 0) > 0:
            details.append(t(locale, 'distance_unit_km', value=compact_number(exercise.get('distance_km', 0))))
        if exercise.get('duration_min', 0) > 0:
            details.append(t(locale, 'minutes_unit', value=compact_number(exercise.get('duration_min', 0))))
        if exercise.get('calories', 0) > 0:
            details.append(t(locale, 'calories_unit', value=compact_number(exercise.get('calories', 0))))
        lines.append(f"{exercise_label}: {' / '.join(details)}")
    if steps > 0:
        lines.append(f"{t(locale, 'today_steps')}: {t(locale, 'steps_unit', value=steps)}")
    return '\n'.join(lines) if lines else t(locale, 'no_detail_record')


def generate_plan_text(plan, locale):
    """Render the next-day plan in localized markdown."""
    lines = []
    if plan.get('diet'):
        lines.append(f"**{with_text_icon('diet_plan', t(locale, 'diet_plan'))}**")
        for item in plan.get('diet', []):
            if isinstance(item, dict):
                meal = item.get('meal', item.get('meal_name', ''))
                time = item.get('time', item.get('time_range', item.get('period', '')))
                menu = item.get('menu', '')
                if not menu:
                    items = item.get('items', [])
                    if items:
                        menu = list_separator(locale).join(str(i) for i in items[:3])
                        if len(items) > 3:
                            menu += f" {and_more(locale)}"
                if not menu:
                    menu = item.get('dishes', item.get('menu_detail', item.get('food', item.get('content', ''))))
                calories = item.get('calories', item.get('kcal', ''))
                fat = item.get('fat', item.get('fat_g', ''))
                fiber = item.get('fiber', item.get('fiber_g', ''))
                if menu:
                    nutrition = f"({calories}kcal"
                    if fat:
                        nutrition += f", {t(locale, 'fat')}{fat}g"
                    if fiber:
                        nutrition += f", {t(locale, 'fiber')}{fiber}g"
                    nutrition += ")"
                    lines.append(f"* {time} {menu} {nutrition}")
                elif meal and time:
                    lines.append(f"* {meal} ({time})")
                else:
                    lines.append(f"* {item}")
            else:
                lines.append(f'* {item}')
        lines.append('')
    if plan.get('water'):
        lines.append(f"**{with_text_icon('water_plan', t(locale, 'water_plan'))}**")
        for item in plan.get('water', []):
            if isinstance(item, dict):
                time = item.get('time', item.get('period', ''))
                amount = item.get('amount', item.get('amount_ml', item.get('volume', '')))
                if amount and not any(unit in str(amount) for unit in ['ml', 'L']):
                    amount = f"{amount}ml"
                note = item.get('note', item.get('tip', item.get('remark', '')))
                lines.append(f"* {time} {amount} ({note})")
            else:
                lines.append(f'* {item}')
        lines.append('')
    if plan.get('exercise'):
        lines.append(f"**{with_text_icon('exercise_plan', t(locale, 'exercise_plan'))}**")
        for item in plan.get('exercise', []):
            if isinstance(item, dict):
                time = item.get('time', item.get('time_range', item.get('period', '')))
                activity = item.get('activity', item.get('type', item.get('name', '')))
                duration = item.get('duration', item.get('duration_min', item.get('time_length', '')))
                details = item.get('details', item.get('description', item.get('desc', item.get('content', ''))))
                if activity and duration and details:
                    lines.append(f"* {time} {activity} ({duration}): {details}")
                elif activity and duration:
                    lines.append(f"* {time} {activity} ({duration})")
                elif activity:
                    lines.append(f"* {time} {activity}")
                else:
                    lines.append(f"* {time}")
            else:
                lines.append(f'* {item}')
        lines.append('')
    if plan.get('notes'):
        lines.append(f"**{with_text_icon('special_attention', t(locale, 'special_attention'))}**")
        for item in plan.get('notes', []):
            lines.append(f'* {item}')
    return '\n'.join(lines).strip()

def generate_report(memory_file, date):
    """Generate the localized text report and PDF path."""
    base_config = load_user_config()
    requested_locale = resolve_report_locale(base_config, [memory_file])
    fallback_context = prepare_font_compatible_memory(
        requested_locale=requested_locale,
        source_dir=Path(memory_file).resolve().parent,
        default_memory_file=str(Path(memory_file).resolve()),
    )
    temp_memory_dir = fallback_context.get("temp_dir")

    try:
        working_memory_file = fallback_context.get("memory_file") or str(Path(memory_file).resolve())
        config = force_config_locale(base_config, fallback_context.get("locale"))
        locale = resolve_locale(config)
        render_notice = str(fallback_context.get("render_notice") or "").strip()

        user_profile = config.get('user_profile', {})
        if 'step_target' not in user_profile:
            user_profile['step_target'] = 8000

        conditions = get_profile_conditions(user_profile)
        primary_condition = get_primary_condition(user_profile)
        condition_text = get_conditions_display_name(locale, conditions)
        standards = get_condition_standards(config, conditions)

        health_data = parse_memory_file(working_memory_file)
        if render_notice:
            health_data['render_notice'] = render_notice

        score_report = build_score_report(health_data, config)
        risks = generate_risk_alerts(health_data, config)
        ai_comment, ai_comment_source = generate_ai_comment(health_data, config)
        ai_plan, ai_plan_source = generate_ai_plan(health_data, config)
        health_data['ai_comment'] = ai_comment
        health_data['plan'] = ai_plan
        health_data['risks'] = risks
        health_data['generation_meta'] = {
            'ai_comment': ai_comment_source,
            'next_day_plan': ai_plan_source,
            'risk_alerts': 'local',
        }
        if render_notice:
            health_data['generation_meta']['render_notice'] = render_notice

        tdee = calculate_tdee(calculate_bmr(health_data.get('weight_morning') or 65, user_profile.get('height_cm', 172), user_profile.get('age', 34), user_profile.get('gender', 'male')), user_profile.get('activity_level', 1.2))
        macros = {
            'protein_p': 15, 'fat_p': 25, 'carb_p': 60,
            'protein_g': round(user_profile.get('current_weight_kg', 65) * 1.2),
            'fat_g': round(standards.get('fat_max_g', 50)),
            'carb_g': round(tdee * 0.60 / 4),
            'fiber_min_g': standards.get('fiber_min_g', 25)
        }
        profile_payload = dict(user_profile)
        profile_payload['condition'] = primary_condition
        profile_payload['primary_condition'] = primary_condition
        profile_payload['conditions'] = conditions
        profile_payload['condition_display'] = condition_text

        locale_tag = resolve_locale(locale=locale).replace("-", "_")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        pdf_filename = f"health_report_{locale_tag}_{timestamp}.pdf"
        local_pdf_path = str(REPORTS_DIR / pdf_filename)
        web_dir = os.environ.get("REPORT_WEB_DIR", "")
        base_url = os.environ.get("REPORT_BASE_URL", "").rstrip('/')

        try:
            generate_pdf_report_impl(
                data=health_data,
                profile=profile_payload,
                locale=locale,
                scores=score_report,
                nutrition={
                    'calories': health_data.get('total_calories', 0),
                    'protein': health_data.get('total_protein', 0),
                    'fat': health_data.get('total_fat', 0),
                    'carb': health_data.get('total_carb', 0),
                    'fiber': health_data.get('total_fiber', 0),
                },
                macros=macros,
                risks=risks,
                plan=ai_plan,
                output_path=local_pdf_path,
                water_records=health_data.get('water_records', []),
                meals=health_data.get('meals', []),
                exercise_data=health_data.get('exercise_records', []),
                ai_comment=ai_comment,
                medication_records=health_data.get('medication_records', []),
                custom_sections=health_data.get('custom_sections', {}),
                generation_meta=health_data.get('generation_meta', {}),
            )
            if web_dir and os.path.exists(web_dir) and base_url:
                web_pdf_path = os.path.join(web_dir, pdf_filename)
                shutil.copy2(local_pdf_path, web_pdf_path)
                pdf_url = f"{base_url}/{pdf_filename}"
                print(t(locale, "pdf_copied", path=web_pdf_path), file=sys.stderr)
                print(t(locale, "pdf_download_url", url=pdf_url), file=sys.stderr)
            else:
                print(t(locale, "pdf_saved_local"), file=sys.stderr)
                print(t(locale, "pdf_local_path", path=local_pdf_path), file=sys.stderr)
                pdf_url = local_pdf_path
        except Exception as e:
            print(t(locale, "pdf_generation_failed", error=e), file=sys.stderr)
            import traceback
            traceback.print_exc()
            pdf_url = local_pdf_path

        text_report = generate_text_report(health_data, config, date)
        delivery_message = build_delivery_message(
            locale=locale,
            body=text_report,
            pdf_url=pdf_url,
            report_kind="daily",
            generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
        return text_report, pdf_url, delivery_message
    finally:
        if temp_memory_dir:
            temp_memory_dir.cleanup()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 daily_report_pro.py <memory_file> <date>")
        sys.exit(1)

    memory_file = sys.argv[1]
    date = sys.argv[2]

    try:
        text_report, pdf_url, delivery_message = generate_report(memory_file, date)
        print("=== TEXT_REPORT_START ===")
        print(text_report)
        print("=== TEXT_REPORT_END ===")
        print("=== PDF_URL ===")
        print(pdf_url)
        print("=== DELIVERY_MESSAGE_START ===")
        print(delivery_message)
        print("=== DELIVERY_MESSAGE_END ===")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

