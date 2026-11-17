#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球法规连接器 · MCP Server
=====================================
把 medxpert-reg-hub 知识库（28 份全球法规枢纽资料）封装成本地只读 MCP Server，
供 WorkBuddy / Agent / 小艺 Skill 直接调用检索全球医疗器械法规知识。

特性：
- 本地只读，零网络外发，零凭据
- 4 个工具：list_hubs / search_regulation / get_hub / ask_classification
- 检索返回片段 + 官方链接 + 待核验标注

运行：python reg_connector_server.py   （stdio 模式，供 MCP 客户端调用）
用法：FastMCP stdio 协议，直接作为 MCP server 配置进 WorkBuddy mcp.json
"""

import json
import os
import re
import sys
from pathlib import Path

from fastmcp import FastMCP

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
# 知识库源目录定位（三级回退，确保开箱即用）：
#   1. 包内 references/（本技能自带知识库，发布形态）
#   2. REG_HUB_REFS 环境变量（用户自定义指向其他知识库目录）
#   3. 脚本所在目录的 ../references 或 ./references（源码形态/相对安装）
_BUNDLED = Path(__file__).resolve().parent / "references"
_SIBLING = Path(__file__).resolve().parent.parent / "references"


def _resolve_refs_dir() -> Path:
    env_dir = os.environ.get("REG_HUB_REFS")
    if env_dir:
        p = Path(env_dir)
        if p.is_dir():
            return p.resolve()
    for cand in (_BUNDLED, _SIBLING, Path(__file__).resolve().parent):
        if (cand / "README.md").is_file() or any(cand.glob("*.md")):
            return cand.resolve()
    return _BUNDLED.resolve()


REFS_DIR = _resolve_refs_dir()

SERVER_NAME = "medxpert-reg-connector"
SERVER_VERSION = "1.0.0"
SERVER_DESC = (
    "全球法规连接器：本地只读检索全球医疗器械法规知识库 "
    "(NMPA/FDA/MDR/PMDA 等 27 枢纽 + 骨科实证)，返回片段、官方链接与待核验标注。"
)

mcp = FastMCP(SERVER_NAME, version=SERVER_VERSION, instructions=SERVER_DESC)

# ---------------------------------------------------------------------------
# 知识库加载
# ---------------------------------------------------------------------------
HUB_FILES = {}  # hub_key -> {"title": str, "path": Path, "content": str, "sections": {section_title: text}, "links": [str]}


def _extract_title(content: str, filename: str) -> str:
    """从 # 标题或文件名提取枢纽名"""
    m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return filename.replace(".md", "")


def _split_sections(content: str) -> list:
    """按 ## / ### 标题切分为小节，返回 [(title, body)]"""
    sections = []
    lines = content.splitlines()
    cur_title = "(前言)"
    cur_body = []
    for ln in lines:
        if re.match(r"^#{2,4}\s+", ln):
            if cur_body or cur_title != "(前言)":
                sections.append((cur_title, "\n".join(cur_body).strip()))
            cur_title = re.sub(r"^#{2,4}\s+", "", ln).strip()
            cur_body = []
        else:
            cur_body.append(ln)
    if cur_body or cur_title != "(前言)":
        sections.append((cur_title, "\n".join(cur_body).strip()))
    return [s for s in sections if s[1]]


def _extract_links(content: str) -> list:
    """提取 md 中的 http(s) 链接"""
    return re.findall(r"https?://[^\s\)\]\>\"']+", content)


def load_hubs() -> None:
    if not REFS_DIR.is_dir():
        raise RuntimeError(f"知识库目录不存在: {REFS_DIR}，请设置 REG_HUB_REFS 指向含 .md 的知识库目录")
    for p in sorted(REFS_DIR.glob("*.md")):
        if p.name == "README.md":
            continue
        try:
            content = p.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            content = p.read_text(encoding="gb18030", errors="replace")
        HUB_FILES[p.stem] = {
            "title": _extract_title(content, p.name),
            "path": p,
            "content": content,
            "sections": _split_sections(content),
            "links": list(dict.fromkeys(_extract_links(content))),  # 去重保序
        }


# ---------------------------------------------------------------------------
# 检索核心：中文友好 BM25 近似（无第三方依赖）
# ---------------------------------------------------------------------------
STOPWORDS = {
    "的", "了", "和", "与", "或", "及", "在", "是", "为", "对", "于", "以",
    "这", "那", "个", "中", "上", "下", "等", "之", "也", "而", "并", "其",
    "a", "an", "the", "to", "of", "and", "or", "in", "on", "for", "with",
}


def _tokenize(text: str) -> list:
    """分词：英文按单词，中文按 2-gram 滑动窗口 + 单字回退"""
    text = text.lower()
    tokens = []
    # 英文/数字单词
    for w in re.findall(r"[a-z0-9][a-z0-9\-\.\']{1,}", text):
        tokens.append(w)
    # 中文连续片段
    for seg in re.findall(r"[\u4e00-\u9fff]{2,}", text):
        if len(seg) <= 4:
            tokens.append(seg)
        else:
            for i in range(len(seg) - 1):
                tokens.append(seg[i : i + 2])
    return [t for t in tokens if t and t not in STOPWORDS and len(t) > 1]


def _build_index():
    """为所有枢纽建立 词->[(hub_key, tf, sec_idx)] 索引"""
    index = {}
    for key, hub in HUB_FILES.items():
        for si, (stitle, sbody) in enumerate(hub["sections"]):
            text = stitle + "\n" + sbody
            for tok in set(_tokenize(text)):
                tf = text.lower().count(tok)
                index.setdefault(tok, []).append((key, si, tf))
    return index


