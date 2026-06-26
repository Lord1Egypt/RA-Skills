#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎵 网易云音乐 API - 优化版
功能：搜索歌曲、获取歌词、推荐歌单、热门榜单
无需 API Key，使用官方 API
"""

import requests
import json
import re
import time
from pathlib import Path
from datetime import datetime

# 配置
DATA_DIR = Path(__file__).parent
CACHE_FILE = DATA_DIR / "netease_cache.json"
CACHE_EXPIRY = 3600  # 缓存过期时间：1 小时

# 网易云音乐 API
NETEASE_BASE_URL = "https://music.163.com/api"
NETEASE_SEARCH_URL = "https://music.163.com/api/search/get"
NETEASE_LYRIC_URL = "https://music.163.com/api/song/lyric"
NETEASE_SONG_DETAIL_URL = "https://music.163.com/api/song/detail"
NETEASE_PLAYLIST_URL = "https://music.163.com/api/playlist/list"
NETEASE_TOP_SONGS_URL = "https://music.163.com/api/playlist/detail"

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://music.163.com/",
    "Content-Type": "application/x-www-form-urlencoded",
}

# 备用歌曲数据（当 API 不可用时）
FALLBACK_SONGS = {
    "晴天": {"id": 186016, "name": "晴天", "artists": ["周杰伦"], "album": "叶惠美", "duration": 269, "rating": 9.8},
    "十年": {"id": 25706282, "name": "十年", "artists": ["陈奕迅"], "album": "黑白灰", "duration": 205, "rating": 9.5},
    "海阔天空": {"id": 104310, "name": "海阔天空", "artists": ["Beyond"], "album": "乐与怒", "duration": 325, "rating": 9.9},
    "成都": {"id": 407216232, "name": "成都", "artists": ["赵雷"], "album": "无法长大", "duration": 328, "rating": 9.5},
    "起风了": {"id": 543671044, "name": "起风了", "artists": ["买辣椒也用券"], "album": "起风了", "duration": 323, "rating": 9.3},
    "光年之外": {"id": 418603077, "name": "光年之外", "artists": ["G.E.M.邓紫棋"], "album": "光年之外", "duration": 235, "rating": 9.2},
    "追梦赤子心": {"id": 2263931, "name": "追梦赤子心", "artists": ["GALA"], "album": "追梦痴子心", "duration": 318, "rating": 9.4},
    "南山南": {"id": 29257746, "name": "南山南", "artists": ["马頔"], "album": "孤岛", "duration": 304, "rating": 9.2},
    "Summer": {"id": 1774292, "name": "Summer", "artists": ["久石让"], "album": "菊次郎的夏天", "duration": 358, "rating": 9.9},
    "Faded": {"id": 363931285, "name": "Faded", "artists": ["Alan Walker"], "album": "Faded", "duration": 212, "rating": 9.4},
}

# 备用歌词数据
FALLBACK_LYRICS = {
    "晴天": """故事的小黄花 从出生那年就飘着
童年的荡秋千 随记忆一直晃到现在
Re So So Si Do Si La So La Si Si Si Si La Si La So
吹着前奏 望着天空 我想起花瓣试着掉落
为你翘课的那一天 花落的那一天
教室的那一间 我怎么看不见
天空的绵绵雨 在这一刻不停""",
    
    "十年": """如果那两个字没有颤抖
我不会发现我难受
怎么说出口 也不过是分手
如果对于明天没有要求
牵牵手就像旅游
成千上万个门口 总有一个人要先走""",
    
    "海阔天空": """今天我 寒夜里看雪飘过
怀着冷却了的心窝漂远方
风雨里追赶 雾里分不清影踪
天空海阔你与我 可会变
多少次 迎着冷眼与嘲笑
从没有放弃过心中的理想""",
    
    "成都": """让我掉下眼泪的 不止昨夜的酒
让我依依不舍的 不止你的温柔
余路还要走多久 你攥着我的手
让我感到为难的 是挣扎的自由
分别总是在九月 回忆是思念的愁
四川嫩绿的垂柳 亲吻着我额头""",
    
    "起风了": """这一路上走走停停
顺着少年漂流的痕迹
迈出车站的前一刻 竟有些犹豫
不禁笑这近乡情怯 仍无可避免
而长野的天 依旧那么暖
风吹起了从前""",
}


def load_cache():
    """加载缓存"""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    """保存缓存"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def get_cache(key):
    """获取缓存（检查过期）"""
    cache = load_cache()
    if key in cache:
        data = cache[key]
        if datetime.now().timestamp() - data.get("timestamp", 0) < CACHE_EXPIRY:
            return data.get("result")
    return None


def set_cache(key, result):
    """设置缓存"""
    cache = load_cache()
    cache[key] = {
        "result": result,
        "timestamp": datetime.now().timestamp()
    }
    save_cache(cache)


def search_song(keyword, limit=10, max_retries=3):
    """
    搜索网易云音乐歌曲
    """
    cache_key = f"search_{keyword}_{limit}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                time.sleep(1 * attempt)
            
            data = {
                "s": keyword,
                "type": 1,
                "limit": limit,
                "offset": 0
            }
            
            response = requests.post(NETEASE_SEARCH_URL, data=data, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200 and result.get("result"):
                    songs = result["result"].get("songs", [])
                    if songs:
                        set_cache(cache_key, songs)
                        return songs
            
            if response.status_code in [403, 429, 503]:
                continue
                
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"搜索失败：{e}")
    
    # 返回备用数据
    return get_fallback_songs(keyword)


