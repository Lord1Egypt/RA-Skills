"""
M5/M6/M7 简报生成流水线（Pipeline 编排）。

一次生成流程：
  采集(M2) → 清洗(M3) → 去重+相关性(M4) → 聚类 → 逐篇摘要 → 板块洞察 → 综述
  → 渲染 Markdown(M7) → 写库 + 归档文件

设计取舍：
  * 「先规则过滤、后进 LLM」——先用关键词给所有条目打分排序，只对 Top-K 抓正文并摘要，
    显著降低抓取量与 token 成本（对应风险对策表）。
  * 聚类采用轻量贪心算法（token 集合 Jaccard），无需 sklearn。
"""
from __future__ import annotations

import json
import logging
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any, Dict, List

import collector
import dedup as dedup_mod
import relevance
import cleaner
import store
import summarizer
from config import (
    BRIEF_DIR, CLUSTER_THRESHOLD, CURATED_PICKS, CUSTOM_MAX_PER_SUB,
    MAX_SECTIONS, TOP_K_ARTICLES,
)
from sources import all_source_meta, default_sources

log = logging.getLogger("industryradar.generator")


def _resolve_sources(sub: Dict) -> List[Dict]:
    """订阅里可携带 sources_json（源 id 列表）；为空则用默认源目录。

    自定义源以 `cs:<id>` 表示，只解析**属于该订阅用户**且已启用的条目，
    并限制单订阅可用的自定义源数量（CUSTOM_MAX_PER_SUB）。
    """
    try:
        ids = json.loads(sub.get("sources_json") or "[]")
    except Exception:  # noqa: BLE001
        ids = []
    if not ids:
        return default_sources()
    metas = {s["id"]: s for s in all_source_meta()}
    picked: List[Dict] = [dict(metas[i]) for i in ids if i in metas]

    custom_ids: List[int] = []
    for sid in ids:
        if isinstance(sid, str) and sid.startswith("cs:"):
            try:
                custom_ids.append(int(sid[3:]))
            except ValueError:
                continue
    if custom_ids and sub.get("user_id"):
        by_id = {s["id"]: s for s in store.list_custom_sources(int(sub["user_id"]))}
        for cid in custom_ids[:CUSTOM_MAX_PER_SUB]:
            c = by_id.get(cid)
            if not c or not c.get("enabled"):
                continue
            picked.append({
                "id": f"cs:{cid}",
                "name": c["name"],
                "url": c["url"],
                "category": "自定义",
                "enabled": True,
                "_strict_xml": True,
                "_custom_id": cid,
            })
    return picked or default_sources()


def _keywords(sub: Dict) -> List[str]:
    return (relevance.parse_keywords(sub.get("industry_kw", ""))
            + relevance.parse_keywords(sub.get("tech_kw", ""))
            + relevance.parse_keywords(sub.get("extra_kw", "")))


def _primary_keyword(art: Dict) -> str:
    """选出文章的主关键词（命中次数最多者；并列时按声明顺序取首个）。"""
    hits = art.get("keyword_hits") or {}
    if not hits:
        return ""
    return max(hits, key=lambda k: hits[k])


def _cluster(articles: List[Dict], threshold: float = CLUSTER_THRESHOLD
             ) -> List[tuple]:
    """主题聚类：按「主关键词」分桶，未命中任何关键词的条目用 token Jaccard 归并。

    * 每篇文章归入「命中次数最多的那个关键词」对应的板块（如 芯片 / 算力 / 大模型），
      直接对齐用户关注的「行业词 × 技术词」，板块标题清晰、与业务语义一致。
    * 不做关键词集合求并（避免传递式大合并），也不依赖长文本 Jaccard（避免碎片化）。
    * 板块数量超过 MAX_SECTIONS 时，把较小板块合并为「其他动态」。

    返回 [(板块标题, [文章, ...]), ...]，板块标题即主关键词（或「综合动态/其他动态」），
    保证标题与业务语义一致、稳定可复现。
    """
    buckets: "OrderedDict[str, List[Dict]]" = OrderedDict()
    others: List[Dict] = []

    for art in articles:
        pk = _primary_keyword(art)
        if pk:
            buckets.setdefault(pk, []).append(art)
        else:
            others.append(art)

    # 未命中关键词的条目：用 token Jaccard 合并进已有板块或自成一组
    if others:
        cluster_tokens = {pk: set() for pk in buckets}
        for pk, items in buckets.items():
            for a in items:
                cluster_tokens[pk] |= set(dedup_mod.tokenize(f"{a.get('title','')} {a.get('content','')[:800]}"))
        for art in others:
            toks = set(dedup_mod.tokenize(f"{art.get('title','')} {art.get('content','')[:800]}"))
            best, best_sim = None, 0.0
            for pk, ct in cluster_tokens.items():
                inter = len(toks & ct)
                union = len(toks | ct) or 1
                sim = inter / union
                if sim > best_sim:
                    best, best_sim = pk, sim
            if best and best_sim >= threshold:
                buckets[best].append(art)
                cluster_tokens[best] |= toks
            else:
                buckets.setdefault("综合动态", []).append(art)

    # 按板块条目数降序；超出上限的合并为「其他动态」
    ordered = sorted(buckets.items(), key=lambda kv: len(kv[1]), reverse=True)
    if len(ordered) > MAX_SECTIONS:
        head = ordered[:MAX_SECTIONS - 1]
        tail_items: List[Dict] = []
        for _, items in ordered[MAX_SECTIONS - 1:]:
            tail_items.extend(items)
        result = list(head)
        if tail_items:
            result.append(("其他动态", tail_items))
        return result
    return ordered


