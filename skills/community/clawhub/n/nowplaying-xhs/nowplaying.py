#!/usr/bin/env python3
"""
NowPlaying - 当前院线电影推荐
获取正在热映的电影信息、评分、排片等
"""

import urllib.request
import re
import json
from datetime import datetime

# 数据源配置
SOURCES = {
    'rottentomatoes': 'https://www.rottentomatoes.com/browse/movies_in_theaters',
    'variety': 'https://variety.com/v/film/',
}

def fetch_nowplaying_movies():
    """获取正在热映的电影"""
    movies = []
    
    try:
        # 从 Rotten Tomatoes 获取
        url = SOURCES['rottentomatoes']
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # 清理 HTML
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        
        # 解析带评分的电影（模式 1）
        pattern1 = r'(\d+)%\s+([A-Z][^\(]+?)\s+(?:Opens?|Opened)\s+(\w+\s+\d+,\s+\d{4})'
        matches = re.findall(pattern1, text, re.IGNORECASE)
        
        for match in matches:
            rating, title, date_str = match
            title = title.strip()
            if title and len(title) < 100 and not any(w in title.lower() for w in ['watchlist', 'trailer']):
                movies.append({
                    'title': title,
                    'rating': int(rating),
                    'release_date': date_str.strip(),
                    'source': 'Rotten Tomatoes',
                    'url': f"https://www.rottentomatoes.com/search?search={title.replace(' ', '+')}"
                })
        
        # 解析无评分的新片（模式 2）
        pattern2 = r'([A-Z][^%\[\]]+?)\s+(?:Opens?|Opened)\s+(\w+\s+\d+,\s+\d{4})'
        matches2 = re.findall(pattern2, text, re.IGNORECASE)
        
        for match in matches2[:10]:
            title, date_str = match
            title = title.strip()
            # 过滤无效标题
            if (title and len(title) < 80 and 
                '%' not in title and 
                'Watchlist' not in title and
                not any(w in title.lower() for w in ['trailer', 'streaming', 'coming soon'])):
                # 检查是否已存在
                if not any(m['title'] == title for m in movies):
                    movies.append({
                        'title': title,
                        'rating': None,
                        'release_date': date_str.strip(),
                        'source': 'Rotten Tomatoes',
                        'url': f"https://www.rottentomatoes.com/search?search={title.replace(' ', '+')}"
                    })
    
    except Exception as e:
        print(f"⚠️ 获取 Rotten Tomatoes 失败：{e}")
    
    return movies

def fetch_box_office_news():
    """获取票房新闻"""
    news = []
    
    try:
        url = SOURCES['variety']
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # 提取票房相关新闻
        box_office_pattern = r'(\$[\d.]+\s*(?:million|billion))'
        matches = re.findall(box_office_pattern, html, re.IGNORECASE)
        
        if matches:
            news.append({
                'title': '票房动态',
                'content': f'本周票房数据：{", ".join(matches[:3])}',
                'source': 'Variety'
            })
    
    except Exception as e:
        print(f"⚠️ 获取 Variety 新闻失败：{e}")
    
    return news

def format_output(movies, news=None, detailed=True):
    """格式化输出"""
    output = []
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    output.append(f"# 🎬 当前院线热映 ({date_str})")
    output.append("")
    
    # 高评分推荐（Top 5）
    rated_movies = [m for m in movies if m.get('rating')]
    rated_movies.sort(key=lambda x: x['rating'], reverse=True)
    
    output.append("## 🌟 高评分推荐")
    output.append("")
    
    for i, movie in enumerate(rated_movies[:5], 1):
        stars = "⭐" * (movie['rating'] // 20)
        output.append(f"{i}. **{movie['title']}** {stars}")
        output.append(f"   - 评分：{movie['rating']}% | 上映：{movie['release_date']}")
        output.append(f"   - [详情]({movie['url']})")
        output.append("")
    
    output.append("---")
    output.append("")
    
    # 新片速递
    output.append("## 🎥 本周新片")
    output.append("")
    
    new_releases = [m for m in movies if 'Apr 17' in m.get('release_date', '') or 'Apr 16' in m.get('release_date', '')]
    
    if new_releases:
        for movie in new_releases[:5]:
            rating_str = f"{movie['rating']}%" if movie.get('rating') else "暂无评分"
            output.append(f"- **{movie['title']}** ({rating_str}) - {movie['release_date']}")
    else:
        output.append("- 暂无本周新片信息")
    
    output.append("")
    output.append("---")
    output.append("")
    
    # 票房新闻
    if news:
        output.append("## 📰 票房新闻")
        output.append("")
        for item in news:
            output.append(f"- **{item['title']}**: {item['content']}")
        output.append("")
    
    # 详细信息（可选）
    if detailed:
        output.append("## 📊 完整片单")
        output.append("")
        output.append("| 电影 | 评分 | 上映日期 |")
        output.append("|------|------|----------|")
        
        for movie in movies[:15]:
            rating_str = f"{movie['rating']}%" if movie.get('rating') else "-"
            output.append(f"| {movie['title']} | {rating_str} | {movie['release_date']} |")
        
        output.append("")
    
    return '\n'.join(output)

def main():
    print("🎬 开始获取当前院线电影信息...\n")
    
    # 获取电影列表
    print("📽️  获取热映电影...")
    movies = fetch_nowplaying_movies()
    print(f"✅ 找到 {len(movies)} 部电影")
    
    # 获取票房新闻
    print("📰 获取票房新闻...")
    news = fetch_box_office_news()
    print(f"✅ 找到 {len(news)} 条新闻")
    
    # 格式化输出
    print("\n" + "="*60)
    print(format_output(movies, news, detailed=True))
    
    # 保存结果
    output_file = f"/tmp/nowplaying_{datetime.now().strftime('%Y%m%d')}.md"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(format_output(movies, news, detailed=True))
        print(f"\n💾 报告已保存：{output_file}")
    except Exception as e:
        print(f"\n⚠️  保存失败：{e}")

if __name__ == "__main__":
    main()
