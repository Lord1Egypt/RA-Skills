#!/usr/bin/env python3
"""
博客园发布工具
功能：将 Markdown 文件发布到博客园

使用方式：
    python publish_to_cnblogs.py <markdown文件路径> --token <你的PAT> --title <标题>
    python publish_to_cnblogs.py <markdown文件路径> --token <你的PAT>  # 自动从文件提取标题

常见问题：
    - 如果遇到 "No such file or directory" 错误，尝试使用绝对路径
    - Windows 用户建议使用: python G:\\path\\to\\publish_to_cnblogs.py
    - 或先 cd 到脚本所在目录再执行
"""

import argparse
import sys
import re
import os
from pathlib import Path

# 尝试导入 requests，如果失败给出友好提示
try:
    import requests
except ImportError:
    print("[ERROR] 请先安装依赖: pip install requests")
    sys.exit(1)

CNBLOGS_API = "https://i.cnblogs.com/openapi/v1/posts"

def setup_encoding():
    """解决 Windows 下的编码问题"""
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass
    try:
        import io
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

def normalize_path(path_str: str) -> Path:
    """规范化路径，处理 Windows 和 Unix 路径格式"""
    # 转换反斜杠为正斜杠
    path_str = path_str.replace('\\', '/')
    # 处理 ~ 家目录
    if path_str.startswith('~'):
        path_str = str(Path.home()) + path_str[1:]
    return Path(path_str)

def extract_title_from_markdown(content: str) -> str:
    """从 Markdown 内容中提取标题"""
    match = re.match(r'^#\s+(.+)$', content.strip(), re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""

def extract_description_from_markdown(content: str) -> str:
    """从 Markdown 内容中提取描述（摘要）"""
    lines = content.strip().split('\n')
    description = []
    in_code_block = False
    
    for line in lines[1:20]:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if line.strip().startswith('#'):
            break
        if line.strip():
            description.append(line.strip())
        if len(description) >= 3:
            break
    
    desc = ' '.join(description)
    return desc[:200] if len(desc) > 200 else desc

def publish_to_cnblogs(title: str, body: str, token: str, description: str = "", post_type: str = "BlogPost") -> bool:
    """发布文章到博客园"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Authorization-Type": "pat",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": title,
        "body": body,
        "description": description,
        "postType": post_type,
        "postFormat": "Markdown"
    }
    
    try:
        response = requests.post(CNBLOGS_API, headers=headers, json=data, timeout=30)
        result = response.json()
        
        if response.status_code == 200 or response.status_code == 201:
            post_id = result.get('id', result.get('postId', 'unknown'))
            print(f"[OK] Published successfully! Post ID: {post_id}")
            print(f"[INFO] Response: {result}")
            return True
        else:
            print(f"[ERROR] Failed: {result}")
            return False
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return False

def main():
    setup_encoding()
    
    parser = argparse.ArgumentParser(description='博客园 Markdown 发布工具')
    parser.add_argument('input', help='Markdown 文件路径')
    parser.add_argument('--token', '-t', required=True, help='博客园 PAT (Personal Access Token)')
    parser.add_argument('--title', '-T', default='', help='文章标题（默认从文件提取）')
    parser.add_argument('--description', '-d', default='', help='文章摘要')
    parser.add_argument('--post-type', default='BlogPost', choices=['BlogPost', 'Article'], help='文章类型')
    parser.add_argument('--preview', '-p', action='store_true', help='仅预览，不发布')
    
    args = parser.parse_args()
    
    # 规范化输入路径
    input_path = normalize_path(args.input)
    if not input_path.exists():
        print(f"[ERROR] File not found: {args.input}")
        print(f"[INFO] 尝试使用绝对路径，例如: python G:\\\\path\\\\to\\\\publish_to_cnblogs.py")
        sys.exit(1)
    
    content = input_path.read_text(encoding='utf-8')
    
    title = args.title or extract_title_from_markdown(content)
    if not title:
        print("[ERROR] Cannot extract title. Please provide with --title")
        sys.exit(1)
    
    description = args.description or extract_description_from_markdown(content)
    
    print(f"[INFO] Title: {title}")
    print(f"[INFO] Description: {description[:50]}..." if len(description) > 50 else f"[INFO] Description: {description}")
    
    if args.preview:
        print("\n" + "=" * 50)
        print("PREVIEW MODE - No actual publish")
        print("=" * 50)
        print(f"\nTitle: {title}\n")
        print(f"Body (first 500 chars):\n{content[:500]}...")
        return
    
    success = publish_to_cnblogs(title, content, args.token, description, args.post_type)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()