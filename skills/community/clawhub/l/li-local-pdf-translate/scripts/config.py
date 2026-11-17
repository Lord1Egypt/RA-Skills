#!/usr/bin/env python3
"""
模型配置管理 - 独立的配置模块
"""

import json
import os
import re

# 配置文件路径
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_DIR, "default.json")
USER_CONFIG_FILE = os.path.join(CONFIG_DIR, "user.json")

# 默认配置
DEFAULT_CONFIG = {
    "api_url": "http://localhost:8001/v1/chat/completions",
    "api_key": "llama2025",
    "model": "models/Hy-MT2-7B-Q4_K_M.gguf",
    "direction": "en2zh",
    "depth": "standard",
    "batch_size": 3,
    "max_chunk_size": 1500,
    "temperature": 0.3,
    "max_tokens": 4096
}

# 项目根目录（用于解析相对路径，全程不依赖机器绝对目录）
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def _expand_env(value):
    """展开字符串中的环境变量占位符（支持 %VAR% 与 ${VAR}）"""
    if not isinstance(value, str):
        return value
    if "%" in value:
        value = os.path.expandvars(value)
    value = _ENV_PATTERN.sub(lambda m: os.environ.get(m.group(1), m.group(0)), value)
    return value


def resolve_local_path(path):
    """将相对路径解析为基于 skill 根目录的路径（仅用于展示/校验，存储值保持相对路径）"""
    if not path or os.path.isabs(path):
        return path
    return os.path.normpath(os.path.join(SKILL_ROOT, path))

# 支持的八大主要语言
LANGUAGES = {
    "zh": {"name": "中文", "name_en": "Chinese"},
    "en": {"name": "英语", "name_en": "English"},
    "ja": {"name": "日语", "name_en": "Japanese"},
    "ko": {"name": "韩语", "name_en": "Korean"},
    "fr": {"name": "法语", "name_en": "French"},
    "de": {"name": "德语", "name_en": "German"},
    "es": {"name": "西班牙语", "name_en": "Spanish"},
    "ru": {"name": "俄语", "name_en": "Russian"},
}


def normalize_lang(code):
    """
    规范化语言代码，支持 zh-CN / zh_Hans / en-US 等变体，仅取前两位

    Args:
        code: 语言代码，如 "zh-CN"、"en"、"ja"

    Returns:
        str: 两位语言代码
    """
    if not code:
        return None
    return code.lower().replace("_", "-").split("-")[0][:2]


def parse_direction(direction=None):
    """
    解析翻译方向，返回 (source, target) 语言代码元组

    Args:
        direction: 如 "en2zh"、"zh2ja"、"ja2en"（同时兼容 "en-zh" 格式）

    Returns:
        (src, tgt): 两位语言代码元组

    Raises:
        ValueError: 方向格式无效或语言不受支持
    """
    if not direction:
        direction = load_config().get("direction", "en2zh")
    direction = str(direction).strip()
    parts = direction.replace("-", "2").split("2")
    if len(parts) != 2 or not all(parts):
        raise ValueError(
            f"Invalid direction: {direction!r}. Use format like 'en2zh' or 'zh2ja'"
        )
    src = normalize_lang(parts[0].strip())
    tgt = normalize_lang(parts[1].strip())
    supported = ", ".join(sorted(LANGUAGES))
    if src not in LANGUAGES:
        raise ValueError(f"Unsupported source language: {src!r}. Supported: {supported}")
    if tgt not in LANGUAGES:
        raise ValueError(f"Unsupported target language: {tgt!r}. Supported: {supported}")
    return src, tgt


def build_direction(src, tgt):
    """构建方向字符串，如 en2zh"""
    return f"{normalize_lang(src)}2{normalize_lang(tgt)}"


def get_language_info(code):
    """获取语言信息字典"""
    norm = normalize_lang(code)
    if norm in LANGUAGES:
        return LANGUAGES[norm]
    return {"name": code, "name_en": str(code).upper()}


def get_language_name(code, lang="zh"):
    """获取语言名称（lang='zh'返回中文名，否则返回英文名）"""
    info = get_language_info(code)
    return info.get("name" if lang == "zh" else "name_en", str(code))


