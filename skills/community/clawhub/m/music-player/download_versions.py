# -*- coding: utf-8 -*-
"""
下载音乐 - 指定版本
"""

import requests
import json
import sys
import os

def search_music(query, limit=10):
    """搜索音乐"""
    print(f"正在搜索：{query}...")
    
    url = f"https://music.163.com/api/search/get"
    params = {
        's': query,
        'type': 1,
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

def download_music(song_id, save_path):
    """下载音乐"""
    print(f"正在下载：{save_path}")
    
    url = f"https://music.163.com/song/media/outer/url?id={song_id}.mp3"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=30, allow_redirects=True)
        
        print(f"状态码：{response.status_code}")
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
            
            print(f"下载成功：{save_path} ({downloaded/1024/1024:.2f} MB)")
            return True
        else:
            print(f"下载失败，状态码：{response.status_code}")
            return False
    except Exception as e:
        print(f"下载失败：{e}")
        return False

def main():
    query = "One by One"
    save_base = "C:\\Users\\Administrator\\.openclaw\\workspace\\music\\"
    
    results = search_music(query, limit=10)
    
    if not results:
        return
    
    print("\n搜索结果:")
    for i, song in enumerate(results, 1):
        print(f"{i}. {song['name']} - {song['artists']} ({song['album']}) [{song['duration']}秒]")
    
    # 下载前 3 个版本
    for i, song in enumerate(results[:3], 1):
        safe_name = f"{song['artists']}_{song['name']}".replace('/', '_').replace('\\', '_')
        save_path = f"{save_base}{safe_name}.mp3"
        
        print(f"\n=== 下载版本 {i}: {song['name']} - {song['artists']} ===")
        
        if download_music(song['id'], save_path):
            print(f"✓ 版本 {i} 下载成功")
        else:
            print(f"✗ 版本 {i} 下载失败")

if __name__ == '__main__':
    main()
