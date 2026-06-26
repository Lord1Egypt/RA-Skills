import sys
import requests
import os
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.heybossai.com/v1"


def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()


def get_baidu_hot():
    try:
        # 使用 SkillBoss API Hub scraping 类型抓取百度实时热搜页面
        result = pilot({
            "type": "scraper",
            "inputs": {"url": "https://top.baidu.com/board?tab=realtime"}
        })
        content = result["result"]["data"]["markdown"]

        # 使用 SkillBoss API Hub chat 类型从页面内容中提取热搜词条
        chat_result = pilot({
            "type": "chat",
            "inputs": {
                "messages": [
                    {
                        "role": "user",
                        "content": f"从以下百度热搜页面内容中提取前5个热搜词条，每行一个，只输出词条名称，不要编号：\n{str(content)[:3000]}"
                    }
                ]
            },
            "prefer": "balanced"
        })
        text = chat_result["result"]["choices"][0]["message"]["content"]
        hot_items = [line.strip() for line in text.strip().split('\n') if line.strip()][:5]
        return hot_items
    except Exception as e:
        logging.error(f"Error fetching Baidu hot search: {e}")
        return []


def get_google_trends():
    try:
        # 使用 SkillBoss API Hub search 类型搜索 Google 热搜趋势
        result = pilot({
            "type": "search",
            "inputs": {"query": "Google trending searches today US top 5"},
            "prefer": "balanced"
        })
        results = result["result"]

        hot_items = []
        if isinstance(results, list):
            for item in results[:5]:
                if isinstance(item, dict):
                    title = item.get("title") or item.get("name") or str(item)
                else:
                    title = str(item)
                hot_items.append(title)
        elif isinstance(results, dict):
            items = results.get("results") or results.get("items") or results.get("organic_results") or []
            for item in items[:5]:
                if isinstance(item, dict):
                    hot_items.append(item.get("title", str(item)))
                else:
                    hot_items.append(str(item))
        return hot_items[:5]
    except Exception as e:
        logging.error(f"Error fetching Google Trends: {e}")
        return []


def get_daily_news():
    now = datetime.datetime.now()
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    baidu_hot = get_baidu_hot()
    google_hot = get_google_trends()

    all_hot = []
    if baidu_hot:
        all_hot.extend(baidu_hot)
    if google_hot:
        all_hot.extend(google_hot)

    # Take top 10 unique keywords
    final_hot = []
    seen = set()
    for item in all_hot:
        if item not in seen:
            final_hot.append(item)
            seen.add(item)
            if len(final_hot) >= 10:
                break

    greeting = f"现在是北京时间 {current_time_str}，今日热搜榜单如下："
    news_list = ""
    for i, item in enumerate(final_hot, 1):
        news_list += f"{i}. {item}\n"

    return f"{greeting}\n{news_list}"


if __name__ == "__main__":
    print(get_daily_news())
