#!/usr/bin/env python3
"""
发布文章到微信公众号草稿箱
"""

import requests
import json
import os
import sys
import markdown

# 加载配置
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

APP_ID = config.get('appId')
APP_SECRET = config.get('appSecret')

def get_access_token():
    """获取 access token"""
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}'
    resp = requests.get(url, verify=False)
    data = resp.json()
    if 'access_token' in data:
        return data['access_token']
    else:
        print(f"获取 token 失败：{data}")
        sys.exit(1)

def markdown_to_html(md_content):
    """简单的 Markdown 转 HTML"""
    # 这里用基础转换，实际可以用 markdown 库
    html = md_content
    return html

def create_draft(token, title, content):
    """创建草稿"""
    url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}'
    
    data = {
        "title": title,
        "content": content
    }
    
    resp = requests.post(url, json=data, verify=False)
    result = resp.json()
    
    if 'media_id' in result:
        return result['media_id']
    else:
        print(f"创建草稿失败：{result}")
        return None

def main():
    if len(sys.argv) < 2:
        print("用法：python3 publish_wechat.py <article.md> [options]")
        print("选项:")
        print("  --cover-image <path>  封面图路径")
        print("  --template <name>     模板名称")
        sys.exit(1)
    
    article_path = sys.argv[1]
    cover_image = None
    template = 'viral'
    
    # 解析参数
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--cover-image' and i + 1 < len(sys.argv):
            cover_image = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--template' and i + 1 < len(sys.argv):
            template = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    # 读取文章
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题（第一行）
    title = content.split('\n')[0].lstrip('# ').strip()
    
    # 获取 token
    print("获取 access token...")
    token = get_access_token()
    
    # 创建草稿
    print(f"发布文章：{title}")
    media_id = create_draft(token, title, content)
    
    if media_id:
        print(f"✅ 草稿已创建")
        print(f"媒体 ID: {media_id}")
        
        # 保存结果
        result = {
            "title": title,
            "media_id": media_id,
            "template": template
        }
        
        result_path = os.path.join(os.path.dirname(article_path), 'publish_result.json')
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"结果已保存到：{result_path}")
    else:
        print("❌ 发布失败")
        sys.exit(1)

if __name__ == '__main__':
    main()
