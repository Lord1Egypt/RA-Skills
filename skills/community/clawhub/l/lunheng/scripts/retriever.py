"""
pipeline/retriever.py — 检索模块
从 pipeline.py 拆分而来 (2026-07-18)
职责：案情要素 → 并行检索 (入库案例/法律法规/优秀文书)
"""

import json
import os
import re
import sys
import time
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from error_utils import retry_with_backoff, log_error, log_warning, log_info

# ─── 路径 ───────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data" / "shape_spirit"
REFS_DIR = SKILL_DIR / "refs"

sys.path.insert(0, str(SKILL_DIR))
from shape_spirit_index import ShapeSpiritIndex, CAUSE_MAP
from style_retriever import retrieve_style_examples, format_for_prompt

# ─── Ref 文档加载 ──────────────────────────────────────
def _load_ref(name: str) -> str:
    ref_path = REFS_DIR / name
    if ref_path.exists():
        return ref_path.read_text(encoding="utf-8")
    return ""


def _load_cause_refs(cause: str) -> str:
    """根据案由加载对应的知识库参考文档"""
    CAUSE_REF_MAP = {
        "民间借贷": "kb_laws.md", "买卖合同": "kb_laws.md",
        "租赁合同": "kb_laws.md", "建设工程": "kb_laws.md",
        "劳动合同": "kb_laws.md", "交通事故": "kb_laws.md",
        "侵权责任": "kb_laws.md", "离婚": "kb_laws.md",
        "物业服务": "kb_laws.md", "医疗损害": "kb_laws.md",
        "著作权": "kb_laws.md", "专利权": "kb_laws.md",
        "商标权": "kb_laws.md", "公司决议": "kb_laws.md",
        "行政处罚": "kb_laws.md", "保险": "kb_laws.md",
        "不当得利": "kb_laws.md", "保证合同": "kb_laws.md",
    }
    parts = []
    for key, ref_name in CAUSE_REF_MAP.items():
        if key in cause:
            content = _load_ref(ref_name)
            if content:
                parts.append(f"## 法律法规参考\n{content[:3000]}")
            break
    writing_ref = _load_ref("kb_writing.md")
    if writing_ref:
        parts.append(f"## 写作范式参考\n{writing_ref[:2000]}")
    return "\n\n".join(parts)


def _load_retrieval_refs(elements) -> str:
    """加载检索阶段的参考文档"""
    parts = []
    cases_ref = _load_ref("kb_cases.md")
    if cases_ref:
        parts.append(f"## 入库案例检索指南\n{cases_ref[:2000]}")
    formatting_ref = _load_ref("kb_formatting.md")
    if formatting_ref:
        parts.append(f"## 格式规范\n{formatting_ref[:1500]}")
    return "\n\n".join(parts)


# ─── IMA 凭证（从统一配置模块导入，可选）───────────
from config import IMA_API_KEY, IMA_CLIENT_ID

# IMA 知识库 ID（用户自行配置）
KB_CASES = os.environ.get("LH_KB_CASES", "")
KB_LEGAL = os.environ.get("LH_KB_LEGAL", "")
KB_GOOD_WRITING = None


# ─── 数据结构 ──────────────────────────────────────────
@dataclass
class RetrievalResult:
    """检索结果"""
    source: str = ""
    title: str = ""
    content: str = ""
    relevance: float = 0.0
    metadata: dict = field(default_factory=dict)


