#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块 - 提取可独立测试的功能
"""

import re
import json
import urllib.request
from typing import List, Dict, Optional, Tuple
from pathlib import Path


def extract_image_urls(text: str) -> List[str]:
    """
    从文本中提取图片 URL
    
    支持格式：
    - Markdown: ![alt](url) 或 ![alt](url "title")
    - HTML: <img src="url">
    
    Args:
        text: 要解析的文本
    
    Returns:
        去重后的 URL 列表（最多 10 个）
    """
    if not text or not isinstance(text, str):
        return []
    
    urls = []
    
    # Markdown: ![alt](url) 或 ![alt](url "title") - 只提取 URL 部分
    # 修复：处理 URL 中包含空格和 title 的情况
    for match in re.finditer(r'!\[([^\]]*)\]\(([^\s")]+)(?:\s+["\'][^"\']*["\'])?\)', text):
        url = match.group(2).strip()
        if url and url not in urls:
            urls.append(url)
    
    # HTML: <img src="url">
    html_img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)
    for match in html_img_pattern.finditer(text):
        url = match.group(1).strip()
        if url and url not in urls:
            urls.append(url)
    
    return urls[:10]


def download_image(url: str, temp_dir: Path, max_retries: int = 3, index: int = 0) -> Optional[Path]:
    """
    下载图片到本地
    
    Args:
        url: 图片 URL
        temp_dir: 临时目录
        max_retries: 最大重试次数
        index: 图片索引，用于生成唯一文件名
    
    Returns:
        下载后的本地路径，失败返回 None
    """
    import sys
    from urllib.parse import urlparse
    import os
    
    # 清理 URL（移除控制字符和多余空格）
    url = url.strip()
    url = ''.join(char for char in url if ord(char) >= 32 or char in '\t\n\r')
    
    # 提取文件名
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path) or "image.png"
    # 清理文件名中的非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    if not filename or filename == '.':
        filename = "image.png"
    
    # 添加索引前缀避免文件名冲突（如 image.png -> 0_image.png）
    filename = f"{index}_{filename}"
    
    local_path = temp_dir / filename
    
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
                }
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                with open(local_path, 'wb') as f:
                    f.write(response.read())
            return local_path
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to download image {url} (attempt {attempt}/{max_retries}): {e}\n")
            if attempt == max_retries:
                return None
    
    return None


def image_to_base64(image_path: Path) -> Optional[str]:
    """
    将图片转换为 base64 编码字符串（仅使用标准库）
    
    注意：此函数不进行图片缩放，仅做 base64 编码
    如需缩放，建议在调用前使用其他工具处理
    
    Args:
        image_path: 图片本地路径
    
    Returns:
        base64 编码的字符串（带 data URI 前缀），失败返回 None
    """
    import base64
    
    try:
        # 读取图片文件
        with open(image_path, 'rb') as f:
            img_bytes = f.read()
        
        # 通过文件扩展名和魔数检测图片格式
        ext = image_path.suffix.lower()
        
        # 检查文件头魔数
        mime_type = 'image/jpeg'  # 默认
        
        if img_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
            mime_type = 'image/png'
        elif img_bytes.startswith(b'GIF87a') or img_bytes.startswith(b'GIF89a'):
            mime_type = 'image/gif'
        elif img_bytes.startswith(b'RIFF') and img_bytes[8:12] == b'WEBP':
            mime_type = 'image/webp'
        elif img_bytes.startswith(b'BM'):
            mime_type = 'image/bmp'
        elif img_bytes.startswith(b'\xff\xd8\xff'):
            mime_type = 'image/jpeg'
        elif ext in ['.png']:
            mime_type = 'image/png'
        elif ext in ['.gif']:
            mime_type = 'image/gif'
        elif ext in ['.webp']:
            mime_type = 'image/webp'
        elif ext in ['.bmp']:
            mime_type = 'image/bmp'
        elif ext in ['.jpg', '.jpeg']:
            mime_type = 'image/jpeg'
        
        # 转换为 base64
        base64_str = base64.b64encode(img_bytes).decode('utf-8')
        
        return f"data:{mime_type};base64,{base64_str}"
        
    except Exception as e:
        import sys
        sys.stderr.write(f"Warning: Failed to convert image to base64 {image_path}: {e}\n")
        return None


def process_issue_images(issue_body: str, temp_dir: Path, max_images: int = 5) -> List[Dict]:
    """
    处理 Issue 中的图片：下载并转换为 base64
    
    Args:
        issue_body: Issue 正文内容
        temp_dir: 临时目录
        max_images: 最大处理图片数量
    
    Returns:
        图片信息列表，每项包含：
        - url: 原始 URL
        - local_path: 本地路径
        - base64: base64 编码（带 data URI 前缀）
        - size: 文件大小（字节）
    """
    import sys
    
    image_urls = extract_image_urls(issue_body)
    if not image_urls:
        return []
    
    results = []
    for i, url in enumerate(image_urls[:max_images]):
        # 下载图片
        local_path = download_image(url, temp_dir)
        if not local_path:
            continue
        
        # 转换为 base64
        base64_data = image_to_base64(local_path)
        if not base64_data:
            continue
        
        # 获取文件大小
        file_size = local_path.stat().st_size
        
        results.append({
            'url': url,
            'local_path': str(local_path),
            'base64': base64_data,
            'size': file_size
        })
        
        sys.stderr.write(f"Info: Processed image {i+1}/{min(len(image_urls), max_images)}: {url} -> {file_size} bytes\n")
    
    return results


def deepwiki_query(repo: str, question: str, base_timeout: int = 120, max_retries: int = 3) -> Tuple[str, str]:
    """
    调用 DeepWiki MCP 查询
    
    Args:
        repo: 仓库名，格式为 "owner/repo"
        question: 查询问题
        base_timeout: 超时时间（秒）
        max_retries: 最大重试次数
    
    Returns:
        (answer, status) 元组
        - answer: DeepWiki 返回的答案
        - status: "ok", "failed", "skipped"
    """
    import sys
    import time
    import urllib.error
    
    if "/" not in repo:
        return "", "skipped"

    class DeepWikiMCPClient:
        def __init__(self, timeout: int = 120, max_retries: int = 3):
            self.base_url = "https://mcp.deepwiki.com/mcp"
            self.request_id = 0
            self.initialized = False
            self.timeout = timeout
            self.max_retries = max_retries

        def _make_request(self, method: str, params: dict = None) -> dict:
            self.request_id += 1
            payload = {
                "jsonrpc": "2.0",
                "id": self.request_id,
                "method": method,
                "params": params or {}
            }
            data = json.dumps(payload).encode('utf-8')
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/event-stream',
                'User-Agent': 'gitcode-issue-reply/1.4.1',
            }
            req = urllib.request.Request(
                self.base_url,
                data=data,
                headers=headers,
                method='POST'
            )
            last_error = None
            for attempt in range(self.max_retries + 1):
                try:
                    with urllib.request.urlopen(req, timeout=self.timeout) as response:
                        content_type = response.headers.get('Content-Type', '')
                        raw_data = response.read().decode('utf-8')
                        if 'text/event-stream' in content_type:
                            return self._parse_sse_response(raw_data)
                        else:
                            return json.loads(raw_data)
                except urllib.error.HTTPError as e:
                    last_error = f"HTTP {e.code}: {e.reason}"
                    if attempt < self.max_retries:
                        time.sleep(2 ** attempt)
                except urllib.error.URLError as e:
                    last_error = str(e)
                    if attempt < self.max_retries:
                        time.sleep(2 ** attempt)
                except json.JSONDecodeError as e:
                    last_error = f"JSON 解析错误: {e}"
                    break
                except Exception as e:
                    last_error = str(e)
                    if attempt < self.max_retries:
                        time.sleep(2 ** attempt)
            return {"error": f"Request failed after {self.max_retries + 1} attempts: {last_error}"}

        def _parse_sse_response(self, data: str) -> dict:
            result = {}
            for line in data.split('\n'):
                if line.startswith('data:'):
                    try:
                        result = json.loads(line[5:].strip())
                    except json.JSONDecodeError:
                        pass
            return result

        def initialize(self) -> dict:
            result = self._make_request("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "gitcode-issue-reply",
                    "version": "1.4.1"
                }
            })
            if "result" in result:
                self.initialized = True
                self._send_initialized_notification()
            return result

        def _send_initialized_notification(self):
            self._make_request("notifications/initialized", {})

        def ask_question(self, repo: str, question: str) -> dict:
            if not self.initialized:
                self.initialize()
            return self._make_request("tools/call", {
                "name": "ask_question",
                "arguments": {
                    "repoName": repo,
                    "question": question
                }
            })

    def extract_text(result) -> str:
        if isinstance(result, dict):
            content = result.get("content", [])
            if content and isinstance(content, list):
                texts = [item.get("text", "") for item in content
                         if isinstance(item, dict) and item.get("type") == "text"]
                return "\n".join(texts)
            if "result" in result.get("structuredContent", {}):
                return result["structuredContent"]["result"]
        return str(result)

    try:
        client = DeepWikiMCPClient(timeout=base_timeout, max_retries=max_retries)
        
        init_result = client.initialize()
        if "error" in init_result:
            sys.stderr.write(f"Warning: DeepWiki init error: {init_result['error']}\n")
            return "", "failed"
        
        data = client.ask_question(repo, question)
        if "error" in data:
            sys.stderr.write(f"Warning: DeepWiki query error: {data['error']}\n")
            return "", "failed"
        
        raw_result = data.get("result", {})
        answer_text = extract_text(raw_result)
        
        if not answer_text or answer_text.strip() == "{}":
            answer_text = (
                f"【请求已成功到达 DeepWiki】MCP 返回空结果。可能：该问题在知识库无匹配，或仓库未在 MCP 侧索引。"
                f"可尝试更泛化的问题，或访问 https://deepwiki.com/{repo} 浏览文档。"
            )
        
        return answer_text, "ok"

    except Exception as e:
        sys.stderr.write(f"Warning: DeepWiki query failed: {e}\n")
        return "", "failed"


if __name__ == "__main__":
    # 简单测试
    print("Testing extract_image_urls...")
    
    # 测试图片 URL 提取
    test_text = """
    ![image.png](https://example.com/image.png 'image.png')
    ![alt text](https://example.com/image2.png)
    <img src="https://example.com/image3.png">
    ![image with space](https://example.com/image 4.png "title")
    """
    urls = extract_image_urls(test_text)
    print(f"Extracted {len(urls)} URLs:")
    for url in urls:
        print(f"  - {url}")
    
    print("\nTesting deepwiki_query...")
    # 注意：实际测试需要网络连接
    # answer, status = deepwiki_query("Ascend/RecSDK", "What is this project?")
    # print(f"Status: {status}")
    # print(f"Answer: {answer[:200]}..." if answer else "No answer")
    print("(Skipped - requires network)")
