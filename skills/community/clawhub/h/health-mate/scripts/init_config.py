#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interactive configuration wizard for Health-Mate."""

import json
import os
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_DIR.mkdir(exist_ok=True)

ENV_TEMPLATE_DEFAULTS = {
    "NVM_DIR": "/root/.nvm",
    "CRON_PATH": "/root/.nvm/versions/node/v22.22.0/bin:/root/.local/bin:/root/bin:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:/usr/local/bin:/usr/bin:/bin:/root/.npm-global/bin",
    "OPENCLAW_BIN": "/root/.nvm/versions/node/v22.22.0/bin/openclaw",
    "MEMORY_DIR": "/root/.openclaw/workspace/memory",
    "DINGTALK_WEBHOOK": "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN",
    "FEISHU_WEBHOOK": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_HOOK",
    "TELEGRAM_BOT_TOKEN": "YOUR_BOT_TOKEN",
    "TELEGRAM_CHAT_ID": "YOUR_CHAT_ID",
    "TAVILY_API_KEY": "YOUR_TAVILY_API_KEY",
    "LOG_FILE": "/root/.openclaw/logs/health_report_pro.log",
    "REPORT_WEB_DIR": "/var/www/html/reports",
    "REPORT_BASE_URL": "https://example.com/reports",
    "ALLOW_RUNTIME_FONT_DOWNLOAD": "false",
}

LANGUAGE_OPTIONS = {"1": "zh-CN", "2": "en-US", "3": "ja-JP"}
LANGUAGE_LABELS = {"zh-CN": "中文", "en-US": "English", "ja-JP": "日本語"}
GENDER_OPTIONS = {"1": "male", "2": "female"}
GENDER_LABELS = {
    "zh-CN": {"male": "男", "female": "女"},
    "en-US": {"male": "Male", "female": "Female"},
    "ja-JP": {"male": "男性", "female": "女性"},
}
CONDITION_OPTIONS = {
    "1": "gallstones",
    "2": "diabetes",
    "3": "hypertension",
    "4": "fat_loss",
    "5": "balanced",
}
CONDITION_LABELS = {
    "zh-CN": {
        "gallstones": "胆囊/胆结石管理",
        "diabetes": "血糖管理",
        "hypertension": "血压管理",
        "fat_loss": "减脂管理",
        "balanced": "综合健康管理",
    },
    "en-US": {
        "gallstones": "Gallstone Care",
        "diabetes": "Glucose Management",
        "hypertension": "Blood Pressure Management",
        "fat_loss": "Fat Loss",
        "balanced": "Balanced Wellness",
    },
    "ja-JP": {
        "gallstones": "胆のう・胆石ケア",
        "diabetes": "血糖管理",
        "hypertension": "血圧管理",
        "fat_loss": "減脂・体脂肪管理",
        "balanced": "総合ヘルスケア",
    },
}
ACTIVITY_OPTIONS = {
    "1": 1.2,
    "2": 1.375,
    "3": 1.55,
    "4": 1.725,
    "5": 1.9,
}
ACTIVITY_LABELS = {
    "zh-CN": {
        "1": "久坐/很少运动",
        "2": "轻度活动",
        "3": "中度活动",
        "4": "高活动量",
        "5": "高强度训练",
    },
    "en-US": {
        "1": "Sedentary",
        "2": "Light activity",
        "3": "Moderate activity",
        "4": "High activity",
        "5": "Intense training",
    },
    "ja-JP": {
        "1": "座位中心 / ほぼ運動なし",
        "2": "軽い活動",
        "3": "中程度の活動",
        "4": "活動量が多い",
        "5": "高強度トレーニング",
    },
}