def _render_markdown(sub: Dict, period_start: str, period_end: str,
                     overall: str, sections: List[Dict],
                     stats: Dict, sources_used: List[str]) -> str:
    lines = [
        f"# {sub.get('name', '行业技术简报')}",
        "",
        f"> **统计周期**：{period_start} ~ {period_end}　|　"
        f"**关注领域**：{sub.get('industry_kw','')} × {sub.get('tech_kw','')}",
        f"> **生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}　|　"
        f"**有效信息**：{stats.get('total_articles', 0)} 条　|　"
        f"**主题板块**：{len(sections)} 个",
        "",
        "---",
        "",
        "## 一、本周综述",
        "",
        overall,
        "",
        "---",
        "",
        "## 二、主题板块",
        "",
    ]
    for i, s in enumerate(sections, 1):
        lines.append(f"### {i}. {s['cluster_title']}")
        lines.append("")
        lines.append(s["content"])
        lines.append("")
        for a in s["articles"]:
            src = a.get("source_name", "")
            pub = (a.get("published_at") or "")[:10]
            lines.append(f"- [{a.get('title','')}]({a.get('url','')})"
                         + (f" — {src}" if src else "")
                         + (f" · {pub}" if pub else ""))
        lines.append("")
    lines += [
        "---",
        "",
        "## 三、信息源与说明",
        "",
        f"- 本期使用信息源：{('、'.join(sources_used)) or '默认源'}",
        "- 所有内容均来自公开渠道，摘要与洞察基于原文生成，**每条信息附原文链接可溯源**。",
        "- 本简报由「智汇简报 IndustryRadar」自动生成，仅供参考，不构成投资建议。",
        "",
    ]
    return "\n".join(lines)


def _render_curated_markdown(sub: Dict, period_start: str, period_end: str,
                             intro: str, picks: List[Dict], curated: List[Dict],
                             closing: Dict, stats: Dict,
                             sources_used: List[str]) -> str:
    """编辑精选式周报渲染（style=curated）：
    开场白 → N 篇精选（定位/核心/启发/星级+适合谁/原文链接）
    → 三条结论 → 只读两篇推荐。
    """
    lines = [
        f"# {sub.get('name', '编辑精选')}",
        "",
        f"> **统计周期**：{period_start} ~ {period_end}　|　"
        f"**关注领域**：{sub.get('industry_kw','')} × {sub.get('tech_kw','')}",
        f"> **生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}　|　"
        f"**候选池**：{stats.get('pool_size', len(picks))} 条　|　"
        f"**本期精选**：{len(picks)} 篇",
        "",
        "---",
        "",
        "## 编辑开场白",
        "",
        intro,
        "",
        "---",
        "",
        "## 本期精选",
        "",
    ]
    for i, (a, c) in enumerate(zip(picks, curated), 1):
        src = a.get("source_name", "")
        pub = (a.get("published_at") or "")[:10]
        meta = " · ".join(x for x in [src, pub] if x)
        lines += [
            f"### {i}. {a.get('title','')}",
            "",
        ]
        if meta:
            lines += [f"*{meta}*", ""]
        lines += [
            f"**为什么上榜**：{c['hook']}",
            "",
            f"**核心内容**：{c['core']}",
            "",
            f"**实际启发**：{c['insight']}",
            "",
            f"**值不值得读全文**：{c['stars']} —— {c['verdict']}",
            "",
            f"[查看原文]({a.get('url','')})",
            "",
            "---",
            "",
        ]
    lines += ["## 本周最值得带走的三条结论", ""]
    for j, t in enumerate(closing.get("takeaways") or [], 1):
        lines.append(f"{j}. {t}")
    lines += ["", "## 如果只读两篇", ""]
    top2 = closing.get("top2") or []
    if top2:
        url_by_title = {a.get("title", ""): a.get("url", "") for a in picks}
        for t in top2:
            title = t.get("title", "")
            url = url_by_title.get(title, "")
            link = f"[{title}]({url})" if url else title
            lines.append(f"- {link} —— {t.get('reason', '')}")
    lines += [
        "",
        "---",
        "",
        "## 信息源与说明",
        "",
        f"- 本期使用信息源：{('、'.join(sources_used)) or '默认源'}",
        "- 星级为编辑综合评估（★ 必读 / ☆ 可略），仅代表本期内的相对优先级。",
        "- 所有内容均来自公开渠道，点评基于原文生成，**每条信息附原文链接可溯源**。",
        "- 本简报由「智汇简报 IndustryRadar」自动生成，仅供参考，不构成投资建议。",
        "",
    ]
    return "\n".join(lines)


