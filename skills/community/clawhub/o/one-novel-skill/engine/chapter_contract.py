#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chapter_contract.py — 章节契约系统

SKILL.md 声明功能：
- 每章正文写作前，先生成章节契约，用户确认后再动笔
- 契约格式：章节编号/必达节拍/禁止事项/目标情绪/章末钩子/张力曲线/风险等级
- 流程：Agent生成契约 → 用户确认 → 开始写作 → 归档到 追踪/章节契约/

与 engine/spec_builder.py 的关系：
- SpecBuilder 是底层技术规格构建器（嵌入 contract 字典）
- ChapterContractEngine 是面向用户的契约系统（完整流程 + 归档）
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

_log = logging.getLogger("chapter_contract")


class ChapterContract:
    """单章契约"""

    def __init__(
        self,
        chapter: int,
        required_beats: List[str] = None,
        forbidden_moves: List[str] = None,
        emotion_target: str = "",
        hook_goal: str = "",
        tension_curve: str = "",
        risk_level: str = "低",
        risk_note: str = "",
        continuity_checks: List[str] = None,
        word_target: int = 2500,
    ):
        self.chapter = chapter
        self.required_beats = required_beats or []
        self.forbidden_moves = forbidden_moves or []
        self.emotion_target = emotion_target
        self.hook_goal = hook_goal
        self.tension_curve = tension_curve
        self.risk_level = risk_level
        self.risk_note = risk_note
        self.continuity_checks = continuity_checks or []
        self.word_target = word_target
        self.created_at = datetime.now().isoformat()
        self.confirmed = False
        self.confirmed_at = ""

    def confirm(self):
        """用户确认契约"""
        self.confirmed = True
        self.confirmed_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "chapter": self.chapter,
            "required_beats": self.required_beats,
            "forbidden_moves": self.forbidden_moves,
            "emotion_target": self.emotion_target,
            "hook_goal": self.hook_goal,
            "tension_curve": self.tension_curve,
            "risk_level": self.risk_level,
            "risk_note": self.risk_note,
            "continuity_checks": self.continuity_checks,
            "word_target": self.word_target,
            "created_at": self.created_at,
            "confirmed": self.confirmed,
            "confirmed_at": self.confirmed_at,
        }

    def to_markdown(self) -> str:
        """输出人类可读的契约文本"""
        status = "✅ 已确认" if self.confirmed else "⏳ 待确认"
        lines = [
            f"# 第{self.chapter}章 章节契约",
            f"",
            f"**状态**: {status}",
            f"**创建时间**: {self.created_at}",
            f"**目标字数**: {self.word_target}字",
            f"**风险等级**: {'🔴' if self.risk_level == '高' else '🟡' if self.risk_level == '中' else '🟢'} {self.risk_level}",
            f"",
            f"## 必达节拍（本章必须完成的情节推进）",
        ]
        for i, beat in enumerate(self.required_beats, 1):
            lines.append(f"{i}. {beat}")
        if not self.required_beats:
            lines.append("（未定义）")

        lines.append("")
        lines.append("## 禁止事项（本章禁止的操作）")
        for i, forbid in enumerate(self.forbidden_moves, 1):
            lines.append(f"- ❌ {forbid}")
        if not self.forbidden_moves:
            lines.append("（无特殊禁止事项）")

        lines.append("")
        lines.append("## 目标情绪")
        lines.append(f"读者读完后应有的情绪：{self.emotion_target or '（未定义）'}")

        lines.append("")
        lines.append("## 章末钩子")
        lines.append(f"结尾钩子目标：{self.hook_goal or '（未定义）'}")

        lines.append("")
        lines.append("## 张力曲线")
        lines.append(f"张力变化路径：{self.tension_curve or '（未定义）'}")

        lines.append("")
        lines.append("## 连续性检查")
        for i, check in enumerate(self.continuity_checks, 1):
            lines.append(f"- {check}")
        if not self.continuity_checks:
            lines.append("（无特殊连续性检查项）")

        if self.risk_note:
            lines.append("")
            lines.append("## 风险说明")
            lines.append(self.risk_note)

        return "\n".join(lines)


