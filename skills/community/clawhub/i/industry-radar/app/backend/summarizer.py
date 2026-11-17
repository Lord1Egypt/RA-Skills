"""
M5/M6 摘要与洞察生成。

两级策略（关键设计，保证「任何环境都能跑通」）：
  * 在线：调用 OpenAI 兼容的大模型接口（华为云 ModelArts Studio / 盘古 / 任意兼容网关），
    采用「基于原文、必须引用」的 Prompt，抑制幻觉。
  * 离线降级：未配置 LLM 时，使用抽取式摘要 + 规则聚类标题 + 统计洞察，
    功能不中断（免费、零成本），只是文本不如大模型自然。

所有对外函数都保证「永不抛异常」，返回可用的字符串。
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, List, Optional

import requests

from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, LLM_TIMEOUT, USE_LLM

log = logging.getLogger("industryradar.summarizer")

_SENT_SPLIT = re.compile(r"(?<=[。！？!?\.])\s*")


# ------------------------------------------------------------------ LLM
def _chat(messages: List[Dict], temperature: float = 0.3, max_tokens: int = 800) -> str:
    """调用 OpenAI 兼容 chat/completions 接口。失败返回空串。"""
    if not USE_LLM:
        return ""
    url = f"{LLM_BASE_URL}/chat/completions"
    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=LLM_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        return (data["choices"][0]["message"]["content"] or "").strip()
    except Exception as exc:  # noqa: BLE001
        log.warning("LLM call failed: %s", exc)
        return ""


# ---------------------------------------------------------------- 抽取式
def _split_sentences(text: str) -> List[str]:
    # 折叠句内换行（RSS 正文常把一句话拆成多行，渲染后会出现孤立引号/断句）
    parts = [re.sub(r"[\r\n]+", "", s).strip()
             for s in _SENT_SPLIT.split(text or "")]
    return [p for p in parts if len(p) > 8]


def _sent_fingerprint(s: str) -> str:
    """句子指纹：去掉空白与标点后取前 40 字，用于识别重复句。"""
    return re.sub(r"[\s，。；：、！？‘’“”（）()《》【】\[\]—·,.;:!?\-]", "", s)[:40]


def _is_dup_fingerprint(fp: str, seen: List[str]) -> bool:
    """前缀包含判定：RSS 复读段常带微小尾巴（如标题行后接日期），
    精确匹配漏检，故只要两个指纹互为前缀即视为重复。"""
    return any(fp.startswith(s) or s.startswith(fp) for s in seen)


# 图源/题图等图片括注，抽取正文时剔除（RSS 摘要常夹带）
_CAPTION_RE = re.compile(r"[（(](?:图源|图片来源|题图|封面图?|配图)[^）)]{0,40}[）)]")


def extractive_summary(text: str, keywords: List[str], max_sentences: int = 3,
                       title: str = "") -> str:
    """无 LLM 时的抽取式摘要：按关键词密度 + 位置给句子打分，取前 N 句。

    带指纹去重：同一文本内重复出现的句子（源 RSS 复读段、summary 与
    正文拼接导致的重复）只保留首次出现；传入 title 时，与标题相同/
    互为前缀的复读句也跳过（标题已在条目头部展示，摘要不再复读）。
    """
    text = _CAPTION_RE.sub("", text or "")
    sents = _split_sentences(text)
    if not sents:
        return (text or "")[:180]
    title_fp = _sent_fingerprint(title) if title else ""
    scored = []
    seen: List[str] = []
    for i, s in enumerate(sents[:80]):
        fp = _sent_fingerprint(s)
        if not fp or _is_dup_fingerprint(fp, seen):
            continue
        if title_fp and len(title_fp) >= 8 and _is_dup_fingerprint(fp, [title_fp]):
            continue
        seen.append(fp)
        hits = sum(s.count(k) for k in keywords) if keywords else 0
        pos_bonus = max(0, 3 - i) * 0.5      # 靠前的句子略加权
        length_penalty = -abs(len(s) - 60) / 120.0
        scored.append((hits + pos_bonus + length_penalty, i, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = sorted(scored[:max_sentences], key=lambda x: x[1])
    return "".join(s for _, _, s in top)[:400]


# ---------------------------------------------------------------- 对外 API
def summarize_article(art: Dict, keywords: List[str]) -> str:
    """单篇摘要。优先 LLM，降级抽取式。"""
    title = art.get("title", "")
    body = (art.get("content", "") or "")[:3000]
    if USE_LLM:
        prompt = (
            "你是行业情报编辑。请基于下面这篇原文写一句 60~100 字的中文摘要，"
            "只陈述原文事实，不得编造数据或结论。直接输出摘要，不要任何前缀。\n\n"
            f"标题：{title}\n正文：{body}"
        )
        out = _chat([{"role": "user", "content": prompt}], max_tokens=200)
        if out:
            return out.replace("\n", " ").strip()[:300]
    return extractive_summary(f"{title}。{body}", keywords)


def section_insight(cluster_title: str, articles: List[Dict], keywords: List[str]) -> str:
    """板块洞察（趋势/事件/观点）。优先 LLM，降级规则归纳。"""
    snippets = []
    for a in articles[:6]:
        snippets.append(f"- {a.get('title','')}（{a.get('source_name','')}）：{a.get('summary','')[:120]}")
    block = "\n".join(snippets)

    if USE_LLM:
        prompt = (
            "你是行业分析师，正在撰写《行业技术简报》的一个板块。"
            f"板块主题：{cluster_title}。关注关键词：{'、'.join(keywords)}。\n"
            "请基于以下素材，写 2~3 句中文洞察，总结这组信息反映的趋势或关键事件。"
            "只依据素材，不得编造；如信息不足就点到为止。直接输出正文。\n\n"
            f"素材：\n{block}"
        )
        out = _chat([{"role": "user", "content": prompt}], max_tokens=400)
        if out:
            return out.strip()

    # 规则归纳
    srcs = sorted({a.get("source_name", "") for a in articles if a.get("source_name")})
    titles = "；".join(a.get("title", "") for a in articles[:3])
    return (
        f"本周共收录 {len(articles)} 条与「{cluster_title}」相关的信息，"
        f"来源包括 {('、'.join(srcs)) or '多渠道'}。"
        f"主要动态：{titles}。"
        f"建议持续跟踪该方向的关键词：{'、'.join(keywords[:4])}。"
    )


def overall_insight(sub: Dict, sections: List[Dict], total: int) -> str:
    """整份简报的综述。优先 LLM，降级统计式。"""
    ind, tech = sub.get("industry_kw", ""), sub.get("tech_kw", "")
    if USE_LLM:
        outline = "\n".join(f"- {s['cluster_title']}（{len(s['article_ids'])} 条）" for s in sections)
        prompt = (
            f"你在为《{sub.get('name','')}》周报写一段 3~4 句的总体综述。"
            f"关注领域：{ind} × {tech}。本周共采集 {total} 条有效信息，分板块如下：\n{outline}\n"
            "请概括本周整体态势，只依据给定信息，不得编造。直接输出正文。"
        )
        out = _chat([{"role": "user", "content": prompt}], max_tokens=400)
        if out:
            return out.strip()
    return (
        f"本期聚焦「{ind} × {tech}」，共筛选 {total} 条有效信息，"
        f"划分为 {len(sections)} 个主题板块。整体信息量稳定，"
        f"建议重点关注与「{tech or ind}」直接相关的技术与市场动态。"
    )


def cluster_title(articles: List[Dict], keywords: List[str]) -> str:
    """为一个聚类生成中文标题。优先 LLM，降级用高频关键词拼接。"""
    titles = " | ".join(a.get("title", "") for a in articles[:5])
    if USE_LLM:
        prompt = (
            "下面是同一主题的多条新闻标题，请给出一个 6~14 个字的中文板块标题，"
            "只输出标题本身。\n\n" + titles
        )
        out = _chat([{"role": "user", "content": prompt}], max_tokens=60)
        if out:
            return out.replace("\n", " ").strip().strip("《》")[:20]

    freq: Dict[str, int] = {}
    for kw in keywords:
        c = titles.count(kw)
        if c:
            freq[kw] = c
    top = sorted(freq, key=freq.get, reverse=True)[:2]
    if top:
        return "·".join(top) + " 动态"
    return (articles[0].get("title", "综合动态") if articles else "综合动态")[:16]


# ================================================================== 编辑精选模式（curated）
# 模板源自用户提供的两期示例刊物，结构固定为：
#   编辑开场白（筛选标准 + 本期数量）→ N 篇精选条目
#   （定位判断 hook / 核心内容 core / 实际启发 insight / 星级 + 适合谁 verdict）
#   → 本周三条结论 → 只读两篇推荐。
# 双路径：LLM 编辑人格提示词优先；未配置 LLM 时按规则合成，保证任何环境可跑通。

def _stars(rating: float) -> str:
    """把 1~5 的评分渲染成 ★★★★☆ 形式（半星粒度）。"""
    rating = max(1.0, min(5.0, round(rating * 2) / 2))
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    return "★" * full + "☆" * (half + (5 - full - half))


def _parse_json(text: str) -> Optional[dict]:
    """宽容解析 LLM 输出的 JSON（剥掉 ``` fence、截取首尾花括号）。"""
    if not text:
        return None
    t = text.strip()
    if t.startswith("```"):
        t = t.strip("`")
        if t.lower().startswith("json"):
            t = t[4:]
    i, j = t.find("{"), t.rfind("}")
    if i < 0 or j <= i:
        return None
    try:
        data = json.loads(t[i:j + 1])
    except Exception:
        return None
    # LLM 受外部文章内容影响，可能返回列表/标量等合法但结构不符的 JSON
    return data if isinstance(data, dict) else None


