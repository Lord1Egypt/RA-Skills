# -*- coding: utf-8 -*-
"""
使用 go-music-api 下载音乐
参考：https://github.com/caorushizi/go-music-api
"""

import requests
import json
import sys
import os

# go-music-api 的公开 API 端点（多个备选）
API_BASES = [
    "https://music-api.caorushizi.cn",
    "https://api.uomg.com",
    "https://music.163.com/api",
]

def search_music(query, limit=5):
    """搜索音乐 - 使用 go-music-api"""
    print(f"正在搜索：{query}...")
    
    for base in API_BASES:
        try:
            if 'caorushizi' in base:
                # go-music-api 格式
                url = f"{base}/api/search"
                params = {'keyword': query, 'limit': limit}
            elif 'uomg' in base:
                # UOMG API
                url = f"{base}/api/search"
                params = {'keyword': query, 'limit': limit}
            else:
                # 网易云 API
                url = f"{base}/search/get"
                params = {'s': query, 'type': 1, 'limit': limit}
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://music.163.com/'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            data = response.json()
            
            # 解析不同 API 的响应格式
            results = []
            if 'result' in data and 'songs' in data['result']:
                # 网易云格式
                for song in data['result']['songs']:
                    results.append({
                        'id': song['id'],
                        'name': song['name'],
                        'artists': ', '.join([a['name'] for a in song.get('artists', [])]),
                        'album': song.get('album', {}).get('name', ''),
                        'duration': song.get('duration', 0) // 1000
                    })
            elif 'data' in data:
                # go-music-api 格式
                song_data = data['data']
                if isinstance(song_data, list):
                    for song in song_data:
                        results.append({
                            'id': song.get('id', ''),
                            'name': song.get('name', ''),
                            'artists': song.get('artist', ''),
                            'album': song.get('album', ''),
                            'duration': song.get('duration', 0)
                        })
            
            if results:
                return results
                
        except Exception as e:
            print(f"API {base} 失败：{e}")
            continue
    
    print("所有 API 都失败了")
    return []

def download_music(song_id, save_path):
    """下载音乐"""
    print(f"正在下载：{save_path}")
    
    # 使用网易云外链
    url = f"https://music.163.com/song/media/outer/url?id={song_id}.mp3"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=30, allow_redirects=True)
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            
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
    query = "One by One Enya"
    save_path = "C:\\Users\\Administrator\\.openclaw\\workspace\\music\\Enya_One_by_One_go.mp3"
    
    results = search_music(query)
    
    if not results:
        print("未找到歌曲")
        return
    
    print("\n搜索结果:")
    for i, song in enumerate(results, 1):
        print(f"{i}. {song['name']} - {song['artists']} ({song['album']})")
    
    if results:
        song = results[0]
        print(f"\n选择：{song['name']} - {song['artists']}")
        
        if download_music(song['id'], save_path):
            print(f"\n文件已保存：{save_path}")

if __name__ == '__main__':
    main()
