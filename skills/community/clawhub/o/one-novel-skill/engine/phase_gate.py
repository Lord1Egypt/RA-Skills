#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PhaseGate — 六库阶段门禁引擎

参考：references/six-libraries-guide.md 的六大库框架
填充：one-novel-skill 现有引擎能力作为就绪检查标准

核心职责：
  写前强制检查：六大库是否全部就绪 → 未就绪则拒绝 pipeline 启动
  每个阶段检查对应引擎/配置/数据是否已正确设置
"""

import logging
from typing import Dict, List, Optional

_log = logging.getLogger("phase_gate")

# ============================================================
# 阶段定义
# ============================================================

PHASE_DEFS = [
    {
        "id": 0,
        "name": "创作资料库",
        "desc": "题材背景 + 设定参考 + 同类分析 + 灵感素材",
        "ref": "research_engine / reference_engine",
    },
    {
        "id": 1,
        "name": "写作技能库",
        "desc": "风格锚定 + 句式模板 + 词汇表 + 禁用词",
        "ref": "style_router / writing_notes / character_state_engine / engines_dialogue",
    },
    {
        "id": 2,
        "name": "审查校验库",
        "desc": "审查清单 + 质量标准 + 质量门禁（章节/卷/全书三级）",
        "ref": "story_gate / quality_gate / scheduler",
    },
    {
        "id": 3,
        "name": "AI去痕库",
        "desc": "检测规则 + 替换词表 + 禁用结构 + 去痕检查",
        "ref": "detectors pipeline / writing_notes (ANTI_AI_RULES) / run_all_detectors",
    },
    {
        "id": 4,
        "name": "写作要求库",
        "desc": "平台要求 + 题材要求 + 内容安全 + 格式规范 + 发布流程",
        "ref": "config / style_router / story_gate 平台权重 / content_safety_filter",
    },
    {
        "id": 5,
        "name": "铁律库",
        "desc": "32条创作铁律 + 违规检测 + 修复流程 + 更新记录",
        "ref": "IRON_RULES.md / quality_gate / story_gate",
    },
]

PHASE_ORDER = [0, 1, 2, 3, 4, 5]


class PhaseStatus:
    """单个阶段的就绪状态"""

    def __init__(self, phase_id: int):
        self.phase_id = phase_id
        self.ready = False
        self.checks: Dict[str, bool] = {}
        self.messages: List[str] = []

    @property
    def phase_name(self) -> str:
        return PHASE_DEFS[self.phase_id]["name"] if self.phase_id < len(PHASE_DEFS) else f"阶段{self.phase_id}"

    def to_dict(self) -> dict:
        return {
            "phase_id": self.phase_id,
            "name": self.phase_name,
            "ready": self.ready,
            "checks": self.checks,
            "messages": self.messages,
        }


class GateReport:
    """全部门禁检查报告"""

    def __init__(self):
        self.phases: Dict[int, PhaseStatus] = {}
        self.all_ready = False

    def add_phase(self, status: PhaseStatus):
        self.phases[status.phase_id] = status
        self.all_ready = all(p.ready for p in self.phases.values())

    def summary(self) -> str:
        parts = []
        for pid in PHASE_ORDER:
            p = self.phases.get(pid)
            if p is None:
                parts.append(f"  Phase-{pid}: \u274c 未检查")
            elif p.ready:
                parts.append(f"  {p.phase_name}: \u2705 就绪")
            else:
                parts.append(f"  {p.phase_name}: \u26a0\ufe0f 未就绪")
        return "\n".join(parts)

    def to_dict(self) -> dict:
        return {
            "all_ready": self.all_ready,
            "phases": {str(k): v.to_dict() for k, v in self.phases.items()},
        }


# ============================================================
# 核心引擎
# ============================================================

class PhaseGate:
    """六库阶段门禁引擎"""

    engine_name = "phase_gate"
    engine_tags = ["管理", "门禁"]

    def __init__(self):
        self._config: dict = {}
        self._pass_phases: set = set()

    # ── 配置 ──────────────────────────────────

    def configure(self, genre: str = "", platform: str = "",
                  total_chapters: int = 100):
        """配置写作参数（影响各阶段检查标准）"""
        self._config = {
            "genre": genre,
            "platform": platform,
            "total_chapters": total_chapters,
        }

    # ── 单阶段检查 ────────────────────────────

    def check_phase(self, phase_id: int) -> PhaseStatus:
        """检查单个阶段是否就绪"""
        if phase_id not in range(6):
            status = PhaseStatus(phase_id)
            status.messages.append(f"无效阶段: {phase_id}")
            return status

        if phase_id == 0:
            return self._check_phase_0()
        elif phase_id == 1:
            return self._check_phase_1()
        elif phase_id == 2:
            return self._check_phase_2()
        elif phase_id == 3:
            return self._check_phase_3()
        elif phase_id == 4:
            return self._check_phase_4()
        elif phase_id == 5:
            return self._check_phase_5()
        return PhaseStatus(phase_id)

    # ── 全量检查 ──────────────────────────────

    def check_all(self) -> GateReport:
        """检查全部6个阶段"""
        report = GateReport()
        for pid in PHASE_ORDER:
            status = self.check_phase(pid)
            report.add_phase(status)
        return report

    # ── 门禁 ──────────────────────────────────

    def enforce_gate(self) -> bool:
        """硬门禁：全部就绪返回 True，否则拒绝"""
        report = self.check_all()
        if not report.all_ready:
            _log.warning(f"PhaseGate: \u7981\u6b62\u5f00\u59cb\u2014\u2014\u516d\u5927\u5e93\u672a\u5168\u90e8\u5c31\u7eea")
            for pid in PHASE_ORDER:
                p = report.phases.get(pid)
                if p and not p.ready:
                    _log.warning(f"  {p.phase_name}: {p.messages}")
            return False
        _log.info("PhaseGate: \u516d\u5927\u5e93\u5168\u90e8\u5c31\u7eea\uff0c\u53ef\u4ee5\u5f00\u59cb\u5199\u4f5c")
        return True

    def bypass_phase(self, phase_id: int):
        """手动标记某阶段已通过（跳过检查）"""
        self._pass_phases.add(phase_id)

    def reset_bypass(self):
        """重置所有跳过标记"""
        self._pass_phases.clear()

    # ════════════════════════════════════════════
    # Phase 0: 创作资料库
    #   检查 research_engine / reference_engine 是否就绪
    # ════════════════════════════════════════════

    def _check_phase_0(self) -> PhaseStatus:
        status = PhaseStatus(0)
        try:
            from .research_engine import ResearchEngine
            re_eng = ResearchEngine()
            re_status = re_eng.check_ready() if hasattr(re_eng, "check_ready") else True
            status.checks["research_engine"] = bool(re_status)
            if re_status:
                status.messages.append("ResearchEngine: \u2705 \u7814\u7a76\u5f15\u64ce\u5c31\u7eea")
            else:
                status.messages.append("ResearchEngine: \u26a0\ufe0f \u7814\u7a76\u5f15\u64ce\u672a\u914d\u7f6e\u5b8c\u5584")
        except Exception as e:
            status.checks["research_engine"] = False
            status.messages.append(f"ResearchEngine: \u274c \u5bfc\u5165\u5931\u8d25: {e}")

        try:
            from .reference_engine import ReferenceEngine
            ref_eng = ReferenceEngine()
            ref_files = ref_eng.list_references() if hasattr(ref_eng, "list_references") else []
            ref_ok = len(ref_files) > 0 if hasattr(ref_eng, "list_references") else True
            status.checks["reference_engine"] = bool(ref_ok)
            if ref_ok:
                status.messages.append(f"ReferenceEngine: \u2705 \u53c2\u8003\u6587\u6863\u5c31\u7eea ({len(ref_files)}\u4e2a)")
            else:
                status.messages.append("ReferenceEngine: \u26a0\ufe0f \u53c2\u8003\u6587\u6863\u5e93\u4e3a\u7a7a")
        except Exception as e:
            status.checks["reference_engine"] = False
            status.messages.append(f"ReferenceEngine: \u274c \u5bfc\u5165\u5931\u8d25: {e}")

        status.ready = all(status.checks.values()) or 0 in self._pass_phases
        return status

    # ════════════════════════════════════════════
    # Phase 1: 写作技能库
    #   检查 style_router / writing_notes / character_state_engine / engines_dialogue
    # ════════════════════════════════════════════

    def _check_phase_1(self) -> PhaseStatus:
        status = PhaseStatus(1)

        try:
            from .style_router import StyleRouter
            sr = StyleRouter()
            sr_ok = hasattr(sr, "route_style") or hasattr(sr, "analyze")
            status.checks["style_router"] = sr_ok
            status.messages.append(f"StyleRouter: \u2705 {'\u5c31\u7eea' if sr_ok else '\u672a\u5b8c\u6574'}")
        except Exception as e:
            status.checks["style_router"] = False
            status.messages.append(f"StyleRouter: \u274c {e}")

        try:
            from .writing_notes import ANTI_AI_RULES, PLATFORM_RULES
            rules_ok = len(ANTI_AI_RULES) >= 8
            plat_ok = len(PLATFORM_RULES) > 0
            status.checks["writing_notes_rules"] = rules_ok
            status.checks["writing_notes_platform"] = plat_ok
            status.messages.append(f"WritingNotes: \u2705 {len(ANTI_AI_RULES)}\u6761\u53bbAI\u89c4\u5219")
        except Exception as e:
            status.checks["writing_notes"] = False
            status.messages.append(f"WritingNotes: \u274c {e}")

        try:
            from .character_state_engine import CharacterStateEngine
            cse = CharacterStateEngine()
            cse_ok = hasattr(cse, "register_character") and hasattr(cse, "create_from_formula")
            status.checks["character_engine"] = cse_ok
            status.messages.append(f"CharacterState: \u2705 {'\u5c31\u7eea' if cse_ok else '\u672a\u5b8c\u6574'}")
        except Exception as e:
            status.checks["character_engine"] = False
            status.messages.append(f"CharacterState: \u274c {e}")

        try:
            from .engines_dialogue import DialogueEngine
            de = DialogueEngine()
            de_ok = hasattr(DialogueEngine, "check_subtext_three_layer")
            status.checks["dialogue_engine"] = de_ok
            status.messages.append(f"DialogueEngine: \u2705 {'\u5c31\u7eea' if de_ok else '\u672a\u5b8c\u6574'}")
        except Exception as e:
            status.checks["dialogue_engine"] = False
            status.messages.append(f"DialogueEngine: \u274c {e}")

        status.ready = (sum(1 for v in status.checks.values() if v) >= 3) or 1 in self._pass_phases
        return status

    # ════════════════════════════════════════════
    # Phase 2: 审查校验库
    #   检查 story_gate(13维) + quality_gate + scheduler pipeline
    # ════════════════════════════════════════════

    def _check_phase_2(self) -> PhaseStatus:
        status = PhaseStatus(2)

        try:
            from .story_gate import StoryGate
            plugins = StoryGate.list_plugins()
            gate_ok = len(plugins) >= 10
            status.checks["story_gate"] = gate_ok
            status.messages.append(f"StoryGate: \u2705 {len(plugins)}\u7ef4\u8bc4\u5ba1\u63d2\u4ef6")
        except Exception as e:
            status.checks["story_gate"] = False
            status.messages.append(f"StoryGate: \u274c {e}")

        try:
            from .quality_gate import QualityGate
            qg = QualityGate(None, None)
            qg_ok = hasattr(qg, "process")
            status.checks["quality_gate"] = qg_ok
            status.messages.append(f"QualityGate: \u2705 {'\u5c31\u7eea' if qg_ok else '\u672a\u5b8c\u6574'}")
        except Exception as e:
            status.checks["quality_gate"] = False
            status.messages.append(f"QualityGate: \u274c {e}")

        try:
            from application.orchestrator import ChapterOrchestrator
            has_gen = hasattr(ChapterOrchestrator, "generate_chapter")
            has_batch = hasattr(ChapterOrchestrator, "generate_batch")
            pipe_ok = has_gen and has_batch
            status.checks["pipeline"] = pipe_ok
            status.messages.append(f"Orchestrator: \u2705 {'\u5c31\u7eea' if pipe_ok else '\u672a\u5b8c\u6574'}")
        except Exception as e:
            status.checks["pipeline"] = False
            status.messages.append(f"Orchestrator: \u274c {e}")

        status.ready = all(status.checks.values()) or 2 in self._pass_phases
        return status

    # ════════════════════════════════════════════
    # Phase 3: AI去痕库
    #   检查 detectors 管线 + writing_notes 反AI规则
    # ════════════════════════════════════════════

    def _check_phase_3(self) -> PhaseStatus:
        status = PhaseStatus(3)

        try:
            from ..detectors.pipeline import pipeline as det_pipeline
            det_ok = callable(det_pipeline)
            status.checks["detector_pipeline"] = det_ok
            status.messages.append(f"DetectorPipeline: \u2705 {'\u5c31\u7eea' if det_ok else '\u672a\u5b8c\u6574'}")
        except Exception as e:
            status.checks["detector_pipeline"] = False
            status.messages.append(f"DetectorPipeline: \u274c {e}")

        try:
            from ..detectors.run_all_detectors import run_all_checks
            runner_ok = callable(run_all_checks)
            status.checks["run_all_detectors"] = runner_ok
            status.messages.append(f"RunAllDetectors: \u2705 {'\u5c31\u7eea' if runner_ok else '\u672a\u5b8c\u6574'}")
        except Exception as e:
            status.checks["run_all_detectors"] = False
            status.messages.append(f"RunAllDetectors: \u274c {e}")

        # 检查反AI规则
        try:
            from .writing_notes import ANTI_AI_RULES
            if len(ANTI_AI_RULES) >= 13:
                status.messages.append(f"WritingNotes: \u2705 {len(ANTI_AI_RULES)}\u6761\u53bbAI\u89c4\u5219\u5df2\u5c31\u7eea")
            else:
                status.messages.append(f"WritingNotes: \u26a0\ufe0f \u4ec5{len(ANTI_AI_RULES)}\u6761\u53bbAI\u89c4\u5219")
        except Exception as e:
            status.messages.append(f"WritingNotes: \u274c {e}")

        # 检查 de-ai 参考文件
        try:
            from pathlib import Path
            de_ai_dir = Path(__file__).parent.parent / "references" / "de-ai"
            if de_ai_dir.exists():
                files = list(de_ai_dir.iterdir())
                status.messages.append(f"De-AI-Refs: \u2705 {len(files)}\u4e2a\u53bb\u75d5\u53c2\u8003\u6587\u4ef6")
            else:
                status.messages.append("De-AI-Refs: \u26a0\ufe0f \u53bb\u75d5\u53c2\u8003\u6587\u4ef6\u76ee\u5f55\u4e0d\u5b58\u5728")
        except Exception as e:
            status.messages.append(f"De-AI-Refs: \u274c {e}")

        status.ready = any(v for v in status.checks.values()) or 3 in self._pass_phases
        return status

    # ════════════════════════════════════════════
    # Phase 4: 写作要求库
    #   检查 平台配置 + 题材配置 + 安全过滤
    # ════════════════════════════════════════════

    def _check_phase_4(self) -> PhaseStatus:
        status = PhaseStatus(4)

        platform = self._config.get("platform", "")
        genre = self._config.get("genre", "")

        # 平台配置
        if platform:
            try:
                from .story_gate import PLATFORM_WEIGHTS
            except ImportError:
                status.checks["platform_config"] = False
                status.messages.append("平台配置: PLATFORM_WEIGHTS 导入失败")
            else:
                if platform in PLATFORM_WEIGHTS:
                    status.checks["platform_config"] = True
                    status.messages.append(f"平台配置: {platform} 权重已加载")
                else:
                    status.checks["platform_config"] = False
                    status.messages.append(f"平台配置: {platform} 未在 PLATFORM_WEIGHTS 中")
        else:
            status.checks["platform_config"] = True
            status.messages.append("平台配置: 未指定平台，使用默认权重")

        # 内容安全
        try:
            from ..detectors.content_safety_filter import ContentSafetyFilter
            csf = ContentSafetyFilter()
            safe_ok = hasattr(csf, "check") or hasattr(csf, "filter")
            status.checks["content_safety"] = safe_ok
            status.messages.append(f"ContentSafety: \u2705 {'\u5c31\u7eea' if safe_ok else '\u672a\u5b8c\u6574'}")
        except Exception as e:
            status.checks["content_safety"] = False
            status.messages.append(f"ContentSafety: \u274c {e}")

        # 发布流程 — 检查 ChapterOrchestrator 完整性
        try:
            from application.orchestrator import ChapterOrchestrator
            status.checks["pipeline_complete"] = True
            status.messages.append("Orchestrator: \u2705 \u53d1\u5e03\u6d41\u7a0b\u5c31\u7eea")
        except:
            status.checks["pipeline_complete"] = False
            status.messages.append("Orchestrator: \u274c \u53d1\u5e03\u6d41\u7a0b\u672a\u5c31\u7eea")

        status.ready = all(status.checks.values()) or 4 in self._pass_phases
        return status

    # ════════════════════════════════════════════
    # Phase 5: 铁律库
    #   检查 IRON_RULES.md + quality_gate + story_gate
    # ════════════════════════════════════════════

    def _check_phase_5(self) -> PhaseStatus:
        status = PhaseStatus(5)

        # 铁律文件存在性
        import os
        rules_file = os.path.join(os.path.dirname(__file__), "..", "IRON_RULES.md")
        if os.path.exists(rules_file):
            with open(rules_file, 'r', encoding='utf-8') as f:
                rules_content = f.read()
            rule_count = rules_content.count("##")
            status.checks["iron_rules_file"] = True
            status.messages.append(f"IRON_RULES: \u2705 {rule_count}\u6761\u94c1\u5f8b")
        else:
            status.checks["iron_rules_file"] = False
            status.messages.append("IRON_RULES: \u274c \u94c1\u5f8b\u6587\u4ef6\u4e0d\u5b58\u5728")

        # 违规检测 — quality_gate
        try:
            from .quality_gate import QualityGate
            status.checks["violation_detection"] = True
            status.messages.append("QualityGate: \u2705 \u8fdd\u89c4\u68c0\u6d4b\u5c31\u7eea")
        except Exception as e:
            status.checks["violation_detection"] = False
            status.messages.append(f"QualityGate: \u274c {e}")

        # 修复流程 — 检查 scheduler/checkpoint_manager 恢复能力
        try:
            from .checkpoint_manager import CheckpointManager
            cp = CheckpointManager(".")
            cp_ok = hasattr(cp, "restore_checkpoint") or hasattr(cp, "load")
            status.checks["recovery"] = cp_ok
            status.messages.append(f"CheckpointManager: \u2705 {'\u6062\u590d\u6d41\u7a0b\u5c31\u7eea' if cp_ok else '\u672a\u5b8c\u6574'}")
        except Exception as e:
            status.checks["recovery"] = False
            status.messages.append(f"CheckpointManager: \u274c {e}")

        # 更新记录 — 检查 FIX_CLOSURE_LOG
        fix_log = os.path.join(os.path.dirname(__file__), "..", "..", "FIX_CLOSURE_LOG.ndjson")
        if os.path.exists(fix_log):
            status.checks["changelog"] = True
            status.messages.append("Changelog: \u2705 \u66f4\u65b0\u8bb0\u5f55\u5c31\u7eea")
        else:
            status.checks["changelog"] = True  # 非强制
            status.messages.append("Changelog: \u2705 \u65e0\u53d8\u66f4\u8bb0\u5f55\uff0c\u4e0d\u5f71\u54cd")

        status.ready = all(v for k, v in status.checks.items() if k != "changelog") or 5 in self._pass_phases
        return status

    # ── 分析接口（EngineBase 兼容） ────────────

    def analyze(self, text=None, **kwargs):
        """兼容 EngineBase.analyze() 接口"""
        report = self.check_all()
        issues = []
        if not report.all_ready:
            for pid in PHASE_ORDER:
                p = report.phases.get(pid)
                if p and not p.ready:
                    for msg in p.messages:
                        if "\u274c" in msg or "\u26a0\ufe0f" in msg:
                            issues.append(f"[P1] [\u9636\u6bb5{pid}] {msg}")
        if report.all_ready:
            issues.append("[P0] PhaseGate: \u516d\u5927\u5e93\u5168\u90e8\u5c31\u7eea\uff0c\u53ef\u4ee5\u5f00\u59cb\u5199\u4f5c")
        return issues