def _rule_rating(art: Dict, pool_best: float) -> float:
    """离线星级：按相关性得分在候选池内的相对位置映射 3~5 星。"""
    s = float(art.get("score") or 0)
    if pool_best <= 0:
        return 3.5
    rel = s / pool_best
    if rel >= 0.95:
        return 5.0
    if rel >= 0.85:
        return 4.5
    if rel >= 0.70:
        return 4.0
    if rel >= 0.50:
        return 3.5
    return 3.0


def curate_article(art: Dict, keywords: List[str], pool_best: float = 1.0,
                   index: int = 0, used_tpls: Optional[set] = None) -> Dict[str, Any]:
    """单篇精选条目：hook（一句话定位）/ core（核心内容）/
    insight（实际启发）/ rating + verdict（星级与适合谁读）。

    LLM 路径用「资深技术主编」人格产出；离线路径用规则合成，保证格式一致。
    used_tpls：跨条目共享的「已用模板槽位」集合（("hook", 档, 槽) / ("insight", 槽)），
    实现贪心占位——撞槽自动顺延到下一个空槽，保证 5 篇条目句式不雷同。
    """
    if used_tpls is None:
        used_tpls = set()

    def _pick_slot(kind: str, n: int, seed: int, sub: str = "") -> int:
        """按种子选槽；被占用则顺延到下一个空槽（环内最多走一圈）。
        sub 用于区分同一 kind 下的独立模板池（如 hook 的 4 个档位）。
        """
        slot = seed % n
        for _ in range(n):
            key = (kind, sub, slot)
            if key not in used_tpls:
                used_tpls.add(key)
                return slot
            slot = (slot + 1) % n
        return seed % n  # 全满兜底：仅当同档条目数 > 槽数时发生
    title = art.get("title") or "（无标题）"
    body = (art.get("content") or art.get("summary") or "")[:3000]
    result = None
    if USE_LLM:
        prompt = (
            "你是一位资深技术周刊主编，为智能硬件 / AR / AI 产品团队写内部周报。"
            "风格：第一人称、有观点、只留高信号内容，反对堆砌 benchmark。\n"
            "请基于下面这篇文章，为「编辑精选式周报」写一个条目，严格只输出 JSON：\n"
            '{"hook": "1~2句定位判断：价值在哪、为什么上榜（编辑口吻，可点名对产品架构/端侧部署/交互实现的意义）",\n'
            ' "core": "2~4句核心内容：做了什么、关键数字或结论",\n'
            ' "insight": "1~3句实际启发：给工程/产品团队的可操作建议，可用 A → B → C 链路表达",\n'
            ' "rating": 4.5,\n'
            ' "verdict": "一句话说明适合谁读"}\n'
            f"订阅关键词：{'、'.join(keywords)}\n"
            f"标题：{title}\n"
            f"来源：{art.get('source_name')}｜日期：{art.get('published_at')}｜相关性得分：{art.get('score')}\n"
            f"正文：{body}"
        )
        out = _chat([{"role": "user", "content": prompt}], max_tokens=900)
        result = _parse_json(out)
    if result and all(result.get(k) for k in ("hook", "core", "insight")):
        try:
            rating = float(result.get("rating") or 4)
        except (TypeError, ValueError):
            rating = _rule_rating(art, pool_best)
        return {
            "hook": str(result["hook"]).strip(),
            "core": str(result["core"]).strip(),
            "insight": str(result["insight"]).strip(),
            "rating": max(1.0, min(5.0, rating)),
            "verdict": str(result.get("verdict") or "值得快速过一遍。").strip(),
        }

    # ---------- 规则式降级：保证无 LLM 环境格式完全一致 ----------
    summ = art.get("summary") or ""
    body_text = (summ + "\n" + body).strip()
    # 核心内容：按关键词密度抽取最优句；传 title 过滤「标题复读句」
    core = (extractive_summary(body_text, keywords, max_sentences=3, title=title)
            or summ[:200] or "正文抽取受限，关键细节建议跳转原文确认。")

    kws = sorted(keywords, key=lambda k: -((body.count(k) + title.count(k))))
    focus = kws[0] if kws else "该方向"
    rating = _rule_rating(art, pool_best)
    score = float(art.get("score") or 0)

    # hook：按本期排位分档 + 同档多句式轮换（标题哈希+排位决定取哪条），避免逐篇雷同
    src_name = art.get("source_name") or "该来源"
    hook_tpls: List[List[str]] = [
        # 档 1：本期最高相关
        [f"本期「{focus}」主线相关度最高的一篇，建议最优先处理。",
         f"如果只给一件事排优先级，就先看这篇——「{focus}」方向信号最强、信息密度也最高。",
         f"「{focus}」方向本周的头号信号，来自 {src_name}，值得放在阅读队列最前面。",
         f"整期围绕「{focus}」的讨论基本绕不开这一篇，先读它能给其余条目定基调。"],
        # 档 2：高信号
        [f"直接命中「{focus}」主线，且信息量足够支撑一次选型或跟进判断。",
         f"对「{focus}」产品路线有直接影响的一篇，读完基本能形成自己的判断。",
         f"{src_name} 这篇把「{focus}」的关键进展讲得比较实，适合纳入本周决策材料。",
         f"「{focus}」方向的强信号，关键结论可以直接引用到内部讨论里。"],
        # 档 3：有效信号
        [f"「{focus}」方向的有效信号，与本期其他条目对照阅读价值更高。",
         f"不是最急的一篇，但补上了「{focus}」拼图里的一块，建议对照高星条目一起看。",
         f"作为「{focus}」动态的旁证收录，与同方向条目交叉验证后结论更稳。",
         f"「{focus}」方向的增量信息，单看平平，拼进全景后价值会放大。"],
        # 档 4：背景补充
        [f"作为「{focus}」方向的背景补充保留，不占用主要精力。",
         f"轻度相关，主要价值在于提供「{focus}」方向的行业语境。",
         f"时间有限的话这篇可以最后看，但它能帮你理解「{focus}」周边的生态动向。",
         f"收录它更多是为了完整呈现「{focus}」的讨论氛围，本身不必精读。"],
    ]
    tier = (0 if (pool_best > 0 and score >= pool_best) else
            1 if rating >= 4.5 else
            2 if rating >= 3.5 else 3)
    tpls = hook_tpls[tier]
    hook = tpls[_pick_slot("hook", len(tpls), sum(map(ord, title)) + index,
                         sub=f"t{tier}")]

    # insight：确定性轮换模板（标题哈希+排位 + 跨条目贪心占位），8 句式保 5 篇不撞
    insight_tpls = [
        f"建议纳入「{focus}」跟进清单：先判断它影响的是架构选型还是单点能力，再决定是否投入验证。",
        f"值得在下次评审中同步给团队：重点评估它对「{focus}」产品路线与端侧部署约束的实际影响。",
        f"可与其他来源交叉验证后沉淀进知识库；若与现有方案冲突，优先核对时效与适用边界再下结论。",
        f"更适合当作决策输入而非结论：放进「{focus}」的季度规划讨论里，看它是否改变既有取舍。",
        f"如果正在做相关 PoC，这篇里的取舍可以直接对照自查；暂时没做的话，留意它的落地时间表即可。",
        f"对前端/端侧团队的意义大于算法团队：交互链路与状态设计可以先按它的方向做预案。",
        f"短期不必跟，但值得设一个复查点：等它出现规模化落地案例再重新评估投入。",
        f"读的时候带着自己的架构图对照，标出哪些模块会被它影响，这比单纯记结论更有用。",
    ]
    insight = insight_tpls[_pick_slot("insight", len(insight_tpls),
                                      sum(map(ord, title)) + index)]
    if rating >= 4.5:
        verdict = "本期高信号，建议精读。"
    elif rating >= 3.5:
        verdict = "值得快速过一遍，按需深入。"
    else:
        verdict = "时间紧张时读摘要即可。"
    return {"hook": hook, "core": core, "insight": insight,
            "rating": rating, "verdict": verdict}


