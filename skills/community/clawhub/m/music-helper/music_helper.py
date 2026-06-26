#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎵 Music Helper - 音乐助手（优化版）
功能：音乐推荐、歌词获取、歌单管理、热门榜单
对接网易云音乐 API
"""

import json
import random
from pathlib import Path
from datetime import datetime

# 导入网易云 API
from netease_api import (
    search_song, get_lyric, get_song_detail,
    get_playlist_recommend, get_top_songs,
    format_song_info
)

# 数据文件路径
DATA_DIR = Path(__file__).parent
FAVORITES_FILE = DATA_DIR / "favorites.json"
PLAYLISTS_FILE = DATA_DIR / "playlists.json"

# 场景对应类型
SCENE_MAP = {
    "学习": ["纯音乐", "古典"],
    "工作": ["纯音乐", "轻音乐"],
    "睡眠": ["纯音乐", "古典", "轻音乐"],
    "运动": ["摇滚", "电子", "说唱"],
    "通勤": ["流行", "民谣"],
    "派对": ["电子", "摇滚", "说唱"],
    "阅读": ["纯音乐", "古典"],
    "开车": ["流行", "摇滚"],
}

# 心情对应类型
MOOD_MAP = {
    "开心": ["流行", "电子"],
    "难过": ["民谣", "抒情"],
    "放松": ["纯音乐", "民谣", "轻音乐"],
    "兴奋": ["摇滚", "电子", "说唱"],
    "治愈": ["纯音乐", "民谣"],
    "emo": ["民谣", "抒情"],
    "孤独": ["抒情", "民谣"],
    "充满能量": ["摇滚", "电子"],
}

# 音乐类型
MUSIC_TYPES = [
    "流行", "摇滚", "民谣", "电子", "古典", "纯音乐",
    "说唱", "爵士", "蓝调", "乡村", "金属", "朋克",
    "抒情", "轻音乐", "新世纪", "原声"
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


def recommend_by_scene(scene):
    """根据场景推荐"""
    # 直接搜索场景关键词
    songs = search_song(scene, limit=5)
    if songs:
        return songs[:5]
    return []


def recommend_by_mood(mood):
    """根据心情推荐"""
    # 搜索心情关键词
    songs = search_song(mood, limit=5)
    if songs:
        return songs[:5]
    return []


def recommend_by_type(music_type):
    """根据类型推荐"""
    songs = search_song(music_type, limit=5)
    if songs:
        return songs[:5]
    return []


def get_hot_songs():
    """获取热门歌曲（飙升榜）"""
    return get_top_songs(playlist_id=3778678)


def get_new_songs():
    """获取新歌"""
    return get_top_songs(playlist_id=3779629)


def search_song_detail(keyword):
    """搜索并获取歌曲详情"""
    songs = search_song(keyword, limit=1)
    
    if songs and songs[0].get('id'):
        detail = get_song_detail(songs[0]['id'])
        if detail:
            return detail
    
    return songs[0] if songs else None


def get_song_lyric(keyword):
    """获取歌曲歌词"""
    songs = search_song(keyword, limit=1)
    
    if songs and songs[0].get('id'):
        return get_lyric(songs[0]['id'])
    
    return "暂无歌词~"


def add_favorite(title, artist=""):
    """添加收藏"""
    favorites = load_json(FAVORITES_FILE)
    
    # 检查是否已存在
    if any(s.get("name") == title for s in favorites):
        return False, "这首歌已经收藏过了"
    
    favorites.append({
        "name": title,
        "artist": artist,
        "added_date": datetime.now().strftime("%Y-%m-%d"),
        "play_count": 1
    })
    save_json(FAVORITES_FILE, favorites)
    return True, "已添加到收藏"


def remove_favorite(title):
    """取消收藏"""
    favorites = load_json(FAVORITES_FILE)
    
    for i, song in enumerate(favorites):
        if song.get("name") == title:
            favorites.pop(i)
            save_json(FAVORITES_FILE, favorites)
            return True, "已取消收藏"
    
    return False, "未找到这首歌"


def create_playlist(name, songs):
    """创建歌单"""
    playlists = load_json(PLAYLISTS_FILE)
    
    # 检查是否已存在
    if any(p.get("name") == name for p in playlists):
        return False, "歌单名已存在"
    
    playlists.append({
        "name": name,
        "songs": songs,
        "created_date": datetime.now().strftime("%Y-%m-%d")
    })
    save_json(PLAYLISTS_FILE, playlists)
    return True, f"已创建歌单《{name}》"


def get_favorites():
    """获取收藏列表"""
    return load_json(FAVORITES_FILE)


def get_playlists():
    """获取歌单列表"""
    return load_json(PLAYLISTS_FILE)


def main(query):
    """主函数"""
    query_lower = query.lower()
    
    # 场景推荐
    for scene in SCENE_MAP.keys():
        if scene in query:
            songs = recommend_by_scene(scene)
            if songs:
                response = f"🎧 适合**{scene}**的音乐：\n\n"
                for i, s in enumerate(songs, 1):
                    response += f"{i}. {format_song_info(s)}\n\n"
                return response
            return f"😅 没找到适合{scene}场景的音乐"
    
    # 心情推荐
    for mood in MOOD_MAP.keys():
        if mood in query:
            songs = recommend_by_mood(mood)
            if songs:
                response = f"😊 根据你的**{mood}**心情，推荐：\n\n"
                for i, s in enumerate(songs, 1):
                    response += f"{i}. {format_song_info(s)}\n\n"
                return response
            return f"😅 没找到适合{mood}心情的音乐"
    
    # 类型推荐
    for t in MUSIC_TYPES:
        if t in query:
            songs = recommend_by_type(t)
            if songs:
                response = f"🎵 **{t}**音乐推荐：\n\n"
                for i, s in enumerate(songs, 1):
                    response += f"{i}. {format_song_info(s)}\n\n"
                return response
            return f"😅 没找到{t}类型的音乐"
    
    # 热门榜单
    if "热门" in query or "榜单" in query or "飙升" in query or "top" in query_lower:
        songs = get_hot_songs()
        if songs:
            response = "🔥 **网易云飙升榜** 前 10 首：\n\n"
            for i, s in enumerate(songs[:10], 1):
                name = s.get("name", "未知")
                artists = ", ".join([a.get("name", "") for a in s.get("artists", [])])
                response += f"{i}. 《{name}》- {artists}\n"
            return response
    
    # 新歌推荐
    if "新歌" in query:
        songs = get_new_songs()
        if songs:
            response = "🆕 **网易云新歌榜** 前 10 首：\n\n"
            for i, s in enumerate(songs[:10], 1):
                name = s.get("name", "未知")
                artists = ", ".join([a.get("name", "") for a in s.get("artists", [])])
                response += f"{i}. 《{name}》- {artists}\n"
            return response
    
    # 搜索歌曲/查询歌词
    if "查" in query or "歌词" in query or "搜索" in query or "找" in query:
        # 尝试提取歌曲名
        test_titles = ["晴天", "十年", "海阔天空", "成都", "起风了", 
                       "光年之外", "追梦赤子心", "南山南", "Summer", "Faded"]
        
        found_title = None
        for t in test_titles:
            if t in query:
                found_title = t
                break
        
        if found_title:
            song = search_song_detail(found_title)
            if song:
                info = f"🎵 《{song.get('name', found_title)}》\n"
                info += f"🎤 歌手：{song.get('artists', '未知')}\n"
                if song.get('album'):
                    info += f"📀 专辑：{song['album']}\n"
                if song.get('duration'):
                    minutes = song['duration'] // 60
                    seconds = song['duration'] % 60
                    info += f"⏱️ 时长：{minutes}:{seconds:02d}\n"
                
                if "歌词" in query:
                    lyric = get_song_lyric(found_title)
                    info += f"\n📝 歌词：\n{lyric}"
                
                return info
        
        # 通用搜索
        if '"' in query:
            parts = query.split('"')
            if len(parts) > 1:
                song = search_song_detail(parts[1])
                if song:
                    return f"🎵 找到歌曲：\n{format_song_info(song)}"
        
        return "😅 没找到这首歌，试试其他名字？"
    
    # 收藏
    if "收藏" in query or "喜欢" in query:
        # 简单实现
        success, msg = add_favorite("未知歌曲")
        return f"❤️ {msg}\n\n（详细收藏功能需要指定歌曲名）"
    
    # 查看收藏
    if "我的收藏" in query or "收藏列表" in query:
        favorites = get_favorites()
        if favorites:
            response = "❤️ **我的收藏**：\n\n"
            for f in favorites[-10:]:
                response += f"🎵 {f['name']} - {f.get('artist', '')}\n"
            return response
        return "❤️ 暂无收藏"
    
    # 查看歌单
    if "歌单" in query and "列表" in query:
        playlists = get_playlists()
        if playlists:
            response = "📋 **我的歌单**：\n\n"
            for p in playlists:
                response += f"🎵 《{p['name']}》- {len(p['songs'])}首 ({p['created_date']})\n"
            return response
        return "📋 暂无歌单"
    
    # 默认回复
    return """🎵 音乐助手

**功能**：
1. 场景推荐 - "学习时听什么"
2. 心情推荐 - "难过的歌"
3. 类型推荐 - "推荐摇滚"
4. 热门榜单 - "看看飙升榜"
5. 查询歌曲 - "查一下晴天"
6. 查看歌词 - "晴天的歌词"
7. 收藏歌曲 - "收藏晴天"
8. 我的歌单 - "查看收藏列表"

**支持的心情**：
开心 | 难过 | 放松 | 兴奋 | 治愈 | emo | 孤独 | 充满能量

**支持的场景**：
学习 | 工作 | 睡眠 | 运动 | 通勤 | 派对 | 阅读 | 开车

**支持的类型**：
流行 | 摇滚 | 民谣 | 电子 | 古典 | 纯音乐 | 说唱 | 爵士...

告诉我你想听什么？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("🎵 音乐助手 - 测试")
    print("=" * 60)
    
    print("\n🎧 测试：学习的时候听什么")
    print(main("学习的时候听什么"))
    
    print("\n" + "=" * 60)
    print("🔥 测试：看看飙升榜")
    print(main("看看飙升榜"))
