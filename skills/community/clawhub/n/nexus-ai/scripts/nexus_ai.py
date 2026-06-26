#!/usr/bin/env python3
"""Nexus-AI 主脚本：发布资源 / 查询报告 / 智能问答"""

import argparse
import json
import os
import re
import urllib.parse
import urllib.request
import urllib.error
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QR_IMAGE = os.path.join(SCRIPT_DIR, 'nexus_qr.png')

NEXUS_BASE = 'https://nexus-saas-45653-8-1317958785.sh.run.tcloudbase.com'
RAG_URL = 'https://ai.hydts.cn/ai/rag-stream'


def get_miniapp_url(path='pages/index/index'):
    """动态获取小程序链接"""
    url = f'{NEXUS_BASE}/sys/get-app-url'
    payload = {'path': path, 'env_version': 'release'}
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            if result.get('code') == 0:
                return result.get('url_link', '')
    except Exception as e:
        pass
    return ''


# ── 工具函数 ────────────────────────────────────────────────

def detect_label(title: str, content: str) -> str:
    """根据标题和内容自动判断资源类型 label"""
    text = (title + ' ' + content).lower()
    if any(kw in text for kw in ['招聘', '实习', '校招', '校园', '春招', '秋招', '应届', '管培']):
        return '社会招聘'
    if any(kw in text for kw in ['投资', '融资', '天使轮', 'a轮', 'b轮', '估值', '资金']):
        return '投/融资'
    if any(kw in text for kw in ['活动', '交流会', '论坛', '峰会', '沙龙', '会议', 'meetup']):
        return '活动交流'
    if any(kw in text for kw in ['推广', '置顶', 'vip', '赞助', '推广位', '广告']):
        return '置顶推广'
    return '需求'


def strip_html(text: str) -> str:
    """去除 HTML 标签，保留纯文本"""
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<p[^>]*>', '\n', text)
    text = re.sub(r'</p>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ── 功能一：发布资源 ─────────────────────────────────────────

def cmd_post(phone: str, title: str, content: str):
    label = detect_label(title, content)
    print(f'自动识别 label: {label}')

    params = urllib.parse.urlencode({
        'phone': phone,
        'title': title,
        'content': content,
        'label': label
    })
    url = f'{NEXUS_BASE}/job/open-claw-create-job?{params}'
    req = urllib.request.Request(url, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            print(json.dumps(result, ensure_ascii=False, indent=2))
            if result.get('code') == 0:
                job_id = result.get('jobId', '')
                print(f'\n✅ 发布成功！资源ID: {job_id}')
                # 动态获取小程序链接，资源详情页 path
                mini_path = f'pages/jobInfo/jobInfoDetail/jobInfoDetail?jobId={job_id}' if job_id else 'pages/index/index'
                mini_url = get_miniapp_url(mini_path)
                if mini_url:
                    print(f'\n🔗 Nexus：{mini_url}')
                else:
                    print(f'\n🔗 Nexus：获取链接失败')
                print(f'📷 二维码图片：{QR_IMAGE}')
            else:
                print(f'\n❌ 发布失败: {result.get("msg", "未知错误")}')
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f'HTTP Error {e.code}: {body}')
        sys.exit(1)


# ── 功能二：查询使用报告 ──────────────────────────────────────

def cmd_summary(phone: str):
    url = f'{NEXUS_BASE}/summary/content_by_phone?phone={phone}'
    req = urllib.request.Request(url, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            if result.get('code') == 0:
                content_html = result.get('content', '')
                content_text = strip_html(content_html)
                print(content_text)
                # 动态获取小程序首页链接
                mini_url = get_miniapp_url('pages/index/index')
                if mini_url:
                    print(f'\n🔗 Nexus：{mini_url}')
                print(f'📷 二维码图片：{QR_IMAGE}')
            else:
                print(f'错误: {result.get("msg", "未知错误")}')
                sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f'HTTP Error {e.code}')
        sys.exit(1)


# ── 功能三：智能问答 ──────────────────────────────────────────

def cmd_ask(query: str, session_id: str = None, identity: str = None):
    """调用 RAG 智能搜索接口（流式 SSE 响应）"""
    payload = {
        'query': query,
        'mod': 'coze',
        'identity': identity or 'default',
        'intelligent_agent': '7615042672550068270',
    }
    if session_id:
        payload['session_id'] = session_id

    req = urllib.request.Request(
        RAG_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            content_type = resp.headers.get('Content-Type', '')
            raw = resp.read()

            # 判断是否 SSE 流式响应
            if 'text/event-stream' in content_type or raw.startswith(b'session_id'):
                # SSE 格式：第一行是 session_id，后续是内容
                lines = raw.decode('utf-8', errors='replace').split('\n')
                first = lines[0].strip()
                # 如果第一行是纯数字/session_id，把它单独输出
                if first and not first.startswith('{') and len(first) < 100:
                    print(first)
                    print()
                    content = '\n'.join(lines[1:]).strip()
                else:
                    content = raw.decode('utf-8', errors='replace').strip()

                # 去除 Nexus 小程序链接和 URL
                content = re.sub(r'资源链接[：:]\s*[^\n]*', '', content)
                content = re.sub(r'(?<= \| )/pages/[^\n|]*(?=\s*\|)', '', content)
                content = re.sub(r'https?://[^\s\n|]+', '', content)
                content = re.sub(r'\n{3,}', '\n\n', content)
                content = re.sub(r'\s+\|', '|', content)
                content = re.sub(r'\|\s+', '|', content)
                print(content.strip())
                # 动态获取小程序首页链接
                mini_url = get_miniapp_url('pages/index/index')
                if mini_url:
                    print(f'\n🔗 Nexus：{mini_url}')
                print(f'📷 二维码图片：{QR_IMAGE}')
            else:
                # 普通 JSON 响应
                result = json.loads(raw.decode('utf-8'))
                text = result.get('text', result.get('content', ''))
                if session_id:
                    print(session_id)
                    print()
                    print(text)
                else:
                    print(text)
                # 动态获取小程序首页链接
                mini_url = get_miniapp_url('pages/index/index')
                if mini_url:
                    print(f'\n🔗 Nexus：{mini_url}')
                print(f'📷 二维码图片：{QR_IMAGE}')
    except urllib.error.HTTPError as e:
        print(f'HTTP Error {e.code}: {e.read().decode("utf-8")}')
        sys.exit(1)
    except Exception as e:
        print(f'请求失败: {e}')
        sys.exit(1)


# ── CLI 入口 ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Nexus-AI 智能助手')
    sub = parser.add_subparsers(dest='cmd', required=True)

    # post
    p = sub.add_parser('post', help='发布资源/岗位/活动')
    p.add_argument('--phone', required=True, help='用户手机号')
    p.add_argument('--title', required=True, help='标题')
    p.add_argument('--content', required=True, help='正文内容')

    # summary
    s = sub.add_parser('summary', help='查询使用报告')
    s.add_argument('--phone', required=True, help='用户手机号')

    # ask
    a = sub.add_parser('ask', help='智能问答 RAG 搜索')
    a.add_argument('--query', required=True, help='询问内容')
    a.add_argument('--session-id', default=None, help='会话 ID（可选）')
    a.add_argument('--identity', default=None, help='身份标识（可选）')

    args = parser.parse_args()

    if args.cmd == 'post':
        cmd_post(args.phone, args.title, args.content)
    elif args.cmd == 'summary':
        cmd_summary(args.phone)
    elif args.cmd == 'ask':
        cmd_ask(args.query, args.session_id, args.identity)


if __name__ == '__main__':
    main()