def curated_intro(sub: Dict, picked: List[Dict], pool_size: int) -> str:
    """编辑开场白：交代筛选标准（信号 vs 噪音）与本期精选数量。"""
    industry = (sub.get("industry_kw") or "").split(",")[0] or "目标行业"
    tech = (sub.get("tech_kw") or "").split(",")[0] or "关键技术"
    if USE_LLM:
        titles = "；".join(a["title"] for a in picked[:5])
        prompt = (
            "你是一位资深技术周刊主编，正在写本周刊物的开场白，第一人称、克制、有观点。\n"
            f"本周订阅主题是「{industry} × {tech}」，候选池共 {pool_size} 篇，"
            f"你精选了 {len(picked)} 篇高信号内容。\n"
            "请写 2~3 句开场白：先交代筛选标准（看重对产品架构/端侧部署/交互实现的实际价值，"
            "不堆纯 benchmark 和公关稿），再报出本期精选数量。直接输出正文，不要列表。\n"
            f"入选文章标题：{titles}"
        )
        out = _chat([{"role": "user", "content": prompt}], max_tokens=300)
        if out:
            return out.strip()
    # 规则式降级
    dropped = max(pool_size - len(picked), 0)
    return (
        f"本周围绕「{industry} × {tech}」共筛掉候选池中 {dropped} 篇低信号内容，"
        f"最终留下 {len(picked)} 篇。筛选标准很直接：优先保留对产品架构、端侧部署和交互实现"
        f"有实际参考价值的内容，纯发布稿与重复消息一律不收。每篇都给出定位判断、实际启发"
        f"和星级评价——值不值得读全文，看完条目就能决定。"
    )