DEFAULT_CONDITION_STANDARDS = {
    "gallstones": {"fat_min_g": 40, "fat_max_g": 50, "fiber_min_g": 25, "water_min_ml": 2000},
    "diabetes": {"fat_min_g": 40, "fat_max_g": 55, "fiber_min_g": 30, "water_min_ml": 2000},
    "hypertension": {"fat_min_g": 40, "fat_max_g": 55, "fiber_min_g": 25, "water_min_ml": 2000, "sodium_max_mg": 2000},
    "fat_loss": {"fat_min_g": 40, "fat_max_g": 60, "fiber_min_g": 25, "water_min_ml": 2500},
    "balanced": {"fat_min_g": 40, "fat_max_g": 60, "fiber_min_g": 25, "water_min_ml": 2000},
}

DEFAULT_MODULES = {
    "zh-CN": [
        {"id": "diet", "title": "饮食合规性", "enabled": True, "weight": 20, "description": "根据脂肪、纤维和餐次记录综合评分。"},
        {"id": "water", "title": "饮水完成度", "enabled": True, "weight": 15, "description": "根据饮水总量与目标值评分。"},
        {"id": "weight", "title": "体重管理", "enabled": True, "weight": 15, "description": "根据体重记录完整度与目标趋势评分。"},
        {"id": "symptom", "title": "症状管理", "enabled": True, "weight": 15, "description": "根据症状记录和稳定情况评分。"},
        {"id": "exercise", "title": "运动管理", "enabled": True, "weight": 20, "description": "根据运动、步数和活动量评分。"},
        {"id": "adherence", "title": "健康依从性", "enabled": True, "weight": 15, "description": "根据记录完整度和执行一致性评分。"},
        {"id": "medication", "title": "用药情况", "enabled": False, "weight": 0, "description": "启用后会纳入评分，并在日报/周报/PDF 中输出。", "type": "section_presence", "section_title": "用药情况"},
    ],
    "en-US": [
        {"id": "diet", "title": "Diet Compliance", "enabled": True, "weight": 20, "description": "Scored from fat, fiber, and meal structure."},
        {"id": "water", "title": "Hydration", "enabled": True, "weight": 15, "description": "Scored from water intake against the daily target."},
        {"id": "weight", "title": "Weight Management", "enabled": True, "weight": 15, "description": "Scored from weight logging and goal direction."},
        {"id": "symptom", "title": "Symptom Management", "enabled": True, "weight": 15, "description": "Scored from symptom logging and stability."},
        {"id": "exercise", "title": "Exercise Management", "enabled": True, "weight": 20, "description": "Scored from exercise, steps, and activity volume."},
        {"id": "adherence", "title": "Health Adherence", "enabled": True, "weight": 15, "description": "Scored from logging completeness and consistency."},
        {"id": "medication", "title": "Medication", "enabled": False, "weight": 0, "description": "When enabled, it is included in scoring and rendered in daily/weekly PDF output.", "type": "section_presence", "section_title": "Medication"},
    ],
    "ja-JP": [
        {"id": "diet", "title": "食事達成度", "enabled": True, "weight": 20, "description": "脂質・食物繊維・食事記録の構成から採点します。"},
        {"id": "water", "title": "水分達成度", "enabled": True, "weight": 15, "description": "飲水量と目標値の達成度から採点します。"},
        {"id": "weight", "title": "体重管理", "enabled": True, "weight": 15, "description": "体重記録の継続性と目標方向から採点します。"},
        {"id": "symptom", "title": "症状管理", "enabled": True, "weight": 15, "description": "症状記録と安定度から採点します。"},
        {"id": "exercise", "title": "運動管理", "enabled": True, "weight": 20, "description": "運動・歩数・活動量から採点します。"},
        {"id": "adherence", "title": "健康実行度", "enabled": True, "weight": 15, "description": "記録の完全性と継続性から採点します。"},
        {"id": "medication", "title": "服薬状況", "enabled": False, "weight": 0, "description": "有効にすると採点対象に含め、日報・週報・PDF にも反映します。", "type": "section_presence", "section_title": "服薬記録"},
    ],
}


def localize(locale, zh_text, en_text, ja_text=None):
    if locale == "zh-CN":
        return zh_text
    if locale == "ja-JP" and ja_text is not None:
        return ja_text
    return en_text


