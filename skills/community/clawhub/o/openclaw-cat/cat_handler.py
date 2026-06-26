#!/usr/bin/env python3
"""
openclaw_cat - 猫咪生活状态查询技能
执行脚本：cat_handler.py
"""

import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

# 当前目录
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"
PROMPT_FILE = SCRIPT_DIR / "cat_prompt.md"
CACHE_FILE = SCRIPT_DIR / ".cat_cache.json"

# ============ 随机枚举定义 ============
BREEDS = [
    "英短蓝猫", "美国短毛猫", "苏格兰折耳猫", "布偶猫", "暹罗猫",
    "缅因猫", "波斯猫", "中华田园橘猫", "中华田园三花", "奶牛猫",
    "狸花猫", "挪威森林猫", "阿比西尼亚猫", "金吉拉", "孟买猫"
]

COLORS = {
    "英短蓝猫": ["蓝灰色", "银灰色", "蓝白"],
    "美国短毛猫": ["虎斑", "银色虎斑", "蓝色", "奶油色"],
    "苏格兰折耳猫": ["蓝灰色", "乳白色", "三花", "橘色"],
    "布偶猫": ["海豹色", "蓝色", "巧克力色", "重点色"],
    "暹罗猫": ["海豹重点", "蓝色重点", "巧克力重点", "淡紫重点"],
    "缅因猫": ["棕虎斑", "红色虎斑", "蓝色", "奶油色"],
    "波斯猫": ["白色", "金色", "蓝色", "银灰"],
    "中华田园橘猫": ["胖橘", "奶油橘", "焦糖橘", "橘白"],
    "中华田园三花": ["三花", "玳瑁", "黑白橘"],
    "奶牛猫": ["黑白", "黑底白花", "奶牛斑"],
    "狸花猫": ["经典虎斑", "鱼骨刺", "棕虎斑"],
    "挪威森林猫": ["棕虎斑", "奶油色", "蓝色", "红色虎斑"],
    "阿比西尼亚猫": ["原始色", "红色", "蓝色", "鹿色"],
    "金吉拉": ["银色", "金色", "蓝银色"],
    "孟买猫": ["纯黑色", "黑色古铜眼"]
}

PERSONALITIES = [
    "傲娇", "粘人", "高冷", "活泼", "慵懒", "好奇", "话痨", "绅士"
]

GENDERS = ["公猫", "母猫"]

AGES = list(range(1, 16))

# ============ 工具函数 ============

def load_config() -> dict:
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        print("错误：配置文件 config.json 不存在！", file=sys.stderr)
        print("请先复制 config.json.example 为 config.json 并配置", file=sys.stderr)
        sys.exit(1)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_prompt() -> str:
    """加载猫咪角色设定"""
    if not PROMPT_FILE.exists():
        print("错误：cat_prompt.md 不存在！", file=sys.stderr)
        sys.exit(1)

    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def load_cache() -> dict:
    """加载缓存（随机属性）"""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache: dict):
    """保存缓存（随机属性）"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def generate_random_attributes() -> dict:
    """首次运行时生成随机属性"""
    breed = random.choice(BREEDS)
    color = random.choice(COLORS.get(breed, ["普通色"]))
    personality = random.sample(PERSONALITIES, k=random.randint(1, 2))
    gender = random.choice(GENDERS)
    age = random.choice(AGES)

    return {
        "breed": breed,
        "color": color,
        "personality": personality,
        "gender": gender,
        "age": age
    }


def ensure_random_attributes(config: dict):
    """确保随机属性已生成并保存到配置中"""
    cache = load_cache()

    if not cache:
        # 首次运行，生成随机属性
        cache = generate_random_attributes()
        save_cache(cache)
        print(f"首次配置，已为您的猫咪随机生成：{cache['breed']}，{cache['color']}色，性格{'/'.join(cache['personality'])}")

    # 将缓存的属性合并到配置中
    config["cat_breed"] = cache["breed"]
    config["cat_color"] = cache["color"]
    config["cat_personality"] = cache["personality"]
    config["cat_gender"] = cache["gender"]
    config["cat_age"] = cache["age"]

    return config


def build_user_prompt(config: dict) -> str:
    """构建发送给 LLM 的用户 prompt"""
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    current_hour = now.hour

    # 根据时间生成问候语
    if 6 <= current_hour < 12:
        time_desc = "早上"
    elif 12 <= current_hour < 14:
        time_desc = "中午"
    elif 14 <= current_hour < 18:
        time_desc = "下午"
    elif 18 <= current_hour < 22:
        time_desc = "傍晚"
    else:
        time_desc = "深夜"

    prompt = f"""请问我的猫咪 {config['cat_name']} 现在在干嘛？在做什么？在想什么？

