#!/usr/bin/env python3

"""

ai_summarize.py — AI 生成中文论文简述（200-300 字）



每条请求只包含：一篇论文的标题/元数据/摘要。

摘要随 API 请求结束即销毁，从不进入主对话上下文。

生成的中文简述写回文件，AI 后续可通过 strip_abstracts.py --summary

查看元数据、按需读取单篇简述。



用法：

  python ai_summarize.py -i ai_ranked.json -o summarized.json --top 15

  python ai_summarize.py -i ai_ranked.json -o summarized.json --top 15 --concurrency 8



输出：在原始 JSON 基础上添加 _cn_summary 字段。

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



import aiohttp



from utils.pipeline_schema import validate, report, stamp, check_version, PIPELINE_VERSION



import sys, os




# ---------------------------------------------------------------------------

# 配置

# ---------------------------------------------------------------------------



DEFAULT_MODEL = "deepseek-v4-pro"

DEFAULT_BASE_URL = "https://api.deepseek.com"

DEFAULT_MAX_TOKENS = 800

DEFAULT_TEMPERATURE = 0.4

DEFAULT_CONCURRENCY = 8



SYSTEM_PROMPT = """You are a bilingual academic paper summarizer. 



Given a paper's metadata and abstract, write a Chinese summary of 200-300 Chinese characters.

The summary should:

1. State the core contribution/problem in one sentence

2. Describe the method/approach briefly

3. Mention key findings or conclusions

4. Use natural, flowing Chinese academic language

5. Do NOT translate verbatim - distill and rephrase