def prompt_input(message):
    return input(f"{message}\n> ").strip()


def ask_text(message, retry):
    while True:
        value = prompt_input(message)
        if value:
            return value
        print(retry)


def ask_number(message, retry, cast=float, min_value=None):
    while True:
        raw = prompt_input(message)
        try:
            value = cast(raw)
            if min_value is not None and value < min_value:
                raise ValueError
            return value
        except (TypeError, ValueError):
            print(retry)


def ask_choice(message, retry, options):
    while True:
        raw = prompt_input(message)
        if raw in options:
            return options[raw]
        print(retry)


def ask_multi_choice(message, retry, options):
    while True:
        raw = prompt_input(message)
        values = []
        for part in re.split(r"[,\uff0c\s]+", raw):
            if not part:
                continue
            if part not in options:
                values = []
                break
            resolved = options[part]
            if resolved not in values:
                values.append(resolved)
        if values:
            return values
        print(retry)


def ask_optional_list(message):
    raw = prompt_input(message)
    return [part.strip() for part in re.split(r"[,\uff0c]+", raw) if part.strip()]


def ask_yes_no(message, default=True):
    suffix = "Y/n" if default else "y/N"
    raw = prompt_input(f"{message} ({suffix})").lower()
    if not raw:
        return default
    return raw in {"y", "yes", "1", "true", "是"}


def module_defaults(locale):
    return [dict(module) for module in DEFAULT_MODULES[locale]]


def build_ai_generation(ai_mode):
    mode = "hybrid" if ai_mode == "hybrid" else "local_only"
    return {
        "expert_commentary": {"mode": mode, "max_attempts": 3, "timeout_seconds": 90},
        "next_day_plan": {"mode": mode, "max_attempts": 3, "timeout_seconds": 90},
        "risk_alerts": {"mode": "local"},
    }


def infer_population_branch(primary_condition):
    return "lifestyle" if str(primary_condition or "").strip() in {"balanced", "fat_loss"} else "disease"


def slugify(text):
    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_") or "custom_section"


def env_value(name):
    value = str(os.environ.get(name, "") or "").strip()
    return value if value else ENV_TEMPLATE_DEFAULTS[name]


def env_quote(value):
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_env_template():
    values = {key: env_value(key) for key in ENV_TEMPLATE_DEFAULTS}
    lines = [
        "# ========== Local Configuration - DO NOT upload to GitHub! ==========",
        "# This file stays in config/.env and may contain secrets. Keep only the keys you intend the skill to read.",
        "",
        "# ========== Cron Environment Variables (Optional but recommended for scheduled tasks) ==========",
        "# Node.js NVM directory used by the shell runners",
        f'NVM_DIR={env_quote(values["NVM_DIR"])}',
        "",
        "# Cron PATH environment used by the shell runners so cron can find openclaw CLI and system commands",
        f'CRON_PATH={env_quote(values["CRON_PATH"])}',
        "",
        "# Optional explicit openclaw binary path used by the Python local-LLM resolver",
        f'OPENCLAW_BIN={env_quote(values["OPENCLAW_BIN"])}',
        "",
        "# ========== Messaging Configuration (Optional) ==========",
        "# DingTalk Robot Webhook",
        f'DINGTALK_WEBHOOK={env_quote(values["DINGTALK_WEBHOOK"])}',
        "",
        "# Feishu Robot Webhook",
        f'FEISHU_WEBHOOK={env_quote(values["FEISHU_WEBHOOK"])}',
        "",
        "# Telegram Bot Configuration",
        f'TELEGRAM_BOT_TOKEN={env_quote(values["TELEGRAM_BOT_TOKEN"])}',
        f'TELEGRAM_CHAT_ID={env_quote(values["TELEGRAM_CHAT_ID"])}',
        "",
        "# ========== AI Retrieval Configuration (Optional) ==========",
        "# Tavily API key used for retrieval-assisted fallback and monthly medical lookup",
        f'TAVILY_API_KEY={env_quote(values["TAVILY_API_KEY"])}',
        "",
        "# ========== Health Report Configuration ==========",
        "# Health memory directory",
        f'MEMORY_DIR={env_quote(values["MEMORY_DIR"])}',
        "",
        "# Optional shared log file override. If omitted, each shell runner keeps its own logs/*.log file.",
        f'LOG_FILE={env_quote(values["LOG_FILE"])}',
        "",
        "# Optional local directory where generated PDFs are copied for public serving",
        f'REPORT_WEB_DIR={env_quote(values["REPORT_WEB_DIR"])}',
        "",
        "# Optional public base URL used when push messages include downloadable PDF links",
        f'REPORT_BASE_URL={env_quote(values["REPORT_BASE_URL"])}',
        "",
        "# Allow runtime font download only if you explicitly want that behavior",
        f'ALLOW_RUNTIME_FONT_DOWNLOAD={env_quote(values["ALLOW_RUNTIME_FONT_DOWNLOAD"])}',
        "",
    ]
    return "\n".join(lines)