def _as_text_list(value: Any, limit: int) -> List[str]:
    """把 LLM 字段收敛成字符串列表；非列表、或元素不是标量的项一律丢弃。"""
    if not isinstance(value, (list, tuple)):
        return []
    out: List[str] = []
    for item in value:
        if isinstance(item, bool) or not isinstance(item, (str, int, float)):
            continue
        text = str(item).strip()
        if text:
            out.append(text)
        if len(out) >= limit:
            break
    return out


def _as_top2(value: Any, limit: int = 2) -> List[Dict[str, str]]:
    """把 LLM 的 top2 收敛成 [{title, reason}]；非字典元素或 title 非字符串则丢弃。"""
    if not isinstance(value, (list, tuple)):
        return []
    out: List[Dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        title = item.get("title")
        if not isinstance(title, str) or not title.strip():
            continue
        reason = item.get("reason")
        out.append({
            "title": title.strip(),
            "reason": reason.strip() if isinstance(reason, str) else "",
        })
        if len(out) >= limit:
            break
    return out


def curated_closing(picked: List[Dict], sub: Dict) -> Dict[str, Any]:
    """收尾三件套：本周三条结论（takeaways）+ 只读两篇推荐（top2）。

    LLM 返回内容来自外部文章上下文，结构不可信：这里做严格类型收敛，
    并整体兜在 try/except 内，任何异常都回落规则合成，绝不中断简报生成。
    """
    industry = (sub.get("industry_kw") or "").split(",")[0] or "目标行业"
    tech = (sub.get("tech_kw") or "").split(",")[0] or "关键技术"
    takeaways: List[str] = []
    top2: List[Dict] = []
    if USE_LLM:
        lines = "\n".join(
            f"{i}. {a['title']}（{a.get('source_name')}）：{(a.get('summary') or '')[:150]}"
            for i, a in enumerate(picked, 1)
        )
        prompt = (
            "你是一位资深技术周刊主编，基于本周精选文章写收尾。严格只输出 JSON。\n"
            '{"takeaways": ["结论1", "结论2", "结论3"],\n'
            ' "top2": [{"title": "照抄原文标题", "reason": "为什么最优先读"}]}\n'
            "要求：takeaways 是 3 条跨文章的趋势判断（每条 1~2 句，编辑口吻，讲方向不讲细节）；"
            f"top2 是「如果只读两篇」的优先顺序，从下面文章里选，title 必须照抄原文标题。\n"
            f"本周主题：{industry} × {tech}\n{lines}"
        )
        try:
            out = _chat([{"role": "user", "content": prompt}], max_tokens=700)
            data = _parse_json(out)
            if isinstance(data, dict):
                takeaways = _as_text_list(data.get("takeaways"), 3)
                top2 = _as_top2(data.get("top2"))
        except Exception as exc:  # 结构异常/网络异常都走规则降级
            log.warning("curated_closing LLM 结果不可用，回落规则合成: %s", exc)
            takeaways, top2 = [], []
    # 数量不足视为「不可用」而不是「部分可用」：整体回落规则合成，
    # 保证版式固定为 3 条结论 + 2 篇推荐。
    if len(takeaways) < 3:
        takeaways = []
    if len(top2) < 2:
        top2 = []
    if not takeaways:
        # 规则式降级：按关键词命中频次合成三条结论
        kw_count: Dict[str, int] = {}
        all_kw = [k.strip() for k in (sub.get("tech_kw") or "").split(",")]
        all_kw += [k.strip() for k in (sub.get("industry_kw") or "").split(",")]
        for a in picked:
            text = (a.get("title") or "") + (a.get("summary") or "")
            for k in all_kw:
                if k and k in text:
                    kw_count[k] = kw_count.get(k, 0) + 1
        hot = sorted(kw_count, key=kw_count.get, reverse=True)
        srcs = sorted({a.get("source_name") or "来源" for a in picked})
        if hot:
            takeaways.append(
                f"「{hot[0]}」是本周讨论的最大公约数——{len(picked)} 篇精选中 "
                f"{kw_count[hot[0]]} 篇同时命中，建议列为下期跟踪主线。"
            )
        else:
            takeaways.append(f"本周 {industry} × {tech} 的讨论集中于产品侧动态，技术侧一手结果有限。")
        takeaways.append(
            f"信息源分布（{'、'.join(srcs[:3])}）显示该主题仍以行业媒体驱动，"
            f"学术与工程一手内容建议补充订阅源。"
        )
        if len(hot) > 1:
            takeaways.append(
                f"「{hot[1]}」在多篇精选中反复出现，建议纳入下一轮选型评估，避免单点信息误导。"
            )
        else:
            takeaways.append(
                f"整体判断：{tech} 当前处于产品化落地期，关注交付与生态信号多于论文信号。"
            )
    if not top2:
        ranked = sorted(
            picked,
            key=lambda a: (float(a.get("score") or 0), len(a.get("summary") or "")),
            reverse=True,
        )
        for rank, a in enumerate(ranked[:2], 1):
            sc = float(a.get("score") or 0)
            if rank == 1:
                reason = (f"本期相关度与信息量综合排名第一（得分 {sc:.2f}），"
                          f"适合作为理解本周主题的第一入口。")
            else:
                reason = (f"综合排名第二（得分 {sc:.2f}），与第一篇互为补充，"
                          f"时间有限时可只读其条目点评。")
            top2.append({"title": a.get("title") or "", "reason": reason})
    return {"takeaways": takeaways, "top2": top2}

