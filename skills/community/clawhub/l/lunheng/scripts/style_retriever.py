#!/usr/bin/env python3
"""
style_retriever.py — 优秀文书范式检索器

根据案由和关键词，从 210 篇《形与神》获奖文书 + 700+ 篇百篇优秀文书中
检索最相关的说理范式，作为 few-shot 示例注入 LLM prompt。

用法：
    from style_retriever import retrieve_style_examples
    examples = retrieve_style_examples("民间借贷纠纷", ["借贷合意", "利息计算"])
"""

import json
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

# ─── 路径配置 ─────────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent
SHAPE_SPIRIT_DIR = SKILL_DIR / "data" / "shape_spirit"
AWARD_DOCS_DIR = SKILL_DIR / "data" / "award_docs"

VOLUMES = ["civil", "commercial", "criminal", "administrative"]

# ─── 案由→卷册映射 ────────────────────────────────────
CAUSE_VOLUME_MAP = {
    # 民事
    "民间借贷": "civil", "买卖合同": "civil", "租赁合同": "civil",
    "物业服务": "civil", "劳动争议": "civil", "交通事故": "civil",
    "婚姻家庭": "civil", "继承": "civil", "人格权": "civil",
    "侵权责任": "civil", "环境污染": "civil", "医疗损害": "civil",
    "建设工程": "civil", "房屋买卖": "civil", "相邻关系": "civil",
    # 商事
    "公司": "commercial", "股权": "commercial", "保险": "commercial",
    "票据": "commercial", "证券": "commercial", "破产": "commercial",
    "知识产权": "commercial", "商标": "commercial", "专利": "commercial",
    "著作权": "commercial", "不正当竞争": "commercial",
    # 刑事
    "故意杀人": "criminal", "故意伤害": "criminal", "抢劫": "criminal",
    "盗窃": "criminal", "诈骗": "criminal", "贪污": "criminal",
    "受贿": "criminal", "走私": "criminal", "毒品": "criminal",
    "交通肇事": "criminal", "危险驾驶": "criminal",
    # 行政
    "行政征收": "administrative", "行政许可": "administrative",
    "行政处罚": "administrative", "行政强制": "administrative",
    "政府信息公开": "administrative", "国家赔偿": "administrative",
}


@dataclass
@dataclass
class StyleExample:
    """一个优秀文书范式示例"""
    title: str                          # 案例标题
    keywords: list                      # 关键词
    brief_facts: str                    # 简要案情
    writing_experience: str             # 撰写心得（核心：说理范式）
    expert_analysis: str                # 专家评析
    relevance_score: float = 0.0        # 相关性评分
    source: str = "shape_spirit"        # 数据来源
    volume: str = ""                    # 卷册


@dataclass
class StyleResult:
    """检索结果"""
    cause: str                          # 输入案由
    matched_volume: str                 # 匹配的卷册
    total_candidates: int               # 候选总数
    top_examples: list                  # Top N 示例（StyleExample dict）
    writing_patterns: list              # 提取的说理结构范式
    common_pitfalls: list               # 常见扣分项
    representative_judges: list         # 代表性法官


def _load_shape_spirit(volume: str) -> list[dict]:
    """加载指定卷册的结构化案例数据"""
    path = SHAPE_SPIRIT_DIR / f"{volume}.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("extracted_cases", [])


def _compute_relevance(case: dict, cause: str, keywords: list[str]) -> float:
    """计算案例与查询的相关性评分（0-1）"""
    score = 0.0
    cause_lower = cause.lower()
    
    # 标题匹配（权重 0.3）
    title = case.get("title", "").lower()
    if cause_lower in title:
        score += 0.3
    # 部分关键词匹配
    for kw in keywords[:3]:
        if kw.lower() in title:
            score += 0.05
    
    # 关键词匹配（权重 0.4）
    case_keywords = [k.lower() for k in case.get("keywords", [])]
    matched_kw = 0
    for kw in keywords:
        kw_lower = kw.lower()
        for ck in case_keywords:
            if kw_lower in ck or ck in kw_lower:
                matched_kw += 1
                break
    if keywords:
        score += 0.4 * (matched_kw / len(keywords))
    
    # 案情匹配（权重 0.2）
    brief_facts = case.get("brief_facts", "").lower()
    fact_matches = sum(1 for kw in keywords if kw.lower() in brief_facts)
    if keywords:
        score += 0.2 * (fact_matches / len(keywords))
    
    # 撰写心得存在（权重 0.1）
    if case.get("writing_experience", "").strip():
        score += 0.1
    
    return min(score, 1.0)


def _detect_volume(cause: str) -> str:
    """根据案由自动检测卷册"""
    cause_lower = cause.lower()
    for keyword, volume in CAUSE_VOLUME_MAP.items():
        if keyword in cause_lower:
            return volume
    # 默认搜索所有卷册
    return "all"


def _extract_writing_patterns(examples: list[dict]) -> list[str]:
    """从多个范例中提取共性说理结构"""
    patterns = []
    
    # 常见说理结构关键词
    structure_keywords = [
        "争议焦点", "法律适用", "构成要件", "举证责任",
        "因果关系", "过错认定", "损害赔偿", "量刑情节",
        "合同效力", "违约责任", "程序合法性", "实体审查"
    ]
    
    for ex in examples[:5]:
        writing = ex.get("writing_experience", "")
        for kw in structure_keywords:
            if kw in writing and kw not in patterns:
                patterns.append(kw)
    
    return patterns[:8]  # 最多返回 8 个


