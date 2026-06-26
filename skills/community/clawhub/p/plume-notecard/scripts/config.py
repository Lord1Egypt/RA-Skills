#!/usr/bin/env python3
"""
plume-notecard 配置系统

环境检测、EXTEND.md 加载、路径选择、凭证剥离。
支持 Claude Code / OpenClaw / Cursor / Cline / 通用环境。
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

SKILL_NAME = "plume-notecard"

# ─── 凭证剥离 ──────────────────────────────────────────────

CREDENTIAL_PATTERNS = [
    r'sk-[a-zA-Z0-9]{20,}',
    r'AIza[a-zA-Z0-9_-]{35}',
    r'ghp_[a-zA-Z0-9]{36}',
    r'xox[baprs]-[a-zA-Z0-9-]+',
    r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*',
]


def strip_credentials(content: str) -> str:
    """剥离内容中的凭证/密钥/Token"""
    for pattern in CREDENTIAL_PATTERNS:
        content = re.sub(pattern, '[REDACTED]', content, flags=re.IGNORECASE)
    return content


# ─── 环境检测 ──────────────────────────────────────────────

def detect_agent_env() -> dict:
    """检测当前 Agent 环境，返回 agent/media_dir"""
    env = {"agent": "generic", "media_dir": None}

    # 优先检测 Claude Code（通过环境变量）
    # CLAUDE_SKILL_DIR: skill 执行时设置
    # CLAUDE_SESSION_ID: Claude Code 会话环境
    # CLAUDECODE: Claude Code CLI 环境
    if (os.environ.get("CLAUDE_SKILL_DIR") or
        os.environ.get("CLAUDE_SESSION_ID") or
        os.environ.get("CLAUDECODE")):
        env["agent"] = "claude-code"
        env["media_dir"] = str(Path.home() / ".claude" / "media" / SKILL_NAME)
        return env

    # 其次检测 OpenClaw
    if os.path.exists(os.path.expanduser("~/.openclaw")):
        env["agent"] = "openclaw"
        env["media_dir"] = str(Path.home() / ".openclaw" / "media" / SKILL_NAME)
        return env

    # 最后检查 ~/.claude 目录存在（可能是其他方式运行的 Claude Code）
    if os.path.exists(os.path.expanduser("~/.claude")):
        env["agent"] = "claude-code"
        env["media_dir"] = str(Path.home() / ".claude" / "media" / SKILL_NAME)
        return env

    # 通用环境使用 ~/.agent/ 目录
    env["media_dir"] = str(Path.home() / ".agent" / SKILL_NAME)
    return env


# ─── EXTEND.md 配置加载 ────────────────────────────────────

def _find_extend_md() -> Optional[Path]:
    """按优先级查找 EXTEND.md：项目级 > 用户级"""
    # 项目级
    project_path = Path(f".{SKILL_NAME}") / "EXTEND.md"
    if project_path.exists():
        return project_path

    # 用户级
    user_path = Path.home() / f".{SKILL_NAME}" / "EXTEND.md"
    if user_path.exists():
        return user_path

    return None


def _parse_yaml_frontmatter(text: str) -> Optional[dict]:
    """解析 EXTEND.md 的 YAML frontmatter（纯标准库，不依赖 PyYAML）"""
    text = text.strip()
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    yaml_block = text[3:end].strip()

    result = {}
    current_section = None
    for line in yaml_block.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # 顶层 key: value
        if not line.startswith(" ") and not line.startswith("\t"):
            if ":" in stripped:
                key, _, val = stripped.partition(":")
                key = key.strip()
                val = val.strip()
                if val and val != "null":
                    # 去除引号
                    if val.startswith('"') and val.endswith('"'):
                        val = val[1:-1]
                    elif val.startswith("'") and val.endswith("'"):
                        val = val[1:-1]
                    # 布尔/数字转换
                    if val.lower() == "true":
                        val = True
                    elif val.lower() == "false":
                        val = False
                    else:
                        try:
                            val = int(val)
                        except ValueError:
                            try:
                                val = float(val)
                            except ValueError:
                                pass
                    result[key] = val
                elif val == "null":
                    result[key] = None
                else:
                    result[key] = {}
                    current_section = key
            continue

        # 嵌套 key: value
        if current_section is not None and ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "null":
                val = None
            elif val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            elif val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            else:
                try:
                    val = int(val)
                except ValueError:
                    try:
                        val = float(val)
                    except ValueError:
                        pass
            if isinstance(result.get(current_section), dict):
                result[current_section][key] = val

    return result


def load_extend_config() -> dict:
    """加载 EXTEND.md 配置，返回合并后的 dict"""
    path = _find_extend_md()
    if not path:
        return {}
    try:
        text = path.read_text(encoding="utf-8")
        return _parse_yaml_frontmatter(text) or {}
    except OSError:
        return {}


# ─── 媒体目录 ──────────────────────────────────────────────

def get_media_dir() -> Path:
    """获取媒体存储目录（优先 EXTEND.md 配置，否则自动检测）"""
    config = load_extend_config()
    storage = config.get("storage", {})
    if isinstance(storage, dict) and storage.get("media_dir"):
        return Path(storage["media_dir"])

    env = detect_agent_env()
    return Path(env["media_dir"])


# ─── API Key ──────────────────────────────────────────────

def get_api_key() -> Optional[str]:
    """多源获取 API Key"""
    # 1. 环境变量
    key = os.environ.get("PLUME_API_KEY")
    if key:
        return key

    # 2. EXTEND.md 中指定的环境变量名
    config = load_extend_config()
    api_key_env = config.get("api_key_env")
    if api_key_env and isinstance(api_key_env, str):
        key = os.environ.get(api_key_env)
        if key:
            return key

    # 3. OpenClaw 配置文件
    env = detect_agent_env()
    if env["agent"] == "openclaw":
        openclaw_config = Path.home() / ".openclaw" / "openclaw.json"
        if openclaw_config.exists():
            try:
                data = json.loads(openclaw_config.read_text(encoding="utf-8"))
                # OpenClaw 配置结构：env.vars.PLUME_API_KEY
                # 向后兼容：也支持可能的 env.PLUME_API_KEY 结构
                key = (data.get("env", {}).get("vars", {}).get("PLUME_API_KEY") or
                       data.get("env", {}).get("PLUME_API_KEY"))
                if key:
                    return key
            except (json.JSONDecodeError, OSError):
                pass

    return None


def get_api_base() -> str:
    """获取 API Base URL"""
    config = load_extend_config()
    return config.get("api_base_url") or "https://design.useplume.app"
