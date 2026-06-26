#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sqlite3
import requests
import os
import hashlib
import datetime
import json
from dotenv import load_dotenv

# 加载配置
load_dotenv()
PLATFORM_TOKEN = os.getenv('PLATFORM_TOKEN')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'works.db')
UPLOAD_URL = "https://platform.acedata.cloud/api/v1/files/"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 初始化上传记录表
def init_upload_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_hash TEXT NOT NULL UNIQUE,
            file_path TEXT NOT NULL,
            url TEXT NOT NULL,
            upload_time INTEGER NOT NULL,
            expire_time INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 计算文件MD5哈希
def get_file_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# 上传图片
def upload_image(file_path):
    if not os.path.exists(file_path):
        return {"success": False, "msg": "文件不存在"}
    
    # 计算文件哈希
    file_hash = get_file_md5(file_path)
    now = int(datetime.datetime.now().timestamp())
    
    # 查询数据库是否有未过期的记录
    conn = get_db_connection()
    record = conn.execute('''
        SELECT url FROM uploaded_files 
        WHERE file_hash = ? AND expire_time > ?
    ''', (file_hash, now)).fetchone()
    
    if record:
        conn.close()
        return {"success": True, "url": record['url'], "from_cache": True}
    
    # 上传到服务器
    try:
        headers = {
            "authorization": f"Bearer {PLATFORM_TOKEN}"
        }
        files = {
            "file": open(file_path, "rb")
        }
        response = requests.post(UPLOAD_URL, headers=headers, files=files, timeout=60)
        response.raise_for_status()
        result = response.json()
        url = result.get('url')
        if not url:
            return {"success": False, "msg": "上传失败，返回URL为空"}
        
        # 保存到数据库，有效期24小时
        expire_time = now + 86400
        conn.execute('''
            INSERT OR REPLACE INTO uploaded_files 
            (file_hash, file_path, url, upload_time, expire_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_hash, file_path, url, now, expire_time))
        conn.commit()
        conn.close()
        
        return {"success": True, "url": url, "from_cache": False}
    except Exception as e:
        conn.close()
        return {"success": False, "msg": f"上传失败: {str(e)}"}

def main():
    init_upload_table()
    parser = argparse.ArgumentParser(description='图片上传工具')
    parser.add_argument('-file', required=True, type=str, help='要上传的图片路径')
    args = parser.parse_args()
    
    result = upload_image(args.file)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
