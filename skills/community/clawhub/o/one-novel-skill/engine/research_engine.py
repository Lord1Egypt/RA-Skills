#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""研究引擎 v2 — 基于文档索引的精准知识检索

新功能:
  - search_by_context(genre, platform, chapter_position, max_results=3)
  - search_by_topic(topic, max_results=2)
  - search(query) — 向后兼容的全文搜索 (智能路由到新方法)

所有操作纯本地执行, 零网络依赖, 零API调用。
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any


_INDEX = [
    {"key": 'pacing-guide', "file": 'writing-techniques-allinone/pacing-guide.md', "tag": '节奏', "platforms": ['番茄','起点','七猫','飞卢']},
    {"key": 'opening-design', "file": 'writing-techniques-allinone/05-golden-three-chapters.md', "tag": '开篇', "platforms": ['番茄','起点','七猫']},
    {"key": 'foreshadowing', "file": 'writing-techniques-allinone/foreshadowing-design.md', "tag": '伏笔', "platforms": ['番茄','起点']},
    {"key": 'character-design', "file": 'writing-techniques-allinone/character-design.md', "tag": '人设', "platforms": ['番茄','起点','七猫']},
    {"key": 'world-building', "file": 'writing-techniques-allinone/world-building.md', "tag": '世界观', "platforms": ['起点','七猫']},
    {"key": 'dialogue-guide', "file": 'writing-techniques-allinone/dialogue-guide.md', "tag": '对话', "platforms": ['番茄','起点','七猫','飞卢']},
    {"key": 'reader-engagement', "file": 'writing-techniques-allinone/reader-engagement.md', "tag": '黏性', "platforms": ['番茄','起点']},
    {"key": 'style-anchor', "file": 'writing-techniques-allinone/style-anchor.md', "tag": '风格', "platforms": ['番茄','起点']},
    {"key": 'scene-usage', "file": 'writing-techniques-allinone/scene-usage.md', "tag": '场景', "platforms": ['起点','番茄']},
    {"key": 'content-expansion', "file": 'writing-techniques-allinone/content-expansion.md', "tag": '扩展', "platforms": ['番茄','七猫','飞卢']},
    {"key": 'writing-craft', "file": 'writing-techniques-allinone/writing-craft.md', "tag": '技法', "platforms": ['番茄','起点']},
    {"key": 'platform-analysis', "file": 'writing-techniques-allinone/platform-analysis.md', "tag": '平台', "platforms": ['番茄','起点','七猫','飞卢']},
    {"key": 'tomato-tags', "file": 'writing-techniques-allinone/tomato-tags.md', "tag": '标签', "platforms": ['番茄']},
    {"key": 'platform-strategy', "file": 'platform-strategy.md', "tag": '平台策略', "platforms": ['番茄','起点','七猫','飞卢']},
    {"key": 'reader-psychology', "file": 'writing-techniques-allinone/04-reader-psychology.md', "tag": '读者心理', "platforms": ['番茄','起点']},
    {"key": 'narrative-arch', "file": 'writing-techniques-allinone/01-narrative-architectures.md', "tag": '叙事架构', "platforms": ['起点','番茄']},
    {"key": 'web-novel-genres', "file": 'writing-techniques-allinone/02-web-novel-genres.md', "tag": '题材', "platforms": ['番茄','起点','七猫']},
    {"key": 'classic-techniques', "file": 'writing-techniques-allinone/03-classic-techniques.md', "tag": '经典技法', "platforms": ['起点','番茄']},
    {"key": 'outline-planning', "file": 'writing-techniques-allinone/outline-planning.md', "tag": '大纲', "platforms": ['起点','番茄']},
    {"key": 'outline-review', "file": 'writing-techniques-allinone/outline-review.md', "tag": '大纲审核', "platforms": ['起点']},
    {"key": 'quality-check', "file": 'writing-techniques-allinone/quality-check.md', "tag": '质量', "platforms": ['番茄','起点']},
    {"key": 'naming-guide', "file": 'writing-techniques-allinone/naming-guide.md', "tag": '命名', "platforms": ['番茄','起点','七猫','飞卢']},
    {"key": 'context-management', "file": 'writing-techniques-allinone/context-management.md', "tag": '上下文', "platforms": ['起点','番茄']},
    {"key": 'editor-perspective', "file": 'writing-techniques-allinone/09-editor-perspective.md', "tag": '编辑视角', "platforms": ['起点']},
    {"key": 'anti-ai-instinct', "file": 'de-ai/anti-ai-instinct.md', "tag": '反AI', "platforms": ['番茄','起点']},
    {"key": 'ai-text-signals', "file": 'de-ai/ai-text-signals.md', "tag": 'AI痕迹', "platforms": ['番茄','起点','七猫']},
    {"key": 'humanizer-zh', "file": 'de-ai/humanizer-zh.md', "tag": '人性化', "platforms": ['番茄','七猫']},
    {"key": 'qmai-de-ai', "file": 'de-ai/qmai-de-ai.md', "tag": '去AI', "platforms": ['番茄','七猫']},
    {"key": 'batch-strategy', "file": 'batch-writing/daily-strategy.md', "tag": '日更', "platforms": ['番茄','飞卢']},
    {"key": 'mid-novel-slump', "file": 'batch-writing/mid-novel-slump.md', "tag": '中期乏力', "platforms": ['番茄','起点']},
    {"key": 'writer-block', "file": 'batch-writing/writer-block.md', "tag": '卡文', "platforms": ['番茄','起点','七猫','飞卢']},
    {"key": 'reader-feedback', "file": 'review/reader-feedback-loop.md', "tag": '读者反馈', "platforms": ['番茄','起点']},
    {"key": 'long-form-consistency', "file": 'review/long-form-consistency.md', "tag": '长文一致', "platforms": ['起点','番茄']},
    {"key": 'update-guide', "file": 'writing-techniques-allinone/update-guide.md', "tag": '更新策略', "platforms": ['番茄','起点']},
    {"key": 'platform-algorithms', "file": 'writing-techniques-allinone/06-platform-algorithms.md', "tag": '算法', "platforms": ['番茄','起点']},
    {"key": 'ai-detection-anti', "file": 'writing-techniques-allinone/07-ai-detection-anti-strategies.md', "tag": '反检测', "platforms": ['番茄','七猫']},
    {"key": 'dialogue-subtext', "file": 'writing-techniques-allinone/08-dialogue-subtext.md', "tag": '潜台词', "platforms": ['番茄','起点']},
    {"key": 'book-publishing', "file": 'writing-techniques-allinone/book-publishing-workflow.md', "tag": '出版', "platforms": ['起点']},
]

