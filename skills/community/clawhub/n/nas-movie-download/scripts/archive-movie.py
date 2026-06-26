#!/usr/bin/env python3
"""
电影归档脚本
功能：将下载完成的电影从SSD移动到机械硬盘，并删除qBittorrent种子
"""

import argparse
import sys
import time
from smb.SMBConnection import SMBConnection
import urllib.request
import urllib.parse
import json

class MovieArchiver:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        
    def connect(self, share_name):
        """连接SMB共享"""
        conn = SMBConnection(
            self.username, 
            self.password, 
            'openclaw-client', 
            self.server, 
            use_ntlm_v2=True
        )
        if not conn.connect(self.server, 445):
            raise Exception(f"无法连接到SMB共享: {share_name}")
        return conn
    
    def find_movie_folder(self, conn, share, path, movie_name):
        """在SSD上查找电影文件夹"""
        try:
            files = conn.listPath(share, path)
            movie_lower = movie_name.lower().replace(' ', '.')
            
            for f in files:
                if f.filename in ['.', '..']:
                    continue
                if f.isDirectory:
                    # 匹配文件夹名
                    fname_lower = f.filename.lower()
                    if movie_lower in fname_lower or movie_name.lower() in fname_lower:
                        return f.filename
            return None
        except Exception as e:
            print(f"❌ 查找电影文件夹失败: {e}")
            return None
    
    def move_to_hdd(self, ssd_conn, hdd_conn, folder_name):
        """将电影从SSD移动到机械硬盘"""
        ssd_path = f"/qb/downloads/{folder_name}"
        hdd_path = f"/movie/{folder_name}"
        
        print(f"📦 移动电影: {folder_name}")
        print(f"   从: super8083 (SSD) {ssd_path}")
        print(f"   到: sata11 (机械硬盘) {hdd_path}")
        
        try:
            # 检查HDD上是否已存在
            try:
                hdd_conn.listPath('sata11-139XXXX8083', hdd_path)
                print(f"⚠️  目标位置已存在该电影，跳过移动")
                return True
            except:
                pass  # 不存在，继续
            
            # 创建目标文件夹
            hdd_conn.createDirectory('sata11-139XXXX8083', hdd_path)
            
            # 遍历并复制所有文件
            files = ssd_conn.listPath('super8083', ssd_path)
            for f in files:
                if f.filename in ['.', '..']:
                    continue
                    
                src_path = f"{ssd_path}/{f.filename}"
                dst_path = f"{hdd_path}/{f.filename}"
                
                if f.isDirectory:
                    # 递归复制子目录
                    self._copy_directory(ssd_conn, hdd_conn, src_path, dst_path)
                else:
                    # 复制文件
                    print(f"   📄 复制: {f.filename}")
                    self._copy_file(ssd_conn, hdd_conn, src_path, dst_path)
            
            # 删除源文件夹（可选，暂时保留）
            # self._delete_directory(ssd_conn, 'super8083', ssd_path)
            
            print(f"✅ 电影归档完成: {folder_name}")
            return True
            
        except Exception as e:
            print(f"❌ 归档失败: {e}")
            return False
    
    def _copy_file(self, ssd_conn, hdd_conn, src, dst):
        """复制单个文件"""
        # 读取文件
        with open('/tmp/smb_temp_file', 'wb') as fp:
            ssd_conn.retrieveFile('super8083', src, fp)
        
        # 写入文件
        with open('/tmp/smb_temp_file', 'rb') as fp:
            hdd_conn.storeFile('sata11-139XXXX8083', dst, fp)
    
    def _copy_directory(self, ssd_conn, hdd_conn, src, dst):
        """递归复制目录"""
        hdd_conn.createDirectory('sata11-139XXXX8083', dst)
        files = ssd_conn.listPath('super8083', src)
        
        for f in files:
            if f.filename in ['.', '..']:
                continue
            
            src_path = f"{src}/{f.filename}"
            dst_path = f"{dst}/{f.filename}"
            
            if f.isDirectory:
                self._copy_directory(ssd_conn, hdd_conn, src_path, dst_path)
            else:
                self._copy_file(ssd_conn, hdd_conn, src_path, dst_path)
    
    def delete_torrent(self, qb_url, username, password, movie_name):
        """删除qBittorrent中的种子"""
        print(f"🗑️  删除qBittorrent种子...")
        
        try:
            # 登录获取cookie
            import http.cookiejar
            import urllib.request
            
            cookie_jar = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(cookie_jar)
            )
            
            # 登录
            login_data = urllib.parse.urlencode({
                'username': username,
                'password': password
            }).encode()
            
            login_req = urllib.request.Request(f"{qb_url}/api/v2/auth/login", 
                                                data=login_data)
            login_response = opener.open(login_req)
            
            if b'Ok' not in login_response.read():
                print("❌ qBittorrent登录失败")
                return False
            
            # 获取种子列表
            torrents_req = urllib.request.Request(f"{qb_url}/api/v2/torrents/info")
            torrents_response = opener.open(torrents_req)
            torrents = json.loads(torrents_response.read())
            
            # 查找匹配的种子
            movie_lower = movie_name.lower()
            deleted = False
            
            for t in torrents:
                t_name = t.get('name', '').lower()
                if movie_lower in t_name or movie_name.lower().replace(' ', '.') in t_name:
                    torrent_hash = t.get('hash')
                    print(f"   找到种子: {t.get('name')}")
                    
                    # 删除种子和文件
                    delete_data = urllib.parse.urlencode({
                        'hashes': torrent_hash,
                        'deleteFiles': 'true'
                    }).encode()
                    
                    delete_req = urllib.request.Request(
                        f"{qb_url}/api/v2/torrents/delete",
                        data=delete_data
                    )
                    opener.open(delete_req)
                    print(f"   ✅ 已删除种子")
                    deleted = True
            
            if not deleted:
                print(f"   ⚠️  未找到匹配的种子")
            
            return True
            
        except Exception as e:
            print(f"❌ 删除种子失败: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='电影归档工具')
    parser.add_argument('--movie-name', required=True, help='电影名称')
    parser.add_argument('--ssd-share', default='super8083', help='SSD共享名')
    parser.add_argument('--ssd-path', default='qb/downloads', help='SSD下载路径')
    parser.add_argument('--hdd-share', default='sata11-139XXXX8083', help='HDD共享名')
    parser.add_argument('--hdd-path', default='movie', help='HDD电影路径')
    parser.add_argument('--qb-url', default='http://192.168.1.246:8888', help='qBittorrent URL')
    parser.add_argument('--qb-user', default='admin', help='qBittorrent用户名')
    parser.add_argument('--qb-pass', default='adminadmin', help='qBittorrent密码')
    parser.add_argument('--smb-user', default='13917908083', help='SMB用户名')
    parser.add_argument('--smb-pass', default='Roger0808', help='SMB密码')
    parser.add_argument('--server', default='192.168.1.246', help='SMB服务器')
    
    args = parser.parse_args()
    
    print("========================================")
    print("📦 电影归档工具")
    print("========================================")
    print(f"电影: {args.movie_name}")
    print(f"SSD: {args.ssd_share} -> HDD: {args.hdd_share}")
    print("")
    
    # 创建归档器
    archiver = MovieArchiver(args.server, args.smb_user, args.smb_pass)
    
    try:
        # 连接两个共享
        print("🔌 连接SMB共享...")
        ssd_conn = archiver.connect(args.ssd_share)
        hdd_conn = archiver.connect(args.hdd_share)
        print("✅ SMB连接成功")
        print("")
        
        # 查找电影文件夹
        print(f"🔍 查找电影文件夹...")
        folder_name = archiver.find_movie_folder(
            ssd_conn, args.ssd_share, f"/{args.ssd_path}", args.movie_name
        )
        
        if not folder_name:
            print(f"❌ 未找到电影文件夹: {args.movie_name}")
            print(f"   请确认电影已下载到 {args.ssd_share}/{args.ssd_path}")
            return 1
        
        print(f"✅ 找到电影: {folder_name}")
        print("")
        
        # 移动到机械硬盘
        if archiver.move_to_hdd(ssd_conn, hdd_conn, folder_name):
            # 删除种子
            archiver.delete_torrent(args.qb_url, args.qb_user, args.qb_pass, args.movie_name)
        
        # 断开连接
        ssd_conn.close()
        hdd_conn.close()
        
        print("")
        print("========================================")
        print("✅ 归档流程完成")
        print("========================================")
        return 0
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
