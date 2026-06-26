#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import requests


def convert_md_to_word(md_file_path):
    """
    将.md文件转换为Word文件
    :param md_file_path: .md文件路径
    :return: 转换后的Word文件路径
    """
    try:
        # 读取.md文件内容
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # 首先获取网站的初始页面，获取必要的cookies和token
        session = requests.Session()
        session.headers.update(headers)
        
        # 访问md2word.com网站
        print("正在连接md2word.com...")
        response = session.get('https://md2word.com/en')
        response.raise_for_status()
        
        # 准备文件上传
        word_file_path = os.path.splitext(md_file_path)[0] + '.docx'
        
        # 使用requests直接上传文件
        print("正在上传文件...")
        files = {
            'file': (os.path.basename(md_file_path), open(md_file_path, 'rb'), 'text/markdown')
        }
        
        # 发送文件上传请求
        upload_response = session.post('https://md2word.com/en', files=files, allow_redirects=True)
        upload_response.raise_for_status()
        
        # 等待转换完成
        print("正在转换文件，请稍候...")
        time.sleep(5)  # 给服务器一些时间处理文件
        
        # 尝试获取下载链接
        # 注意：这里需要根据网站的实际API或下载链接格式进行调整
        # 由于md2word.com的具体API可能会变化，这里使用一种通用的方法
        
        # 模拟下载请求
        download_url = 'https://md2word.com/en/export/docx'
        download_response = session.get(download_url, stream=True)
        download_response.raise_for_status()
        
        # 检查响应是否为Word文件
        content_type = download_response.headers.get('Content-Type', '')
        if 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
            # 保存Word文件
            with open(word_file_path, 'wb') as f:
                for chunk in download_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"转换成功！Word文件已保存至: {word_file_path}")
            return word_file_path
        else:
            print("转换失败：未获取到Word文件")
            return None
        
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return None


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("用法: python convert_md_to_word.py <md_file_path>")
        sys.exit(1)
    
    md_file_path = sys.argv[1]
    if not os.path.exists(md_file_path) or not md_file_path.endswith('.md'):
        print("请提供有效的.md文件路径")
        sys.exit(1)
    
    convert_md_to_word(md_file_path)