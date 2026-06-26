"""
Serper API 搜索模板

提供 Google 搜索和 Google Scholar 搜索的异步实现，用于发现 researcher 的个人主页和学术资料。

依赖:
    pip install httpx python-dotenv

使用示例:
    import asyncio
    from serper_search import search_phd_students

    async def main():
        urls = await search_phd_students("reinforcement learning", "YOUR_API_KEY")
        print(f"Found {len(urls)} URLs")

    asyncio.run(main())
"""

import asyncio
import httpx
from typing import List, Dict, Optional


async def serper_search(
    query: str,
    api_key: str,
    search_type: str = "google",
    num_results: int = 20
) -> Dict:
    """
    使用 Serper API 执行搜索

    Args:
        query: 搜索查询字符串
        api_key: Serper API Key
        search_type: "google" 或 "google_scholar"
        num_results: 返回结果数量 (默认 20)

    Returns:
        搜索结果 JSON，包含以下字段:
        - organic: 有机搜索结果列表
        - scholar: 学术搜索结果 (仅 google_scholar)

    Raises:
        httpx.HTTPStatusError: API 请求失败

    Example:
        >>> results = await serper_search("PhD student AI", "api_key")
        >>> for item in results.get("organic", []):
        ...     print(item["link"])
    """
    # 根据搜索类型选择端点
    if search_type == "google_scholar":
        url = "https://google.serper.dev/scholar"
    else:
        url = "https://google.serper.dev/search"

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            url,
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json={
                "q": query,
                "num": num_results
            }
        )
        response.raise_for_status()
        return response.json()


async def search_phd_students(
    research_area: str,
    api_key: str,
    additional_keywords: Optional[List[str]] = None
) -> List[str]:
    """
    搜索特定领域的 PhD 学生

    生成多个搜索查询，聚合结果并去重。

    Args:
        research_area: 研究领域 (如 "reinforcement learning", "embodied AI")
        api_key: Serper API Key
        additional_keywords: 额外的搜索关键词

    Returns:
        去重后的 URL 列表

    Example:
        >>> urls = await search_phd_students("multimodal learning", "api_key")
        >>> print(f"Found {len(urls)} candidate URLs")
    """
    # 生成搜索查询
    queries = [
        f'"{research_area}" PhD student site:*.edu',
        f'"{research_area}" "doctoral candidate" site:github.io',
        f'"{research_area}" researcher personal homepage',
        f'"{research_area}" "PhD candidate" Stanford OR Berkeley OR CMU OR MIT',
    ]

    if additional_keywords:
        for kw in additional_keywords:
            queries.append(f'"{research_area}" "{kw}" PhD')

    all_urls = set()

    for i, query in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] Searching: {query[:50]}...")

        try:
            results = await serper_search(query, api_key)

            # 提取 URL
            urls_found = 0
            for key in ["organic", "scholar", "organic_results"]:
                if key in results:
                    for item in results[key]:
                        link = item.get("link", "")
                        if link and "google.com" not in link:
                            all_urls.add(link)
                            urls_found += 1

            print(f"    -> Found {urls_found} URLs")

        except Exception as e:
            print(f"    -> Error: {e}")

        # 避免触发 API 限流
        await asyncio.sleep(0.5)

    print(f"\nTotal unique URLs: {len(all_urls)}")
    return list(all_urls)


async def search_lab_members(
    lab_name: str,
    university: str,
    api_key: str
) -> List[str]:
    """
    搜索特定实验室的成员

    Args:
        lab_name: 实验室名称 (如 "BAIR", "SAIL")
        university: 大学名称 (如 "Berkeley", "Stanford")
        api_key: Serper API Key

    Returns:
        成员页面 URL 列表

    Example:
        >>> urls = await search_lab_members("BAIR", "Berkeley", "api_key")
    """
    queries = [
        f'site:{university.lower()}.edu "{lab_name}" people',
        f'site:{university.lower()}.edu "{lab_name}" members',
        f'site:{university.lower()}.edu "{lab_name}" PhD students',
        f'"{lab_name}" lab members {university}',
    ]

    all_urls = set()

    for query in queries:
        try:
            results = await serper_search(query, api_key)

            for item in results.get("organic", []):
                link = item.get("link", "")
                if link:
                    all_urls.add(link)

        except Exception as e:
            print(f"Error searching '{query}': {e}")

        await asyncio.sleep(0.5)

    return list(all_urls)


# 预定义的搜索查询模板
SEARCH_TEMPLATES = {
    "embodiment": [
        '"embodied AI" "PhD student" site:*.edu',
        '"robot learning" "PhD candidate" Stanford OR Berkeley OR CMU',
        '"manipulation" "imitation learning" PhD researcher',
        '"VLA" OR "vision-language-action" PhD student',
        '"sim-to-real" robotics "doctoral candidate"',
    ],
    "rl": [
        '"reinforcement learning" "PhD student" site:*.edu',
        '"RLHF" "PPO" PhD researcher personal homepage',
        '"reward modeling" PhD candidate',
        '"policy optimization" "doctoral student" AI',
    ],
    "multimodal": [
        '"multimodal learning" "PhD student" site:*.edu',
        '"vision-language" PhD researcher',
        '"CLIP" OR "BLIP" PhD candidate',
        '"image understanding" LLM PhD',
    ],
    "nlp": [
        '"natural language processing" "PhD student"',
        '"LLM" "pre-training" PhD researcher',
        '"transformer" "attention" PhD candidate',
        '"text generation" "doctoral student" AI',
    ]
}


async def search_by_template(
    template_name: str,
    api_key: str
) -> List[str]:
    """
    使用预定义模板搜索

    Args:
        template_name: 模板名称 (embodiment, rl, multimodal, nlp)
        api_key: Serper API Key

    Returns:
        URL 列表

    Raises:
        ValueError: 模板名称不存在
    """
    if template_name not in SEARCH_TEMPLATES:
        available = ", ".join(SEARCH_TEMPLATES.keys())
        raise ValueError(f"Template '{template_name}' not found. Available: {available}")

    queries = SEARCH_TEMPLATES[template_name]
    all_urls = set()

    for query in queries:
        try:
            results = await serper_search(query, api_key)

            for item in results.get("organic", []):
                link = item.get("link", "")
                if link and "google.com" not in link:
                    all_urls.add(link)

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(0.5)

    return list(all_urls)


# 使用示例
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("SERPER_API_KEY", "")

    if not api_key:
        print("Please set SERPER_API_KEY in .env file")
        exit(1)

    async def main():
        # 示例 1: 按研究领域搜索
        urls = await search_phd_students("reinforcement learning", api_key)
        print(f"\nFound {len(urls)} URLs:")
        for url in urls[:10]:
            print(f"  - {url}")

        # 示例 2: 使用预定义模板
        urls = await search_by_template("embodiment", api_key)
        print(f"\nEmbodiment search found {len(urls)} URLs")

    asyncio.run(main())
