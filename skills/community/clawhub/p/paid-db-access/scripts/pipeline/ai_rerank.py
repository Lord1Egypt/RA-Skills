#!/usr/bin/env python3

"""

ai_rerank.py — AI 直接评判论文相关性 & 质量



核心理念：替代 paper_ranker.py 的 token 重叠评分，由 AI 直接理解论文与

研究主题的关系，给出 relevance/quality/novelty 三维语义评分。



每条请求只包含：研究主题 + 一篇论文的标题/元数据/摘要。

摘要随 API 请求结束即销毁，从不进入主对话上下文。



用法：

  python ai_rerank.py -i enriched.json -o ai_ranked.json -t "AI automated scientific research..."

  python ai_rerank.py -i enriched.json -o ai_ranked.json -t "..." --concurrency 10



评分维度：

  relevance    0-100   与用户研究主题的相关程度（核心输出）

  quality      0-100   论文质量（方法严谨性、论证完整性、venue 级别）

  novelty      0-100   创新程度（方法论/发现的独特性）



输出：在原始 JSON 基础上添加 _ai_scores 字段，按 relevance 降序排列。

"""



import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse

import asyncio

import json

import os

import re

import sys

import time

from pathlib import Path

from typing import Optional



import aiohttp



from utils.pipeline_schema import validate, report, stamp, check_version, PIPELINE_VERSION



import sys, os




# ---------------------------------------------------------------------------

# 配置：API 凭证

# ---------------------------------------------------------------------------



DEFAULT_MODEL = "deepseek-v4-pro"

DEFAULT_BASE_URL = "https://api.deepseek.com"

DEFAULT_MAX_TOKENS = 800

DEFAULT_TEMPERATURE = 0.3

DEFAULT_CONCURRENCY = 8



SYSTEM_PROMPT = """You are an expert academic paper reviewer. Your task is to evaluate the 

relevance, quality, and novelty of a research paper against a given research topic.



Rate each dimension on a 0-100 scale:



- relevance (0-100): How directly does this paper address the stated research topic?

  - 90-100: Core paper directly on the topic

  - 70-89: Strongly related, substantial contribution

  - 50-69: Related but tangential or narrow scope

  - 30-49: Some connection but mostly about something else

  - 0-29: Irrelevant to the topic



- quality (0-100): How rigorous and well-executed is this paper?

  Consider: venue prestige, citation count, methodology soundness, clarity.

  - 90-100: Top venue (Nature/Science/NeurIPS/ICML etc), highly cited

  - 70-89: Good venue, well-cited or clearly strong methodology

  - 50-69: Decent venue, adequate methodology

  - 30-49: Workshop/arXiv, preliminary work

  - 0-29: Clearly flawed or very weak



- novelty (0-100): How innovative is the contribution?

  - 90-100: Paradigm-shifting, opens new field

  - 70-89: Significantly novel approach or finding

  - 50-69: Incremental but non-trivial advance

  - 30-49: Minor variation of existing work

  - 0-29: Replication or trivial extension



Return ONLY a valid JSON object:

{"relevance": <int>, "quality": <int>, "novelty": <int>, "reason": "<1 sentence in English>"}"""





