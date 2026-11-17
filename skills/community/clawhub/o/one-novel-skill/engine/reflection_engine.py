#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reflection_engine.py — 反思机制（后记/回顾/洞察提炼）

参考：概念解析文档中段 — Agent Reflection Mechanism
核心功能：
  - 每章后自动做自我审查
  - 从审查中提炼创作洞察
  - 将洞察存入语义记忆供后续使用
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

_log = logging.getLogger("reflection_engine")


class ReflectionEngine:
    """反思引擎 — 写作后自我审查与洞察提炼"""

    def __init__(self):
        self._insights: List[Dict] = []
        self._reflections: List[Dict] = []
        self._history: List[Dict] = []

    def reflect_on_chapter(self, chapter: int, text: str, issues: List[str]) -> Dict:
        """对一章执行反思，返回审查结果"""
        reflection = {
            "chapter": chapter,
            "timestamp": datetime.now().isoformat(),
            "word_count": len(text),
            "issues_count": len(issues),
            "issues": issues[:10],
            "verdict": "",
            "insights": [],
        }

        # 1. 问题分类
        p0_count = sum(1 for i in issues if i.startswith("[P0]"))
        p1_count = sum(1 for i in issues if i.startswith("[P1]"))

        # 2. 判定
        if p0_count > 0:
            reflection["verdict"] = "严重"
            reflection["insights"].append(f"ch{chapter}: 发现 {p0_count} 个 P0 问题，需重视")
        elif p1_count > 2:
            reflection["verdict"] = "需优化"
            reflection["insights"].append(f"ch{chapter}: 存在 {p1_count} 个 P1 问题建议修改")
        else:
            reflection["verdict"] = "合格"

        # 3. 提取可重复使用的洞察
        for issue in issues:
            # 从 issue 中提取规则性内容
            if "重复" in issue or "模板" in issue:
                insight = {
                    "type": "写作规范",
                    "source": f"ch{chapter}",
                    "content": f"避免{issue.split(']')[-1].strip()[:40]}",
                    "chapter": chapter,
                }
                if insight not in self._insights:
                    self._insights.append(insight)
                    reflection["insights"].append(f"规则提炼: {insight['content']}")

        self._reflections.append(reflection)
        return reflection

    def get_insights_text(self) -> str:
        """获取已提炼的创作洞察"""
        if not self._insights:
            return ""
        lines = ["【创作洞察（从反思中提炼）】"]
        for ins in self._insights[-20:]:
            lines.append(f"  - {ins['content']} ({ins['source']})")
        return "\n".join(lines)

    def check_repeated_issues(self, new_issues: List[str]) -> List[str]:
        """检查新问题是否与历史洞察重复（表示上次没改好）"""
        warnings = []
        for issue in new_issues:
            for ins in self._insights:
                kw = ins["content"].split("避免")[-1] if "避免" in ins["content"] else ""
                if kw and kw[:10] in issue:
                    warnings.append(
                        f"[反思] 历史洞察提醒: {ins['content']} — 当前章节仍出现"
                    )
                    break
        return warnings

    def to_dict(self) -> dict:
        return {"insights": self._insights[-50:], "reflections": self._reflections[-50:]}

    def load_from_dict(self, data: dict):
        self._insights = data.get("insights", [])
        self._reflections = data.get("reflections", [])

    def reset(self):
        self._insights.clear()
        self._reflections.clear()

    def promote_learnings(self, skill_dir=None):
        from datetime import datetime
        findings = []
        for entry in self._history[-20:]:
            score = entry.get('scores', {}).get('overall', 0)
            if score is None:
                score = 0
            issues = entry.get('issues', [])
            if score < 5.0 and len(issues) >= 3:
                cats = list(set(i.get('category', '') for i in issues))
                findings.append({'ch': entry.get('chapter', 0), 'score': score,
                                 'cats': cats, 'issue': issues[0].get('description', '')[:60]})
        if not findings:
            return ''
        lines = ['## 可promote教训 ({})'.format(datetime.now().isoformat()[:19])]
        for f in findings:
            lines.append('- ch{} (评分{}): {}'.format(f['ch'], f['score'], f['issue']))
            lines.append('  分类: {}'.format(','.join(f['cats'])))
        if skill_dir:
            lp = Path(skill_dir) / '.learnings' / 'WRITING_LEARNINGS.md'
            lp.parent.mkdir(parents=True, exist_ok=True)
            lp.write_text(chr(10).join(lines), encoding='utf-8')
        return chr(10).join(lines)