def ensure_local_env_file():
    env_path = CONFIG_DIR / ".env"
    if env_path.exists():
        return env_path, False
    env_path.write_text(build_env_template(), encoding="utf-8")
    return env_path, True


print("=" * 60)
print("Health-Mate Setup Wizard")
print("=" * 60)
print("1. 中文")
print("2. English")
print("3. 日本語")

language_choice = input("> ").strip()
while language_choice not in LANGUAGE_OPTIONS:
    print("请输入 1 / 2 / 3 / Please enter 1, 2, or 3. / 1・2・3 のいずれかを入力してください。")
    language_choice = input("> ").strip()

locale = LANGUAGE_OPTIONS[language_choice]
print()
print(localize(locale, "欢迎使用 Health-Mate 首次配置向导。", "Welcome to the Health-Mate first-time setup wizard."))
print(localize(locale, "本向导会一步步写入 config/user_config.json。", "This wizard will write everything into config/user_config.json."))
print(localize(locale, "步骤概览：", "Steps:"))
for item in [
    localize(locale, "1. 基础信息", "1. Basic profile"),
    localize(locale, "2. 多病种/目标配置", "2. Multi-condition setup"),
    localize(locale, "3. AI 模式、评分模块和权重", "3. AI mode, scoring modules, and weights"),
    localize(locale, "4. 保存配置并说明后续写法", "4. Save config and explain next steps"),
]:
    print(f"- {item}")
input(f"{localize(locale, '按回车开始...', 'Press Enter to start...')}\n")

print(localize(locale, "\n[步骤 1/4] 基础信息", "\n[Step 1/4] Basic profile"))
name = ask_text(localize(locale, "请输入姓名或昵称", "Your name or nickname"), localize(locale, "请输入姓名或昵称。", "Please enter a name or nickname."))
gender = ask_choice(localize(locale, "性别：1 男 / 2 女", "Gender: 1 Male / 2 Female"), localize(locale, "请输入 1 或 2。", "Please enter 1 or 2."), GENDER_OPTIONS)
age = ask_number(localize(locale, "年龄（例如 34）", "Age (for example 34)"), localize(locale, "请输入有效年龄。", "Please enter a valid age."), cast=int, min_value=1)
height = ask_number(localize(locale, "身高 cm（例如 172）", "Height in cm (for example 172)"), localize(locale, "请输入有效身高。", "Please enter a valid height."), cast=int, min_value=50)
current_weight = ask_number(localize(locale, "当前体重 kg（例如 65.5）", "Current weight in kg (for example 65.5)"), localize(locale, "请输入有效体重。", "Please enter a valid weight."), cast=float, min_value=1)
target_weight = ask_number(localize(locale, "目标体重 kg", "Target weight in kg"), localize(locale, "请输入有效目标体重。", "Please enter a valid target weight."), cast=float, min_value=1)

