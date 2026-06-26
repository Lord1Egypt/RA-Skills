#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通用网站分析工具 - 支持任意URL
Usage: python analyze_url.py <url> [--method POST] [--body "key={{key}}"] [--charset gbk]
"""

import sys, io, json, re, argparse, time
from urllib.parse import urlparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("缺少依赖: pip install requests beautifulsoup4")
    sys.exit(1)

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def detect_encoding(url, headers):
    """检测编码"""
    try:
        r = requests.get(url, headers=headers, timeout=15)
        charset = r.apparent_encoding or r.encoding or 'utf-8'
        return charset.lower(), r
    except Exception as e:
        return 'utf-8', None

def analyze_html(html, charset='utf-8'):
    """分析HTML结构"""
    soup = BeautifulSoup(html, 'html.parser')
    
    result = {
        'title': soup.title.string if soup.title else None,
        'charset': charset,
        'forms': [],
        'links': {'internal': 0, 'external': 0},
        'images': len(soup.find_all('img')),
        'scripts': len(soup.find_all('script')),
        'possible_list_containers': [],
        'possible_content_containers': [],
    }
    
    # 分析表单（搜索接口线索）
    for form in soup.find_all('form'):
        form_info = {
            'action': form.get('action', ''),
            'method': form.get('method', 'GET').upper(),
            'inputs': []
        }
        for inp in form.find_all(['input', 'select']):
            form_info['inputs'].append({
                'name': inp.get('name', ''),
                'type': inp.get('type', 'text'),
                'value': inp.get('value', '')
            })
        result['forms'].append(form_info)
    
    # 查找可能的列表容器
    list_patterns = ['list', 'result', 'book', 'item', 'search', 'novel']
    for tag in soup.find_all(['div', 'ul', 'ol', 'section']):
        cls = ' '.join(tag.get('class', []))
        id_ = tag.get('id', '')
        combined = (cls + ' ' + id_).lower()
        if any(p in combined for p in list_patterns):
            children = tag.find_all(['li', 'div', 'a'], recursive=False)
            if len(children) >= 3:
                result['possible_list_containers'].append({
                    'tag': tag.name,
                    'class': cls,
                    'id': id_,
                    'child_count': len(children)
                })
    
    # 查找可能的内容容器
    content_patterns = ['content', 'chapter', 'text', 'article', 'body']
    for tag in soup.find_all(['div', 'article', 'section']):
        cls = ' '.join(tag.get('class', []))
        id_ = tag.get('id', '')
        combined = (cls + ' ' + id_).lower()
        if any(p in combined for p in content_patterns):
            text_len = len(tag.get_text(strip=True))
            if text_len > 200:
                result['possible_content_containers'].append({
                    'tag': tag.name,
                    'class': cls,
                    'id': id_,
                    'text_length': text_len
                })
    
    return result

def find_search_urls(html, base_url):
    """识别搜索接口"""
    soup = BeautifulSoup(html, 'html.parser')
    candidates = []
    
    for form in soup.find_all('form'):
        action = form.get('action', '')
        method = form.get('method', 'GET').upper()
        if action:
            from urllib.parse import urljoin
            full_url = urljoin(base_url, action)
            keyword_inputs = []
            for inp in form.find_all('input'):
                name = inp.get('name', '')
                itype = inp.get('type', 'text')
                if name and itype in ('text', 'search', 'hidden'):
                    keyword_inputs.append(name)
            candidates.append({
                'url': full_url,
                'method': method,
                'params': keyword_inputs,
                'template': f"{full_url}?{keyword_inputs[0]}={{key}}" if keyword_inputs and method == 'GET' else None
            })
    
    return candidates

def main():
    parser = argparse.ArgumentParser(description='通用网站分析')
    parser.add_argument('url', help='目标URL')
    parser.add_argument('--method', default='GET', help='HTTP方法')
    parser.add_argument('--body', default=None, help='POST body模板')
    parser.add_argument('--charset', default=None, help='强制编码')
    parser.add_argument('--search-url', default=None, help='已知搜索URL')
    args = parser.parse_args()
    
    headers = DEFAULT_HEADERS.copy()
    
    print("=" * 60)
    print("步骤 1: 编码检测")
    print("=" * 60)
    detected_charset, resp = detect_encoding(args.url, headers)
    charset = args.charset or detected_charset
    print(f"检测到编码: {charset}")
    
    if args.body:
        print(f"\n步骤 2: POST请求 ({args.url})")
        print(f"Body: {args.body}")
        if 'gbk' in charset:
            encoded_body = args.body.encode('gbk')
        else:
            encoded_body = args.body.encode('utf-8')
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        resp = requests.post(args.url, data=encoded_body, headers=headers, timeout=15)
    elif not resp:
        resp = requests.get(args.url, headers=headers, timeout=15)
    
    print(f"\n状态码: {resp.status_code}")
    print(f"内容长度: {len(resp.text)} 字符")
    
    html = resp.text
    print(f"\n{'=' * 60}")
    print("步骤 3: HTML结构分析")
    print("=" * 60)
    analysis = analyze_html(html, charset)
    print(json.dumps(analysis, ensure_ascii=False, indent=2))
    
    print(f"\n{'=' * 60}")
    print("步骤 4: 搜索接口识别")
    print("=" * 60)
    search_urls = find_search_urls(html, args.url)
    if search_urls:
        for su in search_urls:
            print(f"  方法: {su['method']}")
            print(f"  URL: {su['url']}")
            print(f"  参数: {su['params']}")
            if su['template']:
                print(f"  模板: {su['template']}")
            print()
    else:
        print("  未找到搜索表单，请手动检查 Network 面板")
    
    # 保存HTML
    safe_name = urlparse(args.url).netloc.replace('.', '_')
    out_file = f"{safe_name}_analysis.html"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\nHTML已保存: {out_file}")

if __name__ == '__main__':
    main()