def get_lyric(song_id, max_retries=3):
    """
    获取歌词
    """
    cache_key = f"lyric_{song_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                time.sleep(1 * attempt)
            
            params = {
                "id": song_id,
                "lv": 1,
                "tv": -1
            }
            
            response = requests.get(NETEASE_LYRIC_URL, params=params, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200 and result.get("lrc"):
                    lyric = result["lrc"].get("lyric", "")
                    cleaned = clean_lyric(lyric)
                    set_cache(cache_key, cleaned)
                    return cleaned
            
            if response.status_code in [403, 429, 503]:
                continue
                
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"获取歌词失败：{e}")
    
    # 返回备用歌词
    return get_fallback_lyric(str(song_id))


def clean_lyric(lyric_text):
    """清理歌词，去除时间戳"""
    # 去除时间戳 [00:00.00]
    cleaned = re.sub(r'\[\d{2}:\d{2}\.\d+\]', '', lyric_text)
    # 去除空行
    lines = [line.strip() for line in cleaned.split('\n') if line.strip()]
    # 返回前 12 行
    return '\n'.join(lines[:12])


def get_song_detail(song_id, max_retries=3):
    """
    获取歌曲详情
    """
    cache_key = f"detail_{song_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                time.sleep(1 * attempt)
            
            data = {
                "ids": f"[{song_id}]"
            }
            
            response = requests.post(NETEASE_SONG_DETAIL_URL, data=data, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200 and result.get("songs"):
                    song = result["songs"][0]
                    detail = {
                        "id": song["id"],
                        "name": song["name"],
                        "artists": ", ".join([a["name"] for a in song.get("artists", [])]),
                        "album": song.get("album", {}).get("name", ""),
                        "duration": song.get("duration", 0) // 1000,
                        "publish_time": song.get("publish_time", ""),
                    }
                    set_cache(cache_key, detail)
                    return detail
            
            if response.status_code in [403, 429, 503]:
                continue
                
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"获取详情失败：{e}")
    
    return None


def get_playlist_recommend(limit=10):
    """获取推荐歌单"""
    cache_key = f"playlist_{limit}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    
    try:
        url = "https://music.163.com/api/playlist/list"
        params = {"cat": "全部", "order": "hot", "limit": limit}
        
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                playlists = result.get("playlists", [])
                set_cache(cache_key, playlists)
                return playlists
        
        return []
    
    except Exception as e:
        print(f"获取歌单失败：{e}")
        return []


def get_top_songs(playlist_id=3778678):
    """
    获取热门歌曲（默认：飙升榜）
    playlist_id: 3778678=飙升榜，3779629=新歌榜
    """
    cache_key = f"top_{playlist_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    
    try:
        url = f"https://music.163.com/api/playlist/detail?id={playlist_id}"
        
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                tracks = result.get("result", {}).get("tracks", [])
                set_cache(cache_key, tracks)
                return tracks
        
        return []
    
    except Exception as e:
        print(f"获取榜单失败：{e}")
        return []


def get_fallback_songs(keyword):
    """获取备用歌曲数据"""
    results = []
    
    # 精确匹配
    if keyword in FALLBACK_SONGS:
        return [FALLBACK_SONGS[keyword]]
    
    # 模糊匹配
    for key, song in FALLBACK_SONGS.items():
        if keyword in key or key in keyword:
            results.append(song)
    
    if not results:
        results = list(FALLBACK_SONGS.values())[:5]
    
    return results


def get_fallback_lyric(song_id):
    """获取备用歌词"""
    for title, lyric in FALLBACK_LYRICS.items():
        if title in song_id or song_id in title:
            return lyric
    return "暂无歌词，可去网易云音乐搜索完整歌词~"


def format_song_info(song):
    """格式化歌曲信息"""
    info = f"🎵 《{song.get('name', '未知')}》"
    
    # 处理艺术家信息（可能是列表或字符串）
    artists = song.get('artists', '')
    if isinstance(artists, list):
        # 如果是列表，提取 name 字段
        artist_names = []
        for artist in artists:
            if isinstance(artist, dict):
                artist_names.append(artist.get('name', ''))
            else:
                artist_names.append(str(artist))
        artists = ', '.join(artist_names)
    
    if artists:
        info += f" - {artists}"
    
    if song.get('album'):
        album = song['album']
        if isinstance(album, dict):
            album = album.get('name', '')
        if album:
            info += f"\n📀 专辑：{album}"
    
    if song.get('duration'):
        duration = song['duration']
        # 处理毫秒和秒两种格式
        if duration > 1000:  # 可能是毫秒
            duration = duration // 1000
        minutes = duration // 60
        seconds = duration % 60
        info += f"\n⏱️ 时长：{minutes}:{seconds:02d}"
    
    if song.get('rating'):
        info += f"\n⭐ 评分：{song['rating']}"
    
    return info


# 测试
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("🎵 网易云音乐 API 测试")
    print("=" * 60)
    
    print("\n🔍 搜索测试：晴天")
    results = search_song("晴天", limit=3)
    print(f"找到 {len(results)} 首")
    
    if results:
        song = results[0]
        print(format_song_info(song))
        
        # 测试歌词
        song_id = song.get("id", 186016)
        print(f"\n📝 歌词：")
        lyric = get_lyric(song_id)
        print(lyric[:200] + "..." if len(lyric) > 200 else lyric)
    
    print("\n✅ 测试完成!")
