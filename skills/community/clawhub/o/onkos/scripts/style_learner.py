#!/usr/bin/env python3
"""
风格学习器 - 从已有文本中提取并量化写作风格
词汇频率、句式长度、修辞模式、情感曲线
"""

import os
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter


class StyleLearner:
    """风格学习器 - 量化和复制写作风格"""

    def __init__(self, style_path: str):
        """
        初始化风格学习器

        Args:
            style_path: 风格数据文件路径（JSON）
        """
        self.style_path = Path(style_path)
        self.style_path.parent.mkdir(parents=True, exist_ok=True)
        self.style_data = self._load()

    def _load(self) -> Dict[str, Any]:
        """加载风格数据"""
        if self.style_path.exists():
            with open(self.style_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "profiles": {},
            "metadata": {}
        }

    def _save(self):
        """保存风格数据"""
        with open(self.style_path, 'w', encoding='utf-8') as f:
            json.dump(self.style_data, f, ensure_ascii=False, indent=2)

    def analyze(self, text: str, profile_name: str = "default") -> Dict[str, Any]:
        """
        分析文本风格

        Args:
            text: 待分析文本
            profile_name: 风格配置名称

        Returns:
            风格分析结果
        """
        profile = {
            "name": profile_name,
            "sentence": self._analyze_sentences(text),
            "vocabulary": self._analyze_vocabulary(text),
            "rhetoric": self._analyze_rhetoric(text),
            "emotion": self._analyze_emotion(text),
            "pacing": self._analyze_pacing(text),
            "dialogue": self._analyze_dialogue(text)
        }

        self.style_data["profiles"][profile_name] = profile
        self._save()

        return profile

    def _analyze_sentences(self, text: str) -> Dict[str, Any]:
        """分析句式特征"""
        # 按中文句号、问号、感叹号分句
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return {"avg_length": 0, "length_distribution": {}, "pattern": "unknown"}

        lengths = [len(s) for s in sentences]
        avg_len = sum(lengths) / len(lengths)

        # 长度分布
        short = len([l for l in lengths if l <= 10])
        medium = len([l for l in lengths if 10 < l <= 30])
        long = len([l for l in lengths if l > 30])

        total = len(lengths)
        distribution = {
            "short": f"{short / total * 100:.1f}%",
            "medium": f"{medium / total * 100:.1f}%",
            "long": f"{long / total * 100:.1f}%"
        }

        # 判断句式模式
        if avg_len <= 15:
            pattern = "concise"
        elif avg_len <= 25:
            pattern = "balanced"
        else:
            pattern = "elaborate"

        return {
            "avg_length": round(avg_len, 1),
            "length_distribution": distribution,
            "pattern": pattern,
            "sample_count": total
        }

    def _analyze_vocabulary(self, text: str) -> Dict[str, Any]:
        """分析词汇特征"""
        # 尝试使用 jieba 分词
        try:
            import jieba
            words = list(jieba.cut(text))
            words = [w.strip() for w in words if w.strip() and len(w.strip()) > 1]
        except ImportError:
            # 降级：简单提取中文词
            words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)

        if not words:
            return {"richness": 0, "top_words": [], "genre_markers": []}

        # 词汇丰富度（类型/标记比）
        unique_words = set(words)
        richness = len(unique_words) / len(words) if words else 0

        # 高频词
        word_counts = Counter(words)
        top_words = word_counts.most_common(30)

        # 题材标记词
        genre_markers = self._detect_genre_markers(text)

        return {
            "richness": round(richness, 3),
            "unique_words": len(unique_words),
            "total_words": len(words),
            "top_words": [(w, c) for w, c in top_words],
            "genre_markers": genre_markers
        }

    def _detect_genre_markers(self, text: str) -> List[str]:
        """检测题材标记词"""
        markers = {
            "玄幻": ["灵气", "修为", "丹药", "法术", "阵法", "宗门", "秘境", "道友", "天劫", "元婴"],
            "武侠": ["内力", "轻功", "剑法", "掌法", "江湖", "门派", "侠义", "盟主", "暗器"],
            "科幻": ["星舰", "量子", "AI", "基因", "虚拟", "虫洞", "跃迁", "赛博"],
            "都市": ["公司", "总裁", "咖啡", "地铁", "合同", "项目", "加班"],
            "历史": ["陛下", "臣", "将军", "城池", "朝堂", "奏折", "边关"]
        }

        detected = []
        for genre, keywords in markers.items():
            matches = sum(1 for kw in keywords if kw in text)
            if matches >= 2:
                detected.append(genre)

        return detected

    def _analyze_rhetoric(self, text: str) -> Dict[str, Any]:
        """分析修辞手法"""
        rhetoric = {
            "metaphor_count": 0,
            "parallelism_count": 0,
            "repetition_count": 0,
            "rhetoric_density": 0.0
        }

        # 比喻检测（简化：检测"像""如""似"）
        metaphor_patterns = [r'像.{1,10}一样', r'如.{1,10}般', r'似.{1,8}般', r'宛如.{1,10}']
        for pattern in metaphor_patterns:
            rhetoric["metaphor_count"] += len(re.findall(pattern, text))

        # 排比检测（简化：连续3个以上相同句式开头）
        parallelism_patterns = [r'((?:他|她|它).{2,8}[，。]){3,}']
        for pattern in parallelism_patterns:
            rhetoric["parallelism_count"] += len(re.findall(pattern, text))

        # 重复修辞
        total_chars = len(text)
        if total_chars > 0:
            rhetoric["rhetoric_density"] = round(
                (rhetoric["metaphor_count"] + rhetoric["parallelism_count"]) / total_chars * 1000, 2
            )

        return rhetoric

    def _analyze_emotion(self, text: str) -> Dict[str, Any]:
        """分析情感特征"""
        emotion_keywords = {
            "positive": ["微笑", "欢笑", "温暖", "希望", "感动", "喜悦", "欣慰", "自豪", "幸福"],
            "negative": ["悲伤", "愤怒", "绝望", "恐惧", "痛苦", "孤独", "怨恨", "焦虑", "悔恨"],
            "tense": ["紧张", "危险", "紧迫", "惊恐", "不安", "警惕", "窒息", "凶险"],
            "epic": ["震撼", "磅礴", "浩瀚", "恢弘", "壮丽", "苍茫", "苍穹", "万古"]
        }

        counts = {}
        for emotion, keywords in emotion_keywords.items():
            count = sum(text.count(kw) for kw in keywords)
            counts[emotion] = count

        total = sum(counts.values()) or 1
        distribution = {k: f"{v / total * 100:.1f}%" for k, v in counts.items()}

        # 判断主要情感基调
        dominant = max(counts, key=counts.get) if any(counts.values()) else "neutral"

        return {
            "dominant": dominant,
            "distribution": distribution,
            "raw_counts": counts
        }

    def _analyze_pacing(self, text: str) -> Dict[str, Any]:
        """分析节奏特征"""
        # 按段落分析
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        if not paragraphs:
            return {"avg_paragraph_length": 0, "pacing": "unknown"}

        para_lengths = [len(p) for p in paragraphs]
        avg_len = sum(para_lengths) / len(para_lengths)

        # 对话密度
        dialogue_count = len(re.findall(r'["""].+?["""]|「.+?」|".+?"', text))

        # 判断节奏
        if avg_len < 50:
            pacing = "fast"
        elif avg_len < 150:
            pacing = "moderate"
        else:
            pacing = "slow"

        return {
            "avg_paragraph_length": round(avg_len, 1),
            "paragraph_count": len(paragraphs),
            "dialogue_density": round(dialogue_count / len(paragraphs), 2) if paragraphs else 0,
            "pacing": pacing
        }

    def _analyze_dialogue(self, text: str) -> Dict[str, Any]:
        """分析对话特征"""
        # 提取对话
        dialogues = re.findall(r'["""].+?["""]|「.+?」|".+?"', text)

        if not dialogues:
            return {"ratio": 0, "avg_length": 0, "style": "narrative-heavy"}

        total_chars = len(text)
        dialogue_chars = sum(len(d) for d in dialogues)
        ratio = dialogue_chars / total_chars if total_chars else 0

        avg_length = sum(len(d) for d in dialogues) / len(dialogues)

        if ratio > 0.5:
            style = "dialogue-heavy"
        elif ratio > 0.3:
            style = "balanced"
        else:
            style = "narrative-heavy"

        return {
            "ratio": round(ratio, 3),
            "count": len(dialogues),
            "avg_length": round(avg_length, 1),
            "style": style
        }

    def compare(self, text: str, profile_name: str = "default") -> Dict[str, Any]:
        """
        将文本与指定风格配置进行比较

        Args:
            text: 待比较文本
            profile_name: 目标风格配置

        Returns:
            风格比较结果
        """
        if profile_name not in self.style_data["profiles"]:
            return {"error": f"风格配置 '{profile_name}' 不存在"}

        target = self.style_data["profiles"][profile_name]
        current = self.analyze(text, "_temp_compare")

        comparison = {
            "target_profile": profile_name,
            "overall_similarity": 0.0,
            "dimensions": {}
        }

        # 句式相似度
        target_sent = target.get("sentence", {})
        current_sent = current.get("sentence", {})
        sent_sim = self._cosine_sim_dict({
            "short": self._percent_to_float(target_sent.get("length_distribution", {}).get("short", "0%")),
            "medium": self._percent_to_float(target_sent.get("length_distribution", {}).get("medium", "0%")),
            "long": self._percent_to_float(target_sent.get("length_distribution", {}).get("long", "0%"))
        }, {
            "short": self._percent_to_float(current_sent.get("length_distribution", {}).get("short", "0%")),
            "medium": self._percent_to_float(current_sent.get("length_distribution", {}).get("medium", "0%")),
            "long": self._percent_to_float(current_sent.get("length_distribution", {}).get("long", "0%"))
        })
        comparison["dimensions"]["sentence"] = {"similarity": round(sent_sim, 3)}

        # 对话比相似度
        target_dialogue = target.get("dialogue", {}).get("ratio", 0)
        current_dialogue = current.get("dialogue", {}).get("ratio", 0)
        dialogue_sim = 1 - abs(target_dialogue - current_dialogue)
        comparison["dimensions"]["dialogue"] = {"similarity": round(dialogue_sim, 3)}

        # 节奏相似度
        target_pacing = target.get("pacing", {}).get("pacing", "moderate")
        current_pacing = current.get("pacing", {}).get("pacing", "moderate")
        pacing_sim = 1.0 if target_pacing == current_pacing else 0.5
        comparison["dimensions"]["pacing"] = {"similarity": pacing_sim}

        # 综合相似度
        dims = [v["similarity"] for v in comparison["dimensions"].values()]
        comparison["overall_similarity"] = round(sum(dims) / len(dims), 3) if dims else 0

        return comparison

    def generate_style_guide(self, profile_name: str = "default") -> str:
        """
        生成风格指导文本

        Args:
            profile_name: 风格配置名称

        Returns:
            风格指导文本
        """
        if profile_name not in self.style_data["profiles"]:
            return f"[风格配置 '{profile_name}' 不存在]"

        profile = self.style_data["profiles"][profile_name]

        lines = [
            f"## 写作风格指导: {profile_name}",
            "",
            "### 句式特征",
        ]

        sentence = profile.get("sentence", {})
        lines.append(f"- 平均句长: {sentence.get('avg_length', '?')}字")
        lines.append(f"- 句式模式: {sentence.get('pattern', '?')}")
        lines.append(f"- 长度分布: 短句{sentence.get('length_distribution', {}).get('short', '?')}, "
                     f"中句{sentence.get('length_distribution', {}).get('medium', '?')}, "
                     f"长句{sentence.get('length_distribution', {}).get('long', '?')}")

        lines.append("")
        lines.append("### 对话特征")
        dialogue = profile.get("dialogue", {})
        lines.append(f"- 对话占比: {dialogue.get('ratio', 0) * 100:.1f}%")
        lines.append(f"- 对话风格: {dialogue.get('style', '?')}")

        lines.append("")
        lines.append("### 节奏特征")
        pacing = profile.get("pacing", {})
        lines.append(f"- 节奏: {pacing.get('pacing', '?')}")
        lines.append(f"- 平均段落长度: {pacing.get('avg_paragraph_length', '?')}字")

        lines.append("")
        lines.append("### 情感基调")
        emotion = profile.get("emotion", {})
        lines.append(f"- 主导情感: {emotion.get('dominant', '?')}")
        if emotion.get("distribution"):
            for k, v in emotion["distribution"].items():
                lines.append(f"  - {k}: {v}")

        lines.append("")
        lines.append("### 修辞特征")
        rhetoric = profile.get("rhetoric", {})
        lines.append(f"- 比喻密度: {rhetoric.get('metaphor_count', 0)}/千字")
        lines.append(f"- 排比密度: {rhetoric.get('parallelism_count', 0)}/千字")

        vocab = profile.get("vocabulary", {})
        if vocab.get("genre_markers"):
            lines.append("")
            lines.append("### 题材标记")
            for marker in vocab["genre_markers"]:
                lines.append(f"- {marker}")

        return "\n".join(lines)

    def _cosine_sim_dict(self, a: Dict[str, float], b: Dict[str, float]) -> float:
        """计算两个字典的余弦相似度"""
        keys = set(a.keys()) | set(b.keys())
        vec_a = [a.get(k, 0) for k in keys]
        vec_b = [b.get(k, 0) for k in keys]
        dot = sum(x * y for x, y in zip(vec_a, vec_b))
        norm_a = sum(x ** 2 for x in vec_a) ** 0.5
        norm_b = sum(x ** 2 for x in vec_b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0
        return dot / (norm_a * norm_b)

    def _percent_to_float(self, pct: str) -> float:
        """将百分比字符串转为浮点数"""
        try:
            return float(pct.replace("%", "")) / 100
        except (ValueError, AttributeError):
            return 0.0


    def close(self):
        """无资源需释放，保留接口一致性"""
        pass

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action == "analyze":
            text = params.get("text", "")
            text_file = params.get("text_file")
            if text_file:
                with open(text_file, 'r', encoding='utf-8') as f:
                    text = f.read()
            if not text:
                return {"error": "需要提供文本"}
            return self.analyze(text, params.get("profile", "default"))

        elif action == "compare":
            text = params.get("text", "")
            text_file = params.get("text_file")
            if text_file:
                with open(text_file, 'r', encoding='utf-8') as f:
                    text = f.read()
            if not text:
                return {"error": "需要提供文本"}
            profile_name = params.get("profile", "default")
            if profile_name not in self.style_data.get("profiles", {}):
                return {"error": f"风格配置 '{profile_name}' 不存在，请先使用 analyze-style 创建风格配置"}
            return self.compare(text, profile_name)

        elif action == "guide":
            guide = self.generate_style_guide(params.get("profile", "default"))
            return {"guide": guide}

        elif action == "list-profiles":
            return {"profiles": list(self.style_data.get("profiles", {}).keys())}

        else:
            raise ValueError(f"未知操作: {action}")

def main():
    parser = argparse.ArgumentParser(description='风格学习器')
    parser.add_argument('--style-path', required=True, help='风格数据文件路径')
    parser.add_argument('--action', required=True,
                       choices=['analyze', 'compare', 'guide', 'list-profiles'],
                       help='操作类型')
    parser.add_argument('--text', help='待分析文本')
    parser.add_argument('--text-file', help='待分析文本文件')
    parser.add_argument('--profile', default='default', help='风格配置名称')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    learner = StyleLearner(args.style_path)

    skip_keys = {"style_path", "action", "output"}
    params = {k: v for k, v in vars(args).items()
              if v is not None and k not in skip_keys and not k.startswith('_')}
    result = learner.execute_action(args.action, params)
    if args.output == 'text' and args.action == 'guide':
        print(result.get("guide", ""))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