def list_languages():
    """列出支持的语言代码列表"""
    return list(LANGUAGES.keys())


def get_target_lang(direction=None):
    """
    根据方向获取目标语言代码

    Args:
        direction: 如 "zh2ja"

    Returns:
        str: 目标语言代码，如 "ja"
    """
    try:
        _, tgt = parse_direction(direction)
        return tgt
    except ValueError:
        return "zh"


def load_config(user_only=False):
    """
    加载配置，user.json 优先于 default.json
    
    Args:
        user_only: 仅加载用户配置
    
    Returns:
        dict: 配置字典
    """
    config = DEFAULT_CONFIG.copy()
    
    # 尝试加载 default.json
    if not user_only and os.path.exists(DEFAULT_CONFIG_FILE):
        try:
            with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                config.update(json.load(f))
        except Exception as e:
            print(f"Warning: Failed to load {DEFAULT_CONFIG_FILE}: {e}")
    
    # 尝试加载 user.json (优先级更高)
    if os.path.exists(USER_CONFIG_FILE):
        try:
            with open(USER_CONFIG_FILE, 'r', encoding='utf-8') as f:
                config.update(json.load(f))
        except Exception as e:
            print(f"Warning: Failed to load {USER_CONFIG_FILE}: {e}")

    config = {k: _expand_env(v) for k, v in config.items()}

    for env_name, key in (("PDF_TRANSLATE_API_KEY", "api_key"),
                          ("PDF_TRANSLATE_API_URL", "api_url"),
                          ("PDF_TRANSLATE_MODEL", "model")):
        if os.environ.get(env_name):
            config[key] = os.environ[env_name]

    return config


def save_config(config, is_user=True):
    """
    保存配置
    
    Args:
        config: 配置字典
        is_user: True保存为user.json, False保存为default.json
    """
    target_file = USER_CONFIG_FILE if is_user else DEFAULT_CONFIG_FILE
    
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"Config saved to: {target_file}")


def get_api_config():
    """获取API相关配置"""
    config = load_config()
    return {
        "api_url": config["api_url"],
        "api_key": config["api_key"],
        "model": config["model"]
    }


def get_translation_config():
    """获取翻译相关配置"""
    config = load_config()
    return {
        "direction": config["direction"],
        "depth": config["depth"],
        "batch_size": config["batch_size"],
        "max_chunk_size": config["max_chunk_size"],
        "temperature": config["temperature"],
        "max_tokens": config["max_tokens"]
    }


def show_config():
    """显示当前配置"""
    config = load_config()
    direction = config.get("direction", "en2zh")
    src, tgt = ("", "")
    try:
        src, tgt = parse_direction(direction)
    except ValueError:
        pass

    print("\n=== Current Configuration ===")
    print(f"API URL:     {config['api_url']}")
    api_key = config["api_key"]
    print(f"API Key:     {api_key[:4] + '*' * max(len(api_key) - 4, 0)}")
    print(f"Model:       {os.path.basename(config['model']) if config['model'] else 'default'}")
    print(f"Direction:   {direction}"
          + (f" ({get_language_name(src, 'zh')}->{get_language_name(tgt, 'zh')})" if src else ""))
    print(f"Depth:       {config['depth']}")
    print(f"Batch Size:  {config['batch_size']}")
    print(f"Temperature: {config['temperature']}")
    print(f"Max Tokens:  {config['max_tokens']}")
    print("-----------------------------")
    print("Supported Languages (8):")
    for code, info in LANGUAGES.items():
        print(f"    {code:>3} - {info['name']} ({info['name_en']})")
    print("Direction format: [src]2[tgt], e.g. en2zh / zh2ja / ja2en")
    print("=============================\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "show":
            show_config()
        elif cmd == "set" and len(sys.argv) >= 4:
            key = sys.argv[2]
            value = sys.argv[3]
            config = load_config()
            # 尝试转换类型
            if value.lower() in ("true", "false"):
                value = value.lower() == "true"
            elif value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except:
                    pass
            config[key] = value
            save_config(config)
            print(f"Set {key} = {value}")
        else:
            print("Usage: python config.py [show|set key value]")
    else:
        show_config()
