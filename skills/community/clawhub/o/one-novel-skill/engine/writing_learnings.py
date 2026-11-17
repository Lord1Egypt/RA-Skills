#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
writing_learnings.py — 创作学习沉淀管理

融合源: self-improving-agent 的 promote 决策树
功能: 
  1. 管理 .learnings/ 目录的创作教训
  2. 自动判断"这个创作教训该沉淀到哪"
  3. 提供 promote 决策树
"""

from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime


# === promote 决策树规则 ===

PROMOTE_RULES = {
    "创作规范": {
        "condition": "发现某类问题重复出现2次以上",
        "action": "沉淀到 references/writing-techniques-allinone/ 对应文件",
        "target": "references/writing-techniques-allinone/",
        "frequency_threshold": 2,
    },
    "检测规则": {
        "condition": "发现新的AI味模式或禁用词",
        "action": "更新 detection_config.yaml 或 references/de-ai/",
        "target": "references/de-ai/",
        "frequency_threshold": 1,
    },
    "行为习惯": {
        "condition": "发现用户偏好的写作习惯（字数/节奏/风格）",
        "action": "更新 user_preferences.json → PreferenceManager",
        "target": "user_preferences.json",
        "frequency_threshold": 3,
    },
    "模板优化": {
        "condition": "章节规格或模板有改进空间",
        "action": "更新 templates/ 目录下对应模板",
        "target": "templates/",
        "frequency_threshold": 1,
    },
    "代码修复": {
        "condition": "引擎代码有bug或可优化",
        "action": "更新 engine/ 对应文件",
        "target": "engine/",
        "frequency_threshold": 1,
    },
    "配置参数": {
        "condition": "检测阈值或基准需要校准",
        "action": "更新 detection_config.yaml 或 baselines.json",
        "target": "baselines.json",
        "frequency_threshold": 1,
    },
}


class LearningsManager:
    """创作学习管理者"""

    def __init__(self, skill_dir: Path):
        self.skill_dir = Path(skill_dir)
        self.learnings_dir = self.skill_dir / ".learnings"

    def ensure_dirs(self):
        self.learnings_dir.mkdir(parents=True, exist_ok=True)
        for fname in ["WRITING_LEARNINGS.md", "WRITING_ERRORS.md", "WRITING_INSIGHTS.md"]:
            f = self.learnings_dir / fname
            if not f.exists():
                f.write_text(f"# {fname.replace('.md','')}\n\n> 创作教训管理 | 自动沉淀规则参考 PROMOTE_RULES\n\n", encoding="utf-8")

    def log_learning(self, category: str, content: str, source: str = ""):
        """记录一条创作教训
        
        Args:
            category: correction / insight / best_practice / knowledge_gap
            content: 教训内容
            source: 来源（章节XX/检测XX）
        """
        self.ensure_dirs()
        
        # 决定写入哪个文件
        file_map = {
            "correction": "WRITING_ERRORS.md",
            "insight": "WRITING_INSIGHTS.md",
            "best_practice": "WRITING_LEARNINGS.md",
            "knowledge_gap": "WRITING_LEARNINGS.md",
        }
        fname = file_map.get(category, "WRITING_LEARNINGS.md")
        f = self.learnings_dir / fname
        
        entry = [
            f"\n## [{datetime.now().strftime('%Y%m%d-%H%M')}] {category}",
            f"来源: {source or '未指定'}",
            f"内容: {content}",
            "",
        ]
        with f.open("a", encoding="utf-8") as fh:
            fh.write("\n".join(entry))

    def is_repeat(self, content: str, category: str = "") -> tuple:
        """检查是否是重复问题，返回 (is_repeat, count)"""
        self.ensure_dirs()
        file_map = {
            "correction": "WRITING_ERRORS.md",
            "insight": "WRITING_INSIGHTS.md",
        }
        fname = file_map.get(category, "WRITING_LEARNINGS.md")
        f = self.learnings_dir / fname
        if not f.exists():
            return False, 0
        
        text = f.read_text(encoding="utf-8", errors="replace")
        keywords = content[:30]
        count = text.count(keywords)
        return count >= 1, count

    def check_promote(self) -> List[Dict]:
        """检查是否需要promote到正式文件"""
        results = []
        self.ensure_dirs()
        
        for rule_name, rule in PROMOTE_RULES.items():
            f = self.learnings_dir / "WRITING_ERRORS.md"
            if f.exists():
                text = f.read_text(encoding="utf-8", errors="replace")
                # 统计同类条目数
                sections = text.count("## [")
                if sections >= rule["frequency_threshold"]:
                    results.append({
                        "rule": rule_name,
                        "condition": rule["condition"],
                        "action": rule["action"],
                        "target": rule["target"],
                        "current_count": sections,
                        "threshold": rule["frequency_threshold"],
                    })
        return results

    def summary(self) -> str:
        """输出学习沉淀摘要"""
        self.ensure_dirs()
        lines = [f"=== 创作学习沉淀 ==="]
        for fname in ["WRITING_LEARNINGS.md", "WRITING_ERRORS.md", "WRITING_INSIGHTS.md"]:
            f = self.learnings_dir / fname
            if f.exists():
                text = f.read_text(encoding="utf-8", errors="replace")
                count = text.count("## [")
                lines.append(f"  {fname}: {count} 条记录")
        
        promotes = self.check_promote()
        if promotes:
            lines.append(f"  待promote: {len(promotes)} 条")
            for p in promotes:
                lines.append(f"    → [{p['rule']}] {p['action']}")
        return "\n".join(lines)