_INDEX = {}


def _ensure_index():
    global _INDEX
    if not _INDEX:
        _INDEX = _build_index()
    return _INDEX


def search(query: str, top_k: int = 5, hub_filter: str = None) -> list:
    """
    返回 [{hub_key, title, section, snippet, score, links}]
    score: 词频加权 + 标题命中加权
    """
    q_tokens = _tokenize(query)
    if not q_tokens:
        return []
    index = _ensure_index()
    scores = {}  # (hub_key, sec_idx) -> score
    for tok in q_tokens:
        for key, si, tf in index.get(tok, []):
            if hub_filter and key != hub_filter:
                continue
            scores[(key, si)] = scores.get((key, si), 0) + (1.0 + 0.5 * tf)
    if not scores:
        return []
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    results = []
    for (key, si), score in ranked:
        hub = HUB_FILES[key]
        stitle, sbody = hub["sections"][si]
        # 摘要：截取 400 字
        snippet = re.sub(r"\s+", " ", sbody).strip()
        if len(snippet) > 400:
            snippet = snippet[:400] + "…"
        results.append(
            {
                "hub_key": key,
                "hub_title": hub["title"],
                "section": stitle,
                "snippet": snippet,
                "score": round(score, 2),
                "links": hub["links"][:8],
            }
        )
    return results


# ---------------------------------------------------------------------------
# MCP 工具
# ---------------------------------------------------------------------------
@mcp.tool()
def list_hubs() -> str:
    """列出法规知识库全部枢纽（主题）及覆盖范围，返回 JSON 数组。"""
    hubs = []
    for key in sorted(HUB_FILES.keys()):
        hub = HUB_FILES[key]
        hubs.append(
            {
                "hub_key": key,
                "title": hub["title"],
                "sections": len(hub["sections"]),
                "official_links": len(hub["links"]),
                "phase": _phase_of(hub["content"]),
            }
        )
    return json.dumps(hubs, ensure_ascii=False, indent=2)


@mcp.tool()
def search_regulation(query: str, top_k: int = 5, hub_filter: str = None) -> str:
    """
    在法规知识库中检索关键词（支持中文/英文/法规号，如 'UDI'、'510k'、'MDR PMS'、'委托生产'）。
    返回命中的枢纽、小节、摘要片段、官方链接与相关度得分。
    """
    if not query or not query.strip():
        return json.dumps({"error": "query 不能为空"}, ensure_ascii=False)
    results = search(query, top_k=top_k, hub_filter=hub_filter)
    if not results:
        return json.dumps(
            {"query": query, "count": 0, "hint": "未命中，可尝试更短关键词或切换市场缩写（NMPA/FDA/MDR/PMDA）"},
            ensure_ascii=False,
            indent=2,
        )
    return json.dumps({"query": query, "count": len(results), "results": results}, ensure_ascii=False, indent=2)


@mcp.tool()
def get_hub(hub_key: str) -> str:
    """按 hub_key 取某一枢纽的完整整理内容（含全部小节与官方链接）。先调用 list_hubs 查看可用 hub_key。"""
    hub = HUB_FILES.get(hub_key)
    if not hub:
        keys = list(HUB_FILES.keys())
        return json.dumps(
            {"error": f"未找到枢纽 {hub_key}，可用: {keys[:10]} ...（共 {len(keys)} 个）"},
            ensure_ascii=False,
        )
    return json.dumps(
        {
            "hub_key": hub_key,
            "title": hub["title"],
            "content": hub["content"],
            "official_links": hub["links"],
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def ask_classification(product: str) -> str:
    """
    产品分类与注册路径速查：输入产品描述（如 '骨科金属接骨板'、'一次性使用输液器'），
    返回相关枢纽、分类线索、官方链接与注册路径建议。
    """
    if not product or not product.strip():
        return json.dumps({"error": "product 不能为空"}, ensure_ascii=False)
    results = search(product, top_k=4)
    # 附上骨科实证与分类相关枢纽
    priority_keys = [
        "骨科手术器械_全球注册路径汇编",
        "注册工程师资料枢纽",
        "注册周期费用有效期对比枢纽",
        "市场准入与销售枢纽",
        "注册检验与申报实操枢纽",
    ]
    related = []
    for key in priority_keys:
        if key in HUB_FILES:
            related.append({"hub_key": key, "title": HUB_FILES[key]["title"]})
    return json.dumps(
        {
            "product": product,
            "matches": results,
            "recommended_hubs": related,
            "hint": "分类建议需以目标市场官方分类库为准（NMPA 分类目录 / FDA 产品分类库 / MDR 分类规则），以上仅为知识库线索。",
        },
        ensure_ascii=False,
        indent=2,
    )


def _phase_of(content: str) -> str:
    """粗判枢纽归属的生命周期阶段（用于列表展示）"""
    phase_map = [
        ("立项", "立项与可行性"),
        ("分类", "分类与路径"),
        ("技术文件", "技术文件"),
        ("质量体系", "质量体系"),
        ("注册检验", "注册申报"),
        ("审评", "审评获批"),
        ("上市后", "上市后监管"),
    ]
    for kw, phase in phase_map:
        if kw in content[:800]:
            return phase
    return "综合"


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------
def main() -> None:
    try:
        load_hubs()
    except RuntimeError as e:
        print(f"[reg-connector] FATAL: {e}", file=sys.stderr)
        sys.exit(1)
    n = len(HUB_FILES)
    print(f"[reg-connector] v{SERVER_VERSION} 已加载 {n} 份枢纽资料 from {REFS_DIR}", file=sys.stderr)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
