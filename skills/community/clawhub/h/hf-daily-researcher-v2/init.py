#!/usr/bin/env python3
"""
HF Daily Deep Researcher - 初始化脚本
根据当前环境自动创建初始配置

用法：
  python init.py [--reset]

首次运行：
  1. 自动从 USER.md / MEMORY.md 提取用户信息（如存在）
  2. 如无法提取研究方向，提示用户手动配置
  3. 生成 config.json + keywords.json

重置：
  python init.py --reset
  这会清空所有配置，重新生成
"""

import json
import os
import re
import sys
from datetime import datetime

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")

def _slurp(path):
    """安全读取文件内容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""

def extract_user_info():
    """从环境文件提取用户信息"""
    info = {
        "name": None,
        "institution": None,
        "research_focus": [],
        "current_projects": []
    }

    # 1. 尝试从 USER.md 提取
    user_md = _slurp(os.path.join(WORKSPACE_DIR, "USER.md"))
    if user_md:
        m = re.search(r'[Nn]ame[:：\s*]+(?:\*\*)?(\S+?)(?:\*\*)?(?:\s|$)', user_md)
        if m:
            raw_name = m.group(1).strip().strip('*')
            info["name"] = re.split(r'[（(]', raw_name)[0].strip()

        inst_patterns = [
            r'(?:公司|机构|institution|org)[:：\s]+(\S+)',
            r'(?:就职于|在|at)\s+([\u4e00-\u9fa5A-Za-z]+)',
            r'Huawei|腾讯|字节|阿里|百度|Google|Meta|OpenAI|Microsoft|Amazon|Apple|DeepSeek'
        ]
        for pat in inst_patterns:
            m = re.search(pat, user_md)
            if m:
                info["institution"] = m.group(0) if m.lastindex is None else m.group(1)
                break

    # 2. 尝试从 MEMORY.md 提取研究兴趣
    memory_md = _slurp(os.path.join(WORKSPACE_DIR, "MEMORY.md"))
    if memory_md:
        tech_signals = [
            ("credit assignment", "credit assignment"),
            ("agentic RL", "agentic RL"),
            ("agentic reinforcement learning", "agentic RL"),
            ("multi-scale", "multi-scale RL"),
            ("hierarchical RL", "hierarchical RL"),
            ("policy optimization", "policy optimization"),
            ("reward model", "reward modeling"),
            ("reinforcement learning", "reinforcement learning"),
        ]
        for keyword, label in tech_signals:
            if keyword.lower() in memory_md.lower() and label not in info["research_focus"]:
                info["research_focus"].append(label)

    # 3. 尝试从最近对话记忆提取
    memory_dir = os.path.join(WORKSPACE_DIR, "memory")
    if os.path.isdir(memory_dir):
        files = sorted(
            [f for f in os.listdir(memory_dir) if f.endswith('.md') and len(f) == 14],
            reverse=True
        )[:3]
        for f in files:
            content = _slurp(os.path.join(memory_dir, f))
            if "credit assignment" in content.lower() and "credit assignment" not in info["research_focus"]:
                info["research_focus"].append("credit assignment")
            if "agentic" in content.lower() and "agentic RL" not in info["research_focus"]:
                info["research_focus"].append("agentic RL")

    # 4. 环境变量兜底
    if not info["name"]:
        info["name"] = os.environ.get("USER", os.environ.get("USERNAME", ""))

    return info

def generate_keywords(research_focus):
    """
    根据研究兴趣生成关键词。
    如无法自动识别研究方向，返回空列表，提示用户手动配置。
    """
    if not research_focus:
        return []

    # 研究方向已知，生成相关关键词
    base_keywords = [
        {"term": "credit assignment", "weight": 1.0, "source": "auto", "category": "core"},
        {"term": "agentic reinforcement learning", "weight": 0.95, "source": "auto", "category": "core"},
        {"term": "agentic RL", "weight": 0.95, "source": "auto", "category": "core"},
        {"term": "multi-scale RL", "weight": 0.85, "source": "auto", "category": "core"},
        {"term": "hierarchical RL", "weight": 0.8, "source": "auto", "category": "core"},
        {"term": "turn-level policy optimization", "weight": 0.75, "source": "auto", "category": "core"},
        {"term": "step-level advantage", "weight": 0.75, "source": "auto", "category": "core"},
        {"term": "group policy optimization", "weight": 0.7, "source": "auto", "category": "core"},
        {"term": "GiGPO", "weight": 0.7, "source": "auto", "category": "method"},
        {"term": "GRPO", "weight": 0.7, "source": "auto", "category": "method"},
        {"term": "GAGPO", "weight": 0.6, "source": "auto", "category": "method"},
        {"term": "hindsight credit", "weight": 0.65, "source": "auto", "category": "core"},
        {"term": "hindsight policy optimization", "weight": 0.65, "source": "auto", "category": "core"},
        {"term": "OPD", "weight": 0.5, "source": "auto", "category": "method"},
        {"term": "online preference distillation", "weight": 0.55, "source": "auto", "category": "method"},
        {"term": "process reward model", "weight": 0.5, "source": "auto", "category": "core"},
        {"term": "PRM", "weight": 0.5, "source": "auto", "category": "method"},
        {"term": "tool use RL", "weight": 0.5, "source": "auto", "category": "related"},
        {"term": "tool learning RL", "weight": 0.5, "source": "auto", "category": "related"},
        {"term": "multi-agent RL", "weight": 0.4, "source": "auto", "category": "related"},
        {"term": "MARL", "weight": 0.4, "source": "auto", "category": "related"},
        {"term": "graph-based RL", "weight": 0.45, "source": "auto", "category": "related"},
    ]

    # 根据研究兴趣筛选和提升权重
    focus_lower = [f.lower() for f in research_focus]
    filtered = []
    for kw in base_keywords:
        matched = any(kw["term"].lower() in fl or fl in kw["term"].lower() for fl in focus_lower)
        if matched:
            kw["weight"] = min(1.0, kw["weight"] + 0.15)
            kw["source"] = "inferred"
            filtered.append(kw)
        elif kw["category"] == "core":
            # 核心关键词保留，但降低权重
            kw["weight"] = max(0.3, kw["weight"] - 0.2)
            filtered.append(kw)

    return filtered

def init_config(reset=False):
    """创建初始配置文件"""

    config_path = os.path.join(SKILL_DIR, "config.json")
    keywords_path = os.path.join(SKILL_DIR, "keywords.json")

    if reset or not os.path.exists(config_path):
        user_info = extract_user_info()
        if not user_info["research_focus"]:
            user_info["research_focus"] = []
        if not user_info["current_projects"]:
            user_info["current_projects"] = []

        config = {
            "user_profile": {
                "name": user_info["name"] or "",
                "institution": user_info["institution"] or "",
                "research_focus": user_info["research_focus"],
                "current_projects": user_info["current_projects"]
            },
            "tracking": {
                "base_frequency": "weekly",
                "adaptive": True,
                "sources": ["arxiv", "hf_papers"],
                "max_papers_per_scan": 50,
                "last_scan_date": None,
                "next_scan_date": None
            },
            "keywords": {
                "auto_expand": True,
                "min_weight": 0.1,
                "max_keywords": 30,
                "expansion_model": "default"
            },
            "analysis": {
                "default_level": "scan",
                "auto_deep_read": True,
                "auto_deep_threshold": 0.7,
                "max_deep_papers_per_scan": 3
            },
            "output": {
                "local_save_dir": "~/.openclaw/workspace/skills/hf-daily-deep-researcher/reports",
                "report_naming_pattern": "{source}_{period}_{focus}_Report_{date}.md",
                "version_management": {
                    "enabled": True,
                    "keep_per_period": 1,
                    "period_format": "%Y%m%d"
                },
                "cloud_upload": {
                    "enabled": False,
                    "on_demand": True,
                    "folder_token": None
                },
                "report_format": "markdown",
                "save_history": True,
                "history_dir": "~/.openclaw/workspace/skills/hf-daily-deep-researcher/history"
            },
            "notifications": {
                "p0_alert": True,
                "weekly_summary": True,
                "trend_change_alert": True,
                "author_alert": False
            },
            "version": "4.0.8",
            "created_date": datetime.now().isoformat()
        }

        keywords_data = {
            "keywords": generate_keywords(user_info["research_focus"]),
            "blacklist": [
                "robotics",
                "embodied",
                "game playing",
                "Atari",
                "game AI",
                "player"
            ],
            "authors": [],
            "institutions": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }

        os.makedirs(SKILL_DIR, exist_ok=True)
        os.makedirs(os.path.join(SKILL_DIR, "history"), exist_ok=True)
        os.makedirs(os.path.join(SKILL_DIR, "reports"), exist_ok=True)

        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        with open(keywords_path, 'w') as f:
            json.dump(keywords_data, f, indent=2, ensure_ascii=False)

        print("✅ HF Daily Deep Researcher 初始化完成!")
        print(f"\n📁 配置文件位置: {SKILL_DIR}")

        print(f"\n👤 用户配置:")
        print(f"   名称: {user_info['name'] or '(未识别)'})")
        print(f"   机构: {user_info['institution'] or '(未识别)'})")

        if user_info['research_focus']:
            print(f"   研究方向: {', '.join(user_info['research_focus'])}")
            print(f"\n🔍 已生成 {len(keywords_data['keywords'])} 个追踪关键词")
        else:
            print(f"   研究方向: ❌ 未配置")
            print(f"\n⚠️  重要：首次运行前必须配置研究方向！")
            print(f"   方法 1: 修改 config.json 中的 user_profile.research_focus")
            print(f"   方法 2: 运行 skill 时，主 Agent 会询问你的研究方向")
            print(f"   示例: [\"natural language processing\", \"large language model\", \"reinforcement learning\"]")

        print(f"\n💡 后续操作:")
        print(f"   1. 检查 config.json 中的配置是否符合预期")
        if not user_info['research_focus']:
            print(f"   2. ⚠️  必须先配置研究方向，否则无法搜索到相关论文")
        else:
            print(f"   2. 运行 skill 开始自动追踪论文")
        print(f"   3. 如需飞书同步，配置 output.cloud_upload.folder_token")
        print(f"   4. 使用 --show-keywords 查看完整关键词列表")
        print(f"   5. 使用 --add-keyword 添加新的关注领域")

    else:
        print(f"⚠️  配置文件已存在: {config_path}")
        print(f"   使用 --reset 强制重新生成")
        with open(config_path, 'r') as f:
            existing = json.load(f)
        focus = existing.get("user_profile", {}).get("research_focus", [])
        if not focus:
            print(f"\n❌ 警告：当前配置中研究方向为空！")
            print(f"   请修改 config.json 中的 user_profile.research_focus")

if __name__ == "__main__":
    reset = "--reset" in sys.argv
    init_config(reset=reset)