Return ONLY the Chinese summary text, no JSON wrapper, no labels, no formatting."""





def load_api_config():

    """从 OpenClaw 配置或环境变量加载 API 凭证。"""

    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")

    base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("DEEPSEEK_BASE_URL")

    model = os.environ.get("AI_SUMMARIZE_MODEL")



    if api_key and base_url:

        return api_key, base_url, model or DEFAULT_MODEL, DEFAULT_MAX_TOKENS



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

            preferred = ["custom-api-deepseek-com", "moonshot"]

            for name in preferred:

                p = providers.get(name, {})

                if p.get("apiKey") and p.get("baseUrl"):

                    m = (p.get("models", [{}]) or [{}])[0].get("id", DEFAULT_MODEL)

                    return p["apiKey"], p["baseUrl"], m, DEFAULT_MAX_TOKENS



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





def build_user_message(paper: dict) -> str:

    """构建单篇论文的摘要生成 prompt。"""

    title = paper.get("title", "Unknown")

    authors = paper.get("authors", "Unknown")

    year = paper.get("year", "?")

    venue = paper.get("venue", "Unknown")

    abstract = _resolve_abstract(paper)  # ← 从文件解析



    if abstract and len(abstract) > 2500:

        abstract = abstract[:2500] + "..."



    parts = [

        f"Title: {title}",

        f"Authors: {authors}",

        f"Year: {year} | Venue: {venue}",

    ]

    if abstract and abstract != "[已缓存]":

        parts.extend(["", f"Abstract: {abstract}"])

    else:

        parts.extend(["", "Abstract: [Not available - please summarize based on title and metadata only]"])



    return "\n".join(parts)





async def summarize_one(session: aiohttp.ClientSession, base_url: str, api_key: str,

                        model: str, paper: dict, max_tokens: int,

                        semaphore: asyncio.Semaphore, index: int, total: int) -> str:

    """为单篇论文生成中文简述。"""

    async with semaphore:

        payload = {

            "model": model,

            "messages": [

                {"role": "system", "content": SYSTEM_PROMPT},

                {"role": "user", "content": build_user_message(paper)},

            ],

            "max_tokens": max_tokens,

            "temperature": DEFAULT_TEMPERATURE,

            "thinking": {"type": "disabled"},

        }

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

                        content = data["choices"][0]["message"]["content"].strip()

                        print(f"  [{index+1}/{total}] {len(content)} chars  {title}...",

                              file=sys.stderr)

                        return content

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



        return "（摘要生成失败）"





async def summarize_all(papers: list, api_key: str, base_url: str,

                        model: str, concurrency: int, max_tokens: int) -> list:

    """并发生成中文简述。"""

    semaphore = asyncio.Semaphore(concurrency)

    connector = aiohttp.TCPConnector(limit=concurrency + 5)

    async with aiohttp.ClientSession(connector=connector) as session:

        tasks = [

            summarize_one(session, base_url, api_key, model,

                          paper, max_tokens, semaphore, i, len(papers))

            for i, paper in enumerate(papers)

        ]

        results = await asyncio.gather(*tasks)

    return list(results)





def main():

    parser = argparse.ArgumentParser(

        description="AI-powered Chinese paper summarization",

        formatter_class=argparse.RawDescriptionHelpFormatter,

    )

    parser.add_argument("-i", "--input", required=True,

                        help="Input JSON (ai_ranked.json or enriched.json)")

    parser.add_argument("-o", "--output", required=True,

                        help="Output JSON file")

    parser.add_argument("--top", type=int, default=0,

                        help="Summarize only top N papers (0=all)")

    parser.add_argument("--api-key", help="API key")

    parser.add_argument("--base-url", help="API base URL")

    parser.add_argument("--model", help=f"Model name (default: {DEFAULT_MODEL})")

    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY,

                        help=f"Concurrent requests (default: {DEFAULT_CONCURRENCY})")

    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS,

                        help=f"Max response tokens (default: {DEFAULT_MAX_TOKENS})")

    args = parser.parse_args()



    # --- 加载 API 配置 ---

    api_key, base_url, model, max_tokens = load_api_config()

    api_key = args.api_key or api_key

    base_url = args.base_url or base_url

    model = args.model or model

    max_tokens = args.max_tokens or max_tokens



    if not api_key or not base_url:

        print("[ERROR] No API credentials found.", file=sys.stderr)

        sys.exit(1)



    # --- 加载论文 ---

    with open(args.input, "r", encoding="utf-8") as f:

        data = json.load(f)



    papers = data.get("papers", data if isinstance(data, list) else [])

    total = len(papers)



    if args.top > 0 and args.top < total:

        papers = papers[:args.top]

        total = len(papers)



    if total == 0:

        print("[ERROR] No papers to summarize", file=sys.stderr)

        sys.exit(1)



    with_abs = sum(1 for p in papers if _resolve_abstract(p))

    print(f"[AI Summarizer] {total} papers ({with_abs} with abstracts)", file=sys.stderr)

    print(f"[AI Summarizer] Model: {model} | Concurrency: {args.concurrency}",

          file=sys.stderr)

    print(f"[AI Summarizer] Generating Chinese summaries...", file=sys.stderr)



    # --- 生成 ---

    start = time.time()

    summaries = asyncio.run(summarize_all(

        papers, api_key, base_url, model,

        args.concurrency, max_tokens,

    ))

    elapsed = time.time() - start



    # --- 合并 ---

    chars = 0

    for paper, cn_summary in zip(papers, summaries):

        paper["_cn_summary"] = cn_summary

        chars += len(cn_summary)



    # --- 校验 + 报告 ---

    ok, issues = validate(papers, stage="summarized")

    if issues:

        report(issues, stage="summarized")



    # --- 输出 ---

    if isinstance(data, dict) and "papers" in data:

        data["papers"] = papers

        data["_summarization"] = {

            "total_summarized": total,

            "model": model,

            "elapsed_seconds": round(elapsed, 1),

            "total_chars": chars,

        }

        output_data = data

    else:

        output_data = {"papers": papers}



    out = Path(args.output)

    out.parent.mkdir(parents=True, exist_ok=True)

    stamp(output_data, stage="summarized")

    with open(out, "w", encoding="utf-8") as f:

        json.dump(output_data, f, ensure_ascii=False, indent=2)



    print(f"[AI Summarizer] Done in {elapsed:.1f}s | {chars} total chars",

          file=sys.stderr)

    print(f"Saved to {out}", file=sys.stderr)





if __name__ == "__main__":

    main()