def load_api_config():

    """从 OpenClaw 配置文件或环境变量加载 API 凭证。



    优先级：环境变量 > openclaw.json > 默认值

    """

    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")

    base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("DEEPSEEK_BASE_URL")

    model = os.environ.get("AI_RERANK_MODEL")



    if api_key and base_url:

        return api_key, base_url, model or DEFAULT_MODEL, DEFAULT_MAX_TOKENS



    # 尝试从 openclaw.json 读取

    config_paths = [

        Path.home() / ".openclaw" / "openclaw.json",

        Path.home() / ".openclaw" / "openclaw.json5",

    ]

    for cf in config_paths:

        if cf.exists():

            try:

                with open(cf, "r", encoding="utf-8") as f:

                    config = json.load(f)

            except (json.JSONDecodeError, IOError):

                continue



            providers = config.get("models", {}).get("providers", {})

            # 偏好顺序: deepseek > moonshot > 第一个有 apiKey 的 provider

            preferred = ["custom-api-deepseek-com", "moonshot"]

            for name in preferred:

                p = providers.get(name, {})

                if p.get("apiKey") and p.get("baseUrl"):

                    m = (p.get("models", [{}]) or [{}])[0].get("id", DEFAULT_MODEL)

                    return p["apiKey"], p["baseUrl"], m, DEFAULT_MAX_TOKENS



            # 回退：取任意一个有 key 的 provider

            for name, p in providers.items():

                if p.get("apiKey") and p.get("baseUrl"):

                    m = (p.get("models", [{}]) or [{}])[0].get("id", DEFAULT_MODEL)

                    return p["apiKey"], p["baseUrl"], m, DEFAULT_MAX_TOKENS



    return None, None, DEFAULT_MODEL, DEFAULT_MAX_TOKENS





def _resolve_abstract(paper: dict) -> str:

    """从 _abstract_file 读取摘要（结构化模板 → 提取 Abstract: 之后内容），回退到 inline。"""

    abs_file = paper.get("_abstract_file", "")

    if abs_file and os.path.exists(abs_file):

        try:

            with open(abs_file, "r", encoding="utf-8") as f:

                content = f.read()

            idx = content.find("\nAbstract:\n")

            if idx >= 0:

                return content[idx + len("\nAbstract:\n"):].strip()

            return content.strip()

        except (IOError, UnicodeDecodeError):

            pass

    abstract = paper.get("abstract", "")

    if abstract and abstract != "[已缓存]" and len(abstract) > 20:

        return abstract.strip()

    return ""





# ---------------------------------------------------------------------------

# 构建单篇论文的评分请求

# ---------------------------------------------------------------------------



def build_user_message(topic: str, paper: dict) -> str:

    """构建单篇论文的评分 prompt。"""

    title = paper.get("title", "Unknown")

    authors = paper.get("authors", "Unknown")

    year = paper.get("year", "?")

    venue = paper.get("venue", "Unknown")

    citations = paper.get("citations", "0")

    abstract = _resolve_abstract(paper)  # ← 从文件解析



    if abstract and len(abstract) > 2000:

        abstract = abstract[:2000] + "..."



    parts = [

        f"Research Topic: {topic}",

        "",

        f"Title: {title}",

        f"Authors: {authors}",

        f"Year: {year} | Citations: {citations}",

        f"Venue: {venue}",

    ]

    if abstract and abstract != "[已缓存]":

        parts.extend(["", f"Abstract: {abstract}"])



    return "\n".join(parts)





def build_payload(model: str, topic: str, paper: dict, max_tokens: int) -> dict:

    return {

        "model": model,

        "messages": [

            {"role": "system", "content": SYSTEM_PROMPT},

            {"role": "user", "content": build_user_message(topic, paper)},

        ],

        "max_tokens": max_tokens,

        "temperature": DEFAULT_TEMPERATURE,

    }





def parse_response(text: str) -> dict:

    """从 LLM 响应中提取 JSON。"""

    # 去掉 markdown 代码块包裹

    text = text.strip()

    if text.startswith("```"):

        lines = text.split("\n")

        text = "\n".join(lines[1:]) if len(lines) > 1 else text

        if text.endswith("```"):

            text = text[:-3]

        text = text.strip()



    try:

        result = json.loads(text)

    except json.JSONDecodeError:

        # 尝试提取 JSON 子串

        match = re.search(r'\{[^{}]*"relevance"\s*:\s*\d+[^{}]*\}', text, re.DOTALL)

        if match:

            try:

                result = json.loads(match.group(0))

            except json.JSONDecodeError:

                result = None

        else:

            result = None



    if result is None:

        return {"relevance": 0, "quality": 0, "novelty": 0,

                "reason": f"parse_error"}



    # 确保字段存在

    for key in ("relevance", "quality", "novelty"):

        result.setdefault(key, 0)

    result.setdefault("reason", "")

    return result





# ---------------------------------------------------------------------------

# 并发评分

