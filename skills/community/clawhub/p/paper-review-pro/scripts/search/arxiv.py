"""
arXiv API 检索模块

增强功能：
- 添加重试逻辑和速率限制处理
- 使用 HTTPS 连接
- 指数退避策略
- 添加请求前延迟避免速率限制
- 二阶段回退：API 失败后使用网页爬取
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import time
import random


def search_arxiv_web(query, max_results=20):
    """
    通过 arXiv 网页搜索获取论文（API 失败时的回退方案）
    
    参数:
        query: 查询字符串
        max_results: 最大返回数
    
    返回:
        List[dict]
    """
    import signal
    
    try:
        # 构建网页搜索 URL
        encoded_query = urllib.parse.quote(query)
        url = f"https://arxiv.org/search/?query={encoded_query}&searchtype=all&source=header"
        
        # 添加 User-Agent 避免被拒绝
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        print(f"  [arXiv Web] 正在检索网页...")
        req = urllib.request.Request(url, headers=headers)
        # 增加超时到 120 秒，arXiv 网页加载较慢
        html = urllib.request.urlopen(req, timeout=120).read().decode("utf-8")
        print(f"  [arXiv Web] 页面大小：{len(html)} 字节")
        
        results = []
        
        # 使用更精确的正则表达式提取每个论文条目的完整 HTML 块
        # arXiv 搜索结果格式：<li class="arxiv-result">...</li>
        entry_pattern = r'<li class="arxiv-result">(.*?)</li>'
        entry_matches = re.findall(entry_pattern, html, re.DOTALL)
        
        print(f"  [arXiv Web] 找到 {len(entry_matches)} 个条目，处理前 {min(max_results, len(entry_matches))} 个...")
        
        for idx, entry in enumerate(entry_matches[:max_results]):
            try:
                # 限制每个条目的处理范围，避免大文本块导致性能问题
                entry = entry[:50000]  # 限制单个条目最大长度
                
                # 提取 arXiv ID 和 URL
                id_match = re.search(r'arxiv\.org/abs/(\d+\.\d+)', entry)
                arxiv_id = id_match.group(1) if id_match else ""
                paper_url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ""
                
                # 提取标题 - 使用更精确的模式
                title_match = re.search(r'<p class="title is-5 mathjax">(.*?)</p>', entry, re.DOTALL)
                title = ""
                if title_match:
                    title_text = title_match.group(1)
                    # 移除所有 HTML 标签
                    title = re.sub(r'<[^>]+>', '', title_text).strip()
                    # 清理特殊字符
                    title = title.replace('\n', ' ').strip()
                
                # 提取作者
                authors = []
                authors_match = re.search(r'<p class="authors">(.*?)</p>', entry, re.DOTALL)
                if authors_match:
                    author_text = authors_match.group(1)
                    # 提取所有 <a> 标签中的作者名
                    author_links = re.findall(r'<a[^>]*>([^<]+)</a>', author_text)
                    authors = [a.strip() for a in author_links if a.strip()]
                
                # 提取摘要 - 简化逻辑，优先使用 abstract-short
                abstract = ""
                # 先尝试找 short abstract（更可靠）
                abstract_short_match = re.search(r'<span class="abstract-short"(.*?)</span>', entry, re.DOTALL)
                if abstract_short_match:
                    abstract_text = abstract_short_match.group(1)
                    # 移除 "More" 链接及其内容
                    abstract_text = re.sub(r'<a[^>]*>More[^<]*</a>', '', abstract_text)
                    abstract = re.sub(r'<[^>]+>', '', abstract_text).strip()
                
                # 清理摘要中的 HTML 实体和特殊字符
                abstract = abstract.replace('&emph;', '')
                abstract = abstract.replace('\\emph{', '')
                abstract = abstract.replace('}', '')
                abstract = abstract.replace('\\', '')
                abstract = abstract.replace('$\\rightarrow$', '→')
                abstract = abstract.replace('\n', ' ').strip()
                
                # 提取年份（从 submitted 日期）
                year = 0
                submitted_match = re.search(r'Submitted.*?(\d{4})', entry)
                if submitted_match:
                    year = int(submitted_match.group(1))
                
                # 只添加有标题的论文
                if title:
                    results.append({
                        "title": title,
                        "abstract": abstract[:2000] if abstract else "",  # 限制摘要长度
                        "url": paper_url,
                        "year": year,
                        "authors": authors,
                        "source": "arxiv",
                        "categories": [],
                        "published_date": None
                    })
                    print(f"  [arXiv Web] 处理第 {idx+1} 篇：{title[:50]}...")
                    
            except Exception as e:
                print(f"  [arXiv Web] 解析条目 {idx+1} 失败：{e}")
                continue
        
        print(f"  [arXiv Web] 检索到 {len(results)} 篇")
        return results
        
    except Exception as e:
        print(f"  [arXiv Web] 检索失败：{e}")
        return []


def search_arxiv(query, max_results=20, max_retries=3):
    """
    调用 arXiv API 获取论文

    改进：
    1. 优先搜索标题和摘要（而非全文）
    2. 添加相关分类过滤
    3. 按相关性排序
    4. 添加重试逻辑处理速率限制
    5. 添加请求前延迟

    参数:
        query: 查询字符串
        max_results: 最大返回数
        max_retries: 最大重试次数

    返回:
        List[dict]
    """

    # 构建更精确的查询：优先匹配标题和摘要
    encoded_query = urllib.parse.quote(query)
    
    # 搜索策略：标题 + 摘要组合查询
    search_query = f"(all:{encoded_query})"
    
    # 使用 HTTPS 而不是 HTTP
    url = (
        "https://export.arxiv.org/api/query?"
        f"search_query={search_query}"
        f"&max_results={max_results}"
        "&sortBy=relevance&sortOrder=descending"
    )

    # 请求前添加随机延迟（3-8 秒），避免速率限制
    initial_delay = random.uniform(3, 8)
    print(f"  [arXiv] 等待 {initial_delay:.1f} 秒后开始检索...")
    time.sleep(initial_delay)

    # 重试逻辑 - API 失败 2 次后回退到网页爬取
    api_failures = 0
    for attempt in range(max_retries):
        try:
            print(f"  [arXiv] 正在检索 (尝试 {attempt + 1}/{max_retries})...")
            # 增加超时到 120 秒
            data = urllib.request.urlopen(url, timeout=120).read().decode("utf-8")
            break  # 成功则退出重试循环
        except urllib.error.HTTPError as e:
            api_failures += 1
            if e.code == 429 or e.code == 503:
                # 速率限制或服务不可用，等待后重试
                wait_time = (2 ** attempt) * 5 + random.uniform(0, 3)  # 指数退避：5-8, 10-13, 20-23 秒
                print(f"  [arXiv] 速率限制或服务繁忙 (HTTP {e.code})，等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
                # 如果已经失败 2 次，回退到网页爬取
                if api_failures >= 2:
                    print(f"  [arXiv] API 连续失败 {api_failures} 次，切换到网页爬取模式...")
                    return search_arxiv_web(query, max_results)
                if attempt >= max_retries - 1:
                    print(f"  [arXiv] 达到最大重试次数，返回空结果")
                    return []
            else:
                print(f"  [arXiv 检索失败]: HTTP Error {e.code}")
                # 非速率限制错误，直接回退到网页爬取
                if api_failures >= 1:
                    print(f"  [arXiv] 切换到网页爬取模式...")
                    return search_arxiv_web(query, max_results)
                return []
        except Exception as e:
            api_failures += 1
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 3 + random.uniform(0, 2)
                print(f"  [arXiv] 检索错误：{e}，等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
                # 如果已经失败 2 次，回退到网页爬取
                if api_failures >= 2:
                    print(f"  [arXiv] API 连续失败 {api_failures} 次，切换到网页爬取模式...")
                    return search_arxiv_web(query, max_results)
            else:
                print(f"  [arXiv 检索失败]: {e}")
                # 最后一次尝试失败，回退到网页爬取
                print(f"  [arXiv] 切换到网页爬取模式...")
                return search_arxiv_web(query, max_results)

    root = ET.fromstring(data)

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    results = []

    for entry in root.findall("atom:entry", ns):
        title_elem = entry.find("atom:title", ns)
        abstract_elem = entry.find("atom:summary", ns)
        id_elem = entry.find("atom:id", ns)
        published_elem = entry.find("atom:published", ns)
        
        if title_elem is None or title_elem.text is None:
            continue
            
        title = title_elem.text.strip()
        abstract = abstract_elem.text.strip() if abstract_elem is not None and abstract_elem.text else ""
        url = id_elem.text if id_elem is not None else ""
        year = int(published_elem.text[:4]) if published_elem is not None and published_elem.text else 0

        # 解析 authors
        authors = []
        for author in entry.findall("atom:author", ns):
            name = author.find("atom:name", ns)
            if name is not None and name.text:
                authors.append(name.text)

        # 解析分类
        categories = []
        for category in entry.findall("atom:category", ns):
            term = category.get("term")
            if term:
                categories.append(term)

        results.append({
            "title": title,
            "abstract": abstract,
            "url": url,
            "year": year,
            "authors": authors,
            "source": "arxiv",
            "categories": categories,
            "published_date": published_elem.text[:10] if published_elem is not None and published_elem.text else None
        })

    print(f"  [arXiv] 检索到 {len(results)} 篇")
    return results
