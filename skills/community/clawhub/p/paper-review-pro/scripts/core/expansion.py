"""
Query Expansion 模块（LLM 驱动）

功能：
- 基于 Top-K 论文内容，使用 LLM 生成语义相关的扩展查询词
- 支持 OpenClaw Gateway API 和 Dashscope API
- Fallback 到规则扩展

目标：
- 从 top 论文中提取研究主题/方向/技术术语
- 与原 query 语义相关但角度不同
- 返回结构化扩展词（含置信度评分）
"""

import os
import json
import urllib.request
import re
import argparse

# OpenClaw Gateway 配置
GATEWAY_URL = os.environ.get("OPENCLAW_GATEWAY_URL", "http://localhost:14940")
GATEWAY_TOKEN = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")

# 尝试从 OpenClaw 配置读取 token
if not GATEWAY_TOKEN:
    try:
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                GATEWAY_TOKEN = config.get("gateway", {}).get("auth", {}).get("token", "")
    except Exception:
        pass

# Dashscope 配置（备用）
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
DASHSCOPE_MODEL = os.environ.get("DASHSCOPE_MODEL", "qwen3.5-plus")


def _call_gateway_llm(prompt: str) -> str:
    """
    调用 OpenClaw Gateway API 生成文本
    
    返回生成的文本内容，失败返回 None
    """
    try:
        url = f"{GATEWAY_URL.rstrip('/')}/v1/chat/completions"
        
        payload = {
            "model": "dashscope/qwen3.5-plus",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的学术搜索助手。你的任务是根据用户提供的原始查询和相关论文，生成 3-5 个语义相关的扩展搜索词。扩展词应该是：\n1. 与原查询相关但角度不同\n2. 具体、可搜索的学术术语\n3. 能够发现更多相关文献\n\n只返回扩展词列表，每行一个，格式：扩展词 | 置信度 (0.5-1.0)"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.5,
            "max_tokens": 300
        }
        
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        
        # 如果有 token 则添加认证
        if GATEWAY_TOKEN:
            headers["Authorization"] = f"Bearer {GATEWAY_TOKEN}"
        
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
    except urllib.error.HTTPError as e:
        # 401/403 等认证错误时不打印详细错误（避免干扰）
        if e.code not in [401, 403]:
            print(f"  [Gateway HTTP 错误]: {e.code}")
        return None
    except Exception as e:
        # 其他错误（超时、连接失败等）
        return None


def _call_dashscope_llm(prompt: str) -> str:
    """
    调用 Dashscope API 生成文本（备用方案）
    """
    if not DASHSCOPE_API_KEY:
        return None
    
    try:
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
        payload = {
            "model": DASHSCOPE_MODEL,
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的学术搜索助手。你的任务是根据用户提供的原始查询和相关论文，生成 3-5 个语义相关的扩展搜索词。只返回扩展词列表，每行一个，格式：扩展词 | 置信度 (0.5-1.0)"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            "parameters": {
                "temperature": 0.5,
                "max_tokens": 300
            }
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DASHSCOPE_API_KEY}"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("output", {}).get("text", "")
            
    except Exception as e:
        print(f"  [Dashscope 调用失败]: {e}")
        return None


def _parse_llm_expansions(llm_output: str, original_query: str, max_terms: int) -> list:
    """
    解析 LLM 输出的扩展词
    
    返回：List[dict] [{"term": str, "score": float}]
    """
    if not llm_output:
        return []
    
    expansions = []
    original_lower = original_query.lower()
    seen = set()
    
    lines = llm_output.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 尝试解析 "term | score" 格式
        parts = line.split("|")
        
        if len(parts) >= 2:
            term = parts[0].strip().strip('"').strip("'")
            try:
                score = float(parts[1].strip())
            except ValueError:
                score = 0.75
        else:
            # 只有术语，没有分数
            term = line.strip().strip('"').strip("'").rstrip(",").rstrip(".")
            score = 0.75
        
        # 清理术语
        term = re.sub(r'^[-*•]\s*', '', term)  # 去掉列表符号
        
        # 去重和过滤
        term_lower = term.lower()
        
        # 跳过与原 query 完全相同的
        if term_lower == original_lower:
            continue
        
        # 跳过原 query 的子串
        if term_lower in original_lower or original_lower in term_lower:
            # 但允许更具体的扩展（如 "LLM" -> "large language model"）
            if len(term_lower) < len(original_lower):
                continue
        
        # 跳过已添加的
        if term_lower in seen:
            continue
        
        seen.add(term_lower)
        expansions.append({"term": term, "score": min(1.0, max(0.5, score))})
    
    # 按分数排序并截断
    expansions.sort(key=lambda x: x["score"], reverse=True)
    return expansions[:max_terms]