# ---------------------------------------------------------------------------



async def score_one(session: aiohttp.ClientSession, base_url: str, api_key: str,

                    model: str, topic: str, paper: dict, max_tokens: int,

                    semaphore: asyncio.Semaphore, index: int, total: int) -> dict:

    """对单篇论文评分。"""

    async with semaphore:

        payload = build_payload(model, topic, paper, max_tokens)

        headers = {

            "Authorization": f"Bearer {api_key}",

            "Content-Type": "application/json",

        }

        url = f"{base_url.rstrip('/')}/chat/completions"



        title = paper.get("title", "?")[:60]

        for attempt in range(3):

            try:

                async with session.post(url, json=payload, headers=headers,

                                        timeout=aiohttp.ClientTimeout(total=60)) as resp:

                    if resp.status == 200:

                        data = await resp.json()

                        content = data["choices"][0]["message"]["content"]

                        scores = parse_response(content)

                        print(f"  [{index+1}/{total}] {scores['relevance']:3d}r "

                              f"{scores['quality']:3d}q {scores['novelty']:3d}n  {title}...",

                              file=sys.stderr)

                        return scores

                    elif resp.status == 429:

                        wait = (attempt + 1) * 2

                        print(f"  [{index+1}/{total}] Rate limited, retry in {wait}s...",

                              file=sys.stderr)

                        await asyncio.sleep(wait)

                    else:

                        text = await resp.text()

                        print(f"  [{index+1}/{total}] HTTP {resp.status}",

                              file=sys.stderr)

                        await asyncio.sleep(1)

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:

                print(f"  [{index+1}/{total}] Error: {e}", file=sys.stderr)

                await asyncio.sleep(1)



        return {"relevance": 0, "quality": 0, "novelty": 0,

                "reason": f"API error after 3 retries"}





async def score_all(papers: list, topic: str, api_key: str, base_url: str,

                    model: str, concurrency: int, max_tokens: int) -> list:

    """并发评分所有论文。"""

    semaphore = asyncio.Semaphore(concurrency)

    connector = aiohttp.TCPConnector(limit=concurrency + 5)

    async with aiohttp.ClientSession(connector=connector) as session:

        tasks = [

            score_one(session, base_url, api_key, model, topic,

                      paper, max_tokens, semaphore, i, len(papers))

            for i, paper in enumerate(papers)

        ]

        results = await asyncio.gather(*tasks)

    return list(results)





# ---------------------------------------------------------------------------

# 主流程

# ---------------------------------------------------------------------------