# ─── IMA API 调用 ──────────────────────────────────────
@retry_with_backoff(max_retries=2, base_delay=0.5, max_delay=3.0)
def ima_search(query: str, kb_id: str, limit: int = 5) -> list:
    """搜索 IMA 知识库（含自动重试）"""
    if not IMA_CLIENT_ID or not IMA_API_KEY:
        log_warning("retriever", "ima_search", "IMA 凭证未配置，跳过检索")
        return [{"error": "IMA 凭证未配置"}]

    body = json.dumps({
        "query": query,
        "knowledge_base_id": kb_id,
        "cursor": "",
        "limit": limit
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://ima.qq.com/openapi/wiki/v1/search_knowledge",
        data=body,
        headers={
            "ima-openapi-clientid": IMA_CLIENT_ID,
            "ima-openapi-apikey": IMA_API_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        if data.get("code") == 220021:
            log_warning("retriever", "ima_search", "IMA API 日限额已用完")
            return [{"error": "IMA API 日限额已用完"}]
        return data.get("data", {}).get("info_list", [])
    except urllib.error.URLError as e:
        log_error("retriever", "ima_search", e, {"query": query[:30], "kb_id": kb_id[:10]})
        return [{"error": f"网络错误: {e}"}]
    except Exception as e:
        log_error("retriever", "ima_search", e, {"query": query[:30]})
        return [{"error": str(e)}]


def _filter_case_results(items: list, cause_type: str = "civil") -> list:
    """过滤入库案例结果"""
    filtered = []
    for item in items:
        if "error" in item:
            continue
        title = item.get("title", "")
        if cause_type in ("civil", "commercial") and "检例" in title:
            continue
        filtered.append(item)
    return filtered


# ─── 查询构造 ──────────────────────────────────────────
def _build_search_queries(elements) -> list:
    """构造入库案例检索词"""
    queries = []
    if elements.cause:
        queries.append(elements.cause)
    if elements.cause and elements.disputes:
        for d in elements.disputes[:2]:
            clean = re.sub(r'(?:双方|原被告|对|就|存在|有|争议|分歧|异议)', '', d)[:20]
            if clean.strip():
                queries.append(f"{elements.cause} {clean.strip()}")
    if elements.cause and elements.legal_issues:
        queries.append(f"{elements.cause} {elements.legal_issues[0]}")
    return queries[:4]


def _build_law_queries(elements) -> list:
    """构造法律法规检索词"""
    queries = []
    laws = elements.applicable_laws
    if laws:
        queries.append(laws[0])
    if elements.legal_issues:
        base = laws[0] if laws else "民法典"
        queries.append(f"{base} {elements.legal_issues[0]}")
    return queries[:2]


# ─── 主检索函数 ────────────────────────────────────────
def retrieve_all(elements) -> dict:
    """
    并行检索三个数据源:
    1. 入库案例(IMA 知识库)
    2. 法律法规(IMA 知识库)
    3. 优秀文书范式(形与神本地数据)
    """
    results = {
        "入库案例": [],
        "法律法规": [],
        "优秀文书": [],
    }

    # 判断案件大类
    cause_type = "civil"
    for vol, causes in CAUSE_MAP.items():
        for category, keywords in causes.items():
            if any(kw in elements.cause for kw in keywords):
                cause_type = vol
                break

    # ── 1. 检索入库案例 ──
    print("🔍 检索入库案例...", file=sys.stderr)
    search_queries = _build_search_queries(elements)
    seen_titles = set()
    for q in search_queries[:3]:
        items = ima_search(q, KB_CASES, limit=5)
        items = _filter_case_results(items, cause_type)
        for item in items:
            title = item.get("title", "")
            if title and title not in seen_titles:
                seen_titles.add(title)
                results["入库案例"].append(RetrievalResult(
                    source="入库案例",
                    title=title,
                    content=item.get("highlight_content", ""),
                    metadata={"media_id": item.get("media_id", "")},
                ))
        time.sleep(0.3)

    # ── 2. 检索法律法规 ──
    print("🔍 检索法律法规...", file=sys.stderr)
    law_queries = _build_law_queries(elements)
    seen_laws = set()
    for q in law_queries[:2]:
        items = ima_search(q, KB_LEGAL, limit=5)
        for item in items:
            title = item.get("title", "")
            if title and title not in seen_laws:
                seen_laws.add(title)
                results["法律法规"].append(RetrievalResult(
                    source="法律法规",
                    title=title,
                    content=item.get("highlight_content", ""),
                    metadata={"media_id": item.get("media_id", "")},
                ))
        time.sleep(0.3)

    # ── 3. 优秀文书范式(本地形与神数据 + style_retriever 增强) ──
    print("🔍 检索优秀文书范式...", file=sys.stderr)
    index = ShapeSpiritIndex()

    # 使用 style_retriever 进行相关性排序检索
    style_keywords = elements.legal_issues[:3] + elements.disputes[:2]
    style_result = retrieve_style_examples(elements.cause, style_keywords, top_k=3)

    # 将 style_retriever 结果转为 RetrievalResult 格式
    for ex in style_result.top_examples:
        content_parts = []
        if ex.get("writing_experience"):
            content_parts.append("撰写心得: " + ex["writing_experience"][:400])
        if ex.get("expert_analysis"):
            content_parts.append("专家评析: " + ex["expert_analysis"][:300])
        results["优秀文书"].append(RetrievalResult(
            source="优秀文书",
            title=ex.get("title", ""),
            content="\n".join(content_parts)[:500],
            metadata={
                "volume": ex.get("volume", ""),
                "keywords": ex.get("keywords", []),
                "relevance_score": ex.get("relevance_score", 0),
                "brief_facts": ex.get("brief_facts", "")[:200],
            },
        ))

    # 补充：如果 style_retriever 结果不足，用传统 ShapeSpiritIndex 补充
    if len(results["优秀文书"]) < 2:
        local_cases = index.search_by_cause(elements.cause)
        for lc in local_cases[:3]:
            try:
                case_num = int(lc["num"])
            except (ValueError, TypeError):
                case_num = lc["num"]
            case_data = index.get_case_summary(lc["volume"], case_num)
            if case_data:
                results["优秀文书"].append(RetrievalResult(
                    source="优秀文书",
                    title=case_data.get("title", ""),
                    content=case_data.get("writing_experience", "")[:500],
                    metadata={
                        "volume": lc["volume"],
                        "num": lc["num"],
                        "keywords": case_data.get("keywords", []),
                        "brief_facts": case_data.get("brief_facts", "")[:200],
                    },
                ))

    # 附加：说理结构范式和常见扣分项（存入 metadata 供 assembler 使用）
    if style_result.writing_patterns or style_result.common_pitfalls:
        results["优秀文书"].append(RetrievalResult(
            source="优秀文书",
            title="写作风格指南",
            content=format_for_prompt(style_result, max_chars=1500),
            metadata={
                "is_style_guide": True,
                "writing_patterns": style_result.writing_patterns,
                "common_pitfalls": style_result.common_pitfalls,
                "representative_judges": style_result.representative_judges,
            },
        ))

    # ── 4. 加载参考文档 ──
    print("📚 加载参考文档...", file=sys.stderr)
    ref_content = _load_retrieval_refs(elements)
    if ref_content:
        results["参考文档"] = [RetrievalResult(
            source="参考文档",
            title="知识库参考文档",
            content=ref_content,
        )]
    cause_ref_content = _load_cause_refs(elements.cause)
    if cause_ref_content:
        results["领域知识"] = [RetrievalResult(
            source="领域知识",
            title=f"{elements.cause}领域参考",
            content=cause_ref_content,
        )]

    total = sum(len(v) for v in results.values())
    print(f"📊 检索完成: 入库案例 {len(results['入库案例'])} | "
          f"法律法规 {len(results['法律法规'])} | "
          f"优秀文书 {len(results['优秀文书'])} | "
          f"参考文档 {len(results.get('参考文档', []))} | "
          f"领域知识 {len(results.get('领域知识', []))} | "
          f"总计 {total}", file=sys.stderr)

    return results