def run_pipeline(sub: Dict, save: bool = True) -> Dict[str, Any]:
    """
    对单个订阅执行一次完整生成。返回 {briefing_id, title, markdown, stats}。
    """
    sub_id = sub["id"]
    kws = _keywords(sub)
    industry = relevance.parse_keywords(sub.get("industry_kw", ""))
    tech = relevance.parse_keywords(sub.get("tech_kw", ""))
    extra = relevance.parse_keywords(sub.get("extra_kw", ""))

    period_end = datetime.now().strftime("%Y-%m-%d")
    period_start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    stats: Dict[str, Any] = {}

    # ---- M2 采集
    srcs = _resolve_sources(sub)
    raw = collector.collect(srcs)
    sources_used = sorted({s.get("name", "") for s in srcs if s.get("enabled", True)})
    stats["collected"] = len(raw)

    # ---- M3 轻量清洗（先用 RSS 自带文本，正文延后抓）
    for it in raw:
        it["url_hash"] = cleaner.url_hash(it.get("url", ""))
        # RSS 自带内容含 HTML 标签 / 反爬页乱码，先过一遍清洗
        it["content"] = cleaner.clean_text(it.get("raw_content", "") or "")
        it["score"] = 0.0

    # ---- M4-a 去重
    existing = store.existing_url_hashes(sub_id)
    existing_fps = [dedup_mod.simhash_text(f"{a['title']}") for a in store.recent_articles(sub_id)]
    arts = dedup_mod.deduplicate(raw, existing, existing_fps)
    stats["after_dedup"] = len(arts)

    # ---- M4-b 相关性排序（规则，零成本）
    arts = relevance.filter_relevant(arts, industry, tech, extra)
    stats["relevant"] = len(arts)

    # ---- 取 Top-K，抓正文
    arts = arts[:TOP_K_ARTICLES]
    for it in arts:
        full = cleaner.fetch_fulltext(it.get("url", ""))
        if full:
            it["content"] = full
    stats["top_k"] = len(arts)
    stats["total_articles"] = len(arts)

    if not arts:
        md = (f"# {sub.get('name','行业技术简报')}\n\n"
              f"> {period_start} ~ {period_end}\n\n"
              "本期未采集到与关键词匹配的有效信息。请检查信息源可达性或调整关键词。\n")
        if save:
            path = _save_file(sub, period_end, md)
            bid = store.create_briefing(sub_id, f"{sub.get('name','')} · 周报（{period_end}）",
                                        period_start, period_end, path, "empty", stats)
            store.update_subscription_last_run(sub_id)
            return {"briefing_id": bid, "title": sub.get("name", ""), "markdown": md, "stats": stats}
        return {"briefing_id": None, "title": sub.get("name", ""), "markdown": md, "stats": stats}

    # ---- M5/M6/M7 摘要与渲染（按订阅风格分流）
    style = (sub.get("style") or "standard").lower()
    sections: List[Dict] = []

    if style == "curated":
        # ===== 编辑精选模式：Top-N 高信号条目逐篇点评 =====
        pool_size = len(arts)
        # 日报/快讯拼盘不进精选榜单（正文杂、关键词多为顺带提及）；
        # 池内全是拼盘时才兜底放行，避免空刊。
        non_digest = [a for a in arts if not relevance.is_digest(a)]
        picks = ((non_digest or arts)[:CURATED_PICKS]) or arts[:1]
        pool_best = max((float(a.get("score") or 0) for a in picks), default=0.0)
        if pool_best <= 0:
            pool_best = 1.0
        curated: List[Dict] = []
        used_tpls: set = set()  # 同一期共享模板槽位，保证 hook/insight 句式不雷同
        for idx, a in enumerate(picks):
            a["summary"] = summarizer.summarize_article(a, kws)
            c = summarizer.curate_article(a, kws, pool_best, index=idx,
                                          used_tpls=used_tpls)
            c["stars"] = summarizer._stars(c["rating"])
            curated.append(c)
        intro = summarizer.curated_intro(sub, picks, pool_size)
        closing = summarizer.curated_closing(picks, sub)
        stats["pool_size"] = pool_size
        stats["curated_picks"] = len(picks)
        stats["sections"] = len(picks)
        for i, (a, c) in enumerate(zip(picks, curated)):
            sections.append({
                "cluster_title": (a.get("title", "") or "精选条目")[:30],
                "content": (f"{c['hook']}\n\n{c['core']}\n\n{c['insight']}\n\n"
                            f"值不值得读全文：{c['stars']} —— {c['verdict']}"),
                "articles": [a],
                "article_ids": [],     # 落库后回填
                "sort_no": i,
            })
        md = _render_curated_markdown(sub, period_start, period_end,
                                      intro, picks, curated, closing,
                                      stats, sources_used)
        arts = picks          # 精选模式只落库精选条目
    else:
        # ===== 标准模式：聚类 → 板块洞察 → 综述 =====
        grouped = _cluster(arts)
        sort_no = 0
        for label, group in grouped:
            for a in group:
                a["summary"] = summarizer.summarize_article(a, kws)
            # 板块标题直接用主关键词（对齐业务语义）；无关键词时才回退到归纳标题
            title = label or summarizer.cluster_title(group, kws)
            content = summarizer.section_insight(title, group, kws)
            sections.append({
                "cluster_title": title,
                "content": content,
                "articles": group,
                "article_ids": [],     # 落库后回填
                "sort_no": sort_no,
            })
            sort_no += 1

        # ---- M6 综述
        overall = summarizer.overall_insight(sub, sections, len(arts))
        stats["sections"] = len(sections)

        # ---- M7 渲染
        md = _render_markdown(sub, period_start, period_end, overall, sections, stats, sources_used)

    if not save:
        return {"briefing_id": None, "title": sub.get("name", ""), "markdown": md, "stats": stats}

    # ---- 落库
    # 先建立「文章对象 -> 板块序号」映射，用于回填 article.cluster_id
    section_no_of: Dict[int, int] = {}
    for s in sections:
        for a in s["articles"]:
            section_no_of[id(a)] = s["sort_no"]

    article_rows = [{
        "subscription_id": sub_id,
        "title": a.get("title", ""),
        "url": a.get("url", ""),
        "url_hash": a.get("url_hash", ""),
        "source_name": a.get("source_name", ""),
        "published_at": a.get("published_at", ""),
        "content": (a.get("content", "") or "")[:6000],
        "summary": a.get("summary", ""),
        "score": a.get("score", 0.0),
        "cluster_id": section_no_of.get(id(a), -1),
        "created_at": store.now(),
    } for a in arts]
    # insert_articles 返回与入参顺序一致的自增主键，据此回填各板块的 article_ids
    inserted_ids = store.insert_articles(article_rows)
    id_by_obj = {id(a): aid for a, aid in zip(arts, inserted_ids)}
    for s in sections:
        s["article_ids"] = [id_by_obj[id(a)] for a in s["articles"] if id(a) in id_by_obj]

    path = _save_file(sub, period_end, md)
    bid = store.create_briefing(sub_id, f"{sub.get('name','')} · 周报（{period_end}）",
                                period_start, period_end, path, "done", stats)
    for s in sections:
        store.add_section(bid, s["cluster_title"], s["content"], s["article_ids"], s["sort_no"])
    store.update_subscription_last_run(sub_id)

    # ---- M8 推送（站内默认记录；SMN 邮件在云端启用）
    store.add_push_log(bid, "inbox", sub.get("user_id", ""), "delivered")

    log.info("pipeline done sub=%s briefing=%s articles=%d", sub_id, bid, len(arts))
    return {"briefing_id": bid, "title": sub.get("name", ""), "markdown": md, "stats": stats}


def _save_file(sub: Dict, period_end: str, md: str) -> str:
    fname = f"sub{sub['id']}_{period_end}_{datetime.now().strftime('%H%M%S')}.md"
    path = BRIEF_DIR / fname
    path.write_text(md, encoding="utf-8")
    return str(path)