def _extract_pitfalls(examples: list[dict]) -> list[str]:
    """从范例中提取常见扣分项"""
    pitfalls = []
    pitfall_keywords = {
        "说理不充分": "说理",
        "事实认定不清": "事实认定",
        "逻辑跳跃": "逻辑",
        "遗漏诉辩意见": "遗漏",
        "法条引用错误": "法条",
        "文字冗余": "冗余",
    }
    
    for ex in examples[:5]:
        analysis = ex.get("expert_analysis", "") + ex.get("writing_experience", "")
        for pitfall, kw in pitfall_keywords.items():
            if kw in analysis and pitfall not in pitfalls:
                pitfalls.append(pitfall)
    
    return pitfalls


def retrieve_style_examples(
    cause: str,
    keywords: list[str] = None,
    top_k: int = 3,
    min_score: float = 0.1,
) -> StyleResult:
    """
    根据案由和关键词检索优秀文书范式。
    
    Args:
        cause: 案由（如"民间借贷纠纷"）
        keywords: 关键词列表（如["借贷合意", "利息计算"]）
        top_k: 返回最相关的前 N 个案例
        min_score: 最低相关性阈值
    
    Returns:
        StyleResult 包含范式示例、说理结构、常见扣分项等
    """
    if keywords is None:
        keywords = []
    
    # 检测目标卷册
    volume = _detect_volume(cause)
    
    # 加载候选案例
    candidates = []
    if volume == "all":
        for v in VOLUMES:
            for case in _load_shape_spirit(v):
                case["_volume"] = v
                candidates.append(case)
    else:
        for case in _load_shape_spirit(volume):
            case["_volume"] = volume
            candidates.append(case)
    
    # 计算相关性并排序
    scored = []
    for case in candidates:
        score = _compute_relevance(case, cause, keywords)
        if score >= min_score:
            scored.append((score, case))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]
    
    # 构建结果
    top_examples = []
    for score, case in top:
        example = StyleExample(
            title=case.get("title", ""),
            keywords=case.get("keywords", []),
            brief_facts=case.get("brief_facts", ""),
            writing_experience=case.get("writing_experience", ""),
            expert_analysis=case.get("expert_analysis", ""),
            relevance_score=round(score, 3),
            source="shape_spirit",
            volume=case.get("_volume", ""),
        )
        top_examples.append(asdict(example))
    
    # 提取共性范式
    writing_patterns = _extract_writing_patterns([c for _, c in top])
    pitfalls = _extract_pitfalls([c for _, c in top])
    
    # 代表性法官（从快速索引提取）
    representative_judges = _get_representative_judges(volume)
    
    return StyleResult(
        cause=cause,
        matched_volume=volume,
        total_candidates=len(candidates),
        top_examples=top_examples,
        writing_patterns=writing_patterns,
        common_pitfalls=pitfalls,
        representative_judges=representative_judges,
    )


def _get_representative_judges(volume: str) -> list[str]:
    """获取该卷册的代表性法官"""
    judge_map = {
        "civil": ["王亦非（浙江）", "费汉定（广东）", "何琼（浙江）", "龚雪林（江西）"],
        "commercial": ["佟姝（最高法）", "王亦非（浙江）", "费汉定（广东）"],
        "criminal": ["魏海（广东）", "仇晓敏（最高法）", "蔡智玉（河南）"],
        "administrative": ["李纬华（最高法）", "马小莉（陕西）", "黄胜敏（海南）"],
    }
    if volume == "all":
        all_judges = []
        for v in VOLUMES:
            all_judges.extend(judge_map.get(v, []))
        return all_judges[:6]
    return judge_map.get(volume, [])


def format_for_prompt(result: StyleResult, max_chars: int = 3000) -> str:
    """
    将检索结果格式化为可注入 LLM prompt 的文本。
    
    控制在 max_chars 字符以内，避免占用过多 context。
    """
    lines = []
    lines.append(f"## 优秀文书范式参考（案由：{result.cause}）")
    lines.append(f"匹配卷册：{result.matched_volume} | 候选案例：{result.total_candidates} 篇")
    lines.append("")
    
    # 说理结构范式
    if result.writing_patterns:
        lines.append("### 推荐说理结构")
        lines.append(" → ".join(result.writing_patterns))
        lines.append("")
    
    # Top 示例
    for i, ex in enumerate(result.top_examples, 1):
        lines.append(f"### 参考案例 {i}：{ex['title']}")
        lines.append(f"相关度：{ex['relevance_score']} | 来源：{ex['source']}")
        lines.append("")
        
        # 撰写心得（核心）
        writing = ex.get("writing_experience", "")
        if writing:
            # 截取关键段落
            if len(writing) > 800:
                writing = writing[:800] + "..."
            lines.append(f"**撰写心得**：{writing}")
            lines.append("")
        
        # 专家评析（精简）
        analysis = ex.get("expert_analysis", "")
        if analysis and len(lines) < max_chars // 50:
            if len(analysis) > 400:
                analysis = analysis[:400] + "..."
            lines.append(f"**专家评析**：{analysis}")
            lines.append("")
    
    # 常见扣分项
    if result.common_pitfalls:
        lines.append("### 应避免的问题")
        for p in result.common_pitfalls:
            lines.append(f"- {p}")
        lines.append("")
    
    # 代表性法官
    if result.representative_judges:
        lines.append(f"**代表性获奖法官**：{'、'.join(result.representative_judges)}")
    
    text = "\n".join(lines)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[...已截断]"
    return text


# ─── CLI 入口 ─────────────────────────────────────────
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 style_retriever.py <案由> [关键词1 关键词2 ...]")
        print("示例: python3 style_retriever.py 民间借贷纠纷 借贷合意 利息计算")
        sys.exit(1)
    
    cause = sys.argv[1]
    keywords = sys.argv[2:] if len(sys.argv) > 2 else []
    
    result = retrieve_style_examples(cause, keywords)
    print(format_for_prompt(result))
