import feedparser
import httpx

def fetch_clean_headlines(source_name: str, url: str, limit: int = 3, keywords: list = None, negative_keywords: list = None) -> str:
    try:
        # 伪装 Header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*'
        }
        
        with httpx.Client(timeout=15.0, headers=headers, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            feed = feedparser.parse(response.text)
            
    except httpx.HTTPStatusError as exc:
        return f"⚠️ 抓取 {source_name} 失败: HTTP 状态码 {exc.response.status_code} (可能被拦截)"
    except Exception as e:
        return f"⚠️ 抓取 {source_name} 失败: {str(e)}"

    if feed.bozo and not feed.entries:
        return f"⚠️ 解析 {source_name} 失败：返回的数据不是有效的 XML 格式。"

    results = []
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        
        # 1. 黑名单过滤（精准剔除胡萝卜、番茄等生活类噪音）
        if negative_keywords:
            if any(nk.lower() in title.lower() for nk in negative_keywords):
                continue  # 命中黑名单，直接跳过本条新闻
        
        # 2. 白名单过滤
        if keywords:
            if any(kw.lower() in title.lower() for kw in keywords):
                results.append(f"- [{title}]({link})")
        else:
            results.append(f"- [{title}]({link})")
            
        if len(results) >= limit:
            break
            
    # 兜底逻辑
    if keywords and not results:
        results.append(f"*(今日无重点关注的特定消息。为您推送当前热门：)*")
        # 兜底时也要避开黑名单
        fallback_count = 0
        for entry in feed.entries:
            if negative_keywords and any(nk.lower() in entry.title.lower() for nk in negative_keywords):
                continue
            results.append(f"- [{entry.title}]({entry.link})")
            fallback_count += 1
            if fallback_count >= 2:
                break

    header = f"### {source_name} 今日要闻\n"
    body = "\n".join(results) if results else "- 今日暂无更新。"
    
    return header + body

if __name__ == "__main__":
    print(f"正在全速并发抓取全球权威信息源...\n")
    
    # 1. 国际要闻 (BBC 保持稳定)
    bbc_news = fetch_clean_headlines(
        "国际要闻 (BBC World)", 
        "https://feeds.bbci.co.uk/news/world/rss.xml", 
        limit=3
    )
    print(bbc_news)
    print("\n" + "-" * 30 + "\n")
    
    # 2. 硬核科技 (Solidot - 开启负面词清洗)
    tech_news = fetch_clean_headlines(
        "硬核科技 (Solidot)", 
        "https://www.solidot.org/index.rss", 
        limit=3,
        negative_keywords=["胡萝卜", "番茄", "烹饪", "饮食", "食谱"]
    )
    print(tech_news)
    print("\n" + "-" * 30 + "\n")
    
    # 3. 游戏大作源 (换用 Polygon，对 RSS 抓取极度友好)
    game_news = fetch_clean_headlines(
        "游戏大作 (Polygon)", 
        "https://www.polygon.com/rss/index.xml", 
        limit=3, 
        keywords=["GTA", "Cyberpunk", "Witcher", "CDPR", "Black Ops", "Call of Duty"] 
    )
    print(game_news)
    print("\n" + "-" * 30 + "\n")
    
    
# 1. 纯粹的前沿科学与奇闻 (满足你对硬核知识的偏好)
    # 使用 ScienceDaily 的核心流。它只发经过同行评审的最新突破，且极其干净。
    # 经常会出现类似“深海发现非光合作用生态系统”或“量子纠缠的宏观验证”这种顶级文章。
    science_news = fetch_clean_headlines(
        "前沿科学突破 (ScienceDaily)", 
        "https://www.sciencedaily.com/rss/top/science.xml", 
        limit=3
    )
    print(science_news)
    print("\n" + "-" * 30 + "\n")

    # 2. 开源 AI 与底层算力硬件 (追踪技术红利期的核心脉搏)
    # 相比于泛科技，直接锁定底层算力、GPU 架构以及本地大模型 (LLM) 的前沿动向。
    # Tom's Hardware 是全球最老牌的硬核硬件媒体，配合关键词只抓取最有价值的底层技术。
    # 3. 专注 Agent 框架演进 (追踪 OpenClaw 官方 GitHub Releases)
    # 只要作者发了新版本，这里就会第一时间抓取到更新日志
    openclaw_news = fetch_clean_headlines(
        "核心框架动态 (OpenClaw Updates)", 
        "https://github.com/joargp/openclaw/releases.atom", 
        limit=2
    )
    print(openclaw_news)
