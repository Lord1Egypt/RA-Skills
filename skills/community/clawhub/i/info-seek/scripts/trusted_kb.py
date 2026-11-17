#!/usr/bin/env python3
"""
trusted_kb.py — Infoseek 可信资源知识库模块

功能：
  - kb_lookup(topic, limit=5)  : 按主题查询KB，返回匹配源
  - kb_merge(web_results, kb_hits): 合并web+KB结果，KB源享credibility提升
  - kb_add(entry)              : 自动沉淀新源（高分已验证源）
  - kb_fallback(topic, limit=5): web search无结果时KB兜底返回

数据文件：references/trusted-sources.json
"""

import json, os, re, logging
from typing import Optional

log = logging.getLogger(__name__)

# KB 文件路径（相对于 skill 根目录）
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_PATH = os.path.join(SKILL_DIR, "references", "trusted-sources.json")


def _load_kb() -> dict:
    """加载知识库"""
    if not os.path.exists(KB_PATH):
        log.warning(f"KB文件不存在: {KB_PATH}")
        return {"version": "2.0.0", "schema": "dual-segment(v2.0)", "white_list": [], "kb_sources": []}
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_kb(kb: dict) -> bool:
    """写回知识库"""
    try:
        with open(KB_PATH, "w", encoding="utf-8") as f:
            json.dump(kb, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        log.error(f"KB写入失败: {e}")
        return False


def kb_lookup(topic: str, limit: int = 5) -> list:
    """
    按主题查询KB，返回匹配源。

    匹配逻辑：
    - 将 topic 拆分为关键词
    - 任一关键词出现在 source.topics 中 → 命中
    - 按匹配关键词数量排序
    """
    if not topic:
        return []

    # 提取关键词（中文/英文词）
    keywords = set()
    for token in re.split(r'[\s,，、/]', topic):
        token = token.strip()
        if len(token) >= 2:  # 至少2个字符
            keywords.add(token.lower())

    kb = _load_kb()
    matches = []
    for src in kb.get("kb_sources", []) + kb.get("white_list", []):
        src_topics = [t.lower() for t in src.get("topics", [])]
        matched_kws = [kw for kw in keywords if any(kw in st or st in kw for st in src_topics)]
        if matched_kws:
            matches.append({
                "domain": src["domain"],
                "name": src["name"],
                "score": src["credibility"],
                "topics": src.get("topics", []),
                "type": src.get("type", ""),
                "entry": f"https://{src['domain']}",
                "entry_type": "URL",
                "_from_kb": True,
                "_credibility_base": src["credibility"],
                "_match_count": len(matched_kws),
            })

    # 按匹配度和可信度排序
    matches.sort(key=lambda x: (x["_match_count"], x["_credibility_base"]), reverse=True)
    return matches[:limit]


def kb_fallback(topic: str, limit: int = 5) -> list:
    """
    兜底查询 — web search无/少结果时调用

    与 kb_lookup 相同逻辑，但返回结果标注 `_is_fallback: True`
    便于下游流程区分优先级
    """
    results = kb_lookup(topic, limit)
    for r in results:
        r["_is_fallback"] = True
    return results


# 域种子词：域感知扩展查询（kb_enrich 用，与 domain_router 5 域体系对齐）
KB_DOMAIN_SEEDS = {
    "tech-research": ["工艺", "材料", "技术", "软件", "代码", "算法", "芯片", "硬件", "制造", "标准"],
    "market-research": ["市场", "行业", "规模", "消费", "需求", "报告", "用户", "数据"],
    "finance-research": ["股票", "基金", "债券", "期货", "行情", "估值", "上市公司", "证券"],
    "policy-research": ["政策", "法规", "标准", "监管", "政府", "条例"],
    "competitor-intel": ["企业", "公司", "工商", "竞品", "股东", "融资", "股权"],
}


def kb_enrich(query: str, domain: Optional[str] = None, limit: int = 8,
              prefer_kb: bool = False) -> list:
    """
    域感知扩展查询：单主题命中不足时，用域种子词横向扩展检索面。

    - domain 可显式传入（如 detect_domain 判定结果）；缺省时自动尝试判定
    - 返回 kb_lookup 同构结果（含 _kb_domain 标注），按可信度降序
    - 自动判定失败 / domain 无种子词 → 返回 []（非致命）
    """
    try:
        from domain_router import detect_domain
    except ImportError:
        return []
    if not domain:
        det = detect_domain(query)
        if not det or not det.get("domain"):
            return []
        domain = det["domain"]
    seeds = KB_DOMAIN_SEEDS.get(domain)
    if not seeds:
        return []
    hits, seen, hit_counts = [], set(), {}
    for kw in seeds:
        for r in kb_lookup(kw, limit=limit):
            entry = r.get("entry", "")
            hit_counts[entry] = hit_counts.get(entry, 0) + 1
            if entry in seen:
                continue
            seen.add(entry)
            r["_kb_domain"] = domain
            hits.append(r)
    # G3/G4 (v1.7.2)：注入多 KB 命中数，供 prefer_kb 分段（单 KB +8 / 多 KB 额外 +4
    # 合计 +12，与 domain_router.kb_intersect_bonus 口径一致 · v1.8.3 勘误）实际触发
    for r in hits:
        r["_kb_hit_count"] = hit_counts.get(r.get("entry", ""), 1)
    # prefer_kb（交集场景）：排序键叠加交集加分 → KB 源上浮
    if prefer_kb:
        try:
            from domain_router import kb_intersect_bonus
            hits.sort(key=lambda x: x.get("_credibility_base", 0) + kb_intersect_bonus(x),
                      reverse=True)
        except ImportError:
            hits.sort(key=lambda x: x.get("_credibility_base", 0), reverse=True)
    else:
        hits.sort(key=lambda x: x.get("_credibility_base", 0), reverse=True)
    return hits[:limit]


def kb_merge(web_results: list, kb_hits: list, prefer_kb: bool = False) -> list:
    """
    合并web搜索结果与KB命中结果。

    规则：
    1. KB源享 credibility 加成：默认 +5；prefer_kb（多域交集场景）时改为分段
       （单 KB +8 / 多 KB +12，与 domain_router.kb_intersect_bonus 对齐）
    2. 去重：domain 相同则合并，取高评分
    3. KB源排在同等分 web 源之前
    """
    # 去重映射
    domain_map = {}

    # 先处理 web 结果
    for r in web_results:
        domain = _extract_domain(r.get("entry", ""))
        r["_domain"] = domain
        domain_map[domain] = r

    # 处理 KB 结果
    for r in kb_hits:
        domain = _extract_domain(r.get("entry", ""))
        r["_domain"] = domain
        # KB源 credibility 加成：默认 +5；prefer_kb 交集场景按分段（+8 / +12）
        _boost = 5
        if prefer_kb:
            try:
                from domain_router import kb_intersect_bonus
                _boost = max(_boost, kb_intersect_bonus(r))
            except ImportError:
                pass
        cred_boost = r.get("_credibility_base", 80) + _boost
        r["_kb_boosted"] = True
        r["_original_score"] = r.get("score", 0)

        if domain in domain_map:
            # 已存在，取较高分
            existing = domain_map[domain]
            if cred_boost > existing.get("score", 0):
                existing["score"] = cred_boost
                existing["_from_kb"] = True
        else:
            # 新源，设置增强后的分数
            r["score"] = cred_boost
            domain_map[domain] = r

    return list(domain_map.values())


def kb_add(
    domain: str,
    name: str,
    topics: list,
    credibility: int,
    source_type: str = "",
    verified: bool = False,
) -> bool:
    """
    自动沉淀新源到KB。

    门控条件（防止噪声入库）：
    - credibility ≥ 75（至少专业媒体级别）
    - domain 不重复
    - topics 非空
    """
    if credibility < 75 or not domain or not topics:
        log.info(f"KB沉淀门控未通过: credibility={credibility} domain={domain}")
        return False

    kb = _load_kb()
    existing = [s for s in (kb.get("kb_sources", []) + kb.get("white_list", [])) if s.get("domain") == domain]
    if existing:
        log.info(f"KB已存在: {domain}")
        return False

    entry = {
        "domain": domain,
        "name": name,
        "domain_key": "general",
        "topics": topics[:8],  # 最多保留8个主题词
        "credibility": credibility,
        "type": source_type or "web",
        "access": "web",
        "verified": verified,
        "tier": 2 if credibility >= 85 else 3,
        "weight": 20 if credibility >= 85 else 13,
        "patterns": [],
    }
    kb.setdefault("kb_sources", []).append(entry)
    ok = _save_kb(kb)
    if ok:
        log.info(f"KB新增源: {domain} ({credibility}分)")
    return ok


def _extract_domain(url: str) -> str:
    """从URL提取域名"""
    if not url:
        return ""
    m = re.search(r"https?://([^/]+)", url)
    return m.group(1) if m else ""


# 快速测试
if __name__ == "__main__":
    print("=== KB 查询测试 ===")
    for q in ["碳纤维 预浸料", "PCB 焊接 失效", "工程机械", "标准 GB"]:
        hits = kb_lookup(q, limit=3)
        print(f"\n查询: {q}")
        for h in hits:
            print(f"  [{h['_credibility_base']}分] {h['name']} ({h['domain']}) 匹配{h['_match_count']}词")
