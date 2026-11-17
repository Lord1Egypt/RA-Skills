"""
pipeline.py — [DEPRECATED] 5层管线编排

逻辑已迁移到 application/orchestrator.py (ChapterOrchestrator).
此文件保留用于向后兼容导入，新代码请使用 ChapterOrchestrator.
"""
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

_log = logging.getLogger("pipeline")


from .config import PipelineConfig, ErrorMessages

# Global config instance
_CFG = PipelineConfig()
# Clean explicit imports (all engines are in the same package)
from .engines_algorithm import AlgorithmEngine
from .engines_dialogue import DialogueEngine
from .engines_literature import LiteratureEngine
from .engines_nlp import NLPEngine
from .engines_reasoning import ReasoningEngine
from .engines_screenplay import ScreenplayEngine
from .engines_writing import WritingEngine
from .engines_analysis import AnalysisEngine
from .engines_architecture import ArchitectureEngine
from .engines_development import DevelopmentEngine
from .engines_inspiration import InspirationEngine
from .simulation import SimulationEngine
from .engines_utils import DigitalEngine, StatisticsEngine, LearningEngine



class GenerationPipeline:
    """5层生成管线 — 纯函数管道（无状态回调）"""

    def __init__(self,
                 generator: Any,
                 detector: Any,
                 planning: Any,
                 state: Any,
                 book_dir: str,
                 auto_correct_fn: Any = None):
        self.generator = generator
        self.detector = detector
        self.planning = planning
        self.state = state
        self.book_dir = Path(book_dir)
        self.auto_correct_fn = auto_correct_fn

    def run_chapter(self,
                    ch: int,
                    total: int,
                    platform: str,
                    genre: str,
                    style_lock: str = "") -> Dict[str, Any]:
        """执行单章完整流水线: Planning → Spec → Generate → Detect → Gate → Write

        checkpoint 由 run_batch() 创建/回滚（处理熔断线程 detach 场景）。
        """
        from .quality_gate import QualityGate
        from .input_adapter import build_plan_context

        try:
            # StateAccessor — 统一的 _state 访问门面
            from .state_accessor import StateAccessor
            sa = StateAccessor(self.state)

            # --- Phase A: Planning (with ArcManager rolling plan) ---
            hooks_dict = self.state.hooks_list if hasattr(self.state, '_state') else {}
            plot_points = list(hooks_dict.values())[:3] if hooks_dict else []
            chars_data = sa.get_characters()
            before_characters = [
                {"name": k, "state": v.get("state", "?"), "location": v.get("location", "?")}
                for k, v in chars_data.items()
            ]
            ctx = build_plan_context(
                chapter_id=ch, total_chapters=total,
                platform=platform, genre=genre,
                core_summary=sa.get_title(),
                plot_points=plot_points,
                before_state={"characters": [
                    {"name":k,"state":v.get("state","?"),"location":v.get("location","?")}
                    for k,v in (self.state.all_characters() or {}).items()
                ]},
            )
            from .arc_manager import ArcManager
            arc_mgr = ArcManager(str(self.book_dir))
            # Auto-init if not yet initialized
            if not arc_mgr.get_status()["total_arcs"]:
                arc_mgr.init_plan(3, ["第一卷：崛起", "第二卷：风云", "第三卷：巅峰"])
            # Advance arc if needed
            arc_mgr.advance_arc(ch)
            ch_range = arc_mgr.get_current_chapter_range()
            # Use arc-aware plan, fallback to total if arc range seems off
            effective_total = max(total, ch_range[1])
            plan = self.planning.chapter_plan(
                ch, effective_total, platform=platform
            )
            from .spec_builder import SpecBuilder
            spec = SpecBuilder.build(
                plan, str(self.book_dir), novel_state=self.state
            )
            spec_data = spec.get("spec", {})

            # AI Director — 导演规划检查 (参考 AI-Novel-Writing-Assistant)
            try:
                director_check = self.generator.generate(
                    "director_approve",
                    chapter=ch, genre=genre, platform=platform,
                    plan_summary=spec_data.get("summary", "")[:200],
                )
                if director_check and len(director_check) > 50:
                    _log.info(f"Pipeline: ch{ch} Director: {director_check[:100]}...")
            except Exception as _dr_err:
                _log.warning(f"Pipeline: ch{ch} Director check failed: {_dr_err}")

            # --- Phase A3: Thinking Phase (模拟 DeepSeek 的思考过程) ---
            _log.info(f"Pipeline: ch{ch} thinking phase...")
            thinking_prompt = (
                f"【理解需求】\n"
                f"- 平台: {platform}\n- 题材: {genre}\n"
                f"- 难度: {'开篇' if ch <= 1 else '推进' if ch <= ch_range[1]*0.5 else '高潮' if ch >= ch_range[1]*0.85 else '过渡'}\n"
                f"- 核心情节点数: {len(plan.get('core', '').split(',')) if isinstance(plan.get('core', ''), str) else len(plan.get('core', []))}\n"
                f"【叙事策略】\n"
                f"- 节奏要求: {plan.get('dopamine_phase', '正常')}\n"
                f"- 情绪目标: {plan.get('suggested_emotion', '自然过渡')}\n"
                f"- 钩子类型: {spec_data.get('ending_type', '悬念收尾')}\n"
                f"【格式要求】\n"
                f"- 字数: {spec_data.get('word_count', 2500)}字\n"
                f"- 不允许破折号\n"
                f"- 每段不超过3句\n"
                f"- 句长交替（18-48字混合）\n"
                f"【交叉检查】\n"
                f"- 选用的题材写法是否与本章定位匹配\n"
                f"- 节奏是否与前章衔接\n"
                f"- 钩子方式是否在前文用过（避免重复）\n"
            )
            # Inject multi-agent system identities into thinking phase
            try:
                from .agent_coordinator import AgentCoordinator
                _acoord = AgentCoordinator(str(self.book_dir))
                _id_text = _acoord.get_all_identities_text()
                if _id_text and len(_id_text) > 50:
                    thinking_prompt += "\n\n" + _id_text
            except Exception:
                pass

            thinking_notes = thinking_prompt

            # --- Phase B: Generation (with ContextBuilder) ---
            from .context_builder import ContextBuilder
            cb_ctx = ContextBuilder(self.state, str(self.book_dir))
            llm_ctx = cb_ctx.build_with_memory(ch)
            use_l3 = os.environ.get(_CFG.l3_env_var, "1") == "1" if _CFG.l3_enabled else False
            gen_fn = self.generator.generate_l3 if use_l3 else self.generator.generate

            # ── 上下文组装器（统一注入 ResearchEngine + ReferenceEngine + SoulSkill）──
            try:
                from .context_assembler import ContextAssembler
                assembler = ContextAssembler()
                chars_data = self.state.all_characters() or {}
                soul_chars = [
                    {"name": name, "archetype": info.get("archetype", "")}
                    for name, info in chars_data.items()
                    if isinstance(info, dict) and info.get("archetype")
                ]
                assembled = assembler.assemble(
                    chapter=ch, total=total, platform=platform, genre=genre,
                    characters=soul_chars if soul_chars else None,
                )
                if assembled:
                    llm_ctx += "\n" + assembled
            except Exception:
                pass

            mh = spec_data.get("must_happen", [])
            scenes = spec_data.get("key_scenes", [])
            hooks_data = spec_data.get("new_hooks", [])
            chars_info = ""
            for _ck, _cv in (self.state.all_characters() or {}).items():
                _cs = _cv.get("state","?") if isinstance(_cv, dict) else "?"
                _cl = _cv.get("location","?") if isinstance(_cv, dict) else "?"
                chars_info += f"{_ck}({_cs}@{_cl}); "
            text = gen_fn(
                "write_chapter", context=llm_ctx, chapter=ch, platform=platform,
                word_count=spec_data.get("word_count", 2500),
                plot_points="; ".join(mh) if mh else "章节推进",
                ending_hook=spec_data.get("ending_type", "悬疑收尾"),
                style_lock=style_lock,
                writing_notes=spec_data.get("writing_notes", []),
                chapter_title=spec_data.get("title",""),
                key_scenes="\n".join(str(s)[:200] for s in scenes[:3]) if scenes else "",
                new_hooks="\n".join(str(h)[:200] for h in hooks_data[:3]) if hooks_data else "",
                characters=chars_info,
                thinking_notes=thinking_notes,
            )

            if not text:
                return {"chapter": ch, "success": False,
                        "error": "empty_generation", "text": ""}

            
            # --- Phase B2: Optional A/B Style Generation (关键场景双版本) ---
            if ch <= 3 or ch % 10 == 0:  # 前3章和每10章跑A/B
                try:
                    from .style_router import StyleRouter
                    _sr = StyleRouter()
                    _style_a, _style_b = _sr.get_styles(genre)
                    _prompt_a = _sr.get_style_prompt(_style_a, spec_data.get("summary", "")[:100])
                    _prompt_b = _sr.get_style_prompt(_style_b, spec_data.get("summary", "")[:100])
                    _log.info(f"Pipeline: ch{ch} A/B style check ({_style_a} vs {_style_b})")
                except Exception as _ab_e:
                    _log.debug(f"Pipeline: ch{ch} A/B style fail: {_ab_e}")