_POSITION_TAGS = {
    "开头": ["开篇","节奏","黏性","读者心理","叙事架构","题材"],
    "前期": ["人设","世界观","节奏","对话","经典技法","反AI"],
    "中期": ["伏笔","场景","风格","叙事架构","潜台词","扩展","读者反馈","读者心理"],
    "后期": ["伏笔","长文一致","上下文","叙事架构","大纲审核","编辑视角","出版"],
}

_TOPIC_KEY_MAP = {
    "节奏":"pacing-guide", "钩子":"opening-design", "人设":"character-design",
    "世界观":"world-building", "平台":"platform-analysis", "反AI":"anti-ai-instinct",
    "开篇":"opening-design", "伏笔":"foreshadowing", "对话":"dialogue-guide",
    "大纲":"outline-planning", "命名":"naming-guide", "场景":"scene-usage",
    "质量":"quality-check", "风格":"style-anchor", "叙事":"narrative-arch",
    "日更":"batch-strategy", "卡文":"writer-block", "读者心理":"reader-psychology",
    "AI痕迹":"ai-text-signals", "人性化":"humanizer-zh",
}


class ResearchEngine:
    """纯本地研究引擎 v2 — 基于文档索引的精准知识检索"""

    def __init__(self):
        self._cache = {}
        self._ref_dir = Path(__file__).parent.parent / "references"

    def search_by_context(self, genre, platform, chapter_position="前期", max_results=3):
        """按创作场景自动匹配相关参考文档"""
        recommended_tags = _POSITION_TAGS.get(chapter_position, _POSITION_TAGS["前期"])
        candidates = []
        for entry in _INDEX:
            if entry["platforms"]:
                if not any(p.lower() in platform.lower() or platform.lower() in p.lower() for p in entry["platforms"]):
                    continue
            if entry["tag"] in recommended_tags:
                candidates.append(entry)
        if len(candidates) < max_results:
            for entry in _INDEX:
                if entry in candidates:
                    continue
                if entry["platforms"]:
                    if not any(p.lower() in platform.lower() or platform.lower() in p.lower() for p in entry["platforms"]):
                        continue
                candidates.append(entry)
                if len(candidates) >= max_results * 2:
                    break
        results = []
        for entry in candidates[:max_results * 2]:
            fp = self._ref_dir / entry["file"]
            if not fp.exists():
                continue
            try:
                content = fp.read_text(encoding="utf-8", errors="replace")
                snippet = self._extract_snippet(content, entry["tag"])
                rel = str(fp.relative_to(self._ref_dir.parent.parent))
                results.append({"file": rel[:80], "snippet": snippet[:300], "topic": entry["tag"]})
            except Exception:
                continue
            if len(results) >= max_results:
                break
        ck = "ctx:" + genre + "|" + platform + "|" + chapter_position
        if results:
            self._cache[ck] = results
        return results or [{"file": "本地搜索", "snippet": "未找到匹配: " + genre + "/" + platform + "/" + chapter_position, "topic": "通用"}]

    def search_by_topic(self, topic, max_results=2):
        """按主题精准搜索参考文档"""
        key = _TOPIC_KEY_MAP.get(topic)
        if not key:
            matching = [e for e in _INDEX if topic in e["tag"]]
            if not matching:
                return [{"file": "本地搜索", "snippet": "未找到主题: " + topic, "topic": topic}]
            key = matching[0]["key"]
        entry = next((e for e in _INDEX if e["key"] == key), None)
        if not entry:
            return [{"file": "本地搜索", "snippet": "未知主题: " + topic, "topic": topic}]
        fp = self._ref_dir / entry["file"]
        if not fp.exists():
            return [{"file": "本地搜索", "snippet": "文件缺失: " + entry["file"], "topic": topic}]
        try:
            content = fp.read_text(encoding="utf-8", errors="replace")
            snippet = self._extract_snippet(content, topic)
            rel = str(fp.relative_to(self._ref_dir.parent.parent))
            results = [{"file": rel[:80], "snippet": snippet[:300], "topic": entry["tag"]}]
            for e2 in _INDEX:
                if e2["key"] == key:
                    continue
                if e2["tag"] == entry["tag"]:
                    fp2 = self._ref_dir / e2["file"]
                    if fp2.exists():
                        try:
                            c2 = fp2.read_text(encoding="utf-8", errors="replace")
                            r2 = str(fp2.relative_to(self._ref_dir.parent.parent))
                            results.append({"file": r2[:80], "snippet": self._extract_snippet(c2, topic)[:300], "topic": e2["tag"]})
                        except Exception:
                            pass
                    break
            self._cache["topic:" + topic] = results
            return results[:max_results]
        except Exception:
            return [{"file": "本地搜索", "snippet": "读取失败: " + topic, "topic": topic}]

    def search(self, query, source="all", max_results=3):
        """纯本地全文搜索 (兼容旧版接口)"""
        results = []
        if query in self._cache:
            return self._cache[query][:max_results]
        parts = query.strip().split()
        genre_kw = {"玄幻","仙侠","都市","言情","历史","科幻","悬疑","游戏",
                    "竞技","奇幻","武侠","军事","现实","轻小说","古代","现代","末世","重生"}
        if len(parts) >= 2:
            if parts[0] in genre_kw:
                return self.search_by_context(parts[0], parts[1] if len(parts) > 1 else "番茄", max_results=max_results)
            if parts[0] in ("番茄","起点","七猫","飞卢","晋江"):
                return self.search_by_context(parts[1] if len(parts) > 1 else "玄幻", parts[0], max_results=max_results)
        if query in _TOPIC_KEY_MAP:
            return self.search_by_topic(query, max_results=max_results)
        for tc in ("节奏","钩子","人设","世界观","平台","反AI","开篇","伏笔","对话","大纲","命名","质量","日更","场景","风格","黏性","读者心理"):
            if tc in query:
                return self.search_by_topic(tc, max_results=max_results)
        if source in ("all", "reference") and self._ref_dir.exists():
            for root, dirs, files in os.walk(self._ref_dir):
                for f in files:
                    if not f.endswith(".md"):
                        continue
                    fp = Path(root) / f
                    try:
                        content = fp.read_text(encoding="utf-8", errors="replace")
                        if query in content:
                            rel = fp.relative_to(self._ref_dir.parent.parent)
                            results.append({"file": str(rel)[:60], "snippet": content[:200] + "...", "topic": "全文匹配"})
                            if len(results) >= max_results:
                                break
                    except Exception:
                        continue
                if len(results) >= max_results:
                    break
        if results:
            self._cache[query] = results
        return results or [{"file": "本地搜索", "snippet": "未找到匹配: " + query, "topic": "通用"}]

    def keyword_search(self, keywords, source_dir=None):
        """关键词检索: 在指定目录搜索关键词"""
        if not source_dir:
            source_dir = self._ref_dir
        if not source_dir.exists():
            return []
        results = []
        for root, dirs, files in os.walk(source_dir):
            for f in files:
                if not f.endswith((".md", ".txt", ".json")):
                    continue
                fp = Path(root) / f
                try:
                    content = fp.read_text(encoding="utf-8", errors="replace")
                    for kw in keywords:
                        if kw in content:
                            results.append({"file": str(fp), "keyword": kw})
                            break
                except Exception:
                    import logging as _rlog
                    _rlog.getLogger("research").warning("keyword_search: skip " + str(fp))
        return results[:10]

    def cache_result(self, key, data):
        """缓存搜索结果"""
        self._cache[key] = data

    def load_cache(self, path):
        """从文件加载缓存"""
        if Path(path).exists():
            with open(path, "r", encoding="utf-8") as f:
                self._cache = json.load(f)

    def save_cache(self, path):
        """保存缓存到文件"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._cache, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _extract_snippet(content, topic):
        """从文档内容中提取与主题最相关的一段摘要"""
        lines = content.split("\n")
        best_idx = -1
        best_score = -1
        for i, line in enumerate(lines):
            score = 0
            if topic in line:
                score += 10
            if line.startswith("## "):
                score += 5
            if line.startswith("# "):
                score += 3
            if 20 < len(line.strip()) < 300:
                score += 2
            if score > best_score:
                best_score = score
                best_idx = i
        if best_idx >= 0:
            start = max(0, best_idx - 1)
            end = min(len(lines), best_idx + 5)
            return "\n".join(lines[start:end]).strip()
        return content[:300]