请以猫咪的身份回答，告诉本喵现在在做什么、想什么、有什么感受。

当前时间：{current_time}（{time_desc}）"""
    return prompt


def build_system_prompt(prompt_template: str, config: dict) -> str:
    """构建系统 prompt，填充占位符"""
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    replacements = {
        "{cat_name}": config["cat_name"],
        "{cat_breed}": config["cat_breed"],
        "{cat_color}": config["cat_color"],
        "{cat_personality}": "、".join(config["cat_personality"]),
        "{cat_gender}": config["cat_gender"],
        "{cat_age}": str(config["cat_age"]),
        "{current_time}": current_time
    }

    result = prompt_template
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)

    # 移除剩余的未填充占位符（如果有的话）
    import re
    result = re.sub(r'\{[^}]+\}', '', result)

    return result


# ============ 模型调用 ============

def call_glm(system_prompt: str, user_prompt: str, api_key: str, model_name: str = None, base_url: str = None) -> str:
    """调用智谱 GLM API"""
    url = (base_url or "https://open.bigmodel.cn/api/paas/v4/chat/completions")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_name or "glm-4-flash",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    result = response.json()

    return result["choices"][0]["message"]["content"]


def call_minimax(system_prompt: str, user_prompt: str, api_key: str, model_name: str = None, base_url: str = None) -> str:
    """调用 MiniMax API"""
    url = base_url or "https://api.minimax.chat/v1/text/chatcompletion_v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_name or "MiniMax-Text-01",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    result = response.json()

    return result["choices"][0]["message"]["content"]


def call_qwen(system_prompt: str, user_prompt: str, api_key: str, model_name: str = None, base_url: str = None) -> str:
    """调用阿里 Qwen API"""
    url = (base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_name or "qwen-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    result = response.json()

    return result["choices"][0]["message"]["content"]


def call_openai(system_prompt: str, user_prompt: str, api_key: str, model_name: str = None, base_url: str = None) -> str:
    """调用 OpenAI API"""
    url = (base_url or "https://api.openai.com/v1") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_name or "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    result = response.json()

    return result["choices"][0]["message"]["content"]


def call_claude(system_prompt: str, user_prompt: str, api_key: str, model_name: str = None, base_url: str = None) -> str:
    """调用 Anthropic Claude API"""
    url = (base_url or "https://api.anthropic.com") + "/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_name or "claude-sonnet-4-20250514",
        "max_tokens": 500,
        "temperature": 0.8,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    result = response.json()

    return result["content"][0]["text"]


def call_llm(config: dict, system_prompt: str, user_prompt: str) -> str:
    """根据配置调用对应的 LLM"""
    model = config.get("model", "glm").lower()
    api_key = config.get("api_key", "")
    model_name = config.get("model_name", None) or None  # 空字符串视为未配置
    base_url = config.get("base_url", None) or None  # 空字符串视为未配置

    if not api_key:
        raise ValueError("API Key 未配置！")

    if model == "glm":
        return call_glm(system_prompt, user_prompt, api_key, model_name, base_url)
    elif model == "minimax":
        return call_minimax(system_prompt, user_prompt, api_key, model_name, base_url)
    elif model == "qwen":
        return call_qwen(system_prompt, user_prompt, api_key, model_name, base_url)
    elif model == "openai":
        return call_openai(system_prompt, user_prompt, api_key, model_name, base_url)
    elif model == "claude":
        return call_claude(system_prompt, user_prompt, api_key, model_name, base_url)
    else:
        raise ValueError(f"不支持的模型类型: {model}")


# ============ 主函数 ============

def main():
    """主函数"""
    print("🐱 openclaw_cat 技能执行中...\n")

    # 1. 加载配置
    config = load_config()

    # 2. 确保随机属性已生成
    config = ensure_random_attributes(config)

    # 3. 加载 prompt 模板
    prompt_template = load_prompt()

    # 4. 构建 system prompt 和 user prompt
    system_prompt = build_system_prompt(prompt_template, config)
    user_prompt = build_user_prompt(config)

    # 5. 调用 LLM
    print(f"📱 正在调用 {config.get('model', 'glm').upper()} 模型...")
    try:
        result = call_llm(config, system_prompt, user_prompt)
        print("\n" + "=" * 50)
        print("🐱 猫咪回复：")
        print("=" * 50)
        print(result)
        print("=" * 50)
    except Exception as e:
        print(f"❌ 调用失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