# --- Phase C: Quality Gate + StoryGate ---
            gate = QualityGate(self.detector, self.generator, self.auto_correct_fn)
            report = gate.process(text, chapter=ch)
            # StoryGate — 多视角故事评审
            try:
                from .story_gate import StoryGate
                sg_issues = StoryGate.review(report.text, chapter=ch, genre=genre)
                if sg_issues:
                    report.issues.extend(sg_issues)
                    _log.info(f"Pipeline: ch{ch} StoryGate issues: {sg_issues}")
            except Exception as _sg_err:
                _log.warning(f"Pipeline: ch{ch} StoryGate failed: {_sg_err}")

            # --- 兑现台账检查 ---
            try:
                ledger_issues = self.state.check_promise_health(ch)
                for li in ledger_issues:
                    report.issues.append(li)
            except Exception:
                pass

            # --- Phase C3: Chapter Acceptance (参考 AI-Novel-Writing-Assistant) ---
            if report.classification in ("YELLOW", "RED"):
                try:
                    acceptance = self.generator.generate(
                        "chapter_acceptance",
                        chapter=ch, platform=platform, genre=genre,
                        text=report.text[:500],
                        issues="\n".join(f"- {i}" for i in report.issues[:5]),
                    )
                    if acceptance and "拒绝" in acceptance[:200]:
                        _log.warning(f"Pipeline: ch{ch} Chapter Acceptance: 拒绝")
                        report.issues.append("[验收] 本章未通过验收门")
                except Exception as _ac_err:
                    _log.warning(f"Pipeline: ch{ch} Acceptance check failed: {_ac_err}")

            # --- Phase C2: Auto Deep Review ---
            if report.classification in ("YELLOW", "RED") and len(report.issues) > 3:
                try:
                    review_text = self.generator.generate(
                        "full_dimension_review",
                        project_data=(
                            f"章节：第{ch}章\n平台：{platform}\n题材：{genre}\n字数：{len(report.text)}\n\n"
                            f"正文：\n{report.text[:2000]}\n\n"
                            f"检测问题：\n" + "\n".join(f"- {i}" for i in report.issues[:10])
                        )
                    )
                    if review_text and len(review_text) > 100:
                        _log.info(f"Pipeline: ch{ch} 深度审查: {review_text[:100]}...")
                        if any(kw in review_text[:500] for kw in ["重写","修改","问题严重","建议重写"]):
                            rewritten = self.generator.generate(
                                "rewrite", text=report.text,
                                issues=review_text[:1500]
                            )
                            if rewritten and len(rewritten) > len(report.text) * 0.5:
                                old_len = len(report.text)
                                report.text = rewritten
                                report.rewrite_count += 1
                                _log.info(f"Pipeline: ch{ch} 深度改写 {old_len}->{len(rewritten)}字")
                except Exception as _rv_err:
                    _log.warning(f"Pipeline: ch{ch} 深度审查失败: {_rv_err}")

            # --- Phase C3: Multi-Engine Checks (Psycho/Logic/Tension/MultiLine) ---
            try:
                from .engines_psychology import PsychologyEngine
                psycho = PsychologyEngine()
                psycho_issues = psycho.analyze(report.text, ch=ch)
                for pi in psycho_issues:
                    report.issues.append(f"[心理] {pi}")
            except Exception as _pe:
                _log.warning(f"Pipeline: ch{ch} 心理引擎失败: {_pe}")

            try:
                from .engines_logic import LogicEngine
                logic = LogicEngine()
                logic_issues = logic.analyze(report.text)
                logic_checks = logic.verify(report.text)
                for li in logic_issues + logic_checks:
                    report.issues.append(f"[逻辑] {li}")
            except Exception as _le:
                _log.warning(f"Pipeline: ch{ch} 逻辑引擎失败: {_le}")

            try:
                from .engines_tension import TensionEngine
                tension = TensionEngine()
                tension_result = tension.analyze_full(report.text, ch=ch, total=effective_total)
                if isinstance(tension_result, dict):
                    verdict = tension_result.get("verdict", "")
                    if verdict and "无推拉信号" not in verdict and "完成" not in verdict:
                        report.issues.append(f"[张力] {verdict}")
            except Exception as _te:
                _log.warning(f"Pipeline: ch{ch} 张力引擎失败: {_te}")

            try:
                from .multi_line_engine import MultiLineNarrativeEngine
                mle = MultiLineNarrativeEngine()
                mle_issues = mle.analyze_chapter(report.text, ch)
                for mi in mle_issues:
                    report.issues.append(f"[多线] {mi}")
            except Exception as _mle:
                _log.warning(f"Pipeline: ch{ch} 多线引擎失败: {_mle}")

            # --- Phase C3b: New Engine Trio (Foreshadow/CharacterState/GlobalMemory) ---
            # 引擎副作用暂存（不直接写入 _state），在 Phase D 事务内统一写入
            _pending_foreshadows = None
            _pending_character_states = None
            _pending_global_memory = None

            try:
                from .foreshadow_engine import ForeshadowEngine
                fe = ForeshadowEngine()
                fe.load_from_state(sa.get_raw_state())
                fe_issues = fe.analyze_chapter(report.text, ch)
                for fi in fe_issues:
                    report.issues.append(f"[伏笔] {fi}")
                _pending_foreshadows = fe.to_dict().get('foreshadows', [])
            except Exception as _fe:
                _log.warning(f"Pipeline: ch{ch} 伏笔引擎失败: {_fe}")

            try:
                from .character_state_engine import CharacterStateEngine
                cse = CharacterStateEngine()
                cse.load_from_dict(sa.get_character_states())
                cse_issues = cse.validate_text_against_characters(report.text, ch)
                for ci in cse_issues:
                    report.issues.append(f"[人设] {ci}")
                _pending_character_states = cse.to_dict()
            except Exception as _cse:
                _log.warning(f"Pipeline: ch{ch} 角色状态机失败: {_cse}")

            try:
                from .global_memory_engine import GlobalMemoryEngine
                gme = GlobalMemoryEngine(str(self.book_dir))
                gme.load_from_dict(sa.get_global_memory())
                gme.update(report.text, ch, spec_data)
                _pending_global_memory = gme.to_dict()
            except Exception as _gme:
                _log.warning(f"Pipeline: ch{ch} \u5168\u5c40\u8bb0\u5fc6\u5f15\u64ce\u5931\u8d25: {_gme}")

            # --- Phase C3b-ii: WorldEngine — 世\u754c\u89c2\u89c4\u5219\u6821\u9a8c ---
            try:
                from .world_engine import WorldEngine
                _we = WorldEngine()
                _we_issues = _we.validate_text(report.text)
                for _wi in _we_issues:
                    if _wi not in report.issues:
                        report.issues.append("[\u4e16\u754c\u89c2] " + _wi)
                _we_power_issues = _we.analyze_power_balance()
                for _pi in _we_power_issues:
                    if _pi not in report.issues:
                        report.issues.append("[\u4e16\u754c\u89c2] " + _pi)
            except Exception as _we_e:
                _log.debug("Pipeline: ch{} \u4e16\u754c\u89c2\u5f15\u64ce\u5931\u8d25: {}".format(ch, _we_e))

            # --- Phase C3c-i: StabilityChecker ---
            try:
                from .stability_checker import StabilityChecker
                _sc = StabilityChecker()
                _sc.feed_chapter(ch, report.text)
                if hasattr(self.state, "all_characters"):
                    for _cn in (self.state.all_characters() or {}):
                        _sc.feed_character(_cn, ch)
                _sc_results = _sc.run_all()
                for _si in _sc_results.get("character_consistency", []):
                    if _si not in report.issues:
                        report.issues.append(_si)
                for _si in _sc_results.get("emotional_rhythm", []):
                    if _si not in report.issues:
                        report.issues.append(_si)
            except Exception as _sc_e:
                _log.debug(f"Pipeline: ch{ch} stability check fail: {_sc_e}")

            # --- Phase C3c: Batch-run EngineBase subclasses ---
            # v1.6: 修正 batch engines 调用 — 需要实例化引擎对象而非使用类名字符串
            _batch_engines = [
                ("algorithm", AlgorithmEngine(), {"text": report.text}),
                ("dialogue", DialogueEngine(), {"text": report.text}),
                ("literature", LiteratureEngine(), {"text": report.text}),
                ("nlp", NLPEngine(), {"text": report.text}),
                ("reasoning", ReasoningEngine(), {"text": report.text}),
                ("screenplay", ScreenplayEngine(), {"text": report.text}),
                ("writing", WritingEngine(), {"text": report.text}),
                ("analysis", AnalysisEngine(), {"text": report.text}),
                ("architecture", ArchitectureEngine(), {"text": report.text, "ch": ch, "total": total}),
                ("development", DevelopmentEngine(), {"text": report.text, "ch": ch}),
                ("inspiration", InspirationEngine(), {"text": report.text, "genre": genre}),
                ("simulation", SimulationEngine(), {"text": report.text, "ch": ch}),
                ("digital", DigitalEngine(), {"text": report.text, "platform": platform}),
                ("statistics", StatisticsEngine(), {"text": report.text}),
                ("learning", LearningEngine(), {"text": report.text}),
            ]
            for _ename, _einst, _ekwargs in _batch_engines:
                try:
                    # engines pre-instantiated at module level
                    if hasattr(_einst, 'analyze'):
                        _eresults = _einst.analyze(report.text)
                        if isinstance(_eresults, list):
                            for _er in _eresults:
                                if isinstance(_er, str) and len(_er) > 5:
                                    report.issues.append(f"[{_ename}] {_er}")
                        elif isinstance(_eresults, dict):
                            _everdict = _eresults.get("verdict", "")
                            if _everdict and "完成" not in _everdict and "无数据" not in _everdict:
                                report.issues.append(f"[{_ename}] {_everdict}")
                except Exception as _be:
                    _log.debug(f"Pipeline: ch{ch} batch engine {_ename} fail: {_be}")

            
            # --- Phase C3c-ii: Reflection + Fractal ---
            try:
                from .reflection_engine import ReflectionEngine
                _re = ReflectionEngine()
                _re_ref = _re.reflect_on_chapter(ch, report.text, report.issues)
                _re_chk = _re.check_repeated_issues(report.issues)
                for _ri in _re_chk:
                    report.issues.append(_ri)
            except Exception as _re_e:
                _log.debug(f"Pipeline: ch{ch} reflection fail: {_re_e}")

            try:
                from .fractal_engine import FractalEngine
                _fe = FractalEngine()
                _fe_issue = _fe.validate_chapter_beat(report.text, "\u540e1/3")
                if _fe_issue:
                    report.issues.append(_fe_issue)
            except Exception as _fe_e:
                _log.debug(f"Pipeline: ch{ch} fractal fail: {_fe_e}")

            # --- Phase D: Persistence (with ChapterTransaction) ---
            # 第三轮审查修复: 引擎副作用 + mark_chapter_done 纳入事务 Promise 链
            from .chapter_transaction import ChapterTransaction
            with ChapterTransaction(str(self.book_dir), self.state, ch) as txn:
                # 1. 正文写入
                txn.write_text(f"正文/第{ch:03d}章.txt", report.text)
                # 2. 章节完成标记（纳入事务）
                txn.mark_chapter_done(ch)
                # 3. 规格文件更新
                txn.write_text(f"规格/第{ch:03d}章.json", json.dumps(spec_data, ensure_ascii=False, indent=2))
                # 4. 引擎副作用统一写入（纳入事务，commit 失败时自动回滚）
                if _pending_foreshadows is not None:
                    old_fs = sa.get_foreshadows()
                    txn.update_state("foreshadows", _pending_foreshadows, old_fs)
                if _pending_character_states is not None:
                    old_cs = sa.get_character_states()
                    txn.update_state("character_states", _pending_character_states, old_cs)
                if _pending_global_memory is not None:
                    old_gm = sa.get_global_memory()
                    txn.update_state("global_memory", _pending_global_memory, old_gm)
            # 记录时间线
            try:
                from .engines_timeline import TimelineEngine
                tl = TimelineEngine(str(self.book_dir))
                tl_issues = tl.record_chapter(ch, report.text)
                if tl_issues:
                    _log.warning(f"Pipeline: ch{ch} 时间线问题: {tl_issues}")
            except Exception as _tl_err:
                _log.warning(f"Pipeline: ch{ch} 时间线记录失败: {_tl_err}")
                tl_issues = []

            # 记录剧集记忆
            try:
                from .context_builder import ContextBuilder
                _cb = ContextBuilder(self.state, str(self.book_dir))
                _summary = spec_data.get("summary", "")[:100] or report.text[:100]
                _cb.record_chapter(ch, _summary)
            except Exception as _mem_err:
                _log.warning(f"Pipeline: ch{ch} 剧集记忆记录失败: {_mem_err}")

            _log.info(f"Pipeline: ch{ch} 完成 ({len(report.text)}字)")
            return {
                "chapter": ch, "success": True, "text": report.text,
                "word_count": len(report.text), "issues": report.issues,
                "classification": report.classification, "rewrite_count": report.rewrite_count,
                "timeline_issues": tl_issues,
            }
        except Exception as _e:
            _log.error(f"Pipeline: ch{ch} 失败 ({_e})")
            return {"chapter": ch, "success": False, "error": str(_e), "text": ""}

    def run_batch(self, start: int, total: int, platform: str, genre: str,
                  style_lock: str = "", refine_rounds: int = 0) -> Dict[str, Any]:
        """批量执行章节，每章通过 CircuitBreaker 保护

        Phase 1 #6: 熔断后自动 rollback checkpoint。
        checkpoint 在此层级创建，确保熔断 detach 后仍能回滚。
        """
        results = []
        error_count = 0
        start_time = datetime.now()

        from .circuit_breaker import CircuitBreaker, check_idempotent_chapter
        from .checkpoint_manager import CheckpointManager
        cb = CircuitBreaker()

        _batch_timeout = int(os.environ.get(_CFG.batch_timeout_env, str(_CFG.default_batch_timeout)))
        # 批处理总耗时检查（每章后检查，非精确中断）
        # 替换了失效的 _thr.Timer + throw() 模式
        for ch in range(start, total + 1):
            # 批处理超时检查（非精确中断，只是提前退出）
            if _batch_timeout > 0:
                elapsed = (datetime.now() - start_time).total_seconds()
                if elapsed > _batch_timeout:
                    _log.warning(f"Pipeline: batch timeout {elapsed:.0f}s > {_batch_timeout}s, aborting at ch{ch}")
                    break

            # Idempotent skip
            if not check_idempotent_chapter(self.state, ch):
                _log.info(f"Pipeline: chapter {ch} already exists, skip")
                continue

            # Phase 1 #6: 生成前创建 checkpoint
            _cp = CheckpointManager(str(self.book_dir))
            _cp.snapshot(ch)

            # Run with circuit breaker
            result, success, reason = cb.run_with_timeout(
                self.run_chapter, ch,
                ch, total, platform, genre, style_lock
            )

            if not success:
                error_count += 1
                # Phase 1 #6: 熔断超时/异常 → 回滚 checkpoint
                _log.warning(f"Pipeline: ch{ch} CircuitBreaker {reason}, 回滚 checkpoint")
                _cp.rollback(ch)
                self.state.rollback_state()
                results.append({
                    "chapter": ch, "success": False, "error": reason
                })
                continue

            # === Optional Refine (多轮精修) ===
            if refine_rounds and refine_rounds > 0 and result.get("success"):
                _log.info(f"Pipeline: ch{ch} refining ({refine_rounds} rounds)...")
                try:
                    final_text = GenerationPipeline.refine_loop(
                        result.get("text", ""), self.generator,
                        max_rounds=refine_rounds,
                        rules=["no_dash", "short_paragraphs"],
                    )
                    if final_text and len(final_text) > 50:
                        result["text"] = final_text
                except Exception as _rf_err:
                    _log.warning(f"Pipeline: ch{ch} refine failed: {_rf_err}")

            results.append(result)

        import threading as _thr
        elapsed = (datetime.now() - start_time).total_seconds()
        return {
            "chapters_run": len(results),
            "errors": error_count,
            "elapsed": elapsed,
            "results": results,
        }

    @staticmethod
    def post_process(text: str, rules: list = None) -> str:
        """后处理管线：多轮精修。
        
        支持的 rules:
        - "no_dash": 替换 —— 为其他标点
        - "no_english": 替换英文为中文（保留DNA等通用缩写）
        - "short_paragraphs": 确保段落不超3句
        - "sentence_variety": 检查句首发散性
        - "hook_check": 确保结尾有钩子
        
        用法: pipeline.py 中 post_process(text, ["no_dash", "short_paragraphs"])
        """
        if not rules:
            return text
        import re
        result = text
        
        for rule in rules:
            if rule == "no_dash":
                # 替换全角破折号为句号+空格或逗号
                result = re.sub(r'——+', '。', result)
                result = re.sub(r'—{2,}', '。', result)
            
            elif rule == "no_english":
                # 保留通用缩写（DNA, IP, 等等），替换其他英文为中文
                def _replace_eng(m):
                    word = m.group(0)
                    # 保留通用缩写
                    common = {"DNA","IP","AI","VR","AR","GPS","CEO","CTO",
                             "FBI","CIA","UFO","OK","TV"}
                    if word.upper() in common:
                        return word
                    return word  # 暂不替换，标记
                result = re.sub(r'\b[A-Za-z]{2,}\b', _replace_eng, result)
            
            elif rule == "short_paragraphs":
                # 确保段落不超3句
                paragraphs = result.split('\n\n')
                new_paras = []
                for para in paragraphs:
                    para = para.strip()
                    if not para:
                        continue
                    sentences = re.split(r'(?<=[。！？])', para)
                    sentences = [s.strip() for s in sentences if s.strip()]
                    if len(sentences) > 3:
                        # 每3句拆一段
                        for i in range(0, len(sentences), 3):
                            chunk = ''.join(sentences[i:i+3])
                            new_paras.append(chunk)
                    else:
                        new_paras.append(para)
                result = '\n\n'.join(new_paras)
            
            elif rule == "sentence_variety":
                # 检查连续两句是否同主语开头
                lines = result.split('\n')
                for i in range(len(lines)-1):
                    current = lines[i].strip()
                    next_line = lines[i+1].strip()
                    if not current or not next_line:
                        continue
                    c_start = re.match(r'^([他她它我你我你他这那]),', current)
                    n_start = re.match(r'^([他她它我你我你他这那]),', next_line)
                    if c_start and n_start and c_start.group(1) == n_start.group(1):
                        # 标记（生产环境可用LLM替换）
                        lines[i] = current + ' 【同主语开头】'
                result = '\n'.join(lines)
            
            elif rule == "hook_check":
                # 确保结尾是悬念/钩子
                # 注意：不使用 P0 禁用词（如"他不知道的是"），改用合法悬念句式
                last_100 = result[-200:] if len(result) >= 200 else result
                hook_indicators = ['?','？','突然','就在这时','他“','她“','门开了','脚步声','敲门声']
                has_hook = any(ind in last_100 for ind in hook_indicators)
                if not has_hook:
                    # 用问句替代P0禁用词，既制造悬念又不触发AI检测
                    result = result.rstrip() + '\n\n然后呢？'
        
        return result


    @staticmethod
    def refine_loop(text: str, generator, task: str = "rewrite", max_rounds: int = 3, 
                     rules: list = None, **kwargs) -> str:
        """迭代精修循环：后处理 → LLM精修 → 后处理 → ... 
        
        模拟用户的"多轮补全"习惯。
        """
        current = text
        for round_idx in range(max_rounds):
            # Step 1: 规则后处理
            if rules:
                current = GenerationPipeline.post_process(current, rules)
            
            # Step 2: LLM精修（可选）
            if generator:
                try:
                    refined = generator.generate(task, text=current[:(len(current)//3)], 
                                                  issues="round #{round_idx+1} refinement")
                    if refined and len(refined) > 50:
                        # 仅合并精修后的关键部分
                        current = refined + "\n\n" + current[len(current)//3:]
                except Exception:
                    pass
            
            # Step 3: 检查是否达成
            if round_idx >= max_rounds - 1:
                break
        
        return current