def main():

    parser = argparse.ArgumentParser(

        description="AI-powered paper relevance scoring",

        formatter_class=argparse.RawDescriptionHelpFormatter,

    )

    parser.add_argument("-i", "--input", required=True,

                        help="Input JSON (enriched results from enrich_abstracts.py)")

    parser.add_argument("-o", "--output", required=True,

                        help="Output JSON file")

    parser.add_argument("-t", "--topic", required=True,

                        help="Research topic description")

    parser.add_argument("--api-key", help="API key (default: from env or openclaw.json)")

    parser.add_argument("--base-url", help="API base URL")

    parser.add_argument("--model", help=f"Model name (default: {DEFAULT_MODEL})")

    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY,

                        help=f"Concurrent requests (default: {DEFAULT_CONCURRENCY})")

    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS,

                        help=f"Max response tokens (default: {DEFAULT_MAX_TOKENS})")

    parser.add_argument("--max-papers", type=int, default=0,

                        help="Limit to top N papers by machine score (0=all)")

    args = parser.parse_args()



    # --- 加载 API 配置 ---

    api_key, base_url, model, max_tokens = load_api_config()

    api_key = args.api_key or api_key

    base_url = args.base_url or base_url

    model = args.model or model

    max_tokens = args.max_tokens or max_tokens



    if not api_key or not base_url:

        print("[ERROR] No API credentials found. Set OPENAI_API_KEY + OPENAI_BASE_URL "

              "or configure in openclaw.json", file=sys.stderr)

        sys.exit(1)



    # --- 加载论文 ---

    with open(args.input, "r", encoding="utf-8") as f:

        data = json.load(f)



    papers = data.get("papers", data if isinstance(data, list) else [])

    if args.max_papers > 0:

        papers = papers[:args.max_papers]



    total = len(papers)

    if total == 0:

        print("[ERROR] No papers to score", file=sys.stderr)

        sys.exit(1)



    with_abs = sum(1 for p in papers if _resolve_abstract(p))

    print(f"[AI Ranker] {total} papers ({with_abs} with abstracts)", file=sys.stderr)

    print(f"[AI Ranker] Topic: {args.topic[:100]}...", file=sys.stderr)

    print(f"[AI Ranker] Model: {model} | Concurrency: {args.concurrency}",

          file=sys.stderr)

    print(f"[AI Ranker] Scoring...", file=sys.stderr)



    # --- 评分 ---

    start = time.time()

    all_scores = asyncio.run(score_all(

        papers, args.topic, api_key, base_url, model,

        args.concurrency, max_tokens,

    ))

    elapsed = time.time() - start



    # --- 合并结果 ---

    for paper, scores in zip(papers, all_scores):

        paper["_ai_scores"] = scores

        # 用 AI relevance 覆盖机器 relevance（如果成功）

        if scores["relevance"] > 0:

            if "_scores" not in paper:

                paper["_scores"] = {}

            paper["_scores"]["ai_relevance"] = scores["relevance"]

            paper["_scores"]["ai_quality"] = scores["quality"]

            paper["_scores"]["ai_novelty"] = scores["novelty"]



    # --- 按 AI relevance 排序 ---

    papers.sort(key=lambda p: (

        p.get("_ai_scores", {}).get("relevance", 0),

        p.get("_ai_scores", {}).get("quality", 0),

        p.get("_ai_scores", {}).get("novelty", 0),

    ), reverse=True)



    # --- 重新分类 ---

    for paper in papers:

        ai = paper.get("_ai_scores", {})

        rel = ai.get("relevance", 0)

        qual = ai.get("quality", 0)

        tags = []



        if qual >= 80 and rel >= 70:

            tags.append("landmark")

        if rel >= 75:

            tags.append("core")

        if rel >= 60 and qual >= 50:

            tags.append("solid")

        if rel >= 40 and qual >= 60:

            tags.append("notable")

        if not tags:

            tags.append("background")



        if "_tags" in paper:

            paper["_tags"] = tags  # override machine tags

        else:

            paper["_tags"] = tags



    # --- 统计 ---

    tag_counts = {}

    for p in papers:

        for tag in p.get("_tags", []):

            tag_counts[tag] = tag_counts.get(tag, 0) + 1



    avg_rel = round(sum(p.get("_ai_scores", {}).get("relevance", 0)

                        for p in papers) / max(total, 1), 1)



    print(f"[AI Ranker] Done in {elapsed:.1f}s", file=sys.stderr)

    print(f"[AI Ranker] Avg relevance: {avg_rel}", file=sys.stderr)

    print(f"[AI Ranker] Tags: {', '.join(f'{k}:{v}' for k, v in sorted(tag_counts.items()))}",

          file=sys.stderr)



    # --- 校验 + 报告 ---

    ok, issues = validate(papers, stage="ai_ranked")

    if issues:

        report(issues, stage="ai_ranked")



    # --- 输出 ---

    if isinstance(data, dict) and "papers" in data:

        data["papers"] = papers

        data["_ai_scoring"] = {

            "topic": args.topic,

            "model": model,

            "total_scored": total,

            "avg_relevance": avg_rel,

            "tag_distribution": tag_counts,

            "elapsed_seconds": round(elapsed, 1),

        }

        output_data = data

    else:

        output_data = {"papers": papers}



    out = Path(args.output)

    out.parent.mkdir(parents=True, exist_ok=True)

    stamp(output_data, stage="ai_ranked")

    with open(out, "w", encoding="utf-8") as f:

        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Saved to {out}", file=sys.stderr)





if __name__ == "__main__":

    main()