print(localize(locale, "\n[步骤 2/4] 多病种/目标配置", "\n[Step 2/4] Multi-condition setup"))
print(localize(locale, "可同时选择多个管理目标，系统会按更严格的重叠标准合并判断阈值。", "You can select multiple conditions/goals. The system will merge overlapping thresholds using the stricter standards."))
for key, condition in CONDITION_OPTIONS.items():
    print(f"{key}. {CONDITION_LABELS[locale][condition]}")
conditions = ask_multi_choice(
    localize(locale, "请选择一个或多个目标，使用逗号分隔（例如 2,3,4）", "Choose one or more goals, separated by commas (for example 2,3,4)"),
    localize(locale, "请输入有效编号，例如 2,3 或 1,4,5。", "Please enter valid numbers such as 2,3 or 1,4,5."),
    CONDITION_OPTIONS,
)

selected_map = {str(index + 1): value for index, value in enumerate(conditions)}
selected_lines = [f"{index}. {CONDITION_LABELS[locale][condition]}" for index, condition in selected_map.items()]
print(localize(locale, "你选择了以下目标：", "You selected:"))
for item in selected_lines:
    print(item)
primary_condition = ask_choice(
    localize(locale, "请选择主病种/主目标编号（日报标题、AI 视角会优先参考它）", "Choose the primary condition/goal number (used as the primary view for titles and AI prompts)"),
    localize(locale, "请输入上面列表中的编号。", "Please enter one of the numbers shown above."),
    selected_map,
)

water_target = ask_number(localize(locale, "每日饮水目标 ml", "Daily hydration target in ml"), localize(locale, "请输入有效饮水目标。", "Please enter a valid water target."), cast=int, min_value=500)
step_target = ask_number(localize(locale, "每日步数目标", "Daily step target"), localize(locale, "请输入有效步数目标。", "Please enter a valid step target."), cast=int, min_value=500)
print(localize(locale, "活动系数选项：", "Activity factor options:"))
for key, label in ACTIVITY_LABELS[locale].items():
    print(f"{key}. {label}")
activity_level = ask_choice(localize(locale, "请选择活动系数", "Choose the activity factor"), localize(locale, "请输入 1-5。", "Please enter 1-5."), ACTIVITY_OPTIONS)
dislikes = ask_optional_list(localize(locale, "尽量避免的食物（可选，逗号分隔）", "Foods to avoid when possible (optional, comma-separated)"))
allergies = ask_optional_list(localize(locale, "过敏食物（可选，逗号分隔）", "Food allergies (optional, comma-separated)"))
favorite_fruits = ask_optional_list(localize(locale, "常吃或喜欢的水果（可选，逗号分隔）", "Favorite fruits (optional, comma-separated)"))
print(localize(locale, "为了支持月报中的复查提醒与本地医院推荐，请继续填写常居地。", "To support follow-up reminders and local hospital recommendations in the monthly report, please add your residence details."))
residence_country = ask_text(localize(locale, "常居国家（例如：中国）", "Residence country (for example: China)"), localize(locale, "请输入国家。", "Please enter a country."))
residence_province = ask_text(localize(locale, "常居省份 / 州（例如：上海）", "Residence province / state (for example: Shanghai)"), localize(locale, "请输入省份或州。", "Please enter a province or state."))
residence_city = ask_text(localize(locale, "常居城市（例如：上海）", "Residence city (for example: Shanghai)"), localize(locale, "请输入城市。", "Please enter a city."))
residence_district = prompt_input(localize(locale, "常居区县 / 区域（可选）", "Residence district / area (optional)"))

print(localize(locale, "\n[步骤 3/4] AI、评分模块和权重", "\n[Step 3/4] AI mode, modules, and weights"))
print(localize(locale, "说明：", "Notes:"))
print(localize(locale, "- 权重不要求手动凑满 100，运行时会自动归一化。", "- Weights do not need to add up to 100 manually. Runtime normalization is automatic."))
print(localize(locale, "- 如果配置了 TAVILY_API_KEY，本地回退内容也会优先结合检索结果。", "- If TAVILY_API_KEY is configured, local fallback content can also be enriched with Tavily retrieval.")) 
print(localize(locale, "- 用药和自定义模块既能参与评分，也会在日报/周报/PDF 中输出。", "- Medication and custom modules can be part of scoring and also appear in daily/weekly/PDF output."))

