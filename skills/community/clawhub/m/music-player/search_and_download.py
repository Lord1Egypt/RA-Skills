# -*- coding: utf-8 -*-
"""
搜索并下载音乐
用法：python search_and_download.py "歌曲名" "保存路径.mp3"
"""

import requests
import json
import sys
import os

def search_music(query, limit=5):
    """搜索音乐"""
    print(f"正在搜索：{query}...")
    
    # 使用公开的网易云音乐 API（示例）
    # 实际使用时可以替换为其他 API
    url = f"https://music.163.com/api/search/get"
    params = {
        's': query,
        'type': 1,  # 1: 单曲
        'limit': limit,
        'offset': 0
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://music.163.com/'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if data.get('code') == 200 and data.get('result'):
            songs = data['result'].get('songs', [])
            results = []
            
            for song in songs:
                results.append({
                    'id': song['id'],
                    'name': song['name'],
                    'artists': ', '.join([a['name'] for a in song.get('artists', [])]),
                    'album': song.get('album', {}).get('name', ''),
                    'duration': song.get('duration', 0) // 1000
                })
            
            return results
        else:
            print("未找到相关歌曲")
            return []
    except Exception as e:
        print(f"搜索失败：{e}")
        return []

def get_song_url(song_id):
    """获取歌曲播放 URL"""
    url = "https://music.163.com/song/media/outer/url"
    params = {'id': song_id}
    
    try:
        # 获取重定向后的 URL
        response = requests.get(url, params=params, allow_redirects=False, timeout=10)
        if response.status_code == 302:
            return response.headers['Location']
    except:
        pass
    
    # 备用方案：直接返回网易云外链
    return f"https://music.163.com/song/media/outer/url?id={song_id}.mp3"

def download_music(url, save_path):
    """下载音乐"""
    print(f"正在下载：{save_path}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Range': 'bytes=0-'
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        
        if response.status_code == 200:
            # 确保目录存在
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"下载成功：{save_path}")
            return True
        else:
            print(f"下载失败，状态码：{response.status_code}")
            return False
    except Exception as e:
        print(f"下载失败：{e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("用法：python search_and_download.py \"歌曲名\" [保存路径.mp3]")
        print("示例：python search_and_download.py \"稻香\" \"C:\\music\\daoxiang.mp3\"")
        return
    
    query = sys.argv[1]
    save_path = sys.argv[2] if len(sys.argv) > 2 else f"./{query}.mp3"
    
    # 搜索
    results = search_music(query)
    
    if not results:
        return
    
    # 显示结果
    print("\n搜索结果:")
    for i, song in enumerate(results, 1):
        print(f"{i}. {song['name']} - {song['artists']} ({song['album']}) [{song['duration']}秒]")
    
    # 选择第一首
    if results:
        choice = 0  # 默认选第一首
        song = results[choice]
        print(f"\n选择：{song['name']} - {song['artists']}")
        
        # 获取 URL
        url = get_song_url(song['id'])
        print(f"播放 URL: {url[:50]}...")
        
        # 下载
        if download_music(url, save_path):
            print(f"\n文件已保存：{save_path}")
            print("使用 play_music.py 播放此文件")

if __name__ == '__main__':
    main()
