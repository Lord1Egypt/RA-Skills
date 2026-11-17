"""WPS AI 本地降级后端 — 零依赖、零密钥、永远可用

设计原则：
- 纯 Python 标准库 + kingdoc 已有工具，不调用任何外部 API
- 效果为「基础可用」，真正 AI 能力开放后切换后端即可
- 性能优先：长文本分段处理，避免卡顿
"""
from __future__ import annotations

import re
import math
import statistics
from typing import Dict, List, Optional, Any


class LocalFallbackBackend:
    """本地降级后端"""

    # 写作辅助：润色/扩写/缩写/翻译/续写/改写
    def write(self, text: str, action: str = "polish", **kwargs) -> Dict:
        if action == "polish":
            result = self._polish(text)
        elif action == "expand":
            result = self._expand(text)
        elif action == "shorten":
            result = self._shorten(text)
        elif action == "continue_write":
            result = self._continue_write(text)
        elif action == "rewrite":
            result = self._rewrite(text)
        else:
            result = text
        return {"text": result, "action": action, "backend": "local",
                "note": "本地降级处理，效果有限"}

    def _polish(self, text: str) -> str:
        """润色：去除口语化表达 + 调整句式"""
        replacements = {
            "搞": "处理", "弄": "处理", "做一下": "完成",
            "看上去": "看起来", "就是说": "即", "然后的话": "此外",
            "很重要": "至关重要", "很多": "大量", "很大": "显著",
        }
        result = text
        for old, new in replacements.items():
            result = result.replace(old, new)
        return result

    def _expand(self, text: str) -> str:
        """扩写：基于模板补充说明"""
        return f"{text}\n\n（扩写建议：可补充具体数据、案例或背景信息以增强说服力。）"

    def _shorten(self, text: str) -> str:
        """缩写：删除冗余修饰词"""
        redundant = ["非常", "特别", "十分", "相当", "比较", "基本上", "总的来说"]
        result = text
        for word in redundant:
            result = result.replace(word, "")
        return result

    def _continue_write(self, text: str) -> str:
        """续写：基于上文给出续写方向"""
        return f"{text}\n\n（续写建议：可从以下角度展开：1. 具体实施步骤 2. 预期效果 3. 风险与应对）"

    def _rewrite(self, text: str) -> str:
        """改写：调整语序，把被动改主动等"""
        # 简单的"被"字句改主动
        return re.sub(r"被(\w+)([\w])", r"\1\2", text)

    # 数据分析
    def analyze(self, data: Any, question: str, **kwargs) -> Dict:
        # 解析数据
        rows = self._parse_data(data)
        if not rows:
            return {"analysis": "无法解析数据", "formulas": [], "charts": [],
                    "backend": "local", "note": "请提供表格数据（二维数组或 CSV）"}

        analysis = self._basic_stats(rows, question)
        formulas = self._suggest_formulas(rows, question)
        return {"analysis": analysis, "formulas": formulas, "charts": [],
                "backend": "local", "note": "本地基础统计分析"}

    def _parse_data(self, data: Any) -> List[List[float]]:
        """解析数据为二维数值数组"""
        if isinstance(data, str):
            lines = data.strip().splitlines()
            rows = []
            for line in lines:
                nums = re.findall(r"-?\d+\.?\d*", line)
                if nums:
                    rows.append([float(n) for n in nums])
            return rows
        if isinstance(data, list):
            return [r for r in data if isinstance(r, list) and any(isinstance(x, (int, float)) for x in r)]
        return []

    def _basic_stats(self, rows: List[List[float]], question: str) -> str:
        """基础统计分析"""
        flat = [x for r in rows for x in r if isinstance(x, (int, float))]
        if not flat:
            return "无有效数值数据"
        n = len(flat)
        avg = statistics.mean(flat)
        med = statistics.median(flat)
        try:
            stdev = statistics.stdev(flat)
        except:
            stdev = 0
        total = sum(flat)
        analysis = (
            f"数据概览：共 {n} 个数值\n"
            f"总和：{total:.2f}\n"
            f"均值：{avg:.2f}\n"
            f"中位数：{med:.2f}\n"
            f"标准差：{stdev:.2f}\n"
            f"最小值：{min(flat):.2f}\n"
            f"最大值：{max(flat):.2f}"
        )
        # 简单趋势判断
        if len(flat) >= 3:
            first_half = statistics.mean(flat[:len(flat)//2])
            second_half = statistics.mean(flat[len(flat)//2:])
            if second_half > first_half * 1.05:
                analysis += "\n趋势：整体上升"
            elif second_half < first_half * 0.95:
                analysis += "\n趋势：整体下降"
            else:
                analysis += "\n趋势：基本平稳"
        return analysis

    def _suggest_formulas(self, rows: List[List[float]], question: str) -> List[str]:
        """根据问题建议 Excel 公式"""
        formulas = []
        q = question.lower()
        if "平均" in q or "均值" in q:
            formulas.append("=AVERAGE(数据范围)")
        if "总和" in q or "合计" in q or "total" in q:
            formulas.append("=SUM(数据范围)")
        if "最大" in q or "最高" in q:
            formulas.append("=MAX(数据范围)")
        if "最小" in q or "最低" in q:
            formulas.append("=MIN(数据范围)")
        if "趋势" in q or "增长" in q:
            formulas.append("=SLOPE(因变量范围, 自变量范围)")
        if "占比" in q or "比例" in q:
            formulas.append("=单元格/SUM(数据范围)")
        if not formulas:
            formulas.append("=SUM(数据范围)  — 求和")
            formulas.append("=AVERAGE(数据范围)  — 求平均")
        return formulas

    # PPT 生成
    def ppt(self, outline: str, **kwargs) -> Dict:
        try:
            from engine.local.generators import PptxGenerator
            out = kwargs.get("output_path", "output/wps_ai_ppt.pptx")
            gen = PptxGenerator()
            # 解析大纲
            slides = self._parse_outline(outline)
            if slides:
                gen.add_title_slide(slides[0].get("title", "演示文稿"),
                                    slides[0].get("subtitle", ""))
                for s in slides[1:]:
                    gen.add_content_slide(s.get("title", ""),
                                          s.get("bullets", []))
            else:
                gen.add_title_slide("演示文稿", "由 KingDoc 本地生成")
            gen.save(out)
            return {"file_path": out, "slides_count": max(len(slides), 1),
                    "backend": "local", "note": "本地 python-pptx 生成"}
        except ImportError:
            return {"file_path": "", "slides_count": 0, "backend": "local",
                    "note": "需要 python-pptx：pip install python-pptx"}

    def _parse_outline(self, outline: str) -> List[Dict]:
        """解析 Markdown 大纲"""
        slides = []
        current = None
        for line in outline.splitlines():
            line = line.strip()
            if line.startswith("# "):
                if current:
                    slides.append(current)
                current = {"title": line[2:], "subtitle": "", "bullets": []}
            elif line.startswith("## "):
                if current:
                    current["subtitle"] += line[3:] + " "
            elif line.startswith("- ") or line.startswith("• "):
                if current:
                    current["bullets"].append(line[2:])
        if current:
            slides.append(current)
        return slides

    # 阅读助手
    def read(self, content: str, action: str = "summarize", **kwargs) -> Dict:
        if action == "summarize":
            summary = self._summarize(content)
            return {"summary": summary, "key_points": self._extract_key_points(content),
                    "backend": "local", "note": "本地 TextRank 摘要"}
        elif action == "qa":
            question = kwargs.get("question", "")
            answer = self._qa(content, question)
            return {"answer": answer, "backend": "local", "note": "本地关键词匹配问答"}
        elif action == "mindmap":
            svg = self._mindmap(content)
            return {"mindmap_svg": svg, "backend": "local", "note": "本地关键词提取思维导图"}
        return {"summary": content[:200], "backend": "local"}

    def _summarize(self, text: str, top_n: int = 3) -> str:
        """TextRank 简化版摘要"""
        sentences = re.split(r"[。！？\n]", text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        if not sentences:
            return text[:200]
        # 简单 TF 评分
        word_freq = {}
        for s in sentences:
            for w in re.findall(r"\w+", s):
                word_freq[w.lower()] = word_freq.get(w.lower(), 0) + 1
        scores = []
        for s in sentences:
            words = re.findall(r"\w+", s)
            score = sum(word_freq.get(w.lower(), 0) for w in words) / max(len(words), 1)
            scores.append((s, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        top = scores[:top_n]
        top.sort(key=lambda x: sentences.index(x[0]))
        return "。".join(s[0] for s in top) + "。"

    def _extract_key_points(self, text: str) -> List[str]:
        """提取关键句"""
        sentences = re.split(r"[。！？\n]", text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
        # 含数字/专有名词的句子优先
        key_points = []
        for s in sentences:
            if re.search(r"\d+%?|\d+万|\d+亿|第[一二三四五]|首先|其次|最后", s):
                key_points.append(s)
        return key_points[:5] or sentences[:3]

    def _qa(self, text: str, question: str) -> str:
        """关键词匹配问答"""
        q_words = set(re.findall(r"\w+", question.lower()))
        sentences = re.split(r"[。！？\n]", text)
        best_score = 0
        best_answer = "未找到相关信息"
        for s in sentences:
            s_words = set(re.findall(r"\w+", s.lower()))
            overlap = len(q_words & s_words)
            if overlap > best_score:
                best_score = overlap
                best_answer = s
        return best_answer

    def _mindmap(self, text: str) -> str:
        """提取关键词生成思维导图 SVG"""
        try:
            from engine.local.generators import MindmapGenerator
            words = re.findall(r"\w{2,}", text)
            freq = {}
            for w in words:
                freq[w] = freq.get(w, 0) + 1
            top_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:8]
            if not top_words:
                return ""
            gen = MindmapGenerator()
            root = top_words[0][0]
            gen.add_node("root", root)
            for w, _ in top_words[1:]:
                gen.add_node(w, w, parent_id="root")
            out = "output/wps_ai_mindmap.svg"
            gen.render_svg(out)
            return out
        except:
            return ""

    # === v3.6.0 新增：段落级 AI 深度集成（本地降级占位） ===

    def rewrite_paragraph(self, paragraph: str, style: str = "formal", **kwargs) -> Dict:
        """AI 段落改写（本地降级：返回原文+提示）。"""
        style_hints = {
            "formal": "建议使用正式书面语，避免口语化表达",
            "casual": "建议使用口语化表达，轻松自然",
            "concise": "建议精简语句，删除冗余修饰",
            "elaborate": "建议补充细节和说明，使内容更完整",
        }
        hint = style_hints.get(style, "建议调整表达方式")
        return {
            "original": paragraph,
            "rewritten": paragraph,  # 降级：返回原文
            "style": style,
            "backend": "local",
            "note": f"本地降级占位。WPS AI API 开放后将升级为原生。{hint}",
        }

    def summarize_paragraph(self, paragraph: str, max_length: int = 100, **kwargs) -> Dict:
        """AI 段落总结（本地降级：返回截断原文+提示）。"""
        truncated = paragraph[:max_length]
        if len(paragraph) > max_length:
            truncated += "..."
        return {
            "original_length": len(paragraph),
            "summary": truncated,
            "max_length": max_length,
            "backend": "local",
            "note": "本地降级占位。WPS AI API 开放后将升级为原生段落总结。",
        }

    def continue_paragraph(self, paragraph: str, direction: str = "", **kwargs) -> Dict:
        """AI 段落续写（本地降级：返回续写方向提示）。"""
        direction_hints = {
            "详细说明": "可从以下角度详细说明：具体实施步骤、技术细节、注意事项",
            "举例": "可补充实际案例或示例，使内容更具体",
            "总结": "可进行概括性总结，提炼核心要点",
            "对比": "可与同类方案进行对比分析",
        }
        hint = direction_hints.get(direction, f"可继续围绕'{direction}'方向展开论述")
        return {
            "original": paragraph,
            "continuation": f"\n\n（续写方向：{direction}。{hint}）",
            "direction": direction,
            "backend": "local",
            "note": "本地降级占位。WPS AI API 开放后将升级为原生段落续写。",
        }
