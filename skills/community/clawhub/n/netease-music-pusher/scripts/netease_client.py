#!/usr/bin/env python3
"""
网易云音乐API - 支持登录获取个性化日推
实现了网易云weapi的加密逻辑
"""
import requests
import json
import base64
import os
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class NeteaseCrypto:
    """网易云加密工具"""
    
    # 网易云固定密钥
    MODULUS = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    NONCE = '0CoJUm6Qyw8W8jud'
    PUBKEY = '010001'
    IV = '0102030405060708'
    
    @staticmethod
    def aes_encrypt(text, key):
        """AES-CBC加密"""
        # PKCS7填充
        pad_len = 16 - len(text) % 16
        text = text + chr(pad_len) * pad_len
        
        cipher = Cipher(
            algorithms.AES(key.encode('utf-8')),
            modes.CBC(NeteaseCrypto.IV.encode('utf-8')),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(text.encode('utf-8')) + encryptor.finalize()
        return base64.b64encode(ciphertext).decode('utf-8')
    
    @staticmethod
    def rsa_encrypt(text, pubkey, modulus):
        """RSA加密"""
        text = text[::-1]  # 反转字符串
        text_bytes = text.encode('utf-8')
        text_int = int.from_bytes(text_bytes, 'big')
        
        pubkey_int = int(pubkey, 16)
        modulus_int = int(modulus, 16)
        
        result = pow(text_int, pubkey_int, modulus_int)
        return format(result, 'x').zfill(256)
    
    @staticmethod
    def encrypt(params):
        """网易云weapi加密"""
        # 生成随机密钥 (16位小写字母)
        sec_key = ''.join([chr(ord('a') + (os.urandom(1)[0] % 26)) for _ in range(16)])
        
        # 第一次AES加密
        text = json.dumps(params)
        enc_text = NeteaseCrypto.aes_encrypt(text, NeteaseCrypto.NONCE)
        
        # 第二次AES加密
        enc_text = NeteaseCrypto.aes_encrypt(enc_text, sec_key)
        
        # RSA加密密钥
        enc_sec_key = NeteaseCrypto.rsa_encrypt(sec_key, NeteaseCrypto.PUBKEY, NeteaseCrypto.MODULUS)
        
        return {
            'params': enc_text,
            'encSecKey': enc_sec_key
        }

class NeteaseMusicClient:
    """网易云音乐客户端"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0',
            'Referer': 'https://music.163.com/',
            'Origin': 'https://music.163.com',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        self.crypto = NeteaseCrypto()
        self.cookies_file = '/root/.openclaw/workspace/secrets/netease_cookies.json'
        
    def weapi_request(self, endpoint, params=None):
        """调用weapi接口"""
        url = f'https://music.163.com/weapi{endpoint}'
        params = params or {}
        
        # csrf_token
        cookies = self.session.cookies.get_dict()
        params['csrf_token'] = cookies.get('__csrf', '')
        
        # 加密参数
        data = self.crypto.encrypt(params)
        
        try:
            response = self.session.post(url, data=data, timeout=15)
            return response.json()
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return {'code': -1, 'msg': str(e)}
    
    def send_captcha(self, phone):
        """发送验证码"""
        result = self.weapi_request('/sms/captcha/sent', {
            'cellphone': phone,
            'ctcode': '86'
        })
        
        if result.get('code') == 200:
            print(f"✅ 验证码已发送到 {phone}")
            print("⏰ 验证码5分钟内有效，请查收短信")
            return True
        else:
            msg = result.get('message', result.get('msg', '未知错误'))
            print(f"❌ 发送失败: {msg}")
            return False
    
    def login_with_captcha(self, phone, captcha):
        """使用验证码登录"""
        result = self.weapi_request('/login/cellphone', {
            'phone': phone,
            'captcha': captcha,
            'countrycode': '86',
            'rememberLogin': 'true'
        })
        
        if result.get('code') == 200:
            profile = result.get('profile', {})
            nickname = profile.get('nickname', '用户')
            print(f"✅ 登录成功！欢迎回来，{nickname}～")
            self.save_cookies()
            return True
        else:
            msg = result.get('message', result.get('msg', '未知错误'))
            print(f"❌ 登录失败: {msg}")
            return False
    
    def get_daily_recommend(self):
        """获取每日推荐歌曲"""
        result = self.weapi_request('/v1/discovery/recommend/songs', {
            'offset': 0,
            'total': True,
            'limit': 20
        })
        
        if result.get('code') == 200:
            data = result.get('data', {})
            return data.get('dailySongs', [])
        return []
    
    def get_song_detail(self, song_ids):
        """获取歌曲详情（包含风格标签）"""
        if isinstance(song_ids, list):
            ids = ','.join([str(id) for id in song_ids])
        else:
            ids = str(song_ids)
        
        result = self.weapi_request('/v3/song/detail', {
            'c': json.dumps([{'id': int(id)} for id in ids.split(',')]),
            'ids': ids
        })
        
        if result.get('code') == 200:
            return result.get('songs', [])
        return []
    
    def get_song_url(self, song_id):
        """获取歌曲播放链接"""
        result = self.weapi_request('/song/enhance/player/url', {
            'ids': [song_id],
            'br': 320000
        })
        
        if result.get('code') == 200:
            data = result.get('data', [])
            if data:
                return data[0].get('url')
        return None
    
    def save_cookies(self):
        """保存登录状态"""
        os.makedirs(os.path.dirname(self.cookies_file), exist_ok=True)
        # 处理重复的cookie，只保留第一个
        cookies_dict = {}
        for cookie in self.session.cookies:
            if cookie.name not in cookies_dict:
                cookies_dict[cookie.name] = cookie.value
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies_dict, f)
        print("💾 登录状态已保存")
    
    def load_cookies(self):
        """加载登录状态"""
        try:
            with open(self.cookies_file, 'r') as f:
                cookies = json.load(f)
                self.session.cookies.update(cookies)
                return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False

def format_daily_songs(songs, date_str=None):
    """格式化日推歌曲"""
    if not songs:
        return "❌ 暂无推荐歌曲"
    
    date = date_str or datetime.now().strftime('%m月%d日')
    
    lines = [
        "🎵 网易云日推",
        f"📅 {date}",
        "💝 专属于你的每日推荐",
        "=" * 40,
        ""
    ]
    
    for i, song in enumerate(songs[:10], 1):
        name = song.get('name', '未知')
        song_id = song.get('id', '')
        song_url = f"https://music.163.com/song?id={song_id}" if song_id else ''
        
        artists = song.get('artists', [])
        artist_names = ' / '.join([a.get('name', '未知') for a in artists[:2]])
        
        album = song.get('album', {})
        album_name = album.get('name', '')
        
        # 获取风格标签（如果有）
        tags = []
        if 'tags' in song and song['tags']:
            tags = song['tags']
        elif 'genre' in song and song['genre']:
            tags = [song['genre']]
        
        # 获取推荐理由
        reason = song.get('reason', '')
        
        lines.append(f"{i:2d}. {name}")
        lines.append(f"    🎤 {artist_names}")
        if album_name:
            lines.append(f"    💿 {album_name}")
        if tags:
            lines.append(f"    🏷️ {' | '.join(tags[:3])}")
        if reason:
            lines.append(f"    💡 {reason}")
        if song_url:
            lines.append(f"    🔗 {song_url}")
        lines.append("")
    
    lines.extend([
        "─" * 40,
        "🎧 打开网易云音乐App收听完整版",
        "🌟 每日6:00更新，错过就听不到了哦～"
    ])
    
    return '\n'.join(lines)

def main():
    import sys
    client = NeteaseMusicClient()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 netease_client.py send_captcha <手机号>")
        print("  python3 netease_client.py login <手机号> <验证码>")
        print("  python3 netease_client.py daily")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'send_captcha' and len(sys.argv) > 2:
        phone = sys.argv[2]
        client.send_captcha(phone)
        
    elif cmd == 'login' and len(sys.argv) > 3:
        phone = sys.argv[2]
        captcha = sys.argv[3]
        client.login_with_captcha(phone, captcha)
        
    elif cmd == 'daily':
        if client.load_cookies():
            songs = client.get_daily_recommend()
            if songs:
                # 获取歌曲详情（包含风格标签）
                print("正在获取歌曲风格标签...")
                song_ids = [song.get('id') for song in songs[:10] if song.get('id')]
                song_details = client.get_song_detail(song_ids)
                
                # 将详情信息合并到歌曲数据中
                details_map = {s.get('id'): s for s in song_details}
                for song in songs:
                    song_id = song.get('id')
                    if song_id in details_map:
                        detail = details_map[song_id]
                        # 合并风格标签
                        if 'tags' in detail and detail['tags']:
                            song['tags'] = detail['tags']
                        # 从alia或transNames获取风格信息
                        alia = detail.get('alia', [])
                        if alia and not song.get('tags'):
                            song['tags'] = alia[:2]
                
                print(format_daily_songs(songs))
            else:
                print("❌ 获取日推失败，请检查登录状态")
        else:
            print("❌ 未登录，请先使用 login 命令登录")
    
    else:
        print(f"未知命令: {cmd}")

if __name__ == '__main__':
    main()