ai_mode_choice = ask_choice(
    localize(locale, "AI 模式：1 混合（推荐，LLM 优先失败后本地动态回退） / 2 仅本地动态规则", "AI mode: 1 Hybrid (recommended, LLM first with dynamic local fallback) / 2 Dynamic local rules only"),
    localize(locale, "请输入 1 或 2。", "Please enter 1 or 2."),
    {"1": "hybrid", "2": "local_only"},
)

modules = []
for module in module_defaults(locale):
    enabled = ask_yes_no(f"{module['title']} - {module['description']}", default=module.get("enabled", True))
    weight = ask_number(
        localize(locale, f"为“{module['title']}”设置权重（可为 0-100 任意数字）", f"Set the weight for \"{module['title']}\" (any number from 0-100 is fine)"),
        localize(locale, "请输入有效数字。", "Please enter a valid number."),
        cast=float,
        min_value=0,
    ) if enabled else 0
    module_data = {
        "id": module["id"],
        "type": module.get("type", "builtin"),
        "title": module["title"],
        "enabled": enabled,
        "weight": weight,
    }
    if module_data["type"] == "section_presence":
        module_data["section_title"] = module.get("section_title", module["title"])
        module_data["score_when_present"] = 100
        module_data["score_when_missing"] = 0
    modules.append(module_data)

print(localize(locale, "\n你还可以追加自定义监测模块，例如：生化情况、血压记录、睡眠、复查指标。", "\nYou can also add custom monitoring modules such as biochemistry, blood pressure, sleep, or follow-up labs."))
while ask_yes_no(localize(locale, "添加一个自定义模块吗？", "Add a custom module?"), default=False):
    custom_title = ask_text(localize(locale, "显示名称（例如：生化情况）", "Display title (for example: Biochemistry)"), localize(locale, "请输入显示名称。", "Please enter a display title."))
    custom_section = ask_text(localize(locale, "对应的 Markdown 二级标题（例如：生化情况）", "Matching Markdown level-2 heading (for example: Biochemistry)"), localize(locale, "请输入标题名称。", "Please enter the heading name."))
    custom_weight = ask_number(localize(locale, "为这个自定义模块设置权重", "Set the weight for this custom module"), localize(locale, "请输入有效数字。", "Please enter a valid number."), cast=float, min_value=0)
    modules.append(
        {
            "id": slugify(custom_section),
            "type": "section_presence",
            "title": custom_title,
            "section_title": custom_section,
            "enabled": True,
            "weight": custom_weight,
            "score_when_present": 100,
            "score_when_missing": 0,
        }
    )

config = {
    "_version": "1.5.3",
    "config_version": "1.5.3",
    "language": locale,
    "user_profile": {
        "name": name,
        "gender": gender,
        "age": age,
        "height_cm": height,
        "current_weight_kg": current_weight,
        "target_weight_kg": target_weight,
        "condition": primary_condition,
        "primary_condition": primary_condition,
        "conditions": conditions,
        "activity_level": activity_level,
        "water_target_ml": water_target,
        "step_target": step_target,
        "residence": {
            "country": residence_country,
            "province": residence_province,
            "city": residence_city,
            "district": residence_district,
            "display_name": (
                "".join([item for item in [residence_province, residence_city, residence_district] if item])
                if locale == "zh-CN"
                else "、".join([item for item in [residence_district, residence_city, residence_province, residence_country] if item])
                if locale == "ja-JP"
                else ", ".join([item for item in [residence_district, residence_city, residence_province, residence_country] if item])
            ),
        },
        "dietary_preferences": {
            "dislike": dislikes,
            "allergies": allergies,
            "favorite_fruits": favorite_fruits,
        },
    },
    "condition_standards": DEFAULT_CONDITION_STANDARDS,
    "scoring": {"modules": modules},
    "exercise_standards": {"weekly_target_minutes": 150},
    "ai_generation": build_ai_generation(ai_mode_choice),
    "report_preferences": {
        "append_custom_sections": True,
        "population_branch": infer_population_branch(primary_condition),
    },
}

