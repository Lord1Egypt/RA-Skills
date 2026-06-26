#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 Movie Recommender - 电影推荐助手（优化版）
功能：电影推荐、豆瓣评分查询、观影记录管理、热映榜单
对接豆瓣 API（无需 Key 的爬虫方案）
"""

import json
import random
from pathlib import Path
from datetime import datetime

# 导入豆瓣 API
from douban_api import (
    search_movie, get_movie_detail, get_movie_rating,
    get_top250, format_movie_info
)

# 数据文件路径
DATA_DIR = Path(__file__).parent
WATCHED_FILE = DATA_DIR / "watched.json"
WANT_TO_WATCH_FILE = DATA_DIR / "want_to_watch.json"

# 心情对应类型
MOOD_MAP = {
    "开心": ["喜剧", "爱情"],
    "难过": ["治愈", "励志"],
    "放松": ["喜剧", "治愈", "动画"],
    "刺激": ["动作", "科幻", "惊悚"],
    "烧脑": ["悬疑", "科幻", "犯罪"],
    "累": ["治愈", "喜剧", "动画"],
    "孤独": ["爱情", "治愈", "剧情"],
    "兴奋": ["动作", "冒险", "科幻"],
}

# 电影类型（用于推荐）
MOVIE_TYPES = [
    "剧情", "喜剧", "爱情", "动作", "科幻", "悬疑", 
    "惊悚", "犯罪", "恐怖", "动画", "冒险", "奇幻",
    "治愈", "励志", "战争", "历史", "纪录片"
]


def load_json(filepath):
    """加载 JSON 文件"""
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_json(filepath, data):
    """保存 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def recommend_by_mood(mood):
    """根据心情推荐电影（使用豆瓣 API）"""
    # 心情对应的搜索关键词
    mood_keywords = {
        "开心": "喜剧",
        "难过": "治愈",
        "放松": "喜剧",
        "刺激": "动作",
        "烧脑": "悬疑",
        "累": "治愈",
        "孤独": "爱情",
        "兴奋": "科幻",
    }
    
    keyword = mood_keywords.get(mood, "治愈")
    movies = search_movie(keyword)
    
    # 过滤并返回 3-5 部
    if movies:
        # 优先选择评分高的
        movies = sorted(movies, key=lambda x: x.get('rating', 0), reverse=True)
        return movies[:min(5, len(movies))]
    
    return []


def recommend_by_type(movie_type):
    """根据类型推荐电影"""
    movies = search_movie(movie_type)
    
    if movies:
        movies = sorted(movies, key=lambda x: x.get('rating', 0), reverse=True)
        return movies[:5]
    
    return []


def get_hot_movies():
    """获取热门电影（Top250）"""
    return get_top250(start=0)


def search_movie_detail(title):
    """搜索并获取电影详情"""
    movies = search_movie(title)
    
    if movies and movies[0].get('id'):
        # 获取详细信息
        detail = get_movie_detail(movies[0]['id'])
        if detail:
            return detail
    
    # 返回基本信息
    return movies[0] if movies else None


def add_watched(title, rating=5, comment=""):
    """添加已看电影"""
    watched = load_json(WATCHED_FILE)
    
    # 检查是否已存在
    if any(m.get("title") == title for m in watched):
        return False, "这部电影已经记录过了"
    
    watched.append({
        "title": title,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "rating": rating,
        "comment": comment
    })
    save_json(WATCHED_FILE, watched)
    return True, "已添加观影记录"


def add_want_to_watch(title):
    """添加想看列表"""
    want_to_watch = load_json(WANT_TO_WATCH_FILE)
    
    # 避免重复
    if any(m.get("title") == title for m in want_to_watch):
        return False, "已经在想看列表里了"
    
    want_to_watch.append({
        "title": title,
        "added_date": datetime.now().strftime("%Y-%m-%d")
    })
    save_json(WANT_TO_WATCH_FILE, want_to_watch)
    return True, "已添加到想看列表"


def get_watched_list():
    """获取已看电影列表"""
    return load_json(WATCHED_FILE)


def get_want_to_watch_list():
    """获取想看列表"""
    return load_json(WANT_TO_WATCH_FILE)


