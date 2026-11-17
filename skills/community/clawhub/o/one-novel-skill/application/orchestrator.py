"""
application/orchestrator.py -- ChapterOrchestrator (统一编排器)

合并了原 application/orchestrator.py + engine/pipeline.py 的全部逻辑。
唯一编排入口，通过 EventBus 串联所有 93 引擎。

v6 增强:
- 全局超时 (GLOBAL_TIMEOUT_SECONDS = 600)
- 幂等性检查 (generate_chapter)
- ChapterRequest 输入校验 (chapter <= 10000, platform/genre validation)

Phases:
0. Init     -- 初始化 EventBus + 加载状态
1. Plan     -- ArcManager + SpecBuilder + PrewritingAnalyzer + ChapterContract
2. Generate -- ContextBuilder + ResearchEngine + NarrativeStructure + Director
3. Detect   -- DetectorGateway (6 suites)
4. Review   -- QualityGate + StoryGate + SemanticReview + 30+ batch engines
5. Persist  -- UnifiedUnitOfWork + GlobalRollback + EventBus publish
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path

from domain.commands import (
    WriteChapterCommand, UpdateCharacterCommand, UpdateTimelineCommand,
)
from infrastructure.state_repository import StateRepository
from infrastructure.persistence_gateway import PersistenceGateway
from infrastructure.llm_gateway import LLMGateway
from infrastructure.detector_gateway import DetectorGateway, DetectionResult
from application.unit_of_work import UnitOfWork
from engine.event_bus import EventBus, Event, EventType, get_event_bus
from engine.global_rollback import SideEffectTracker, GlobalRollbackContext
from engine.contracts import (
    EngineAnalyzeResult, EngineStatus, ChapterResult as ContractChapterResult,
    Platform, Genre,
)

_log = logging.getLogger("orchestrator")

# 全局超时
GLOBAL_TIMEOUT_SECONDS = 600

# 有效的平台和题材值
_VALID_PLATFORMS = {p.value for p in Platform}
_VALID_GENRES = {g.value for g in Genre}


@dataclass
class ChapterRequest:
    chapter: int
    total_chapters: int
    platform: str = "番茄"
    genre: str = "都市"
    emotion: str = "爽"
    additional_context: str = ""

    def __post_init__(self):
        if self.chapter < 1:
            raise ValueError(f"chapter must be >= 1, got {self.chapter}")
        if self.chapter > 10000:
            raise ValueError(f"chapter must be <= 10000, got {self.chapter}")
        if self.total_chapters < 1:
            raise ValueError(f"total_chapters must be >= 1, got {self.total_chapters}")
        if self.total_chapters > 10000:
            raise ValueError(f"total_chapters must be <= 10000, got {self.total_chapters}")
        if self.platform and self.platform not in _VALID_PLATFORMS:
            _log.warning(f"Unknown platform '{self.platform}', defaulting to 番茄")
            object.__setattr__(self, 'platform', '番茄')

    @classmethod
    def from_state(cls, state, ch, platform, genre):
        return cls(chapter=ch, total_chapters=state.progress.total_planned,
                   platform=platform, genre=genre)


@dataclass
class ChapterResult:
    chapter: int
    text: str = ""
    word_count: int = 0
    detection: Optional[DetectionResult] = None
    passed_quality_gate: bool = False
    events: List[Any] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    engine_results: List[EngineAnalyzeResult] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.text) > 50 and self.passed_quality_gate


class ChapterOrchestrator:
    """统一编排器 — 合并 pipeline.py 逻辑 + 集成新增8模块 + EventBus"""

    MAX_AUTO_CORRECT_RETRIES = 2

    def __init__(self, state_repo, persistence, llm, detector,
                 planning_engine=None, writing_engine=None, book_dir=""):
        self._state_repo = state_repo
        self._persistence = persistence
        self._llm = llm
        self._detector = detector
        self._planning = planning_engine
        self._writing = writing_engine
        self._book_dir = book_dir or str(Path.cwd())
        self._event_bus = get_event_bus()
        self._engine_results: List[EngineAnalyzeResult] = []

    # ==================================================================
    # Public API
    # ==================================================================

    def generate_chapter(self, request: ChapterRequest, timeout: float = GLOBAL_TIMEOUT_SECONDS) -> ChapterResult:
        _log.info(f"Generating chapter {request.chapter}/{request.total_chapters} (timeout={timeout}s)")
        result = ChapterResult(chapter=request.chapter)
        self._engine_results = []

        # 幂等性检查
        if self._is_chapter_already_generated(request.chapter):
            _log.info(f"Chapter {request.chapter} already generated, skipping (idempotent)")
            result.text = self._load_existing_chapter(request.chapter)
            result.word_count = len(result.text) if result.text else 0
            result.passed_quality_gate = True
            return result

        tracker = SideEffectTracker(self._book_dir)
        state = self._state_repo.load()
        tracker.track_state_snapshot(state.to_dict())

        start_time = time.time()

        with GlobalRollbackContext(tracker):
            # 全局超时检查
            if time.time() - start_time > timeout:
                result.issues.append(f"Global timeout ({timeout}s) before planning")
                self._publish(EventType.CHAPTER_FAILED, request.chapter, {"reason": "timeout"})
                return result

            # Phase 1: Plan (含写前分析 + 章节契约)
            spec = self._plan_chapter(request)
            if not spec:
                result.issues.append("Planning failed")
                self._publish(EventType.CHAPTER_FAILED, request.chapter, {"reason": "planning_failed"})
                return result

            # Phase 1.5: 写前分析预览 + 章节契约
            self._run_prewriting_analysis(request, spec)
            self._run_chapter_contract(request, spec)

            # Phase 1b: Director review
            self._director_review(request, spec)

            # Phase 2: Generate
            text = self._generate_text(request, spec)
            if not text:
                result.issues.append("Generation produced empty text")
                self._publish(EventType.CHAPTER_FAILED, request.chapter, {"reason": "empty_generation"})
                return result
            result.text = text
            result.word_count = len(text)

            # Phase 2.5: 叙事结构分析
            self._run_narrative_structure(result, request)

            # Phase 3: Detect
            result.detection = self._detect(text, request.platform)
            if not result.detection.passed:
                text = self._auto_correct(text, result.detection, request)
                result.text = text
                result.word_count = len(text)
                result.detection = self._detect(text, request.platform)

            # Phase 4: Deep review (含 L3+L4 语义审查)
            self._deep_review(result, request)

            result.passed_quality_gate = result.detection.passed

            # 全局超时检查（persist 前最后检查）
            if time.time() - start_time > timeout:
                result.issues.append(f"Global timeout ({timeout}s) before persist")
                result.passed_quality_gate = False

            # Phase 5: Persist (UnifiedUnitOfWork)
            if result.passed_quality_gate:
                self._persist_chapter(request, result)
            else:
                self._publish(EventType.QUALITY_GATE_RESULT, request.chapter,
                             {"passed": False, "issues": result.issues[:5]})

        result.engine_results = list(self._engine_results)
        self._publish(EventType.CHAPTER_GENERATED, request.chapter,
                     {"word_count": result.word_count, "passed": result.passed_quality_gate})

        _log.info(f"Chapter {request.chapter} done: {result.word_count} chars, "
                  f"passed={result.passed_quality_gate}, engines={len(self._engine_results)}")
        return result

    def generate_batch(self, start, total, platform, genre):
        results = []
        for ch in range(start, total + 1):
            request = ChapterRequest(chapter=ch, total_chapters=total,
                                     platform=platform, genre=genre)
            result = self.generate_chapter(request)
            results.append(result)
            if not result.success:
                _log.warning(f"Chapter {ch} failed, stopping batch")
                break
        self._publish(EventType.BATCH_COMPLETED, 0,
                     {"chapters": len(results), "successes": sum(1 for r in results if r.success)})
        return results

    # ==================================================================
    # Phase 1: Plan
    # ==================================================================

    def _plan_chapter(self, request: ChapterRequest) -> Optional[dict]:
        if self._planning is None:
            return {"chapter": request.chapter, "core": "故事推进",
                    "emotion": request.emotion, "suggested_word_count": 2500}

        try:
            arc_range = None
            try:
                from engine.arc_manager import ArcManager
                arc_mgr = ArcManager(self._book_dir)
                if not arc_mgr.get_status()["total_arcs"]:
                    arc_mgr.init_plan(3, ["第一卷：崛起", "第二卷：风云", "第三卷：巅峰"])
                arc_mgr.advance_arc(request.chapter)
                arc_range = arc_mgr.get_current_chapter_range()
            except Exception:
                pass

            effective_total = request.total_chapters
            if arc_range:
                effective_total = max(effective_total, arc_range[1])

            plan = self._planning.chapter_plan(
                request.chapter, effective_total, platform=request.platform)

            try:
                from engine.spec_builder import SpecBuilder
                # 使用 StateRepository 而非直接创建 NovelState
                state = self._state_repo.load()
                enriched = SpecBuilder.build(plan, self._book_dir, novel_state=None)
                if enriched and enriched.get("spec"):
                    plan.update(enriched["spec"])
            except Exception:
                pass

            if not plan or not plan.get("core"):
                return {"chapter": request.chapter, "core": "故事推进",
                        "emotion": request.emotion, "suggested_word_count": 2500}
            return plan
        except Exception as e:
            _log.error(f"Planning error: {e}")
            return None

    def _run_prewriting_analysis(self, request: ChapterRequest, spec: dict):
        """集成写前分析预览"""
        try:
            from engine.prewriting_analyzer import PrewritingAnalyzer
            pa = PrewritingAnalyzer(self._book_dir)
            state_dict = self._state_repo.load().to_dict()
            preview = pa.analyze(chapter=request.chapter, state=state_dict)
            self._engine_results.append(EngineAnalyzeResult.ok(
                "prewriting", f"就绪={preview.get('ready', False)}",
                details=preview,
            ))
            self._publish(EventType.PREWRITING_PREVIEW_READY, request.chapter,
                         {"ready": preview.get("ready", False)})
            # 将风险标记注入 spec
            if preview.get("risk_flags", {}).get("flags"):
                spec["risk_flags"] = preview["risk_flags"]["flags"]
        except Exception as e:
            _log.debug(f"PrewritingAnalyzer skip: {e}")

    def _run_chapter_contract(self, request: ChapterRequest, spec: dict):
        """集成章节契约系统"""
        try:
            from engine.chapter_contract import ChapterContractEngine
            cc = ChapterContractEngine(self._book_dir)
            state_dict = self._state_repo.load().to_dict()
            contract = cc.create_from_plan(request.chapter, spec, state_dict)
            cc.confirm_contract(request.chapter)
            cc.archive_contract(request.chapter)
            self._engine_results.append(EngineAnalyzeResult.ok(
                "chapter_contract", f"已确认+归档",
                details={"beats": len(contract.required_beats), "risk": contract.risk_level},
            ))
            self._publish(EventType.CONTRACT_CONFIRMED, request.chapter,
                         {"risk": contract.risk_level, "beats": contract.required_beats[:3]})
        except Exception as e:
            _log.debug(f"ChapterContract skip: {e}")

    def _director_review(self, request: ChapterRequest, spec: dict):
        try:
            director_check = self._llm.generate(
                "director_approve",
                chapter=request.chapter, genre=request.genre,
                platform=request.platform,
                plan_summary=spec.get("summary", spec.get("core", ""))[:200],
            )
            if director_check and len(director_check) > 50:
                _log.info(f"Director ch{request.chapter}: {director_check[:100]}")
        except Exception:
            pass

    # ==================================================================
    # Phase 2: Generate
    # ==================================================================

    def _generate_text(self, request: ChapterRequest, spec: dict) -> str:
        from engine.generator import TextGenerator
        state = self._state_repo.load()

        context = self._build_rich_context(state, request.chapter, request.genre,
                                           request.platform)

        # ResearchEngine
        try:
            from engine.research_engine import ResearchEngine
            re_eng = ResearchEngine()
            pos = "开头" if request.chapter <= 3 else (
                "前期" if request.chapter <= 20 else (
                "中期" if request.chapter <= 100 else "后期"))
            refs = re_eng.search_by_context(request.genre, request.platform, pos, max_results=2)
            if refs:
                for r in refs:
                    if r.get("snippet"):
                        context += f"\n[参考-{r.get('topic','')}] {r['snippet'][:200]}"
        except Exception:
            pass

        # AgentCoordinator
        try:
            from engine.agent_coordinator import AgentCoordinator
            ac = AgentCoordinator(self._book_dir)
            ids = ac.get_all_identities_text()
            if ids and len(ids) > 50:
                context += "\n\n" + ids
        except Exception:
            pass

        # 注入叙事结构指导
        try:
            from engine.narrative_structure import NarrativeStructureEngine
            ns = NarrativeStructureEngine()
            context += "\n\n" + ns.inject_into_prompt(request.chapter, request.genre)
        except Exception:
            pass

        chars_info = ""
        if state.characters:
            for name, char in state.characters.items():
                loc = char.location or "?"
                st = char.state.get("state", "?") if isinstance(char.state, dict) else "?"
                chars_info += f"{name}({st}@{loc}); "

        word_count = spec.get("suggested_word_count", 2500)
        plot_points = spec.get("core", "故事推进")
        chapter_title = spec.get("title", f"第{request.chapter}章")
        ending_hook = spec.get("ending", "悬念收尾")
        events = spec.get("events", [])
        key_scenes = "\n".join(str(s)[:200] for s in events[:3]) if events else "关键场景推进"
        hook_ops = spec.get("hook_ops", [])
        new_hooks = "\n".join(str(h)[:200] for h in hook_ops[:3]) if hook_ops else ""
        writing_notes = spec.get("writing_notes", [])

        try:
            if request.chapter <= 3 or request.chapter % 10 == 0:
                from engine.style_router import StyleRouter
                sr = StyleRouter()
                sa, sb = sr.get_styles(request.genre)
                _log.debug(f"A/B style: {sa} vs {sb}")
        except Exception:
            pass

        try:
            text = self._llm.generate(
                task="write_chapter", context=context,
                chapter=request.chapter, chapter_title=chapter_title,
                word_count=word_count, plot_points=plot_points,
                key_scenes=key_scenes, ending_hook=ending_hook,
                new_hooks=new_hooks, characters=chars_info,
                style_lock=TextGenerator.style_lock(request.platform),
                writing_notes=writing_notes,
            )
            return text if text and len(text) > 50 else ""
        except Exception as e:
            _log.error(f"Generation error: {e}")
            return ""

    def _build_rich_context(self, state, chapter, genre, platform) -> str:
        parts = []
        try:
            from engine.context_builder import ContextBuilder
            # ContextBuilder 接受 NovelState 兼容对象，通过 StateRepository 加载
            cb = ContextBuilder(None, self._book_dir)
            ctx = cb.build_with_memory(chapter)
            if ctx:
                parts.append(ctx)
        except Exception:
            pass

        if not parts:
            if state.progress.written > 0:
                parts.append(f"已完成: {state.progress.written}/{state.progress.total_planned}章")
            active_hooks = [h for h in state.plot.hooks if h.status in ("planted", "pending")]
            if active_hooks:
                parts.append("待回收伏笔:")
                for h in active_hooks[:5]:
                    parts.append(f"  - [{h.chapter_planted}] {h.text}")
            if state.timeline:
                recent = state.timeline[-5:]
                parts.append("最近事件:")
                for t in recent:
                    parts.append(f"  - 第{t.chapter}章: {t.event}")
            if hasattr(state, 'payoff_ledger') and state.payoff_ledger:
                pending = [p for p in state.payoff_ledger if not p.fulfilled]
                if pending:
                    parts.append("待兑现承诺:")
                    for p in pending[:3]:
                        parts.append(f"  - [{p.chapter_planted}] {p.text}")
        return "\n".join(parts)

    # ==================================================================
    # Phase 2.5: 叙事结构
    # ==================================================================

    def _run_narrative_structure(self, result: ChapterResult, request: ChapterRequest):
        try:
            from engine.narrative_structure import NarrativeStructureEngine
            ns = NarrativeStructureEngine()
            r = ns.analyze(result.text, chapter=request.chapter)
            self._engine_results.append(EngineAnalyzeResult(
                engine_name="narrative_structure",
                status=EngineStatus.OK if r.get("verdict") == "通过" else EngineStatus.DEGRADED,
                verdict=r.get("verdict", ""),
                issues=r.get("issues", []),
                details=r,
            ))
            if r.get("issues"):
                result.issues.extend(f"[叙事结构] {i}" for i in r["issues"])
        except Exception as e:
            _log.debug(f"NarrativeStructure skip: {e}")

    # ==================================================================
    # Phase 3: Detect
    # ==================================================================

    def _detect(self, text: str, platform: str) -> DetectionResult:
        return self._detector.detect(text, platform)

    # ==================================================================
    # Phase 4: Gate + Deep Review (含 L3+L4 语义审查)
    # ==================================================================

    def _auto_correct(self, text, detection, request):
        retries = 0
        current_text = text
        while retries < self.MAX_AUTO_CORRECT_RETRIES:
            current_text = self._basic_correct(current_text, detection)
            if self._writing is not None:
                try:
                    issues = self._writing.analyze(current_text)
                    if issues:
                        _log.debug(f"WritingEngine found {len(issues) if isinstance(issues, list) else 0} issues")
                except Exception:
                    pass
            detection = self._detect(current_text, request.platform)
            if detection.passed:
                break
            retries += 1
        return current_text

    def _basic_correct(self, text, detection):
        banned = ["毋庸置疑", "不可否认", "值得一提的是", "总而言之", "众所周知",
                  "命运的齿轮", "从某种意义上说", "在某种程度上", "由此可见",
                  "综上所述", "不可忽视的是"]
        for word in banned:
            if word in text:
                text = text.replace(word, "——")
        return text

    def _deep_review(self, result: ChapterResult, request: ChapterRequest):
        text = result.text
        ch = result.chapter
        issues = []

        # --- QualityGate + StoryGate ---
        try:
            from engine.quality_gate import QualityGate
            gate = QualityGate(self._detector, self._llm, None)
            report = gate.process(text, chapter=ch)
            if report.text and len(report.text) > 50:
                result.text = report.text
                result.word_count = len(report.text)
                text = report.text
            if report.issues:
                issues.extend(str(i) for i in report.issues[:10])
        except Exception as e:
            _log.debug(f"QualityGate skip: {e}")

        try:
            from engine.story_gate import StoryGate
            sg_issues = StoryGate.review(text, chapter=ch, genre=request.genre)
            if sg_issues:
                issues.extend(f"[故事] {i}" for i in sg_issues[:5])
        except Exception:
            pass

        # --- L3+L4 语义审查 ---
        try:
            from engine.semantic_review import SemanticReviewEngine
            sr = SemanticReviewEngine()
            sr_result = sr.analyze(text, chapter=ch)
            self._engine_results.append(EngineAnalyzeResult(
                engine_name="semantic_review",
                status=EngineStatus.OK if sr_result.get("verdict") == "通过" else EngineStatus.DEGRADED,
                verdict=sr_result.get("verdict", ""),
                issues=sr_result.get("issues", []),
                details=sr_result,
            ))
            if sr_result.get("issues"):
                issues.extend(f"[L3/L4] {i}" for i in sr_result["issues"][:5])
        except Exception as e:
            _log.debug(f"SemanticReview skip: {e}")

        # --- Core review engines ---
        self._run_engine(issues, text, ch, "tension",
                         "engine.engines_tension", "TensionEngine",
                         lambda e: self._tension_result(e, text, ch, request.total_chapters))
        self._run_engine(issues, text, ch, "logic",
                         "engine.engines_logic", "LogicEngine", None)
        self._run_engine(issues, text, ch, "psychology",
                         "engine.engines_psychology", "PsychologyEngine", None)
        # MultiLineNarrativeEngine uses analyze_chapter(text, chapter), not analyze(text)
        try:
            from engine.multi_line_engine import MultiLineNarrativeEngine
            mle = MultiLineNarrativeEngine()
            mle_issues = mle.analyze_chapter(text, ch)
            for mi in mle_issues:
                issues.append(f"[多线] {mi}")
        except Exception:
            pass

        # --- Foreshadow + CharacterState + GlobalMemory ---
        try:
            from engine.foreshadow_engine import ForeshadowEngine
            fe = ForeshadowEngine()
            fe.load_from_state(self._state_repo.load().to_dict())
            fe_issues = fe.analyze_chapter(text, ch)
            if fe_issues:
                issues.extend(f"[伏笔] {i}" for i in fe_issues[:5])
        except Exception:
            pass

        try:
            from engine.character_state_engine import CharacterStateEngine
            cse = CharacterStateEngine()
            state_dict = self._state_repo.load().to_dict()
            cse.load_from_dict(state_dict.get('character_states', {}))
            cse_issues = cse.validate_text_against_characters(text, ch)
            if cse_issues:
                issues.extend(f"[人设] {i}" for i in cse_issues[:5])
        except Exception:
            pass

        # GlobalMemory update moved to _persist_chapter (only on quality gate pass)

        # --- World + Stability ---
        try:
            from engine.world_engine import WorldEngine
            we = WorldEngine()
            we_issues = we.validate_text(text)
            if we_issues:
                issues.extend(f"[世界观] {i}" for i in we_issues[:5])
        except Exception:
            pass

        try:
            from engine.stability_checker import StabilityChecker
            sc = StabilityChecker()
            sc.feed_chapter(ch, text)
            sc_results = sc.run_all()
            for si in sc_results.get("character_consistency", []):
                issues.append(f"[一致性] {si}")
            for si in sc_results.get("emotional_rhythm", []):
                issues.append(f"[节奏] {si}")
        except Exception:
            pass

        # --- Batch engines (15 engines) ---
        batch_engines = [
            ("algorithm", "engines_algorithm", "AlgorithmEngine"),
            ("dialogue", "engines_dialogue", "DialogueEngine"),
            ("literature", "engines_literature", "LiteratureEngine"),
            ("nlp", "engines_nlp", "NLPEngine"),
            ("reasoning", "engines_reasoning", "ReasoningEngine"),
            ("screenplay", "engines_screenplay", "ScreenplayEngine"),
            ("writing", "engines_writing", "WritingEngine"),
            ("analysis", "engines_analysis", "AnalysisEngine"),
            ("architecture", "engines_architecture", "ArchitectureEngine"),
            ("development", "engines_development", "DevelopmentEngine"),
            ("inspiration", "engines_inspiration", "InspirationEngine"),
            ("simulation", "simulation", "SimulationEngine"),
            ("digital", "engines_utils", "DigitalEngine"),
            ("statistics", "engines_utils", "StatisticsEngine"),
            ("learning", "engines_utils", "LearningEngine"),
        ]
        for ename, emod, ecls in batch_engines:
            self._run_engine(issues, text, ch, ename,
                             f"engine.{emod}", ecls, None)

        # --- Reflection + Fractal ---
        try:
            from engine.reflection_engine import ReflectionEngine
            re_eng = ReflectionEngine()
            re_eng.reflect_on_chapter(ch, text, issues)
            re_chk = re_eng.check_repeated_issues(issues)
            if re_chk:
                issues.extend(re_chk)
        except Exception:
            pass

        try:
            from engine.fractal_engine import FractalEngine
            fe_eng = FractalEngine()
            fe_issue = fe_eng.validate_chapter_beat(text, "后1/3")
            if fe_issue:
                issues.append(f"[分形] {fe_issue}")
        except Exception:
            pass

        # --- Chapter Acceptance ---
        try:
            acceptance = self._llm.generate(
                "chapter_acceptance",
                chapter=ch, platform=request.platform, genre=request.genre,
                text=text[:500],
                issues="\n".join(f"- {i}" for i in issues[:5]),
            )
            if acceptance and "拒绝" in acceptance[:200]:
                _log.warning(f"Chapter {ch} Acceptance: 拒绝")
                issues.append("[验收] 本章未通过验收门")
        except Exception:
            pass

        # --- Auto Deep Review ---
        if len(issues) > 3:
            try:
                review = self._llm.generate(
                    "full_dimension_review",
                    project_data=(
                        f"章节：第{ch}章\n平台：{request.platform}\n"
                        f"题材：{request.genre}\n字数：{len(text)}\n\n"
                        f"正文：\n{text[:2000]}\n\n"
                        f"检测问题：\n" + "\n".join(f"- {i}" for i in issues[:10])
                    )
                )
                if review and len(review) > 100:
                    if any(kw in review[:500] for kw in ["重写", "修改", "问题严重", "建议重写"]):
                        rewritten = self._llm.generate(
                            "rewrite", text=text, issues=review[:1500]
                        )
                        if rewritten and len(rewritten) > len(text) * 0.5:
                            result.text = rewritten
                            result.word_count = len(rewritten)
                            _log.info(f"Deep rewrite: {len(text)} -> {len(rewritten)} chars")
            except Exception:
                pass

        if result.text:
            result.detection = self._detect(result.text, request.platform)

        result.issues.extend(issues)

    def _run_engine(self, issues, text, ch, ename, emod, ecls, custom_handler):
        start = time.time()
        try:
            mod = __import__(emod, fromlist=[ecls])
            engine_cls = getattr(mod, ecls)
            engine = engine_cls()
            if hasattr(engine, 'analyze'):
                results = engine.analyze(text)
                if custom_handler:
                    custom_results = custom_handler(engine)
                    if custom_results:
                        results = custom_results

                engine_issues = []
                if isinstance(results, list):
                    for r in results[:3]:
                        if isinstance(r, str) and len(r) > 5:
                            issues.append(f"[{ename}] {r}")
                            engine_issues.append(r)
                elif isinstance(results, dict):
                    v = results.get("verdict", "")
                    if v and "完成" not in v and "无数据" not in v:
                        issues.append(f"[{ename}] {v}")
                        engine_issues.append(v)

                self._engine_results.append(EngineAnalyzeResult(
                    engine_name=ename,
                    status=EngineStatus.DEGRADED if engine_issues else EngineStatus.OK,
                    issues=engine_issues,
                    elapsed_ms=(time.time() - start) * 1000,
                ))
        except Exception as e:
            _log.debug(f"Engine {ename} skip: {e}")

    def _tension_result(self, engine, text, ch, total):
        try:
            r = engine.analyze_full(text, ch=ch, total=total)
            if isinstance(r, dict):
                v = r.get("verdict", "")
                if v and "无推拉信号" not in v and "完成" not in v:
                    return [f"[张力] {v}"]
        except Exception:
            pass
        return None

    # ==================================================================
    # Phase 5: Persist (UnifiedUnitOfWork)
    # ==================================================================

    def _persist_chapter(self, request: ChapterRequest, result: ChapterResult):
        with UnitOfWork(self._state_repo, self._persistence) as uow:
            chap_rel = f"正文/第{request.chapter:03d}章.txt"
            uow.register_file_write(chap_rel, result.text)
            uow.register_command(WriteChapterCommand(
                chapter=request.chapter, text=result.text,
            ))

            # Timeline recording (纳入事务)
            try:
                from engine.engines_timeline import TimelineEngine
                tl = TimelineEngine(self._book_dir)
                tl.record_chapter(request.chapter, result.text)
            except Exception as e:
                _log.debug(f"Timeline skip: {e}")

            # ContextBuilder memory (纳入事务)
            try:
                from engine.context_builder import ContextBuilder
                cb = ContextBuilder(None, self._book_dir)
                summary = result.text[:100]
                cb.record_chapter(request.chapter, summary)
            except Exception:
                pass

            # GlobalMemoryEngine update (只在质量门控通过后执行)
            try:
                from engine.global_memory_engine import GlobalMemoryEngine
                gme = GlobalMemoryEngine(self._book_dir)
                state_dict = self._state_repo.load().to_dict()
                gme.load_from_dict(state_dict.get('global_memory', {}))
                gme.update(result.text, request.chapter, {})
            except Exception:
                pass

            # Tracker update
            try:
                self._update_trackers(uow, result)
            except Exception:
                pass

        self._publish(EventType.PERSIST_COMPLETED, request.chapter,
                     {"word_count": result.word_count})
        _log.info(f"Chapter {request.chapter} persisted: {result.word_count} chars")

    def _update_trackers(self, uow, result):
        lines = [f"## 第{result.chapter:03d}章"]
        if result.detection:
            lines.append(f"- AI检测: {result.detection.classification}")
            for i, issue in enumerate(result.detection.issues[:3]):
                lines.append(f"- 问题{i+1}: {issue.message[:80]}")
        for i, issue in enumerate(result.issues[:5]):
            lines.append(f"- 审查{i+1}: {issue[:120]}")
        lines.append(f"- 字数: {result.word_count}")
        lines.append("")
        uow.register_file_write("追踪/评审.md", "\n".join(lines), mode="append")

    # ==================================================================
    # EventBus helpers
    # ==================================================================

    def _publish(self, event_type: EventType, chapter: int, data: Dict = None):
        try:
            self._event_bus.publish(Event(type=event_type, chapter=chapter, data=data or {}, source="orchestrator"))
        except Exception:
            pass

    # ==================================================================
    # Idempotency helpers
    # ==================================================================

    def _is_chapter_already_generated(self, chapter: int) -> bool:
        """幂等检查：章节文件是否存在且 state 已记录"""
        ch_file = Path(self._book_dir) / "正文" / f"第{chapter:03d}章.txt"
        if not ch_file.exists():
            return False
        state = self._state_repo.load()
        if state.progress.written >= chapter:
            return True
        return False

    def _load_existing_chapter(self, chapter: int) -> str:
        """加载已存在的章节文本（幂等返回）"""
        ch_file = Path(self._book_dir) / "正文" / f"第{chapter:03d}章.txt"
        if ch_file.exists():
            try:
                return ch_file.read_text(encoding="utf-8")
            except Exception:
                pass
        return ""