def _is_meaningful_phrase(phrase: str) -> bool:
    """
    判断短语是否有意义（过滤无意义的标题片段）
    """
    # 常见无意义开头词
    meaningless_starts = [
        "evidence that", "evidence for", "evidence of",
        "causal evidence", "study of", "analysis of",
        "approach to", "method for", "based on",
        "using ", "with ", "from ", "the ", "a ", "an "
    ]
    
    phrase_lower = phrase.lower().strip()
    
    # 检查是否以无意义词开头
    for start in meaningless_starts:
        if phrase_lower.startswith(start):
            return False
    
    # 检查是否包含常见停用词组合
    stop_patterns = [" that ", " which ", " who ", " what "]
    for pattern in stop_patterns:
        if pattern in phrase_lower:
            return False
    
    # 检查长度（至少 2 个词）
    words = phrase_lower.split()
    if len(words) < 2:
        return False
    
    # 检查是否都是短词
    if all(len(w) < 4 for w in words):
        return False
    
    return True


def _fallback_expansions(top_papers: list, original_query: str, max_terms: int) -> list:
    """
    Fallback：基于规则的扩展词生成（增强版）
    
    改进：
    1. 过滤无意义短语
    2. 优先选择技术性术语
    3. 基于原 query 生成更相关的扩展
    """
    if not top_papers:
        return []
    
    expansions = []
    original_lower = original_query.lower()
    seen = set()
    
    # 技术性术语模式（优先匹配）
    tech_patterns = [
        "learning", "editing", "injection", "updating", "adaptation",
        "fine-tuning", "alignment", "optimization", "distillation",
        "reasoning", "representation", "embedding", "transformer"
    ]
    
    # 从论文标题中提取关键词
    for paper in top_papers[:5]:
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        
        # 提取名词短语
        words = re.findall(r'\b[A-Za-z]{3,}\b', title)
        
        # 生成 2-3 词短语
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            phrase_lower = phrase.lower()
            
            # 过滤无意义短语
            if not _is_meaningful_phrase(phrase):
                continue
            
            # 跳过与原 query 重复的
            if phrase_lower in original_lower or original_lower in phrase_lower:
                continue
            
            if phrase_lower in seen:
                continue
            
            # 检查是否包含技术术语（加分）
            has_tech_term = any(term in phrase_lower for term in tech_patterns)
            
            seen.add(phrase_lower)
            expansions.append({
                "term": phrase,
                "score": 0.70 if has_tech_term else 0.60
            })
        
        # 从摘要提取技术术语
        for tech_term in tech_patterns:
            if tech_term in abstract.lower():
                # 生成相关扩展
                related = [
                    f"{original_query.split()[0]} {tech_term}",
                    f"{tech_term} techniques",
                    f"{tech_term} methods"
                ]
                for r in related:
                    if r not in seen and r != original_lower:
                        seen.add(r)
                        expansions.append({"term": r, "score": 0.75})
    
    # 基于原 query 的领域特定扩展
    query_lower = original_query.lower()
    
    if "knowledge" in query_lower:
        domain_expansions = [
            "knowledge injection",
            "knowledge updating",
            "fact editing",
            "parameter-efficient editing",
            "model editing",
            "LLM knowledge modification"
        ]
    elif "editing" in query_lower:
        domain_expansions = [
            "model editing",
            "parameter editing",
            "weight modification",
            "knowledge injection",
            "fact replacement"
        ]
    else:
        domain_expansions = []
    
    for exp in domain_expansions:
        if exp not in seen:
            seen.add(exp)
            expansions.append({"term": exp, "score": 0.80})
    
    # 按分数排序并截断
    expansions.sort(key=lambda x: x["score"], reverse=True)
    return expansions[:max_terms]