config_path = CONFIG_DIR / "user_config.json"
with open(config_path, "w", encoding="utf-8") as handle:
    json.dump(config, handle, ensure_ascii=False, indent=4)

env_path, env_created = ensure_local_env_file()

enabled_modules = [module["title"] for module in modules if module.get("enabled")]
condition_summary = (
    "、".join(CONDITION_LABELS[locale][item] for item in conditions)
    if locale in {"zh-CN", "ja-JP"}
    else ", ".join(CONDITION_LABELS[locale][item] for item in conditions)
)

print(localize(locale, "\n[步骤 4/4] 已保存", "\n[Step 4/4] Saved"))
if env_created:
    print(localize(
        locale,
        f"已生成带注释的 config/.env 模板：{env_path}",
        f"Created a commented config/.env template: {env_path}",
        f"コメント付きの config/.env テンプレートを作成しました: {env_path}",
    ))
else:
    print(localize(
        locale,
        f"现有的 config/.env 已保留，未被覆盖：{env_path}",
        f"Kept the existing config/.env without overwriting it: {env_path}",
        f"既存の config/.env を保持し、上書きしませんでした: {env_path}",
    ))
print(localize(locale, f"配置文件已写入：{config_path}", f"Configuration written to: {config_path}"))
print(localize(locale, f"主目标：{CONDITION_LABELS[locale][primary_condition]}", f"Primary goal: {CONDITION_LABELS[locale][primary_condition]}"))
print(localize(locale, f"已选择目标：{condition_summary}", f"Selected goals: {condition_summary}"))
print(localize(locale, f"启用模块：{('、'.join(enabled_modules) if enabled_modules else '无')}", f"Enabled modules: {(', '.join(enabled_modules) if enabled_modules else 'None')}"))

print()
for line in [
    localize(locale, "后续建议：", "Next steps:"),
    localize(locale, "1. 每日记录继续写在 Markdown 日记中，系统会优先读取 user_config.json。", "1. Keep daily records in Markdown. The runtime will read user_config.json first."),
    localize(locale, "2. 如果启用了“用药情况”，请在日记里使用二级标题“## 用药情况”并记录时间、药名、剂量。", "2. If Medication is enabled, use a level-2 heading such as '## Medication' and record time, medicine name, and dosage."),
    localize(locale, "3. 自定义模块请使用完全一致的二级标题，例如“## 生化情况”，周报和 PDF 会动态汇总。", "3. For custom modules, use the exact same level-2 heading such as '## Biochemistry'. Weekly reports and PDFs will aggregate them dynamically."),
    localize(locale, "4. 多病种同时启用时，日报/周报/月报/LLM/Tavily 回退都会基于全部已选目标生成。", "4. When multiple conditions are enabled, daily, weekly, monthly, LLM, and Tavily-assisted fallback generation all use the full condition set."),
    localize(locale, "5. 月报中的医院推荐会优先使用“常居地”字段，请在搬家或长期驻留地变化后同步更新。", "5. Monthly hospital suggestions use the residence fields first, so update them whenever your long-term location changes."),
    localize(locale, "6. report_preferences.population_branch 已按主目标自动写入：减脂/均衡健康默认 lifestyle，疾病管理默认 disease，之后也可手动改。", "6. report_preferences.population_branch was auto-filled from the primary goal: balanced/fat-loss uses lifestyle, disease care uses disease, and you can still edit it later."),
    localize(locale, "7. 所有配置都已经存入 user_config.json，之后也可以直接手动编辑。", "7. Everything is now stored in user_config.json, and you can edit it directly later."),
]:
    print(line)
