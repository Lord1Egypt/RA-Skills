#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ReferenceEngine v1.6 — 结构化资料索引 + 多目录搜索 + pipeline 集成

v1.6 新增:
  - 加载 references/index.json 实现标签化搜索
  - 支持 trends/ / original/ / platform-data/ 新目录
  - query_by_phase() 按创作阶段注入精准资料摘要
  - get_platform_profile() 返回读者画像数据
"""

import os, json, re
from pathlib import Path
from typing import List, Dict, Optional


class ReferenceEngine:
    """参考文献数据引擎 — 结构化资料索引 + 搜索"""

    def __init__(self, ref_dir: str = ""):
        if not ref_dir:
            ref_dir = str(Path(__file__).parent.parent / "references")
        self.ref_dir = Path(ref_dir)
        self._cache: Dict[str, str] = {}
        self._ref_index: Dict[str, dict] = {}
        self._tags_index: Dict[str, list] = {}
        self._platform_guide: Dict[str, list] = {}
        self._phase_guide: Dict[str, list] = {}
        self._build_index()
        self._load_json_index()

    def _build_index(self):
        """构建参考文献的搜索索引"""
        if not self.ref_dir.exists():
            return
        skill_dir = Path(__file__).parent.parent
        base = skill_dir
        for f in self.ref_dir.rglob("*.md"):
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
                title = ""
                for line in text.split(chr(10)):
                    ls = line.strip()
                    if ls.startswith("# "):
                        title = ls[2:60]
                        break
                try:
                    rel = f.relative_to(base)
                except ValueError:
                    rel = f
                self._ref_index[f.name] = {"path": str(rel), "title": title, "size": len(text)}
            except Exception:
                pass

    def _load_json_index(self):
        """加载结构化 JSON 索引 (v1.6)"""
        idx_path = self.ref_dir / "index.json"
        if not idx_path.exists():
            return
        try:
            data = json.loads(idx_path.read_text(encoding="utf-8"))
            self._tags_index = data.get("tags_index", {})
            self._platform_guide = data.get("platform_compatibility", {})
            self._phase_guide = data.get("chapter_position_guide", {})
        except Exception:
            pass

    def search_ref(self, keyword, max_results=5):
        """在参考文献中搜索关键词"""
        results = []
        base = self.ref_dir.parent.parent
        for name, info in self._ref_index.items():
            fp = base / info["path"]
            if not fp.exists():
                continue
            text = fp.read_text(encoding="utf-8", errors="replace")
            if keyword in text:
                results.append({"file": name, "title": info["title"], "match": text[:100]})
                if len(results) >= max_results:
                    break
        return results or [{"file": "", "title": "", "match": "未找到: " + keyword}]

    PLATFORM_ALIAS = {"番茄":"番茄小说","起点":"起点中文网","七猫":"七猫","飞卢":"飞卢"}

    def platform_spec(self, platform=""):
        specs = {
            "番茄": {"收费模式": "免费(广告分成)", "目标读者": "下沉市场,碎片阅读", "单章字数": "2000-3000", "核心节奏": "快,前三章出金手指"},
            "起点": {"收费模式": "付费订阅", "目标读者": "深度读者,追求质量", "单章字数": "3000-5000", "核心节奏": "中,世界观铺垫长"},
            "七猫": {"收费模式": "免费+广告", "目标读者": "女性为主,情感向", "单章字数": "2000-3000", "核心节奏": "中,情感线优先"},
            "飞卢": {"收费模式": "付费+打赏", "目标读者": "男频,爽文爱好者", "单章字数": "2000-3000", "核心节奏": "极快,500字内给金手指"},
        }
        return specs.get(platform, specs.get("番茄"))

    def genre_definition(self, genre):
        """题材定义"""
        genres = {"玄幻":"东西方幻想融合, 升级体系, 金手指, 宏大世界观",
                  "修仙":"修炼体系(炼气->化神), 宗门斗争, 天道因果",
                  "都市":"现代背景, 逆袭/赘婿/战神, 系统流",
                  "科幻":"硬科幻OBL<=2, 技术推演, 社会影响",
                  "悬疑":"三幕式谜题: 埋线->伪解->真解, 公平竞赛",
                  "言情":"推拉6:4, 情感五阶段, 浪漫三幕",
                  "恐怖":"未知恐惧公式, 递进(不安->焦虑->恐惧)"}
        return genres.get(genre, "通用类型")

    def list_genres(self):
        return ["玄幻","修仙","都市","科幻","悬疑","言情","恐怖"]

    def read_doc(self, name: str) -> str:
        """读取指定引用文档的完整内容（带缓存）。

        Args:
            name: 文件名（如 "platform-strategy.md"）

        Returns:
            文档内容，不存在返回 ""
        """
        if name in self._cache:
            return self._cache[name]
        # 先按完整文件名匹配
        if name in self._ref_index:
            p = self._resolve_path(self._ref_index[name]["path"])
            if p and p.exists():
                text = p.read_text(encoding="utf-8", errors="replace")
                self._cache[name] = text
                return text
        # 再按文件名末尾匹配
        for fname, info in self._ref_index.items():
            if fname.endswith(name) or fname == name:
                p = self._resolve_path(info["path"])
                if p and p.exists():
                    text = p.read_text(encoding="utf-8", errors="replace")
                    self._cache[name] = text
                    return text
        return ""

    def _resolve_path(self, rel_path) -> Path:
        """解析引用文档的绝对路径。"""
        p = Path(rel_path)
        if p.exists():
            return p
        absp = self.ref_dir.parent.parent / rel_path
        if absp.exists():
            return absp
        absp2 = self.ref_dir.parent / rel_path
        if absp2.exists():
            return absp2
        return None

    def list_docs(self) -> list:
        """列出所有可用的引用文档名。"""
        return sorted(self._ref_index.keys())

    def search_docs_by_tag(self, tag: str) -> list:
        """按标签搜索文档（匹配标题和文件名的关键词）。"""
        results = []
        tag_lower = tag.lower()
        for fname, info in self._ref_index.items():
            if tag_lower in fname.lower() or tag_lower in info.get("title", "").lower():
                results.append({"name": fname, "title": info.get("title", ""), "path": info.get("path", "")})
        return results

    # ── v1.6 新增方法 ──

    def query_by_phase(self, chapter: int, platform: str, genre: str) -> List[Dict]:
        """按创作阶段返回精准资料摘要（用于注入 pipeline Phase A）

        Args:
            chapter: 当前章节编号
            platform: 目标平台
            genre: 题材

        Returns:
            [{topic, snippet, file}] 最多 3 条
        """
        # 判断创作阶段
        if chapter <= 3:
            position = "开头"
        elif chapter <= 20:
            position = "前期"
        elif chapter <= 100:
            position = "中期"
        else:
            position = "后期"

        # 获取该阶段推荐标签
        tags = self._phase_guide.get(position, [])
        if not tags:
            tags = ["开篇", "节奏", "人设"]

        # 按平台筛选标签
        platform_tags = self._platform_guide.get(platform, [])
        if platform_tags:
            tags = [t for t in tags if t in platform_tags] or tags[:3]

        results = []
        for tag in tags[:5]:
            docs = self._tags_index.get(tag, [])
            for doc_path in docs[:2]:
                doc_name = os.path.basename(doc_path)
                content = self.read_doc(doc_name)
                if content and len(content) > 50:
                    snippet = content[:300]
                    results.append({
                        "topic": tag,
                        "snippet": snippet,
                        "file": doc_name,
                    })
                    if len(results) >= 3:
                        return results

        return results[:3]

    def get_platform_profile(self, platform: str) -> Dict:
        """获取平台读者画像数据（v1.6）"""
        profile_path = self.ref_dir / "platform-data" / "platform-reader-profiles.md"
        if profile_path.exists():
            content = profile_path.read_text(encoding="utf-8", errors="replace")
            # 提取对应平台段落
            marker = f"## {platform}"
            if marker in content:
                start = content.index(marker)
                end = content.find("\n## ", start + len(marker))
                if end == -1:
                    end = len(content)
                section = content[start:end]
                return {"platform": platform, "profile": section[:500], "source": "platform-reader-profiles.md"}
        return {"platform": platform, "profile": "", "source": "built-in"}

    def get_genre_opening_template(self, genre: str) -> Optional[str]:
        """获取题材开篇模板（v1.6）"""
        doc = self.read_doc("genre-opening-templates.md")
        if not doc:
            return None
        # 提取对应题材段落
        marker = f"## {genre}"
        alt_markers = {
            "都市": "都市类", "玄幻": "玄幻类",
            "言情": "言情类", "悬疑": "悬疑类",
            "仙侠": "玄幻类", "科幻": "玄幻类",
        }
        if marker in doc:
            start = doc.index(marker)
        elif genre in alt_markers and f"## {alt_markers[genre]}" in doc:
            start = doc.index(f"## {alt_markers[genre]}")
        else:
            return None
        end = doc.find("\n## ", start + len(marker))
        if end == -1:
            end = len(doc)
        return doc[start:end]

    def get_hook_density_guide(self, platform: str) -> str:
        """获取钩子密度指南（v1.6）"""
        doc = self.read_doc("hook-density-model.md")
        if not doc:
            return ""
        return doc[:500]