def expand_query(top_papers: list, original_query: str, max_terms=5, use_llm: bool = True) -> list:
    """
    LLM-based Query Expansion
    
    参数:
        top_papers: List[dict]，相似度最高论文（用于上下文）
        original_query: str，原始查询
        max_terms: int，最大扩展数量
        use_llm: bool，是否使用 LLM 生成扩展词
    
    返回:
        List[dict]: [{"term": str, "score": float}]
    """
    # 确保 max_terms 是整数（处理可能的 dict 类型）
    if isinstance(max_terms, dict):
        max_terms = 3
    elif not max_terms:
        max_terms = 3
    else:
        max_terms = int(max_terms)
    
    if not top_papers:
        return _fallback_expansions([], original_query, max_terms)
    
    if not use_llm:
        return _fallback_expansions(top_papers, original_query, max_terms)
    
    print(f"  [生成扩展词] 基于 {len(top_papers)} 篇论文...")
    
    # 准备论文上下文
    paper_context = []
    for i, p in enumerate(top_papers, 1):
        title = p.get("title", "Unknown")
        abstract = p.get("abstract", "")[:600]  # 限制长度
        paper_context.append(f"[{i}] {title}\n    摘要：{abstract}...")
    
    context_text = "\n\n".join(paper_context)
    
    # 构建提示词
    prompt = f"""原始查询：{original_query}

相关论文：
{context_text}

请生成 3-5 个与原始查询语义相关但角度不同的扩展搜索词。
扩展词应该是具体的学术术语，能够帮助发现更多相关文献。

输出格式（每行一个）：
扩展词 | 置信度 (0.5-1.0)

示例：
knowledge editing techniques | 0.92
model parameter updating | 0.88
"""
    
    # 尝试调用 LLM
    llm_output = _call_gateway_llm(prompt)
    
    if not llm_output:
        llm_output = _call_dashscope_llm(prompt)
    
    if llm_output:
        print(f"  [LLM 调用成功]，输出长度：{len(llm_output)} 字符")
        expansions = _parse_llm_expansions(llm_output, original_query, max_terms)
        if expansions:
            print(f"  [解析结果] 生成 {len(expansions)} 个扩展词")
            return expansions
        else:
            print("  [解析失败] LLM 输出格式不匹配，使用 Fallback")
    
    # Fallback
    print("  [使用 Fallback 扩展词]")
    return _fallback_expansions(top_papers, original_query, max_terms)

def main():
    argparser = argparse.ArgumentParser(description="独立调用 Query Expansion 模块")
    argparser.add_argument("--query", type=str, required=True, help="原始查询")
    argparser.add_argument("--max_terms", type=int, default=5, help="最大扩展词数量")
    argparser.add_argument("--reference_title", type=str, nargs="*", default=[], help="参考论文标题列表")
    argparser.add_argument("--reference_abstract", type=str, nargs="*", default=[], help="参考论文摘要列表")
    argparser.add_argument("--no-llm", default=False, action="store_true", help="禁用 LLM 功能（使用规则 fallback）")
    args = argparser.parse_args()

    top_papers = []
    for title, abstract in zip(args.reference_title, args.reference_abstract):
        top_papers.append({"title": title, "abstract": abstract})

    expand_result = expand_query(top_papers, args.query, max_terms=args.max_terms, use_llm=not args.no_llm)
    print("\n生成的扩展词：")
    for exp in expand_result:
        print(f"{exp['term']} (score: {exp['score']:.2f})")

if __name__ == "__main__":
    main()