#!/usr/bin/env python3
"""
lobster-novel: 6-dimension quality scorer (inspired by novel-evaluator).
Dims: plot, character, writing, worldview, emotion, innovation.
Score 0-100 per dim, 0-600 total.
"""
import re, math, sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Ensure sibling modules are importable
_review_dir = Path(__file__).parent
if str(_review_dir) not in sys.path:
    sys.path.insert(0, str(_review_dir))

# ═══════════════════════════════════════════════════════════════
#  Scoring heuristics — static rules for each dimension
# ═══════════════════════════════════════════════════════════════

@dataclass
class DimScore:
    score: int        # 0-100
    reason: str = ""
    detail: Dict = field(default_factory=dict)


@dataclass
class OverallScore:
    dimensions: Dict[str, DimScore] = field(default_factory=dict)
    total: int = 0
    avg: float = 0.0

    def to_text(self) -> str:
        lines = ["## 6-Dimension Score\n"]
        order = ["plot", "character", "writing", "worldview", "emotion", "innovation"]
        labels = {
            "plot": "情节", "character": "人物", "writing": "文笔",
            "worldview": "世界观", "emotion": "情感", "innovation": "创新",
        }
        for d in order:
            ds = self.dimensions.get(d)
            if ds:
                bar = "█" * (ds.score // 10) + "░" * (10 - ds.score // 10)
                lines.append(f"  {labels[d]:<6} {ds.score:>3}/100 {bar}")
                if ds.reason:
                    lines.append(f"          {ds.reason}")
                lines.append("")
        lines.append(f"  ─────────────────────────────")
        lines.append(f"  总分:    {self.total:>3}/600")
        lines.append(f"  均分:    {self.avg:.0f}/100")
        return "\n".join(lines)


class SixDimScorer:
    """Non-LLM static scorer for the 6 dimensions.
    Each dimension uses a set of heuristics.
    """

    @staticmethod
    def score_plot(text: str) -> DimScore:
        """Evaluate plot structure, pacing, hook, climax."""
        score = 60  # baseline
        details = []

        # Hook check: chapter-end cliffhanger
        paras = [p for p in text.split("\n\n") if p.strip()]
        if paras:
            last = paras[-1]
            hook_words = ["?", "？", "!", "！", "突然", "竟然", "究竟", "难道", "...", "——"]
            hook_count = sum(1 for w in hook_words if w in last)
            if hook_count >= 2:
                score += 15
                details.append("strong hook")
            elif hook_count >= 1:
                score += 8
                details.append("hook present")

        # Pacing: paragraph variety
        if len(paras) >= 10:
            para_lens = [len(p) for p in paras if len(p) > 10]
            if para_lens:
                avg_len = sum(para_lens) / len(para_lens)
                var = sum((l - avg_len)**2 for l in para_lens) / len(para_lens)
                if var > 5000:
                    score += 10
                    details.append("good pacing variety")
                elif var < 500:
                    score -= 5
                    details.append("uniform paragraph length")

        # Climax detection
        climax_words = re.findall(r'(高潮|决战|关键时刻|终于|爆发|真相大白)', text)
        if climax_words:
            score += 8
            details.append("climax beat present")

        # Scene transitions
        scene_breaks = text.count("---") + text.count("***") + text.count("——")
        if scene_breaks >= 2:
            score += 5
            details.append("scene transitions")

        score = max(10, min(100, score))
        return DimScore(score, "; ".join(details) if details else "average", {"climax": len(climax_words)})

    @staticmethod
    def score_character(text: str) -> DimScore:
        """Evaluate character depth: dialog, actions, development."""
        score = 55
        details = []

        # Dialog density
        dialog = re.findall(r'[""「『]([^"」』]{3,})[""」』]', text)
        dialog_count = len(dialog)
        chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        dialog_ratio = dialog_count / max(chars, 1) * 1000

        if dialog_ratio > 30:
            score += 15
            details.append("rich dialog")
        elif dialog_ratio > 10:
            score += 8
            details.append("some dialog")
        elif dialog_ratio < 3 and chars > 500:
            score -= 10
            details.append("too sparse dialog")

        # Action/description ratio
        action_verbs = re.findall(r'(走|跑|跳|打|笑|哭|喊|冲|抓|推|踢|举|放|站|坐|躺|拿|放|看|听|说)', text)
        action_ratio = len(action_verbs) / max(chars, 1) * 100
        if action_ratio > 5:
            score += 10
            details.append("active characters")
        elif action_ratio < 2:
            score -= 5
            details.append("static characters")

        # Emotional range
        emotion_words = re.findall(r'(笑|哭|怒|惧|悲|喜|惊|慌|平静|激动|失落|欣慰|愤怒|悲伤|喜悦|恐惧)', text)
        emotion_set = set(emotion_words)
        if len(emotion_set) >= 5:
            score += 10
            details.append("emotional range")

        score = max(10, min(100, score))
        return DimScore(score, "; ".join(details) if details else "average", {"dialog": dialog_count})

    @staticmethod
    def score_writing(text: str) -> DimScore:
        """Evaluate prose quality: sentence variety, AIGC patterns."""
        score = 60
        details = []

        # Sentence length variety
        sentences = re.split(r'[。！？!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        if sentences:
            lens = [len(s) for s in sentences]
            avg_len = sum(lens) / len(lens)
            var = sum((l - avg_len)**2 for l in lens) / len(lens) if len(lens) > 1 else 0
            if var > 800:
                score += 10
                details.append("sentence variety")
            elif var < 100:
                score -= 8
                details.append("monotonous rhythm")

        # AIGC pattern penalty
        from aigc_detect import AIGCDetector
        aigc_hits = AIGCDetector.scan(text)
        aigc_count = len(aigc_hits)
        score -= aigc_count * 3
        if aigc_count > 0:
            details.append(f"{aigc_count} AIGC patterns detected")

        # Vocabulary richness
        words = re.findall(r'[\u4e00-\u9fff]{2,}', text)
        unique = set(words)
        if words:
            ratio = len(unique) / len(words)
            if ratio > 0.6:
                score += 8
                details.append("rich vocabulary")
            elif ratio < 0.3:
                score -= 5
                details.append("repetitive vocabulary")

        score = max(10, min(100, score))
        return DimScore(score, "; ".join(details) if details else "average", {"aigc_hits": aigc_count})

    @staticmethod
    def score_worldview(text: str, bible_context: str = "") -> DimScore:
        """Evaluate world-building consistency and depth."""
        score = 55
        details = []

        # World-specific vocabulary
        world_indicators = re.findall(r'(世界|大陆|帝国|王朝|宗门|家族|势力|界|域|空间|法则|规则|等级|境界|阶位)', text)
        if len(world_indicators) >= 5:
            score += 12
            details.append("world detail present")
        elif len(world_indicators) >= 2:
            score += 5
            details.append("some world reference")

        # Setting consistency with bible (if provided)
        if bible_context:
            bible_rules = re.findall(r'(规则|设定|禁忌|不能|只能|必须|唯一)', bible_context)
            text_rules = re.findall(r'(规则|设定|禁忌|不能|只能|必须|唯一)', text)
            for rule in bible_rules:
                if rule in text_rules:
                    score += 5
                    details.append("world rule maintained")
                    break

        # Sensory description
        sensory = re.findall(r'(看见|听到|闻到|感觉|触|香气|声音|光线|温度|味道|触感)', text)
        if len(sensory) >= 5:
            score += 8
            details.append("sensory immersion")

        score = max(10, min(100, score))
        return DimScore(score, "; ".join(details) if details else "minimal world detail", {"indicators": len(world_indicators)})

    @staticmethod
    def score_emotion(text: str) -> DimScore:
        """Evaluate emotional engagement and tension."""
        score = 55
        details = []

        # Tension curve: check for emotional buildup
        tension_words = re.findall(r'(紧张|压迫|危机|危险|威胁|恐惧|焦虑|不安|悬念)', text)
        relief_words = re.findall(r'(放松|安全|平静|温暖|喜悦|安心|解决)', text)

        if tension_words and relief_words:
            score += 15
            details.append("emotional arc (tension→relief)")
        elif tension_words:
            score += 8
            details.append("tension present")

        # Empathy hooks
        empathy = re.findall(r'(心疼|共鸣|感动|共情|代入|舍不得|理解)', text)
        if empathy:
            score += 10
            details.append("empathy triggers")

        # Mood variety
        mood_words = re.findall(r'(阴沉|明亮|温暖|寒冷|压抑|轻松|悲伤|欢乐|绝望|希望|忧郁|兴奋)', text)
        mood_set = set(mood_words)
        if len(mood_set) >= 4:
            score += 8
            details.append("mood variety")

        score = max(10, min(100, score))
        return DimScore(score, "; ".join(details) if details else "flat emotion", {"moods": len(mood_set)})

    @staticmethod
    def score_innovation(text: str) -> DimScore:
        """Evaluate originality and avoid cliches."""
        score = 60
        details = []

        # Cliche penalty
        cliches = [
            (r'[醒睁]开眼.*新的一天', "wake up cliche"),
            (r'镜子.*[自己]', "mirror description"),
            (r'这一切都[是]?梦[吗吧]', "it-was-all-a-dream"),
            (r'系统.*[叮提示]', "system notification"),
            (r'宿主', "system-host"),
            (r'穿越.*醒来', "reincarnation wake-up"),
            (r'前世.*[记记得忆]', "past life memory dump"),
        ]
        cliche_hits = []
        for pat, name in cliches:
            if re.search(pat, text):
                cliche_hits.append(name)
                score -= 10
        if cliche_hits:
            details.append(f"cliches: {', '.join(cliche_hits[:3])}")

        # Unique concept check
        unique_patterns = re.findall(r'(原创|独特|前所未有|全新|从未|不同于)', text)
        if unique_patterns:
            score += 8
            details.append("unique elements")

        # Expectation subversion
        subversion = re.findall(r'(出乎意料|反转|逆袭|没想到|居然|竟然)', text)
        if len(subversion) >= 2:
            score += 8
            details.append("surprise elements")

        score = max(10, min(100, score))
        return DimScore(score, "; ".join(details) if details else "formulaic", {"cliches": cliche_hits})

    @classmethod
    def score_all(cls, text: str, bible_context: str = "") -> OverallScore:
        """Run all 6 dimensions and return overall score."""
        dims = {
            "plot": cls.score_plot(text),
            "character": cls.score_character(text),
            "writing": cls.score_writing(text),
            "worldview": cls.score_worldview(text, bible_context),
            "emotion": cls.score_emotion(text),
            "innovation": cls.score_innovation(text),
        }
        total = sum(d.score for d in dims.values())
        avg = total / len(dims)
        return OverallScore(dimensions=dims, total=total, avg=round(avg, 1))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="6-dimension novel scorer")
    parser.add_argument("file", help="chapter file to score")
    parser.add_argument("--bible", help="bible context file (optional)")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    bible = Path(args.bible).read_text(encoding="utf-8") if args.bible else ""
    result = SixDimScorer.score_all(text, bible)
    print(result.to_text())
