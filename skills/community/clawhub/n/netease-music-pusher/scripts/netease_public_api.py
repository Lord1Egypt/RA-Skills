#!/usr/bin/env python3
"""
网易云音乐API - 使用公开API获取榜单数据
无需登录，获取飙升榜、新歌榜等
"""
import requests
import json
from datetime import datetime

class NeteasePublicAPI:
    """网易云公开API - 无需登录"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://music.163.com/'
        })
    
    def get_toplist_detail(self, list_id):
        """获取榜单详情"""
        url = f'https://music.163.com/api/playlist/detail?id={list_id}'
        try:
            response = self.session.get(url, timeout=10)
            result = response.json()
            if result.get('code') == 200:
                playlist = result.get('result', {})
                tracks = playlist.get('tracks', [])
                return {
                    'name': playlist.get('name', '未知榜单'),
                    'tracks': tracks[:10]
                }
            return None
        except Exception as e:
            print(f"❌ 获取失败: {e}")
            return None
    
    def get_toplist(self, name='飙升榜'):
        """获取指定榜单"""
        # 网易云榜单ID
        lists = {
            '飙升榜': 19723756,
            '新歌榜': 3779629,
            '原创榜': 2884035,
            '热歌榜': 3778678,
            '黑胶VIP爱听榜': 5453912201,
            '云音乐说唱榜': 991319590,
            '云音乐古典榜': 71385702
        }
        
        list_id = lists.get(name, 19723756)
        return self.get_toplist_detail(list_id)

def format_song_list(data, date_str=None):
    """格式化歌曲列表为推送文本"""
    if not data or not data.get('tracks'):
        return "❌ 暂无数据"
    
    name = data.get('name', '榜单')
    tracks = data['tracks']
    date = date_str or datetime.now().strftime('%m月%d日')
    
    lines = [
        f"🎵 网易云音乐 | {name}",
        f"📅 {date}",
        "=" * 40,
        ""
    ]
    
    for i, track in enumerate(tracks[:10], 1):
        song_name = track.get('name', '未知')
        artists = track.get('artists', [])
        artist_names = ' / '.join([a.get('name', '未知') for a in artists[:2]])
        
        # 获取专辑名
        album = track.get('album', {})
        album_name = album.get('name', '')
        
        lines.append(f"{i:2d}. {song_name}")
        lines.append(f"    🎤 {artist_names}")
        if album_name and album_name != song_name:
            lines.append(f"    💿 {album_name}")
        lines.append("")
    
    lines.extend([
        "─" * 40,
        "🎧 打开网易云音乐App收听完整版",
        "💬 有好听的歌记得分享给我哦～"
    ])
    
    return '\n'.join(lines)

def push_daily():
    """推送每日榜单"""
    api = NeteasePublicAPI()
    data = api.get_toplist('飙升榜')
    if data:
        return format_song_list(data)
    return "❌ 获取榜单失败"

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'daily':
            print(push_daily())
        elif cmd in ['飙升榜', '新歌榜', '原创榜', '热歌榜']:
            api = NeteasePublicAPI()
            data = api.get_toplist(cmd)
            print(format_song_list(data))
        else:
            print(f"未知命令: {cmd}")
            print("可用: daily, 飙升榜, 新歌榜, 原创榜, 热歌榜")
    else:
        print(push_daily())
