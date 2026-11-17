#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prewriting_analyzer.py — 写前分析预览引擎

SKILL.md 声明功能：
- 每章正文写作前，生成写前分析预览展示给用户确认
- 预览内容：前文摘要/角色状态快照/活跃伏笔/本章风险标记/完成标准
- 流程：读取追踪文件 → 生成预览 → 用户确认 → 进入正文生成
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

_log = logging.getLogger("prewriting_analyzer")


class PrewritingAnalyzer:
    """写前分析预览引擎"""

    def __init__(self, book_dir: str = ""):
        self.book_dir = Path(book_dir) if book_dir else Path.cwd()
        self._track_dir = self.book_dir / "追踪"
        self._text_dir = self.book_dir / "正文"
        self._setting_dir = self.book_dir / "设定"
        self._outline_dir = self.book_dir / "大纲"

    # ====== 核心分析 ======

    def analyze(self, chapter: int, state: Dict = None) -> Dict[str, Any]:
        """生成完整写前分析预览

        Args:
            chapter: 当前要写的章节号
            state: NovelState._state dict 或 StateRoot.to_dict()

        Returns:
            完整预览数据，包含前文摘要/角色快照/活跃伏笔/风险标记/完成标准
        """
        preview = {
            "chapter": chapter,
            "generated_at": datetime.now().isoformat(),
            "previous_summary": self._get_previous_summary(chapter, state),
            "character_snapshot": self._get_character_snapshot(state),
            "active_hooks": self._get_active_hooks(state),
            "risk_flags": self._get_risk_flags(chapter, state),
            "completion_criteria": self._get_completion_criteria(chapter, state),
            "context_reminders": self._get_context_reminders(chapter),
        }

        preview["ready"] = self._check_ready(preview)
        return preview

    def generate_preview_markdown(self, chapter: int, state: Dict = None) -> str:
        """生成人类可读的写前分析预览 Markdown"""
        data = self.analyze(chapter, state)
        lines = [
            f"# 第{chapter}章 写前分析预览",
            f"",
            f"> 生成时间：{data['generated_at'][:19]}",
            f"> 就绪状态：{'✅ 可以开始写作' if data['ready'] else '⚠️ 建议先处理以下问题'}",
            f"",
            f"---",
            f"",
            f"## 📖 前文摘要",
        ]

        ps = data["previous_summary"]
        if ps.get("has_previous"):
            lines.append(f"- 上一章：第{ps['last_chapter']}章")
            if ps.get("last_lines"):
                lines.append(f"- 上一章结尾：")
                for line in ps["last_lines"]:
                    lines.append(f"  > {line}")
            if ps.get("recent_events"):
                lines.append(f"- 最近关键事件：")
                for e in ps["recent_events"][:5]:
                    lines.append(f"  - {e}")
        else:
            lines.append("- 🆕 这是第一章，无前文")
            lines.append("- 建议先完成世界观设定和大纲规划")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 👤 角色状态快照")
        cs = data["character_snapshot"]
        if cs.get("characters"):
            lines.append("")
            lines.append("| 角色 | 身份 | 位置 | 状态 | 最近出场 |")
            lines.append("|------|------|------|------|---------|")
            for char in cs["characters"][:10]:
                lines.append(
                    f"| {char['name']} | {char.get('identity', '?')} | "
                    f"{char.get('location', '?')} | {char.get('state', '?')} | "
                    f"第{char.get('last_seen', '?')}章 |"
                )
            if cs.get("issues"):
                for issue in cs["issues"]:
                    lines.append(f"\n⚠️ {issue}")
        else:
            lines.append("- 暂无角色数据")
            lines.append("- 提示：如为开篇，请先在 设定/人物/ 创建角色卡")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 🪝 活跃伏笔")
        ah = data["active_hooks"]
        if ah.get("hooks"):
            lines.append("")
            lines.append("| 伏笔 | 类型 | 埋设章 | 目标章 | 紧急度 |")
            lines.append("|------|------|--------|--------|--------|")
            for hook in ah["hooks"][:10]:
                urgency_icon = "🔴" if hook.get("urgency", 0) >= 0.85 else "🟡" if hook.get("urgency", 0) >= 0.5 else "🟢"
                lines.append(
                    f"| {hook['text'][:40]} | {hook.get('type', '?')} | "
                    f"第{hook.get('planted', '?')}章 | 第{hook.get('target', '?')}章 | "
                    f"{urgency_icon} {hook.get('urgency', 0):.2f} |"
                )
            if ah.get("overdue"):
                lines.append(f"\n🔴 逾期伏笔: {ah['overdue']} 个，建议本章优先回收")
        else:
            lines.append("- 暂无活跃伏笔")
            if chapter > 3:
                lines.append("- ⚠️ 建议本章埋设新伏笔（开篇后应有至少2-3个活跃伏笔）")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## ⚠️ 本章风险标记")
        rf = data["risk_flags"]
        if rf.get("flags"):
            for flag in rf["flags"]:
                icon = "🔴" if flag.get("severity") == "高" else "🟡" if flag.get("severity") == "中" else "🟢"
                lines.append(f"- {icon} **{flag['type']}**: {flag['description']}")
        else:
            lines.append("- 🟢 未检测到特殊风险")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## ✅ 完成标准")
        cc = data["completion_criteria"]
        if cc.get("criteria"):
            for i, c in enumerate(cc["criteria"], 1):
                lines.append(f"{i}. {c}")
        else:
            lines.append("1. 正文生成完毕，字数符合要求")
            lines.append("2. 通过 AI 检测（GREEN）")
            lines.append("3. 角色状态和伏笔追踪已更新")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 📋 上下文提醒")
        cr = data["context_reminders"]
        if cr.get("reminders"):
            for r in cr["reminders"]:
                lines.append(f"- {r}")
        else:
            lines.append("- 无特殊提醒")

        return "\n".join(lines)

    # ====== 私有方法 ======

    def _get_previous_summary(self, chapter: int, state: Dict = None) -> Dict:
        """获取前文摘要"""
        prev_ch = chapter - 1
        result = {
            "has_previous": False,
            "last_chapter": 0,
            "last_lines": [],
            "recent_events": [],
        }

        if prev_ch < 1:
            return result

        result["has_previous"] = True
        result["last_chapter"] = prev_ch

        # 读取上一章正文
        prev_file = self._text_dir / f"第{prev_ch:03d}章.txt"
        if prev_file.exists():
            try:
                text = prev_file.read_text(encoding="utf-8")
                # 取最后300字作为衔接上下文
                last_part = text[-300:] if len(text) > 300 else text
                lines = [l.strip() for l in last_part.split("\n") if l.strip()]
                result["last_lines"] = lines[-5:]  # 最后5行
            except Exception as e:
                _log.warning(f"读取上一章失败: {e}")

        # 从 state 获取最近事件
        if state:
            timeline = state.get("timeline", [])
            recent = timeline[-5:] if len(timeline) >= 5 else timeline
            result["recent_events"] = [
                f"第{t.get('chapter', '?')}章: {t.get('event', '?')[:60]}"
                for t in recent
            ]

        return result

    def _get_character_snapshot(self, state: Dict = None) -> Dict:
        """获取角色状态快照"""
        result = {"characters": [], "issues": []}

        if not state:
            return result

        # 从 character_states 获取
        char_states = state.get("character_states", {})
        for name, cs in char_states.items():
            if isinstance(cs, dict):
                result["characters"].append({
                    "name": name,
                    "identity": cs.get("relationship_to_mc", "?"),
                    "location": cs.get("location", "?"),
                    "state": cs.get("emotion", "?"),
                    "last_seen": cs.get("last_seen_chapter", "?"),
                })

        # 从 characters 获取（兼容旧格式）
        chars = state.get("characters", {})
        for name, info in chars.items():
            if name not in [c["name"] for c in result["characters"]]:
                if isinstance(info, dict):
                    result["characters"].append({
                        "name": name,
                        "identity": info.get("identity", "?"),
                        "location": info.get("location", "?"),
                        "state": info.get("state", {}).get("state", "?") if isinstance(info.get("state"), dict) else "?",
                        "last_seen": info.get("chapters_appeared", [0])[-1] if info.get("chapters_appeared") else "?",
                    })

        # 检查问题
        if not result["characters"]:
            result["issues"].append("未定义任何角色状态，建议先创建角色卡")

        return result

    def _get_active_hooks(self, state: Dict = None) -> Dict:
        """获取活跃伏笔"""
        result = {"hooks": [], "overdue": 0}

        if not state:
            return result

        hooks = state.get("plot", {}).get("hooks", [])
        for h in hooks:
            status = h.get("status", "active")
            if status in ("resolved", "abandoned"):
                continue
            result["hooks"].append({
                "text": h.get("text", "?")[:40],
                "type": h.get("hook_type", "general"),
                "planted": h.get("planted_at", h.get("chapter_planted", "?")),
                "target": h.get("chapter_target", h.get("planned_reveal_high", "?")),
                "urgency": h.get("urgency", 0),
            })

        # 统计逾期伏笔
        foreshadows = state.get("foreshadows", [])
        for f in foreshadows:
            if f.get("status") in ("resolved", "abandoned"):
                continue
            target = f.get("chapter_target")
            if target and isinstance(target, int):
                progress = state.get("progress", {})
                current_ch = progress.get("written", progress.get("last_chapter", 0))
                if current_ch > target:
                    result["overdue"] += 1
                    result["hooks"].append({
                        "text": f.get("content", "?")[:40],
                        "type": "伏笔",
                        "planted": f.get("chapter_planted", "?"),
                        "target": target,
                        "urgency": 1.0,
                    })

        return result

    def _get_risk_flags(self, chapter: int, state: Dict = None) -> Dict:
        """检测本章风险标记"""
        flags = []

        # 风险1: 开头章节
        if chapter <= 3:
            flags.append({
                "type": "开篇风险",
                "severity": "高",
                "description": f"第{chapter}章属于开篇阶段，前300字必须有钩子，前三章必出金手指（番茄/飞卢）。平台差异化要求严格。",
            })

        # 风险2: 高潮/转折章节
        if state:
            total = state.get("progress", {}).get("total_planned", 100)
            if total > 0:
                ratio = chapter / total
                if 0.45 <= ratio <= 0.55:
                    flags.append({
                        "type": "中点转折",
                        "severity": "高",
                        "description": "本章处于全书中点（45%-55%），建议安排伪胜利或伪失败，完成叙事转折。",
                    })
                if 0.75 <= ratio <= 0.85:
                    flags.append({
                        "type": "高潮前夜",
                        "severity": "高",
                        "description": "接近全书高潮（75%-85%），需确保伏笔就位、情感积累到位、反派动机充分。",
                    })

        # 风险3: 逾期伏笔
        overdue = 0
        if state:
            foreshadows = state.get("foreshadows", [])
            current_ch = state.get("progress", {}).get("written", state.get("progress", {}).get("last_chapter", 0))
            for f in foreshadows:
                if f.get("status") in ("resolved", "abandoned"):
                    continue
                target = f.get("chapter_target")
                if target and isinstance(target, int) and current_ch > target:
                    overdue += 1
        if overdue > 0:
            flags.append({
                "type": "逾期伏笔",
                "severity": "中" if overdue < 3 else "高",
                "description": f"有 {overdue} 个伏笔已逾期未回收，建议本章优先处理。",
            })

        # 风险4: 承诺兑现
        if state:
            payoff = state.get("payoff_ledger", [])
            pending = [p for p in payoff if not p.get("fulfilled") and p.get("status") == "pending"]
            if pending:
                flags.append({
                    "type": "未兑现承诺",
                    "severity": "中",
                    "description": f"有 {len(pending)} 个承诺待兑现: {pending[0].get('text', '?')[:30]}...",
                })

        return {"flags": flags}

    def _get_completion_criteria(self, chapter: int, state: Dict = None) -> Dict:
        """生成完成标准"""
        criteria = [
            f"正文生成完毕，字数在目标范围内",
            f"通过 AI 检测（python run.py detect --file 正文/第{chapter:03d}章.txt）结果 GREEN",
            f"无 P0 禁用词和禁用句式",
            f"章末有具体钩子（非总结式结尾）",
            f"角色状态已更新到 追踪/角色状态.md",
        ]

        if state:
            hooks = state.get("plot", {}).get("hooks", [])
            unresolved = [h for h in hooks if h.get("status") not in ("resolved", "abandoned")]
            if unresolved:
                criteria.append(f"推进或回收至少1个活跃伏笔（当前{len(unresolved)}个）")

        return {"criteria": criteria}

    def _get_context_reminders(self, chapter: int) -> Dict:
        """获取上下文提醒"""
        reminders = []

        # 检查是否有写作指导文件
        notes_path = self._track_dir / "写作指导.md"
        if notes_path.exists():
            reminders.append(f"📝 有写作指导文件，请注意查阅")

        # 检查契约目录
        contract_path = self._track_dir / "章节契约" / f"第{chapter:03d}章-契约.md"
        if contract_path.exists():
            reminders.append(f"📋 本章已有契约，请按契约写作")
        else:
            reminders.append(f"⚠️ 本章尚未创建契约，建议先创建再写作")

        return {"reminders": reminders}

    def _check_ready(self, preview: Dict) -> bool:
        """检查是否准备好开始写作"""
        issues = 0
        if preview["risk_flags"].get("flags"):
            high_risks = [f for f in preview["risk_flags"]["flags"] if f.get("severity") == "高"]
            if high_risks:
                issues += len(high_risks)

        char_snapshot = preview.get("character_snapshot", {})
        if char_snapshot.get("issues"):
            issues += len(char_snapshot["issues"])

        return issues == 0

    # === 兼容 Engine 接口 ===

    def analyze(self, text: str = "", chapter: int = 1, state: Dict = None, **kwargs) -> Dict[str, Any]:
        """统一 analyze 接口（兼容 registry 规范）"""
        return self.analyze_preview(chapter=chapter, state=state)

    def analyze_preview(self, chapter: int, state: Dict = None) -> Dict[str, Any]:
        """直接调用 analyze（明确参数名版本）"""
        return self.analyze(chapter=chapter, state=state)

    def generate_markdown(self, chapter: int, state: Dict = None) -> str:
        """生成 Markdown 格式预览"""
        return self.generate_preview_markdown(chapter, state)
