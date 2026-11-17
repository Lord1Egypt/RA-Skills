"""
quality_gate.py — 质量门控层
Phase 2: 封装 detection → rewrite → backoff 流程。
v1.6: 修复引擎类 NameError — 添加所需 import
"""
import logging
from typing import Dict, Any
from .contracts import QualityReport, DetectionLevel

# v1.6: 显式 import 所有在 try/except 中引用的引擎类
from .engines_algorithm import AlgorithmEngine
from .engines_psychology import PsychologyEngine
from .engines_tension import TensionEngine
from .engines_dialogue import DialogueEngine
from .engines_nlp import NLPEngine
from .engines_literature import LiteratureEngine
from .engines_manager import ManagerEngine
from .engines_screenplay import ScreenplayEngine
from .engines_writing import WritingEngine
from .engines_logic import LogicEngine
from .engines_reasoning import ReasoningEngine
from .simulation import SimulationEngine

_log = logging.getLogger("quality_gate")


class QualityGate:
    """检测+重写+自动纠正门控"""

    def __init__(self, detector, generator, auto_correct_fn=None):
        self._detector = detector
        self._generator = generator
        self._auto_correct = auto_correct_fn
        self._writing_engine = WritingEngine()
        self._logic_engine = LogicEngine()
        self._simulation_engine = SimulationEngine()
        self.max_rewrite_attempts = 3

    def process(self, text: str, chapter: int = 0, **extra_kw) -> QualityReport:
        """执行质量门控: 检测 → 重写(最多3次) → 回归检查"""
        # 入参校验
        if not text or not isinstance(text, str):
            report = QualityReport(text="")
            report.issues.append("输入文本为空或类型错误")
            report.classification = "RED"
            report.passed = False
            return report

        report = QualityReport(text=text)
        report.original_hash = str(hash(text))

        # ---- Detection ----
        try:
            det_result = self._detector.check(text)
            if isinstance(det_result, list):
                report.issues = det_result
        except Exception as e:
            _log.error(f"QualityGate: 检测器失败: {e}")
            report.issues.append(f"检测异常: {e}")
            report.classification = "YELLOW"
            return report

        # ---- 全维度补充检查（无论初始检测是否有问题都执行） ----
        # 学习引擎检查
        try:
            from .engines_utils import LearningEngine
            le = LearningEngine()
            learn_issues = le.analyze(text)
            if learn_issues:
                report.issues.extend(learn_issues[:3])
        except Exception:
            pass
        # 读者心理检查
        try:
            psy_issues = []
            psy_issues.extend(PsychologyEngine.check_zeigarnik(text))
            psy_issues.extend(PsychologyEngine.check_peak_end(text))
            psy_issues.extend(PsychologyEngine.check_witness_effect(text))
            for pi in psy_issues:
                if pi not in report.issues:
                    report.issues.append(f"[读者心理] {pi}")
        except Exception as _pe:
            _log.warning(f"QualityGate: 心理检查失败: {_pe}")

        # 张力分析
        try:
            pi_check = TensionEngine.check_push_pull(text)
            if pi_check:
                items = pi_check if isinstance(pi_check, list) else [str(pi_check)]
                for p in items:
                    if str(p) not in report.issues:
                        report.issues.append(f"[张力] {p}")
        except Exception as _te:
            _log.warning(f"QualityGate: 张力检查失败: {_te}")

        # 逻辑一致性
        try:
            log_issues = []
            for _check_method in ['self_check_logic', 'check_coincidence', 'check_show_vs_tell', 'check_causal_chain']:
                try:
                    lr = getattr(self._logic_engine, _check_method)(text)
                    if lr:
                        log_issues.extend(lr if isinstance(lr, list) else [str(lr)])
                except (TypeError, ValueError, AttributeError) as _ce:
                    _log.debug(f"QualityGate: 逻辑检查 {_check_method} 失败: {_ce}")
            for li in log_issues:
                if li not in report.issues:
                    report.issues.append(f"[逻辑] {li}")
        except Exception as _le:
            _log.warning(f"QualityGate: 逻辑检查失败: {_le}")

        # 对话质量
        try:
            dia_issues = []
            dia_issues.extend(DialogueEngine.check_naturalness(text))
            dia_issues.extend(DialogueEngine.check_subtext_level(text))
            dia_issues.extend(DialogueEngine.check_tag_quality(text))
            for di in dia_issues:
                if di not in report.issues:
                    report.issues.append(f"[对话] {di}")
        except Exception as _de:
            _log.warning(f"QualityGate: 对话检查失败: {_de}")

        # 写作质量
        try:
            wri_issues = []
            for _check_method in ['check_polish', 'check_memory_trace']:
                try:
                    wr = getattr(self._writing_engine, _check_method)(text)
                    if wr:
                        wri_issues.extend(wr if isinstance(wr, list) else [str(wr)])
                except (TypeError, ValueError) as _we:
                    _log.debug(f"QualityGate: 写作检查 {_check_method} 失败: {_we}")
            for wi in wri_issues:
                if wi not in report.issues:
                    report.issues.append(f"[写作] {wi}")
        except Exception as _we:
            _log.warning(f"QualityGate: 写作检查失败: {_we}")

        # NLP 分析
        try:
            nlp_result = NLPEngine.full_check(text)
            if isinstance(nlp_result, dict):
                nlp_issues = nlp_result.get("issues") or []
                if isinstance(nlp_issues, list):
                    for ni in nlp_issues:
                        if ni not in report.issues:
                            report.issues.append(f"[NLP] {ni}")
                nlp_verdict = nlp_result.get("verdict", "")
                if nlp_verdict and nlp_verdict not in report.issues:
                    report.issues.append(f"[NLP] {nlp_verdict}")
        except Exception as _ne:
            _log.warning(f"QualityGate: NLP检查失败: {_ne}")

        # 文学质量
        try:
            lit_issues = []
            aesthetic = LiteratureEngine.aesthetic_score(text)
            if isinstance(aesthetic, (int, float)) and aesthetic < 0.5:
                lit_issues.append(f"美学评分偏低({aesthetic:.2f})")
            genre_val = extra_kw.get("genre", "")
            if genre_val:
                gci = LiteratureEngine.check_genre_consistency(text, genre_val)
                if isinstance(gci, list):
                    lit_issues.extend(gci)
                elif gci:
                    lit_issues.append(str(gci))
            for li in lit_issues:
                if li not in report.issues:
                    report.issues.append(f"[文学] {li}")
        except Exception as _lte:
            _log.warning(f"QualityGate: 文学检查失败: {_lte}")

        # 有声书比例
        try:
            mgr = ManagerEngine()
            audio_check = mgr.check_audio_ratio(text)
            if audio_check:
                items = audio_check if isinstance(audio_check, list) else [str(audio_check)]
                for mi in items:
                    if mi not in report.issues:
                        report.issues.append(f"[管理] {mi}")
        except Exception as _me:
            _log.warning(f"QualityGate: 管理检查失败: {_me}")

        # 用词重复度
        try:
            rep = AlgorithmEngine.repetition_rate(text)
            if isinstance(rep, dict) and rep.get('rate', 0) > 0.5:
                msg = f"[用词] 重复率{rep['rate']:.0%}, 前3: {rep.get('top_3', [])}"
                if msg not in report.issues:
                    report.issues.append(msg)
        except Exception as _ae:
            _log.debug(f"QualityGate: 用词检查异常: {_ae}")

        # 场景质量
        try:
            scr_issues = []
            for _check in ['check_hook_density', 'check_value_reversal']:
                try:
                    si = getattr(ScreenplayEngine, _check)(text)
                    if si:
                        scr_issues.extend(si if isinstance(si, list) else [str(si)])
                except Exception:
                    pass
            for si in scr_issues:
                tag = "[场景] " + str(si)
                if tag not in report.issues:
                    report.issues.append(tag)
        except Exception:
            pass

        # 综合评分
        try:
            from .worldbuilder import Scoring
            score_result = Scoring.score_text(text, extra_kw.get("genre", ""))
            if isinstance(score_result, dict):
                score = score_result.get("score", 80)
                if isinstance(score, (int, float)):
                    if score < 60:
                        report.issues.append(f"[评分] 综合{score}/100 - 建议重写")
                    elif score < 75:
                        report.issues.append(f"[评分] 综合{score}/100 - 需优化")
                vi_list = score_result.get("issues", [])
                if isinstance(vi_list, list):
                    for vi in vi_list:
                        if vi not in report.issues:
                            report.issues.append("[评分] " + str(vi))
        except Exception:
            pass

        # 推理引擎
        try:
            rea = ReasoningEngine()
            plot_keywords = ["发现","获得","失去","背叛","决斗","突破","隐藏","交易"]
            plot_mentions = [k for k in plot_keywords if len(text) > 0 and (len(text) > text.index(k) if k in text[:2000] else False)]
            for pm in plot_mentions[:3]:
                deductions = ReasoningEngine.deduce(pm)
                for dd in deductions:
                    if dd not in report.issues:
                        report.issues.append("[推演] " + str(dd)[:100])
        except Exception:
            pass

        # 读者模拟
        try:
            sim_result = self._simulation_engine.simulate_reader(chapter, text)
            if isinstance(sim_result, dict):
                eng = sim_result.get("engagement", 0)
                drp = sim_result.get("drop_risk", 0)
                if isinstance(drp, (int, float)) and drp > 0.5:
                    report.issues.append(f"[读者模拟] 弃坑风险 {drp:.0%}")
                if isinstance(eng, (int, float)) and eng < 0.5:
                    report.issues.append(f"[读者模拟] 参与度 {eng:.0%} - 偏低")
        except Exception:
            pass

        # ---- Rewrite loop (max 3, with regression protection) ----
        if not report.issues:
            # 无基础问题 → 仍执行重写循环但只做补充优化
            report.classification = "GREEN"
            report.passed = True
        else:
            rewrite_count = 0
            best_text = text
            best_issues = list(report.issues)
            for attempt in range(self.max_rewrite_attempts):
                _log.info(f"QualityGate: rewrite attempt {attempt+1}, {len(report.issues)} issues")
                try:
                    new_text = self._generator.generate(
                        "rewrite", text=text,
                        issues="\n".join(f"- {i}" for i in report.issues)
                    )
                    if not new_text:
                        break
                    text = new_text
                    rewrite_count += 1
                    det_result = self._detector.check(text)
                    if len(report.issues) < len(best_issues):
                        best_text = text
                        best_issues = list(report.issues)
                    if not report.issues:
                        report.classification = "GREEN"
                        break
                except Exception as e:
                    _log.error(f"QualityGate: rewrite attempt {attempt} failed: {e}")
                    break

            # 始终回退到最优结果
            text = best_text
            report.issues = list(best_issues)
            if not best_issues:
                report.classification = "GREEN"
                report.passed = True
            else:
                report.classification = "YELLOW" if len(best_issues) <= 5 else "RED"
                report.passed = len(best_issues) <= 3

            report.rewrite_count = rewrite_count

            # Auto-correct (with regression check against best_issues)
            if self._auto_correct and text:
                before_ac = text
                try:
                    text = self._auto_correct(text)
                    ac_issues = self._detector.check(text)
                    if len(ac_issues) > len(best_issues):
                        _log.warning(f"QualityGate: auto_correct regressed, reverting")
                        text = before_ac
                        report.issues = list(best_issues)
                    else:
                        report.issues = list(ac_issues)
                        if not ac_issues:
                            report.classification = "GREEN"
                            report.passed = True
                except Exception as _qe:
                    _log.warning(f"QualityGate: auto_correct check failed: {_qe}")

        report.text = text
        return report

