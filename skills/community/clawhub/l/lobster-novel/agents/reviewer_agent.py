#!/usr/bin/env python3
"""
lobster-novel: reviewer agent — 7-dimension rule-based quality review.
"""

from __future__ import annotations

import sys, json, re, logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.contract import RuntimeContract
from core.story_state import StoryState


_DIMENSION_WEIGHTS = dict(爽点评估=0.15, 设定一致性=0.15, 节奏评估=0.15, OOC检查=0.10,
                         叙事连贯性=0.15, 追读力评估=0.15, AI味检测=0.15)
_PASS_THRESHOLD = 70.0

_SHUANGDIAN_KW = ["终于", "发现", "突然", "但是", "然而", "就在这时", "这一刻", "真相", "秘密", "力量"]
_AIGC_INLINE = ["突然", "就在这时", "内心充满", "他意识到", "她意识到", "他感到", "她感到", "原来如此", "只见", "就这样"]
_DIALOGUE_MARKERS = {"说", "道", "问", "回答"}
_WORLD_BUILDING = {"世界", "规则", "力量", "历史", "传说"}
_ACTION_KW = {"推", "拉", "走", "跑", "站", "蹲", "握", "举", "打开", "关闭", "拿", "放"}
_EMOTION_KW = {"哭", "笑", "沉默", "颤抖", "紧", "深呼"}
_HOOK_END_KW = ["？", "等待", "接下来", "还没有", "未知", "将", "会", "意味着"]
_SILENT_TRAITS = {"话少", "沉默", "寡言", "不爱说话"}


@dataclass
class ReviewDimension:
    name: str
    score: float = 0.0
    issues: list[str] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
@dataclass
class ReviewReport:
    chapter_number: int
    chapter_title: str
    word_count: int
    dimensions: dict[str, ReviewDimension]
    overall_score: float
    passed: bool
    summary: str
    suggestions: list[str]

