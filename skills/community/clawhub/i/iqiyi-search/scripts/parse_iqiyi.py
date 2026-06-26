#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爱奇艺搜索结果解析器
"""

import json
import re
import sys
from html.parser import HTMLParser

class IqiyiParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.current_tag = {}
        self.in_result_item = False
        self.capture_text = False
        self.text_buffer = ""
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # 检测搜索结果项
        if tag == 'div' and 'class' in attrs_dict:
            classes = attrs_dict.get('class', '')
            if 'qy-search-result-item' in classes or 'result-item' in classes:
                self.in_result_item = True
                self.current_tag = {'type': 'result_item'}
        
        # 检测链接
        elif tag == 'a' and self.in_result_item:
            href = attrs_dict.get('href', '')
            if href and ('iqiyi.com' in href or href.startswith('/')):
                self.current_tag['url'] = href
        
        # 检测标题
        elif tag in ['h3', 'h4'] and self.in_result_item:
            self.capture_text = True
            self.text_buffer = ""
            
        # 检测图片/缩略图
        elif tag == 'img' and self.in_result_item:
            alt = attrs_dict.get('alt', '')
            if alt:
                self.current_tag['title'] = alt
    
    def handle_data(self, data):
        if self.capture_text:
            self.text_buffer += data.strip()
    
    def handle_endtag(self, tag):
        if tag in ['h3', 'h4'] and self.capture_text:
            self.capture_text = False
            if self.text_buffer:
                self.current_tag['title'] = self.text_buffer
                self.text_buffer = ""
        
        if tag == 'div' and self.in_result_item:
            # 保存当前结果
            if 'title' in self.current_tag and 'url' in self.current_tag:
                url = self.current_tag['url']
                if not url.startswith('http'):
                    url = 'https://www.iqiyi.com' + url
                
                self.results.append({
                    'title': self.current_tag.get('title', ''),
                    'type': self.current_tag.get('type_name', '影视'),
                    'description': self.current_tag.get('desc', ''),
                    'url': url,
                    'rating': self.current_tag.get('rating', '')
                })
            
            self.in_result_item = False
            self.current_tag = {}


def parse_from_json(html_content):
    """尝试从页面中的JSON数据提取搜索结果"""
    results = []
    
    # 尝试提取__INITIAL_STATE__
    patterns = [
        r'window\.__INITIAL_STATE__\s*=\s*({.+?});',
        r'window\.__INITIAL_STATE__\s*=\s*({.+?})\s*\u003c/script\u003e',
        r'window\.__INITIAL_STATE__\s*=\s*(\{[\s\S]*?\});\s*\u003c/script\u003e',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                
                # 尝试不同的数据路径
                search_data = None
                if 'searchResult' in data:
                    search_data = data['searchResult']
                elif 'search' in data:
                    search_data = data['search']
                elif 'data' in data and 'searchResult' in data['data']:
                    search_data = data['data']['searchResult']
                
                if search_data:
                    if 'data' in search_data:
                        items = search_data['data']
                    elif 'result' in search_data:
                        items = search_data['result']
                    else:
                        items = search_data
                    
                    for item in items[:10]:
                        if isinstance(item, dict):
                            title = item.get('title', '') or item.get('displayName', '') or item.get('name', '')
                            url = item.get('url', '') or item.get('pageUrl', '') or item.get('playUrl', '')
                            desc = item.get('description', '') or item.get('shortTitle', '') or item.get('brief', '')
                            type_name = item.get('categoryName', '') or item.get('typeName', '') or item.get('category', '影视')
                            rating = item.get('score', '') or item.get('rating', '')
                            
                            if title and url:
                                if not url.startswith('http'):
                                    url = 'https:' + url if url.startswith('//') else 'https://www.iqiyi.com' + url
                                
                                # 清理HTML标签
                                title = re.sub(r'\u003c[^\u003e]+\u003e', '', title)
                                desc = re.sub(r'\u003c[^\u003e]+\u003e', '', desc)
                                
                                results.append({
                                    'title': title,
                                    'type': type_name,
                                    'description': desc[:150] + '...' if len(desc) > 150 else desc,
                                    'url': url,
                                    'rating': str(rating) if rating else ''
                                })
                
                if results:
                    return results
                    
            except json.JSONDecodeError:
                continue
    
    return results


def parse_from_html(html_content):
    """从HTML中提取搜索结果"""
    results = []
    
    # 尝试提取剧集卡片
    # 模式1: 搜索结果卡片
    card_pattern = r'\u003cdiv[^\u003e]*class="[^"]*qy-search-result-item[^"]*"[^\u003e]*\u003e.*?\u003c/div\u003e'
    cards = re.findall(card_pattern, html_content, re.DOTALL | re.IGNORECASE)
    
    seen_urls = set()
    
    for card in cards[:10]:
        # 提取链接
        link_match = re.search(r'\u003ca[^\u003e]*href="([^"]+)"[^\u003e]*\u003e', card)
        if not link_match:
            continue
        
        url = link_match.group(1)
        if url in seen_urls:
            continue
        seen_urls.add(url)
        
        if not url.startswith('http'):
            url = 'https://www.iqiyi.com' + url
        
        # 提取标题
        title = ''
        # 尝试从alt属性提取
        alt_match = re.search(r'alt="([^"]*)"', card)
        if alt_match:
            title = alt_match.group(1)
        
        # 尝试从标题标签提取
        if not title:
            title_match = re.search(r'\u003ch[34][^\u003e]*\u003e.*?\u003e([^\u003c]+)\u003c', card)
            if title_match:
                title = title_match.group(1).strip()
        
        # 尝试从特定class提取
        if not title:
            title_match = re.search(r'class="[^"]*title[^"]*"[^\u003e]*\u003e([^\u003c]+)\u003c', card)
            if title_match:
                title = title_match.group(1).strip()
        
        # 提取描述
        desc = ''
        desc_match = re.search(r'class="[^"]*desc[^"]*"[^\u003e]*\u003e([^\u003c]+)\u003c', card)
        if desc_match:
            desc = desc_match.group(1).strip()
        
        # 提取类型
        type_name = '影视'
        type_match = re.search(r'class="[^"]*category[^"]*"[^\u003e]*\u003e([^\u003c]+)\u003c', card)
        if type_match:
            type_name = type_match.group(1).strip()
        
        # 提取评分
        rating = ''
        rating_match = re.search(r'(\d+\.?\d*)\s*分', card)
        if rating_match:
            rating = rating_match.group(1)
        
        if title:
            results.append({
                'title': title,
                'type': type_name,
                'description': desc[:150] + '...' if len(desc) > 150 else desc,
                'url': url,
                'rating': rating
            })
    
    return results


def parse_from_links(html_content):
    """备用方法：从所有链接中提取"""
    results = []
    seen = set()
    
    # 查找所有iqiyi链接
    pattern = r'\u003ca[^\u003e]*href="(https?://www\.iqiyi\.com/[^"]+)"[^\u003e]*[^\u003e]*\u003e\s*([^\u003c]*(?:\u003c[^\u003e]+\u003e[^\u003c]*)*)\s*\u003c/a\u003e'
    matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
    
    for url, title_html in matches[:10]:
        if url in seen or 'login' in url or 'passport' in url:
            continue
        seen.add(url)
        
        # 清理标题中的HTML标签
        title = re.sub(r'\u003c[^\u003e]+\u003e', '', title_html).strip()
        
        if title and len(title) > 2:
            results.append({
                'title': title,
                'type': '影视',
                'description': '',
                'url': url,
                'rating': ''
            })
    
    return results


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "参数不足", "usage": "parse_iqiyi.py <html_file> <keyword>", "results": []}, ensure_ascii=False))
        sys.exit(1)
    
    html_file = sys.argv[1]
    keyword = sys.argv[2]
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(json.dumps({"error": f"读取文件失败: {str(e)}", "results": []}, ensure_ascii=False))
        sys.exit(1)
    
    # 尝试多种解析方法
    results = parse_from_json(html_content)
    
    if not results:
        results = parse_from_html(html_content)
    
    if not results:
        results = parse_from_links(html_content)
    
    # 返回结果
    output = {
        'keyword': keyword,
        'count': len(results),
        'results': results[:10]  # 最多返回10条
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
