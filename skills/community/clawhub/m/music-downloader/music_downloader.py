#!/usr/bin/env python3
"""
音乐下载工具 - 多源搜索下载
支持: thttt, kugou, kuwo, netease, qq, 5nd, 1ting, 9ku, musicenc, gequbao
"""

import requests
import re
import json
import os
import time
import warnings
from urllib.parse import quote, unquote
from typing import Optional, List, Dict
from random import random

warnings.filterwarnings('ignore')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

class MusicDownloader:
    """音乐下载器 - 多源自动切换"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.sources = ['thttt', 'kugou', 'kuwo', 'netease', 'qq', 'gequbao', '5nd', '1ting', '9ku', 'musicenc']
    
    # ============ 音源1: thttt.com ============
    def search_thttt(self, keyword: str) -> List[Dict]:
        try:
            url = f"https://www.thttt.com/so.php?wd={quote(keyword)}"
            resp = self.session.get(url, timeout=15, verify=False)
            html = resp.text
            
            songs = []
            pattern = r'<a href="/mp3/([a-f0-9]+)\.html"[^>]*>(.*?)</a>'
            matches = re.findall(pattern, html)
            
            for hash_code, title_html in matches[:15]:
                title = re.sub(r'<[^>]+>', '', title_html).strip()
                if not title or re.match(r'^\d+:\d+$', title):
                    continue
                if ' - ' in title:
                    parts = title.split(' - ', 1)
                    artist, name = parts[0].strip(), parts[1].strip()
                else:
                    artist, name = "未知", title
                if name.lower() == 'mv':
                    continue
                songs.append({'hash': hash_code, 'name': name, 'artist': artist, 'source': 'thttt'})
            
            return list({s['hash']: s for s in songs}.values())
        except Exception as e:
            print(f"   thttt失败: {e}")
            return []
    
    def get_url_thttt(self, hash_code: str) -> Optional[str]:
        try:
            url = "https://www.thttt.com/style/js/play.php"
            resp = self.session.post(url, data={'id': hash_code, 'type': 'dance'}, timeout=15, verify=False)
            result = resp.json()
            return result.get('url') if result.get('msg') == 1 else None
        except:
            return None
    
    # ============ 音源2: kugou.com ============
    def search_kugou(self, keyword: str) -> List[Dict]:
        try:
            url = f"https://complexsearch.kugou.com/v2/search/song?keyword={quote(keyword)}&page=1&pagesize=15"
            resp = self.session.get(url, timeout=15, verify=False)
            data = resp.json()
            songs = []
            for item in data.get('data', {}).get('lists', []):
                songs.append({
                    'hash': item.get('FileHash', ''),
                    'name': item.get('SongName', ''),
                    'artist': item.get('SingerName', ''),
                    'source': 'kugou'
                })
            return songs
        except Exception as e:
            print(f"   酷狗失败: {e}")
            return []
    
    def get_url_kugou(self, hash_code: str) -> Optional[str]:
        try:
            url = f"https://www.kugou.com/yy/html/singer.html?hash={hash_code}"
            resp = self.session.get(url, timeout=15, verify=False)
            match = re.search(r'"play_url":"([^"]+)"', resp.text)
            return match.group(1).replace('\\/', '/') if match else None
        except:
            return None
    
    # ============ 音源3: kuwo.cn ============
    def search_kuwo(self, keyword: str) -> List[Dict]:
        try:
            url = f"https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={quote(keyword)}&pn=1&rn=15"
            resp = self.session.get(url, headers={"Referer": "https://www.kuwo.cn"}, timeout=15, verify=False)
            data = resp.json()
            songs = []
            for item in data.get('data', {}).get('list', []):
                songs.append({
                    'rid': item.get('rid', ''),
                    'name': item.get('name', ''),
                    'artist': item.get('artist', ''),
                    'source': 'kuwo'
                })
            return songs
        except Exception as e:
            print(f"   酷我失败: {e}")
            return []
    
    def get_url_kuwo(self, rid: str) -> Optional[str]:
        try:
            url = f"https://www.kuwo.cn/api/v1/www/music/playInfo?mid={rid}&type=music&httpsStatus=1"
            resp = self.session.get(url, timeout=15, verify=False)
            return resp.json().get('data', {}).get('url', '')
        except:
            return None
    
    # ============ 音源4: 网易云 ============
    def search_netease(self, keyword: str) -> List[Dict]:
        try:
            url = f"https://music.163.com/api/search/get?s={quote(keyword)}&type=1&offset=0&limit=15"
            headers = {"Referer": "https://music.163.com"}
            resp = self.session.get(url, headers=headers, timeout=15, verify=False)
            data = resp.json()
            songs = []
            for item in data.get('result', {}).get('songs', []):
                artists = ', '.join([a.get('name', '') for a in item.get('ar', [])])
                songs.append({
                    'id': item.get('id', ''),
                    'name': item.get('name', ''),
                    'artist': artists,
                    'source': 'netease'
                })
            return songs
        except Exception as e:
            print(f"   网易云失败: {e}")
            return []
    
    def get_url_netease(self, song_id: str) -> Optional[str]:
        try:
            # 方法1: 直链
            url = f"https://music.163.com/song/media/outer/url?id={song_id}"
            resp = self.session.get(url, timeout=15, verify=False, allow_redirects=False)
            if resp.status_code == 302:
                loc = resp.headers.get('Location', '')
                if 'music.126.net' in loc:
                    return loc
            # 方法2: 通过详情API
            url = f"https://music.163.com/api/song/enhance/player/url?ids=[{song_id}]&br=320000"
            resp = self.session.get(url, headers={"Referer": "https://music.163.com"}, timeout=15, verify=False)
            data = resp.json()
            return data.get('data', [{}])[0].get('url', '')
        except:
            return None
    
    # ============ 音源5: QQ音乐 ============
    def search_qq(self, keyword: str) -> List[Dict]:
        try:
            url = f"https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=15&w={quote(keyword)}&format=json"
            resp = self.session.get(url, timeout=15, verify=False)
            data = resp.json()
            songs = []
            for item in data.get('data', {}).get('song', {}).get('list', []):
                artists = ', '.join([s.get('name', '') for s in item.get('singer', [])])
                songs.append({
                    'mid': item.get('songmid', ''),
                    'name': item.get('songname', ''),
                    'artist': artists,
                    'source': 'qq'
                })
            return songs
        except Exception as e:
            print(f"   QQ音乐失败: {e}")
            return []
    
    def get_url_qq(self, songmid: str) -> Optional[str]:
        try:
            # QQ音乐需要特殊签名，这里使用简化方案
            # 通过搜索页面的播放链接
            url = f"https://y.qq.com/n/ryqq/songDetail/{songmid}"
            resp = self.session.get(url, timeout=15, verify=False)
            # 尝试提取音频链接
            match = re.search(r'"url":"(https?://[^"]+\.m4a[^"]*)"', resp.text)
            if match:
                return match.group(1).replace('\\/', '/')
            # 备用方案：使用ws关联接口
            url = f"https://u.y.qq.com/cgi-bin/musicu.fcg?data={quote(json.dumps({'req': {'module': 'CDN.SrfCdnDispatchServer', 'method': 'GetCdnDispatch', 'param': {'guid': '1234567890', 'calltype': 0, 'userip': ''}}, 'req_0': {'module': 'vkey.GetVkeyServer', 'method': 'CgiGetVkey', 'param': {'guid': '1234567890', 'songmid': [songmid], 'songtype': [0], 'uin': '0', 'loginflag': 1, 'platform': '20'}}}, ensure_ascii=False))}"
            resp = self.session.get(url, timeout=15, verify=False)
            data = resp.json()
            purl = data.get('req_0', {}).get('data', {}).get('midurlinfo', [{}])[0].get('purl', '')
            sip = data.get('req', {}).get('data', {}).get('sip', [''])[0]
            if sip and purl:
                return sip + purl
        except:
            return None
        return None
    
    # ============ 音源6: gequbao.com ============
    def search_gequbao(self, keyword: str) -> List[Dict]:
        try:
            url = f"https://www.gequbao.com/s/{quote(keyword)}"
            resp = self.session.get(url, timeout=15, verify=False)
            songs = []
            pattern = r'data-id="(\d+)"[^>]*data-name="([^"]*)"[^>]*data-singer="([^"]*)"'
            for song_id, name, singer in re.findall(pattern, resp.text)[:15]:
                songs.append({'id': song_id, 'name': name.strip(), 'artist': singer.strip(), 'source': 'gequbao'})
            return songs
        except Exception as e:
            print(f"   歌曲宝失败: {e}")
            return []
    
    def get_url_gequbao(self, song_id: str) -> Optional[str]:
        try:
            url = f"https://www.gequbao.com/api/song/url?id={song_id}"
            resp = self.session.get(url, timeout=15, verify=False)
            return resp.json().get('url', '')
        except:
            return None
    
    # ============ 音源7: 5nd.com ============
    def search_5nd(self, keyword: str) -> List[Dict]:
        try:
            url = f"https://www.5nd.com/song/0-0-0-0-0-0-0-0-1-0-0-0.html?searchKey={quote(keyword)}"
            resp = self.session.get(url, timeout=15, verify=False)
            songs = []
            # 提取歌曲链接
            pattern = r'href="/song/(\d+)\.htm"[^>]*>([^<]+)</a>'
            for sid, name in re.findall(pattern, resp.text)[:15]:
                songs.append({'id': sid, 'name': name.strip(), 'artist': '未知', 'source': '5nd'})
            return songs
        except Exception as e:
            print(f"   5nd失败: {e}")
            return []
    
    def get_url_5nd(self, song_id: str) -> Optional[str]:
        try:
            url = f"https://www.5nd.com/song/{song_id}.htm"
            resp = self.session.get(url, timeout=15, verify=False)
            # 提取播放链接
            match = re.search(r'href="(https?://[^"]+\.mp3[^"]*)"', resp.text)
            if match:
                return match.group(1)
        except:
            return None
    
    # ============ 音源8: 一听音乐 ============
    def search_1ting(self, keyword: str) -> List[Dict]:
        try:
            url = f"https://www.1ting.com/search?q={quote(keyword)}"
            resp = self.session.get(url, timeout=15, verify=False)
            songs = []
            pattern = r'href="/song/(\d+)"[^>]*>([^<]+)</a>'
            for sid, name in re.findall(pattern, resp.text)[:15]:
                songs.append({'id': sid, 'name': name.strip(), 'artist': '未知', 'source': '1ting'})
            return songs
        except Exception as e:
            print(f"   一听失败: {e}")
            return []
    
    def get_url_1ting(self, song_id: str) -> Optional[str]:
        try:
            url = f"https://www.1ting.com/song/{song_id}"
            resp = self.session.get(url, timeout=15, verify=False)
            match = re.search(r'href="(https?://[^"]+\.mp3[^"]*)"', resp.text)
            if match:
                return match.group(1)
        except:
            return None
    
    # ============ 音源9: 九酷音乐 ============
    def search_9ku(self, keyword: str) -> List[Dict]:
        try:
            url = f"https://www.9ku.com/soso/-k-{quote(keyword)}-k-.htm"
            resp = self.session.get(url, timeout=15, verify=False)
            songs = []
            # 解析歌曲列表
            pattern = r'href="/[a-z]+/(\d+)\.htm"[^>]*title="([^"]+)"'
            for sid, title in re.findall(pattern, resp.text)[:15]:
                name = title.split('-')[1].strip() if '-' in title else title
                artist = title.split('-')[0].strip() if '-' in title else '未知'
                songs.append({'id': sid, 'name': name, 'artist': artist, 'source': '9ku'})
            return songs
        except Exception as e:
            print(f"   九酷失败: {e}")
            return []
    
    def get_url_9ku(self, song_id: str) -> Optional[str]:
        try:
            url = f"https://www.9ku.com/play/{song_id}.htm"
            resp = self.session.get(url, timeout=15, verify=False)
            match = re.search(r'href="(https?://[^"]+\.mp3[^"]*)"', resp.text)
            if match:
                return match.group(1)
            # 备用：查找播放器中的链接
            match = re.search(r'url:\s*"(https?://[^"]+)"', resp.text)
            if match:
                return match.group(1)
        except:
            return None
    
    # ============ 音源10: musicenc.com ============
    def search_musicenc(self, keyword: str) -> List[Dict]:
        try:
            url = f"https://www.musicenc.com/search/{quote(keyword)}.html"
            resp = self.session.get(url, timeout=15, verify=False)
            songs = []
            pattern = r'href="/song/(\d+)\.html"[^>]*>([^<]+)</a>'
            for sid, name in re.findall(pattern, resp.text)[:15]:
                songs.append({'id': sid, 'name': name.strip(), 'artist': '未知', 'source': 'musicenc'})
            return songs
        except Exception as e:
            print(f"   musicenc失败: {e}")
            return []
    
    def get_url_musicenc(self, song_id: str) -> Optional[str]:
        try:
            url = f"https://www.musicenc.com/song/{song_id}.html"
            resp = self.session.get(url, timeout=15, verify=False)
            match = re.search(r'href="(https?://[^"]+\.mp3[^"]*)"', resp.text)
            if match:
                return match.group(1)
        except:
            return None
    
    # ============ 统一接口 ============
    def search_all(self, keyword: str) -> List[Dict]:
        """从所有音源搜索"""
        all_songs = []
        print("🔍 搜索中...")
        
        sources = [
            ('thttt', self.search_thttt),
            ('kugou', self.search_kugou),
            ('kuwo', self.search_kuwo),
            ('netease', self.search_netease),
            ('qq', self.search_qq),
            ('gequbao', self.search_gequbao),
            ('5nd', self.search_5nd),
            ('1ting', self.search_1ting),
            ('9ku', self.search_9ku),
            ('musicenc', self.search_musicenc),
        ]
        
        for name, func in sources:
            try:
                songs = func(keyword)
                if songs:
                    print(f"   ✅ {name}: {len(songs)} 首")
                    all_songs.extend(songs)
                time.sleep(0.2)
            except:
                pass
        
        return all_songs
    
    def download(self, url: str, save_path: str) -> bool:
        """下载文件"""
        if 'kuwo.cn' in url:
            referer = 'https://www.kuwo.cn/'
        elif 'kugou.com' in url:
            referer = 'https://www.kugou.com/'
        elif '163.com' in url or '126.net' in url:
            referer = 'https://music.163.com/'
        elif 'qq.com' in url:
            referer = 'https://y.qq.com/'
        else:
            referer = 'https://www.thttt.com/'
        
        headers = {"User-Agent": HEADERS["User-Agent"], "Referer": referer}
        
        try:
            resp = self.session.get(url, headers=headers, timeout=60, stream=True, verify=False)
            resp.raise_for_status()
            
            size = int(resp.headers.get('content-length', 0))
            if size < 1024:
                print(f"   ⚠️ 文件太小: {size} bytes")
                return False
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                for chunk in resp.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            print(f"   ✅ 下载成功: {save_path}")
            return True
        except Exception as e:
            print(f"   ❌ 下载失败: {e}")
            return False
    
    def search_and_download(self, keyword: str, save_dir: str = "/tmp/music") -> Optional[str]:
        """搜索并下载"""
        print(f"\n🎵 搜索: {keyword}")
        print("=" * 40)
        
        songs = self.search_all(keyword)
        if not songs:
            print("\n❌ 所有音源都未找到")
            return None
        
        tried = set()
        get_url_funcs = {
            'thttt': lambda s: self.get_url_thttt(s['hash']),
            'kugou': lambda s: self.get_url_kugou(s['hash']),
            'kuwo': lambda s: self.get_url_kuwo(s['rid']),
            'netease': lambda s: self.get_url_netease(s['id']),
            'qq': lambda s: self.get_url_qq(s['mid']),
            'gequbao': lambda s: self.get_url_gequbao(s['id']),
            '5nd': lambda s: self.get_url_5nd(s['id']),
            '1ting': lambda s: self.get_url_1ting(s['id']),
            '9ku': lambda s: self.get_url_9ku(s['id']),
            'musicenc': lambda s: self.get_url_musicenc(s['id']),
        }
        
        for song in songs:
            key = f"{song['source']}:{song.get('hash') or song.get('rid') or song.get('id') or song.get('mid')}"
            if key in tried:
                continue
            tried.add(key)
            
            print(f"\n📀 {song['artist']} - {song['name']} ({song['source']})")
            
            source = song['source']
            if source not in get_url_funcs:
                continue
            
            play_url = get_url_funcs[source](song)
            if not play_url:
                print("   ⚠️ 无法获取链接")
                continue
            
            safe_name = re.sub(r'[<>:"/\\|?*]', '_', f"{song['artist']}_{song['name']}")
            save_path = os.path.join(save_dir, f"{safe_name}.mp3")
            
            if self.download(play_url, save_path):
                return save_path
        
        print("\n❌ 所有歌曲都无法下载")
        return None


def download_song(keyword: str, save_dir: str = "/tmp/music") -> Optional[str]:
    downloader = MusicDownloader()
    return downloader.search_and_download(keyword, save_dir)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python music_downloader.py '歌曲名'")
        print("\n支持10个音源: thttt, kugou, kuwo, netease, qq, gequbao, 5nd, 1ting, 9ku, musicenc")
        sys.exit(1)
    
    result = download_song(sys.argv[1])
    print(f"\n{'🎉 ' + result if result else '💥 下载失败'}")