class ReviewerAgent:
    def __init__(self, project_dir: str | Path) -> None:
        self.project_dir = Path(project_dir)
        self._aigc_detector: Any = None
        p = self.project_dir / "review" / "aigc_detect.py"
        if p.is_file():
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("aigc_detect", str(p))
                if spec and spec.loader:
                    m = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(m)
                    self._aigc_detector = m.AIGCDetector
            except Exception:
                pass

    def full_review(self, text: str, ch_num: int, title: str,
                    runtime_contract: RuntimeContract | None = None,
                    story_state: StoryState | None = None) -> ReviewReport:
        if not text or not text.strip():
            return self._empty_report(ch_num, title)
        wc = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
        dims = {d.name: d for d in [
            self._d_shuangdian(text), self._d_consistency(text, story_state),
            self._d_pacing(text, runtime_contract), self._d_ooc(text, story_state),
            self._d_continuity(text), self._d_reader_pull(text), self._d_aigc(text),
        ]}
        overall = round(sum(dims[n].score * _DIMENSION_WEIGHTS[n] for n in _DIMENSION_WEIGHTS), 1)
        passed = overall >= _PASS_THRESHOLD
        r = ReviewReport(ch_num, title, wc, dims, overall, passed,
                         self._generate_summary(dims), self._collect_suggestions(dims))
        print(f"[ReviewerAgent] Ch {ch_num} — {overall:.1f}/100 — {'PASS' if passed else 'FAIL'}")
        return r

    def _d_shuangdian(self, text: str) -> ReviewDimension:
        dim = ReviewDimension(name="爽点评估")
        wc = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff") or 1
        lines = text.split("\n")
        kw_count = sum(1 for l in lines if any(k in l for k in _SHUANGDIAN_KW))
        excl_count = sum(1 for l in lines if l.strip().endswith(("！", "？")))
        # Normalize by word count: expect ~1 kw per 200 chars, ~1 excl per 100 chars
        kw_density = kw_count / (wc / 200)
        excl_density = excl_count / (wc / 100)
        raw = min(kw_density, 1.5) / 1.5 * 50 + min(excl_density, 1.5) / 1.5 * 30 + 20
        dim.score = round(min(100.0, raw), 1)
        if kw_count < max(1, wc // 500):
            dim.issues.append(f"爽点关键词密度偏低（{kw_count}次/约{round(wc/200)}k），建议增加转折/发现/真相类语句")
        if excl_count < max(1, wc // 300):
            dim.issues.append(f"感叹/疑问句偏少（{excl_count}次），情绪张力不足")
        if kw_density > 0.8:
            dim.strengths.append(f"爽点关键词密度高（{round(kw_density,1)}x基线）")
        if excl_density > 0.8:
            dim.strengths.append("感叹/疑问句使用充分")
        return dim

    def _d_consistency(self, text: str, ss: StoryState | None) -> ReviewDimension:
        dim = ReviewDimension(name="设定一致性", score=100.0)
        if ss is None:
            dim.strengths.append("无故事状态数据，跳过设定一致性检查")
            return dim
        contradictions = 0
        last_ch_num = max(ss.chapters.keys()) if ss.chapters else 0
        for cid, cs in ss.characters.items():
            name = cs.name or cid
            appears = name in text or cid in text
            if cs.status == "完成" and appears:
                contradictions += 1
                dim.issues.append(f"角色'{name}'状态为'完成'但仍在章节中")
            elif cs.status == "coming" and appears:
                contradictions += 1
                dim.issues.append(f"角色'{name}'尚未登场(coming)但已出现")
            elif cs.status == "active" and cs.last_appearance >= last_ch_num - 8 and not appears:
                contradictions += 1
                dim.issues.append(f"活跃角色'{name}'未在本章出现")
        dim.score = max(0.0, 100.0 - contradictions * 20)
        if contradictions == 0:
            dim.strengths.append("角色状态一致")
        return dim

    def _d_pacing(self, text: str, rc: RuntimeContract | None) -> ReviewDimension:
        dim = ReviewDimension(name="节奏评估")
        if rc is not None and rc.strand_targets:
            ratios = self._analyze_strands(text)
            dev = sum(abs(ratios.get(s, 0) - rc.strand_targets.get(s, 0)) for s in ("quest", "fire", "constellation"))
            dim.score = round(max(0.0, 100.0 - dev * 100), 1)
            if dev < 0.1:
                dim.strengths.append(f"节奏接近目标（偏差{dev:.2f}）")
            else:
                dim.issues.append(f"节奏偏差{round(dev*100)}%，建议调整各线索比例")
        else:
            paras = [p for p in text.split("\n\n") if p.strip()]
            if not paras:
                dim.score = 50.0
                dim.issues.append("章节过短，无法评估节奏")
                return dim
            s = sum(1 for p in paras if len(p) < 50)
            m = sum(1 for p in paras if 50 <= len(p) <= 150)
            l = sum(1 for p in paras if len(p) > 150)
            variety = min(s, m, l) / len(paras) * 300
            dim.score = round(min(100.0, variety), 1)
            if s > m + l:
                dim.issues.append("短段落过多，节奏偏碎")
            elif l > s + m:
                dim.issues.append("长段落过多，节奏偏慢")
            else:
                dim.strengths.append("段落长度分布合理")
        return dim

    def _d_ooc(self, text: str, ss: StoryState | None) -> ReviewDimension:
        dim = ReviewDimension(name="OOC检查", score=100.0)
        vp = self.project_dir / "voice_library.json"
        if not vp.is_file():
            vp = self.project_dir / "continuity" / "voice_library.json"
        if not vp.is_file():
            logging.debug("reviewer._d_ooc: voice_library.json not found, skipping OOC")
            dim.strengths.append("无声线数据，跳过OOC检查")
            return dim
        try:
            vd = json.loads(vp.read_text(encoding="utf-8"))
        except Exception as e:
            logging.warning(f"reviewer._d_ooc: failed to load {vp}: {e}")
            dim.strengths.append("无声线数据，跳过OOC检查")
            return dim
        dialogs = self._extract_dialogue_lines(text)
        violations = 0
        for cname, voice in vd.items():
            cnt = sum(1 for d in dialogs if cname in d)
            traits = ""
            if isinstance(voice, dict):
                for v in voice.get("catchphrases", []):
                    traits += " " + v
                for s in voice.get("speech_patterns", []):
                    traits += " " + (s.get("description", "") if isinstance(s, dict) else str(s))
            if any(t in traits for t in _SILENT_TRAITS) and cnt > 3:
                violations += 1
                dim.issues.append(f"角色'{cname}'设定沉默但对话{cnt}句")
        dim.score = max(0.0, 100.0 - violations * 25)
        if violations == 0:
            dim.strengths.append("角色声线一致")
        return dim

    def _d_continuity(self, text: str) -> ReviewDimension:
        dim = ReviewDimension(name="叙事连贯性", score=70.0)
        breaks = [(i, l) for i, l in enumerate(text.split("\n")) if l.strip() in ("---", "——")]
        proper = sum(1 for i, _ in breaks if i > 0 and len(text.split("\n")[i - 1].strip()) > 20)
        closed = any((text[-200:] if len(text) >= 200 else text).rstrip().endswith(p) for p in ("。", "！", "？", "”", "」"))
        s = min(100.0, 70.0 + min(15, proper * 5) + (5 if closed else 0))
        if breaks and proper == 0:
            s, _ = max(30.0, s - 10), dim.issues.append("场景转换缺少前置铺垫")
        dim.score = round(s, 1)
        if len(breaks) >= 2:
            dim.strengths.append(f"包含{len(breaks)}个场景转换")
        if closed:
            dim.strengths.append("结尾收束完整")
        return dim

    def _d_reader_pull(self, text: str) -> ReviewDimension:
        dim = ReviewDimension(name="追读力评估", score=50.0)
        opening = text[:200] if len(text) >= 200 else text
        ending = text[-200:] if len(text) >= 200 else text
        op = 0
        if any(k in opening for k in _HOOK_END_KW):
            op += 15
        if "“" in opening or "「" in opening:
            op += 10
        first_para = opening.split("\n\n")[0] if "\n\n" in opening else opening
        if len(first_para) < 100:
            op += 5
        ep = 0
        if any(k in ending for k in _HOOK_END_KW):
            ep += 15
        elif any(ep_word in ending for ep_word in ("不过", "但", "然而")):
            ep += 5
        dim.score = round(min(100.0, 50.0 + op + ep), 1)
        if op >= 15:
            dim.strengths.append("开篇钩子有效")
        else:
            dim.issues.append("开篇吸引力不足，建议前200字设悬念")
        if ep >= 15:
            dim.strengths.append("结尾钩子强烈，追读欲望高")
        else:
            dim.issues.append("结尾缺乏钩子，追读意愿可能不足")
        return dim

    def _d_aigc(self, text: str) -> ReviewDimension:
        dim = ReviewDimension(name="AI味检测", score=100.0)
        count = 0
        if self._aigc_detector is not None:
            try:
                count = len(self._aigc_detector.scan(text))
            except Exception:
                pass
        if count == 0 and self._aigc_detector is None:
            count = sum(text.count(p) for p in _AIGC_INLINE)
        dim.score = round(max(0.0, 100.0 - count * 15), 1)
        if count == 0:
            dim.strengths.append("未检测到AI味表达")
        elif count <= 3:
            dim.strengths.append(f"AI味较少（{count}处）")
            dim.issues.append(f"发现{count}处AI味表达")
        else:
            dim.issues.append(f"AI味较多（{count}处），建议重写模式化表达")
        return dim

    @staticmethod
    def _analyze_strands(text: str) -> dict[str, float]:
        lines = text.split("\n")
        counts = dict(quest=0, fire=0, constellation=0)
        for line in lines:
            s = line.strip()
            if not s:
                continue
            strand = None
            if any(k in s for k in _EMOTION_KW):
                strand = "quest"
            if any(k in s for k in _DIALOGUE_MARKERS) and s.endswith(("。", "！", "？", "”", "」", "』")):
                strand = "constellation" if any(k in s for k in _WORLD_BUILDING) else "fire"
            if strand is None and any(k in s for k in _WORLD_BUILDING):
                strand = "constellation"
            if strand is None and any(k in s for k in _ACTION_KW):
                strand = "quest"
            if strand is None and s and s[-1] in "。！？":
                strand = "quest"
            if strand and strand in counts:
                counts[strand] += 1
        total = sum(counts.values()) or 1
        return {k: round(v / total, 4) for k, v in counts.items()}

    @staticmethod
    def _extract_dialogue_lines(text: str) -> list[str]:
        return [l.strip() for l in text.split("\n") if any(k in l for k in _DIALOGUE_MARKERS) and ("“" in l or "「" in l)]

    @staticmethod
    def _generate_summary(dimensions: dict[str, ReviewDimension]) -> str:
        sorted_dims = sorted(dimensions.values(), key=lambda d: d.score)
        lowest, highest = sorted_dims[0], sorted_dims[-1]
        s = f"最强: {highest.name}({highest.score:.0f}分)；最弱: {lowest.name}({lowest.score:.0f}分)"
        if lowest.score < 50:
            s += f"；建议优先改进'{lowest.name}'"
        return s

    @staticmethod
    def _collect_suggestions(dimensions: dict[str, ReviewDimension]) -> list[str]:
        result = []
        for dim in sorted(dimensions.values(), key=lambda d: d.score):
            for issue in dim.issues:
                if len(result) >= 5:
                    break
                result.append(f"[{dim.name}] {issue}")
            if len(result) >= 5:
                break
        return result

    @staticmethod
    def _empty_report(n: int, t: str) -> ReviewReport:
        dims = {x: ReviewDimension(name=x, score=100.0 if x in ("OOC检查", "AI味检测") else 0.0) for x in _DIMENSION_WEIGHTS}
        return ReviewReport(n, t, 0, dims, 0.0, False, "章节为空，无法评审", ["章节内容为空，请先撰写正文"])
