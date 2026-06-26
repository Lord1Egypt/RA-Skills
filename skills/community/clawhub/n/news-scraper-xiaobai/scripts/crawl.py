#!/usr/bin/env python3
"""
新闻爬取主入口脚本

功能：
1. 从指定新闻网站爬取最新新闻
2. 去重检查（基于URL）
3. 生成AI摘要和关键词
4. 保存为Markdown格式

用法：
    python crawl.py                    # 爬取所有配置网站
    python crawl.py --site aibase      # 爬取指定网站
    python crawl.py --limit 10         # 限制爬取数量
    python crawl.py --skip-ai          # 跳过AI摘要生成
    python crawl.py --force             # 强制重新生成
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from scrapers import get_scraper


def print_news_summary(news_list: list) -> None:
    """输出格式化新闻摘要给用户"""
    if not news_list:
        return

    print(f"\n{'='*60}")
    print(f"📰 本次爬取新闻汇总")
    print(f"{'='*60}\n")

    for i, news in enumerate(news_list, 1):
        title = news.get("title", "无标题")[:40]
        if len(news.get("title", "")) > 40:
            title += "..."

        publish_time = news.get("publish_time", "未知时间")
        # summary暂时为空，等待模型生成
        summary = news.get("summary", "暂无摘要（请使用模型生成）")
        url = news.get("original_url") or news.get("url", "")

        print(f"【{i}】{title}")
        print(f"    发布时间: {publish_time}")
        print(f"    一句话总结: {summary}")
        print(f"    原文链接: {url}")
        print()

    print(f"{'='*60}")
    print("\n💡 提示：如需生成一句话总结，可读取JSON文件内容进行生成")
    print(f"   JSON文件位置：~/Documents/News/{config.NEWS_JSON_FILENAME}")
    print(f"{'='*60}")


def save_to_json(news_list: list, news_dir: Path) -> None:
    """保存新闻到JSON文件（更新同一个文件）"""
    import json

    if not news_list:
        return

    # 使用固定文件名，每次更新同一个文件
    json_file = news_dir / config.NEWS_JSON_FILENAME

    # 构建数据结构
    data = {
        "crawl_time": datetime.now().isoformat(),
        "total_count": len(news_list),
        "news": []
    }

    for news in news_list:
        item = {
            "title": news.get("title", ""),
            "url": news.get("original_url") or news.get("url", ""),
            "publish_time": news.get("publish_time", ""),
            "source": news.get("source", ""),
            "keywords": news.get("keywords", []),
            "summary": news.get("summary", "暂无摘要"),
            "content": news.get("content", ""),
        }
        data["news"].append(item)

    # 保存JSON（中文UTF-8编码）
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[JSON] 已更新: {json_file.name}")


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="新闻爬取工具")
    parser.add_argument(
        "--site",
        type=str,
        help="指定要爬取的网站标识（不指定则爬取所有）"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=config.MAX_NEWS_PER_CRAWL,
        help=f"每次爬取数量（默认{config.MAX_NEWS_PER_CRAWL}）"
    )
    parser.add_argument(
        "--skip-ai",
        action="store_true",
        help="跳过AI摘要生成"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制重新生成已存在的文件"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出JSON到stdout（用于程序调用）"
    )
    return parser.parse_args()


def load_existing_urls(news_dir: Path) -> set:
    """加载已有新闻的URL，用于去重"""
    existing_urls = set()
    if not news_dir.exists():
        return existing_urls

    for md_file in news_dir.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            # 从markdown中提取URL
            for line in content.split("\n"):
                if line.startswith("原文链接:") or line.startswith("url:"):
                    url = line.split(":", 1)[-1].strip()
                    existing_urls.add(url)
        except Exception as e:
            print(f"[警告] 读取文件失败: {md_file}, 错误: {e}")

    return existing_urls


def generate_filename(news: dict, news_dir: Path) -> Path:
    """生成文件名"""
    # 提取日期
    pub_time = news.get("publish_time", "")
    if pub_time:
        try:
            # 尝试解析时间
            dt = datetime.strptime(pub_time.split()[0], "%Y-%m-%d")
            date_str = dt.strftime("%Y%m%d")
        except:
            date_str = datetime.now().strftime("%Y%m%d")
    else:
        date_str = datetime.now().strftime("%Y%m%d")

    # 清理标题作为文件名
    title = news.get("title", "untitled")
    # 移除非文件名字符
    filename = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
    filename = filename[:50]  # 限制长度
    filename = filename.replace(" ", "_")

    # 构建文件名
    site_id = news.get("site_id", "unknown")
    filename = f"{date_str}_{site_id}_{filename}.md"

    return news_dir / filename


def save_news(news: dict, news_dir: Path) -> Path:
    """保存新闻为Markdown"""
    filename = generate_filename(news, news_dir)

    # 如果文件已存在且不强制覆盖，跳过
    if filename.exists() and not args.force:
        print(f"[跳过] 文件已存在: {filename.name}")
        return None

    # 生成markdown内容
    content = f"""# {news.get('title', '无标题')}

