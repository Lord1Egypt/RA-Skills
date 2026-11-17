#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
platform_article.py — 平台文章模式引擎

SKILL.md 声明功能：
- A0 选题与结构：平台、文章类型、核心观点、大纲确认
- A1 正文生成与平台排版：生成→原创性检查→平台格式校验→定稿
- 文章字数体系：小红书笔记300-1000/知乎回答500-3000/头条资讯800-2000/公众号文章1500-5000
"""

import re
import logging
from typing import Dict, List, Optional, Any

_log = logging.getLogger("platform_article")


class PlatformArticleEngine:
    """平台文章模式引擎 — 两阶段流程"""

    # === 平台文章参数 ===
    ARTICLE_SYSTEMS = {
        "小红书笔记": {
            "range": (300, 1000),
            "platform": "小红书",
            "types": ["经验分享", "测评推荐", "教程攻略", "故事分享", "观点输出"],
            "structure": "标题(钩子) → 个人经历(代入感) → 干货/观点 → 总结 → 话题标签",
            "tone": "亲切口语化/第一人称/emoji适度",
            "format_rules": {
                "max_paragraph_length": 100,
                "requires_emoji": False,
                "requires_hashtags": True,
                "requires_image_placeholder": True,
            },
        },
        "知乎回答": {
            "range": (500, 3000),
            "platform": "知乎",
            "types": ["专业解答", "亲历者讲述", "深度分析", "观点辩论", "知识科普"],
            "structure": "开场(一句话抓注意力) → 故事/论证展开 → 观点提炼 → 互动引导",
            "tone": "专业但不冰冷/有理有据/个人经历加分",
            "format_rules": {
                "max_paragraph_length": 400,
                "requires_sections": True,
                "requires_references": False,
            },
        },
        "头条资讯": {
            "range": (800, 2000),
            "platform": "头条",
            "types": ["热点解读", "资讯分析", "观点评论", "知识科普", "故事讲述"],
            "structure": "标题(争议/好奇) → 事件概述 → 深度分析 → 观点输出 → 互动引导",
            "tone": "观点明确/有理有据/引发讨论",
            "format_rules": {
                "max_paragraph_length": 300,
                "requires_title_hook": True,
                "requires_opening_hook": True,
            },
        },
        "公众号文章": {
            "range": (1500, 5000),
            "platform": "公众号",
            "types": ["深度长文", "人物故事", "行业分析", "情感共鸣", "实用干货"],
            "structure": "标题 → 引言(共鸣/悬念) → 分节展开(3-5小节) → 升华/金句 → 引导关注",
            "tone": "有温度/有深度/有独特观点",
            "format_rules": {
                "max_paragraph_length": 350,
                "requires_sections": True,
                "requires_golden_sentence": True,
                "requires_cta": True,
            },
        },
    }

    # === 选题检查 ===
    TOPIC_CHECKLIST = {
        "时效性": "选题是否与当前热点/趋势相关？",
        "独特性": "是否有独特的个人视角或经历？",
        "价值性": "读者读完能获得什么（知识/情感/方法）？",
        "可执行性": "选题是否能在一篇文章内讲清楚？",
        "传播性": "读者是否愿意转发/分享？",
    }

    def __init__(self):
        pass

    # ====== A0: 选题与结构 ======

    def identify_article_type(self, word_count: int, platform: str = "") -> Dict[str, Any]:
        """A0: 识别文章类型和平台"""
        # 匹配文章类型
        matched_type = None
        for name, info in self.ARTICLE_SYSTEMS.items():
            low, high = info["range"]
            if low <= word_count <= high:
                if not platform or info["platform"] == platform:
                    matched_type = name
                    break

        if not matched_type:
            # 按字数最近匹配
            if word_count < 500:
                matched_type = "小红书笔记"
            elif word_count <= 2000:
                matched_type = "头条资讯"
            else:
                matched_type = "公众号文章"

        info = self.ARTICLE_SYSTEMS[matched_type]
        return {
            "phase": "A0",
            "article_type": matched_type,
            "platform": info["platform"],
            "word_range": f"{info['range'][0]}-{info['range'][1]}字",
            "available_types": info["types"],
            "structure": info["structure"],
            "tone": info["tone"],
            "format_rules": info["format_rules"],
        }

    def generate_topic_checklist(self) -> Dict[str, str]:
        """A0: 选题检查清单"""
        return dict(self.TOPIC_CHECKLIST)

    def generate_outline_template(self, article_type: str) -> Dict[str, Any]:
        """A0: 生成大纲模板"""
        info = self.ARTICLE_SYSTEMS.get(article_type, self.ARTICLE_SYSTEMS["小红书笔记"])
        structure_parts = [s.strip() for s in info["structure"].split("→")]

        outline = {
            "title": "",
            "type": article_type,
            "platform": info["platform"],
            "sections": [],
        }

        for i, part in enumerate(structure_parts):
            outline["sections"].append({
                "index": i + 1,
                "name": part,
                "word_allocation": "",
                "key_points": [],
            })

        # 分配字数比例
        total_sections = len(structure_parts)
        if article_type == "小红书笔记":
            ratios = [0.10, 0.35, 0.35, 0.10, 0.10]
        elif article_type == "知乎回答":
            ratios = [0.10, 0.50, 0.30, 0.10]
        elif article_type == "头条资讯":
            ratios = [0.10, 0.25, 0.35, 0.20, 0.10]
        else:  # 公众号
            ratios = [0.05, 0.10, 0.55, 0.20, 0.10]

        for i, section in enumerate(outline["sections"]):
            if i < len(ratios):
                section["word_allocation"] = f"{int(ratios[i] * 100)}%"

        return outline

    def generate_a0_prompt(self, word_count: int, platform: str = "") -> str:
        """A0: 生成选题与结构引导提示"""
        a0 = self.identify_article_type(word_count, platform)

        lines = [f"【A0 选题与结构】"]
        lines.append(f"文章类型: {a0['article_type']}")
        lines.append(f"目标平台: {a0['platform']}")
        lines.append(f"字数范围: {a0['word_range']}")
        lines.append(f"平台风格: {a0['tone']}")
        lines.append("")
        lines.append("可用文章类型:")
        for t in a0["available_types"]:
            lines.append(f"  - {t}")
        lines.append("")
        lines.append("结构模板:")
        lines.append(f"  {a0['structure']}")
        lines.append("")
        lines.append("选题检查清单:")
        for key, question in self.TOPIC_CHECKLIST.items():
            lines.append(f"  [{key}] {question}")

        return "\n".join(lines)

    # ====== A1: 正文生成与平台排版 ======

    def validate_originality(self, text: str) -> Dict[str, Any]:
        """A1: 原创性检查（基于文本特征，非抄袭检测）"""
        issues = []

        # 检查是否过于通用/模板化
        generic_patterns = [
            (r"随着.{0,20}的发展", "模板化开头"),
            (r"在当今社会", "模板化开头"),
            (r"众所周知", "禁用词"),
            (r"毋庸置疑", "禁用词"),
            (r"不可否认", "禁用词"),
            (r"总的来说", "模板化结尾"),
            (r"综上所述", "模板化结尾"),
        ]
        for pattern, category in generic_patterns:
            if re.search(pattern, text):
                issues.append(f"[{category}] {pattern}")

        # 检查句式多样性
        sentences = re.split(r'[。！？\n]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) >= 5]
        if len(sentences) >= 5:
            # 检查是否所有句子都以相同主语开头
            subject_starts = []
            for s in sentences[:10]:
                if len(s) >= 2:
                    subject_starts.append(s[:2])
            unique_starts = len(set(subject_starts))
            if unique_starts <= 2 and len(subject_starts) >= 5:
                issues.append("[句式单一] 句子开头过于重复，缺乏多样性")

        return {
            "check": "原创性",
            "passed": len(issues) == 0,
            "issues": issues,
            "verdict": "✅ 通过" if not issues else "⚠️ 需优化",
        }

    def validate_platform_format(self, text: str, article_type: str) -> Dict[str, Any]:
        """A1: 平台格式校验"""
        info = self.ARTICLE_SYSTEMS.get(article_type, self.ARTICLE_SYSTEMS["小红书笔记"])
        rules = info["format_rules"]
        issues = []

        # 段落长度检查
        paragraphs = [p for p in text.split("\n") if p.strip()]
        max_len = rules.get("max_paragraph_length", 300)
        long_paras = [(i, len(p)) for i, p in enumerate(paragraphs) if len(p) > max_len]
        if long_paras:
            issues.append(f"{len(long_paras)}段超过{info['platform']}建议长度({max_len}字)")

        # 平台特有检查
        if rules.get("requires_hashtags"):
            if not re.search(r'#\S+', text):
                issues.append(f"{info['platform']}需要话题标签 #")

        if rules.get("requires_sections"):
            if not re.search(r'#{1,3}\s', text):
                issues.append(f"{info['platform']}建议使用分节标题")

        if rules.get("requires_golden_sentence"):
            # 检查是否有金句标记（引号中的精炼表达）
            quotes = re.findall(r'["""][^"""]{10,50}["'']', text)
            if not quotes:
                issues.append("公众号文章建议有金句/精炼表达")

        if rules.get("requires_cta"):
            cta_markers = ["关注", "点赞", "在看", "转发", "分享", "留言", "评论", "讨论"]
            if not any(m in text[-300:] for m in cta_markers):
                issues.append("公众号文章建议有引导互动(CTA)")

        if rules.get("requires_title_hook"):
            first_line = paragraphs[0] if paragraphs else ""
            hook_markers = ["？", "!", "震惊", "揭秘", "真相", "原来", "竟然", "为什么", "如何"]
            if not any(m in first_line for m in hook_markers):
                issues.append("头条文章标题需要有吸引力的钩子")

        if rules.get("requires_opening_hook"):
            first_100 = text[:100] if len(text) >= 100 else text
            hook_markers = ["？", "!", "突然", "意外", "发现", "震惊", "原来"]
            if not any(m in first_100 for m in hook_markers):
                issues.append("头条文章开头需要钩子")

        return {
            "platform": info["platform"],
            "article_type": article_type,
            "format_rules": rules,
            "passed": len(issues) == 0,
            "issues": issues,
            "verdict": "✅ 格式通过" if not issues else "⚠️ 需调整格式",
        }

    def generate_platform_styled_output(self, text: str, article_type: str) -> str:
        """A1: 生成平台适配的格式化输出（纯文本层面）"""
        info = self.ARTICLE_SYSTEMS.get(article_type, self.ARTICLE_SYSTEMS["小红书笔记"])

        if article_type == "小红书笔记":
            # 确保有话题标签
            if "#" not in text:
                text += "\n\n#经验分享 #干货 #生活记录"
            # 确保段落短小
            paragraphs = text.split("\n")
            result = []
            for p in paragraphs:
                if len(p) > 150 and "。" in p:
                    # 拆分长段落
                    parts = re.split(r'(?<=[。！？])', p)
                    for part in parts:
                        if part.strip():
                            result.append(part.strip())
                else:
                    result.append(p)
            return "\n\n".join(result)

        elif article_type == "知乎回答":
            # 确保有分节
            if not re.search(r'#{1,3}\s', text):
                parts = text.split("\n\n")
                formatted = []
                for i, part in enumerate(parts):
                    if len(part.strip()) > 100 and i > 0 and not part.startswith("#"):
                        formatted.append(f"## {part[:30]}...")
                    formatted.append(part)
                return "\n\n".join(formatted)

        elif article_type == "公众号文章":
            # 确保有引导关注
            if not any(m in text[-200:] for m in ["关注", "点赞", "在看"]):
                text += "\n\n---\n\n如果觉得有用，欢迎**点赞**、**在看**、**分享**给需要的朋友。"
            return text

        return text

    def validate_complete(self, text: str, article_type: str) -> Dict[str, Any]:
        """A1: 完整校验（原创性+格式）"""
        originality = self.validate_originality(text)
        format_check = self.validate_platform_format(text, article_type)

        all_issues = originality.get("issues", []) + format_check.get("issues", [])
        passed = originality["passed"] and format_check["passed"]

        return {
            "phase": "A1",
            "passed": passed,
            "originality": originality,
            "format": format_check,
            "verdict": "✅ 通过，可以定稿" if passed else "⚠️ 需要修改",
            "action_required": all_issues,
        }

    # ====== 完整流程 ======

    def run_full_workflow(self, word_count: int, platform: str = "", text: str = "",
                          article_type: str = "") -> Dict[str, Any]:
        """执行完整两阶段流程"""
        result = {"word_count": word_count, "platform": platform}

        # A0
        if article_type:
            a0_info = self.ARTICLE_SYSTEMS.get(article_type)
            if a0_info:
                result["A0"] = {
                    "article_type": article_type,
                    "platform": a0_info["platform"],
                    "structure": a0_info["structure"],
                    "tone": a0_info["tone"],
                }
        if "A0" not in result:
            result["A0"] = self.identify_article_type(word_count, platform)

        result["A0_prompt"] = self.generate_a0_prompt(word_count, platform)
        result["A0_outline"] = self.generate_outline_template(
            result.get("A0", {}).get("article_type", article_type or "小红书笔记")
        )

        # A1
        if text:
            at = result.get("A0", {}).get("article_type", article_type or "小红书笔记")
            result["A1"] = self.validate_complete(text, at)
            result["A1_formatted"] = self.generate_platform_styled_output(text, at)
        else:
            result["A1"] = {"status": "等待正文生成"}

        return result

    # === 兼容 Engine 接口 ===

    def analyze(self, text: str = "", article_type: str = "小红书笔记", **kwargs) -> Dict[str, Any]:
        """统一 analyze 接口（兼容 registry 规范）"""
        if not text:
            return {"verdict": "无文本", "issues": ["请提供待检测的文本"]}
        return self.validate_complete(text, article_type)