def main(query):
    """主函数"""
    query_lower = query.lower()
    
    # 心情推荐
    for mood in MOOD_MAP.keys():
        if mood in query:
            movies = recommend_by_mood(mood)
            if movies:
                response = f"😊 根据你的**{mood}**心情，推荐这{len(movies)}部电影：\n\n"
                for i, m in enumerate(movies, 1):
                    response += f"{i}. {format_movie_info(m)}\n\n"
                return response
            return f"😅 没找到适合{mood}心情的电影，换个心情试试？"
    
    # 类型推荐
    for t in MOVIE_TYPES:
        if t in query:
            movies = recommend_by_type(t)
            if movies:
                response = f"🎭 **{t}**电影推荐：\n\n"
                for i, m in enumerate(movies, 1):
                    response += f"{i}. {format_movie_info(m)}\n\n"
                return response
            return f"😅 没找到{t}类型的电影"
    
    # 热映/Top250
    if "热映" in query or "top250" in query_lower or "top 250" in query_lower or "榜单" in query:
        movies = get_hot_movies()
        if movies:
            response = "🏆 **豆瓣 Top250** 前 10 名：\n\n"
            for i, m in enumerate(movies[:10], 1):
                stars = "⭐" * int(m.get('rating', 0) / 2)
                response += f"{i}. 《{m['title']}》 {stars} {m['rating']}分 ({m.get('year', '')})\n"
            return response
    
    # 搜索电影/查询评分
    if "查" in query or "评分" in query or "搜索" in query or "找" in query:
        # 尝试提取电影名（简单实现）
        # 优先匹配已知的电影名
        test_titles = ["星际穿越", "盗梦空间", "肖申克", "泰坦尼克", "黑客帝国", 
                       "阿甘正传", "楚门", "海上钢琴师", "教父", "这个杀手"]
        
        found_title = None
        for t in test_titles:
            if t in query:
                found_title = t
                break
        
        if found_title:
            movie = search_movie_detail(found_title)
            if movie:
                return f"🔍 找到电影：\n\n{format_movie_info(movie)}"
        
        # 通用搜索（提取引号内的内容）
        if '"' in query:
            parts = query.split('"')
            if len(parts) > 1:
                movie = search_movie_detail(parts[1])
                if movie:
                    return f"🔍 找到电影：\n\n{format_movie_info(movie)}"
        
        return "😅 没找到这部电影，试试其他名字？"
    
    # 记录观影
    if "看了" in query or "看完" in query or "记录" in query:
        # 简单实现：提取电影名
        success, msg = add_watched("未知电影", comment="自动记录")
        return f"📝 {msg}\n\n（详细记录功能需要指定电影名和评分）"
    
    # 想看
    if "想看" in query or "加入" in query or "收藏" in query:
        success, msg = add_want_to_watch("未知电影")
        return f"📌 {msg}"
    
    # 查看观影记录
    if "观影记录" in query or "看过的电影" in query:
        watched = get_watched_list()
        if watched:
            response = "📚 **观影记录**：\n\n"
            for w in watched[-5:]:
                response += f"🎬 {w['title']} - {w['date']} - {'⭐'*w['rating']}\n"
            return response
        return "📚 暂无观影记录"
    
    # 查看想看列表
    if "想看列表" in query or "待看" in query:
        want = get_want_to_watch_list()
        if want:
            response = "📌 **想看列表**：\n\n"
            for w in want[-5:]:
                response += f"🎬 {w['title']} - {w['added_date']}\n"
            return response
        return "📌 暂无想看列表"
    
    # 默认回复
    return """🎬 电影推荐助手

**功能**：
1. 心情推荐 - "今天有点累，推荐电影"
2. 类型推荐 - "推荐科幻电影"
3. 查询评分 - "查一下星际穿越的评分"
4. 热映榜单 - "看看 Top250"
5. 记录观影 - "我看了 XXX，评分 5 分"
6. 想看清单 - "把 XXX 加入想看"

**支持的心情**：
开心 | 难过 | 放松 | 刺激 | 烧脑 | 累 | 孤独 | 兴奋

**支持的类型**：
剧情 | 喜剧 | 爱情 | 动作 | 科幻 | 悬疑 | 惊悚 | 犯罪 | 动画 | 治愈 | 励志...

告诉我你想做什么？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("🎬 电影推荐助手 - 测试")
    print("=" * 60)
    
    # 测试心情推荐
    print("\n😊 测试：今天有点累，推荐电影")
    print(main("今天有点累，推荐电影"))
    
    print("\n" + "=" * 60)
    print("🏆 测试：看看 Top250")
    print(main("看看 Top250"))