## 元信息

- **原文链接**: {news.get('url', '')}
- **发布时间**: {news.get('publish_time', '未知')}
- **新闻来源**: {news.get('source', '未知')}
- **关键词**: {', '.join(news.get('keywords', []))}
- **一句话摘要**: {news.get('summary', '暂无摘要')}

---

## 正文

{news.get('content', '无正文内容')}
"""

    # 写入文件
    filename.write_text(content, encoding="utf-8")
    print(f"[保存] {filename.name}")

    return filename


def crawl_site(site_id: str, existing_urls: set) -> list:
    """爬取单个网站"""
    print(f"\n{'='*50}")
    print(f"开始爬取网站: {site_id}")
    print(f"{'='*50}\n")

    try:
        scraper = get_scraper(site_id)
    except ValueError as e:
        print(f"[错误] {e}")
        return []

    # 执行爬取
    news_list = scraper.crawl(limit=args.limit)

    # 去重
    filtered_news = []
    for news in news_list:
        url = news.get("url", "")
        if url in existing_urls:
            print(f"[去重] 跳过重复新闻: {news.get('title', '')[:30]}...")
            continue
        news["site_id"] = site_id
        filtered_news.append(news)

    return filtered_news


def crawl_and_return_json(site: str = "aibase", limit: int = 20, news_dir: str = None) -> dict:
    """
    爬取新闻并返回JSON数据

    参数:
        site: 网站标识符
        limit: 爬取数量
        news_dir: 保存目录路径（可选，不传则AI自行决定）

    返回:
        dict: 包含news列表的字典
    """
    import argparse
    from pathlib import Path

    # 如果没有传入保存目录，AI自行决定使用合适的目录
    if news_dir is None:
        # 使用当前目录下的News文件夹
        news_dir = Path.cwd() / "News"
    else:
        news_dir = Path(news_dir)

    # 临时设置args
    global args
    args = argparse.Namespace(site=site, limit=limit, force=False)

    # 确保保存目录存在
    news_dir.mkdir(parents=True, exist_ok=True)

    # 加载已有URL用于去重
    existing_urls = load_existing_urls(news_dir)

    # 爬取
    news_list = crawl_site(site, existing_urls)

    if not news_list:
        return {"news": [], "message": "没有新新闻"}

    # 保存JSON
    save_to_json(news_list, news_dir)

    # 返回JSON数据供模型生成总结
    return {
        "news": news_list,
        "count": len(news_list)
    }


def main():
    """主函数"""
    import argparse
    import json
    from pathlib import Path

    global args
    args = parse_args()

    # 如果命令行没有指定目录，使用当前目录下的News文件夹
    # AI会根据实际需求选择合适的存储位置
    news_dir = Path.cwd() / "News"
    news_dir.mkdir(parents=True, exist_ok=True)

    # 加载已有URL用于去重
    existing_urls = load_existing_urls(news_dir)

    # 确定要爬取的网站
    sites = [args.site] if args.site else list(config.SITES.keys())

    # 爬取所有网站
    all_news = []
    for site_id in sites:
        news_list = crawl_site(site_id, existing_urls)
        all_news.extend(news_list)

    if not all_news:
        if args.json:
            print(json.dumps({"news": [], "count": 0}, ensure_ascii=False))
        else:
            print("\n没有新新闻需要保存")
        return

    # 如果是JSON模式，输出到stdout
    if args.json:
        output = {
            "news": all_news,
            "count": len(all_news)
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    # 正常模式输出
    print(f"新闻保存目录: {news_dir}")
    print(f"已有新闻数量: {len(existing_urls)}")

    # 保存新闻
    print(f"\n{'='*50}")
    print("保存新闻到JSON...")
    print(f"{'='*50}\n")

    # 保存到JSON
    save_to_json(all_news, news_dir)

    # 输出格式化文案
    print_news_summary(all_news)

    print(f"\n{'='*50}")
    print(f"完成！共爬取 {len(all_news)} 条新闻")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