class ChapterContractEngine:
    """章节契约系统引擎"""

    DEFAULT_REQUIRED_BEATS = [
        "推进主线至少1个关键节点",
        "展示主角特质（通过行动而非描述）",
        "至少1处感官细节描写",
        "章末设置具体钩子（非总结式结尾）",
    ]

    DEFAULT_FORBIDDEN = [
        "禁止使用P0禁用词（毋庸置疑/不可否认/值得一提的是/总而言之等）",
        "禁止直接告知情绪（他很生气/他感到害怕等）",
        "禁止章末感悟总结（他终于明白了/她终于懂得）",
        "禁止模板化结尾（他不知道的是/更大的挑战还在后面）",
    ]

    RISK_LEVELS = {
        "低": "本章为主线日常推进，无高难度场景",
        "中": "本章涉及重要转折/新角色引入/伏笔埋设",
        "高": "本章涉及大高潮/核心伏笔回收/角色死亡/世界观重大揭示",
    }

    def __init__(self, book_dir: str = ""):
        self.book_dir = Path(book_dir) if book_dir else Path.cwd()
        self._contract_dir = self.book_dir / "追踪" / "章节契约"
        self._contracts: Dict[int, ChapterContract] = {}

    # ====== 契约生成 ======

    def create_contract(
        self,
        chapter: int,
        required_beats: List[str] = None,
        forbidden_moves: List[str] = None,
        emotion_target: str = "",
        hook_goal: str = "",
        tension_curve: str = "",
        risk_level: str = "低",
        risk_note: str = "",
        continuity_checks: List[str] = None,
        word_target: int = 2500,
    ) -> ChapterContract:
        """创建新契约"""
        contract = ChapterContract(
            chapter=chapter,
            required_beats=required_beats or list(self.DEFAULT_REQUIRED_BEATS),
            forbidden_moves=forbidden_moves or list(self.DEFAULT_FORBIDDEN),
            emotion_target=emotion_target,
            hook_goal=hook_goal,
            tension_curve=tension_curve,
            risk_level=risk_level if risk_level in self.RISK_LEVELS else "低",
            risk_note=risk_note or self.RISK_LEVELS.get(risk_level, ""),
            continuity_checks=continuity_checks or [],
            word_target=word_target,
        )
        self._contracts[chapter] = contract
        return contract

    def create_from_plan(self, chapter: int, plan: Dict, state: Dict = None) -> ChapterContract:
        """从章节规划自动生成契约"""
        # 从规划中提取必达节拍
        beats = []
        core = plan.get("core", "")
        if core:
            beats.append(f"核心事件: {core}")
        events = plan.get("events", [])
        for e in events[:3]:
            if isinstance(e, str):
                beats.append(f"事件: {e}")
            elif isinstance(e, dict):
                beats.append(f"事件: {e.get('name', str(e))}")

        if len(beats) < 3:
            beats.extend(self.DEFAULT_REQUIRED_BEATS[: 3 - len(beats)])

        # 推测风险等级
        risk = "低"
        dopamine = plan.get("dopamine_phase", "")
        if dopamine in ("兑现释放期-1", "兑现释放期-2"):
            risk = "中"
        if chapter <= 3 or plan.get("ratio", 0) > 0.85:
            risk = "高"

        # 情绪目标
        emotion = plan.get("suggested_emotion", "")
        if not emotion:
            emotion = "读者应感到故事在推进，主角在成长"

        # 钩子目标
        hook = plan.get("ending", "")
        if not hook:
            hook = "章末设置1个具体的新悬念（非'他不知道的是...'模板）"

        # 张力曲线
        tension = f"从{'平静' if chapter % 5 != 0 else '紧张'}→{'紧张→小释放→新紧张' if risk == '中' else '持续上升→峰值'}"

        # 连续性检查
        continuity = []
        if state:
            if state.get("progress", {}).get("written", 0) > 0:
                continuity.append(f"确认上一章结尾钩子已在本章承接")
            hooks = state.get("plot", {}).get("hooks", [])
            unresolved = [h for h in hooks if not h.get("resolved") and h.get("status") not in ("resolved", "abandoned")]
            if unresolved:
                names = [h.get("text", "?")[:30] for h in unresolved[:3]]
                continuity.append(f"活跃伏笔: {', '.join(names)}")

        return self.create_contract(
            chapter=chapter,
            required_beats=beats,
            forbidden_moves=list(self.DEFAULT_FORBIDDEN),
            emotion_target=emotion,
            hook_goal=hook,
            tension_curve=tension,
            risk_level=risk,
            risk_note=self.RISK_LEVELS.get(risk, ""),
            continuity_checks=continuity,
            word_target=plan.get("suggested_word_count", 2500),
        )

    # ====== 确认流程 ======

    def confirm_contract(self, chapter: int) -> bool:
        """用户确认契约"""
        contract = self._contracts.get(chapter)
        if contract is None:
            _log.warning(f"第{chapter}章契约不存在，无法确认")
            return False
        contract.confirm()
        return True

    def is_confirmed(self, chapter: int) -> bool:
        """检查契约是否已确认"""
        contract = self._contracts.get(chapter)
        return contract is not None and contract.confirmed

    def get_contract(self, chapter: int) -> Optional[ChapterContract]:
        """获取契约"""
        return self._contracts.get(chapter)

    # ====== 归档 ======

    def archive_contract(self, chapter: int) -> bool:
        """将已确认的契约归档到 追踪/章节契约/ 目录"""
        contract = self._contracts.get(chapter)
        if contract is None:
            _log.warning(f"第{chapter}章契约不存在，无法归档")
            return False
        if not contract.confirmed:
            _log.warning(f"第{chapter}章契约未确认，归档前请先确认")
            return False

        self._contract_dir.mkdir(parents=True, exist_ok=True)

        # 写入 Markdown（人类可读）
        md_path = self._contract_dir / f"第{chapter:03d}章-契约.md"
        md_path.write_text(contract.to_markdown(), encoding="utf-8")

        # 写入 JSON（机器可读）
        json_path = self._contract_dir / f"第{chapter:03d}章-契约.json"
        json_path.write_text(
            json.dumps(contract.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        _log.info(f"第{chapter}章契约已归档: {md_path}")
        return True

    def archive_batch(self, start: int, end: int) -> Dict[str, Any]:
        """批量归档"""
        results = {"success": [], "failed": [], "skipped": []}
        for ch in range(start, end + 1):
            if ch not in self._contracts:
                results["skipped"].append(ch)
                continue
            if self.archive_contract(ch):
                results["success"].append(ch)
            else:
                results["failed"].append(ch)
        return results

    # ====== 查看 ======

    def load_archived_contract(self, chapter: int) -> Optional[Dict]:
        """加载已归档的契约"""
        json_path = self._contract_dir / f"第{chapter:03d}章-契约.json"
        if json_path.exists():
            try:
                return json.loads(json_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return None

    def list_contracts(self) -> List[Dict]:
        """列出所有契约（活跃+归档）"""
        result = []
        # 内存中的活跃契约
        for ch, contract in self._contracts.items():
            result.append({
                "chapter": ch,
                "status": "已确认" if contract.confirmed else "待确认",
                "risk": contract.risk_level,
                "emotion": contract.emotion_target[:50],
                "source": "活跃",
            })

        # 已归档的
        if self._contract_dir.exists():
            for f in sorted(self._contract_dir.glob("第*章-契约.json")):
                try:
                    ch = int(f.stem.split("第")[1].split("章")[0])
                    if ch not in self._contracts:
                        data = json.loads(f.read_text(encoding="utf-8"))
                        result.append({
                            "chapter": ch,
                            "status": "已归档",
                            "risk": data.get("risk_level", "?"),
                            "emotion": data.get("emotion_target", "")[:50],
                            "source": "归档",
                        })
                except Exception:
                    pass

        return sorted(result, key=lambda x: x["chapter"])

    # ====== 校验 ======

    def validate_against_contract(self, chapter: int, text: str) -> Dict[str, Any]:
        """验证正文是否符合契约"""
        contract = self._contracts.get(chapter)
        if contract is None:
            # 尝试加载归档
            archived = self.load_archived_contract(chapter)
            if archived is None:
                return {"verdict": "无契约", "issues": ["未找到对应的章节契约"]}
            contract_data = archived
        else:
            contract_data = contract.to_dict()

        issues = []

        # 检查禁用事项
        for forbid in contract_data.get("forbidden_moves", []):
            for keyword in ["毋庸置疑", "不可否认", "值得一提的是", "总而言之", "众所周知",
                           "从某种意义上说", "由此可见", "综上所述", "不可忽视的是",
                           "他不知道的是", "他终于明白了", "更大的挑战还在后面"]:
                if keyword in text:
                    issues.append(f"违反禁止事项: 包含'{keyword}'")

        # 检查字数
        word_target = contract_data.get("word_target", 2500)
        actual_chars = len(text)
        if actual_chars < word_target * 0.5:
            issues.append(f"字数不足: {actual_chars}字 (目标{word_target}字)")
        if actual_chars > word_target * 1.5:
            issues.append(f"字数超出: {actual_chars}字 (目标{word_target}字)")

        # 检查章末钩子
        if contract_data.get("hook_goal"):
            last_200 = text[-200:] if len(text) >= 200 else text
            hook_indicators = ["?", "？", "突然", "就在这时", "门开了", "脚步声", "敲门声",
                              "电话响了", "屏幕亮了", "他愣住了", "她愣住了"]
            has_hook = any(ind in last_200 for ind in hook_indicators)
            # 检查是否以总结式结尾
            bad_endings = ["终于明白", "终于懂得", "终于学会", "总的来说", "总而言之",
                          "他不知道的是", "更大的挑战"]
            has_bad_ending = any(be in last_200 for be in bad_endings)
            if has_bad_ending:
                issues.append("章末使用了禁止的总结式结尾")
            elif not has_hook:
                issues.append("章末可能缺少具体钩子")

        return {
            "verdict": "通过" if not issues else "需修改",
            "issues": issues,
            "chapter": chapter,
            "word_count": actual_chars,
            "target_words": word_target,
        }

    # === 兼容 Engine 接口 ===

    def analyze(self, text: str, chapter: int = 1, **kwargs) -> Dict[str, Any]:
        """统一 analyze 接口（兼容 registry 规范）"""
        return self.validate_against_contract(chapter, text)
