#!/usr/bin/env python3
"""
快速获取搜索地址工具 - 基于快速写源订阅源的智能分析

功能：
1. 自动检测网站编码
2. 下载并分析网页
3. 智能识别搜索表单
4. 自动生成搜索地址
5. 可选：生成书源草稿
"""

import sys
import json
import time
import re
import hashlib
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


class QuickSearchUrlExtractor:
    """快速搜索地址提取器"""
    
    def __init__(self, url, headers=None, timeout=10):
        self.url = url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.timeout = timeout
        self.base_url = self._get_base_url()
        
    def _get_base_url(self):
        """提取基础URL"""
        parsed = urlparse(self.url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def fetch_page(self, url=None):
        """获取网页内容"""
        target_url = url or self.url
        print(f"正在获取: {target_url}")
        
        try:
            response = requests.get(
                target_url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            # 检测编码
            charset = self._detect_charset(response)
            if charset:
                response.encoding = charset
            
            print(f"✓ 状态码: {response.status_code}")
            print(f"✓ 编码: {charset or 'UTF-8'}")
            print(f"✓ 大小: {len(response.text)} 字符")
            
            return response.text, charset
            
        except Exception as e:
            print(f"✗ 获取失败: {e}")
            return None, None
    
    def _detect_charset(self, response):
        """检测页面编码"""
        # 优先从响应头获取
        content_type = response.headers.get('Content-Type', '')
        charset_match = re.search(r'charset=([^\s;]+)', content_type, re.I)
        if charset_match:
            return charset_match.group(1).upper()
        
        # 从HTML meta标签获取
        html = response.text
        charset_patterns = [
            r'<meta[^>]+charset=["\']?([^\s"\'>]+)',
            r'<meta[^>]+content=["\'][^"\']*charset=([^\s"\'>]+)'
        ]
        
        for pattern in charset_patterns:
            match = re.search(pattern, html, re.I)
            if match:
                return match.group(1).upper()
        
        return 'UTF-8'  # 默认
    
    def analyze_forms(self, html):
        """分析页面中的表单"""
        soup = BeautifulSoup(html, 'html.parser')
        forms = soup.find_all('form')
        
        print(f"\n找到 {len(forms)} 个表单")
        
        search_results = []
        
        for idx, form in enumerate(forms, 1):
            print(f"\n--- 表单 {idx} ---")
            
            action = form.get('action', '')
            method = form.get('method', 'GET').upper()
            
            # 转换为绝对URL
            if action:
                action = urljoin(self.base_url, action)
            
            print(f"Action: {action}")
            print(f"Method: {method}")
            
            # 分析表单字段
            inputs = form.find_all(['input', 'select', 'textarea'])
            print(f"字段数: {len(inputs)}")
            
            fields = []
            for inp in inputs:
                name = inp.get('name', '')
                field_type = inp.get('type', 'text')
                value = inp.get('value', '')
                placeholder = inp.get('placeholder', '')
                
                fields.append({
                    'name': name,
                    'type': field_type,
                    'value': value,
                    'placeholder': placeholder
                })
                
                print(f"  - {name} (type={field_type}, value={value}, placeholder={placeholder})")
            
            # 智能识别搜索字段
            search_field = self._identify_search_field(fields)
            
            if search_field:
                # 生成搜索地址
                search_url = self._generate_search_url(action, method, fields, search_field)
                
                search_results.append({
                    'index': idx,
                    'action': action,
                    'method': method,
                    'search_field': search_field,
                    'search_url': search_url
                })
                
                print(f"\n✓ 识别为搜索表单!")
                print(f"✓ 搜索字段: {search_field}")
                print(f"✓ 搜索地址: {search_url}")
            else:
                print(f"\n✗ 未识别为搜索表单")
        
        return search_results
    
    def _identify_search_field(self, fields):
        """智能识别搜索字段"""
        # 策略1: 单个字段
        if len(fields) == 1:
            return fields[0]['name']
        
        # 策略2: 常见搜索字段名
        common_names = ['q', 'wd', 'query', 'search', 'key', 'keyword', 'k', 's']
        for field in fields:
            if field['name'].lower() in common_names:
                return field['name']
        
        # 策略3: 包含"search"/"key"的字段名
        for field in fields:
            if 'search' in field['name'].lower() or 'key' in field['name'].lower():
                return field['name']
        
        # 策略4: 文本类型且无默认值
        for field in fields:
            if field['type'] == 'text' and not field['value']:
                return field['name']
        
        return None
    
    def _generate_search_url(self, action, method, fields, search_field):
        """生成搜索地址"""
        # 构建参数
        params = []
        for field in fields:
            if field['name'] == search_field:
                value = '{{key}}'
            elif field['value']:
                value = field['value']
            else:
                # 尝试从select中获取默认值
                value = ''
            
            if value:
                params.append(f"{field['name']}={value}")
        
        body = '&'.join(params)
        
        # 根据方法生成地址
        if method == 'GET' or method == '':
            if body:
                return f"{action}?{body}"
            return action
        elif method == 'POST':
            options = {'method': 'POST', 'body': body}
            
            # 检测编码（如果不是UTF-8）
            # 这里简化处理，实际应该检测
            if not action.startswith('http'):
                action = urljoin(self.base_url, action)
            
            return f"{action},{json.dumps(options)}"
        
        return action
    
    def analyze_explore_links(self, html):
        """分析发现规则链接"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 常见的发现规则关键词
        explore_keywords = [
            'sort', 'list', 'rank', 'tag', 'shuku', 'fenlei',
            'Soft', 'allvisit', 'paihang', 'quanben', 'gudian',
            'lishi', 'dushi', 'wangyou', 'kehuan', 'yanqing',
            'wuxia', 'xuanhuan', 'chuanyue', 'zhentan', 'kongbu',
            'top', 'category', 'mulu'
        ]
        
        # 构建选择器
        explore_links = []
        for keyword in explore_keywords:
            links = soup.select(f'a[href*="{keyword}"]')
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # 排除数字和下一页等
                if text and not text.isdigit() and text not in ['下一页', '登录', '注册', 'More+']:
                    explore_links.append({
                        'title': text,
                        'url': href
                    })
        
        # 去重
        seen = set()
        unique_links = []
        for link in explore_links:
            if link['url'] not in seen:
                seen.add(link['url'])
                unique_links.append(link)
        
        print(f"\n发现 {len(unique_links)} 个潜在的发现规则链接")
        return unique_links[:20]  # 限制数量
    
    def generate_book_source_draft(self, search_results, explore_links, charset):
        """生成书源草稿"""
        if not search_results:
            return None
        
        best_result = search_results[0]
        search_url = best_result['search_url']
        
        # 尝试获取OG元数据
        html, _ = self.fetch_page()
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取OG标签
        og_tags = {}
        for meta in soup.find_all('meta', property=True):
            og_tags[meta['property']] = meta.get('content', '')
        
        # 构建书源草稿
        source = {
            'bookSourceName': f"快速生成的书源_{int(time.time())}",
            'bookSourceUrl': self.base_url,
            'bookSourceType': 0,
            'bookSourceComment': f'//快速写源生成\n//创建时间: {datetime.now().isoformat()}',
            'searchUrl': search_url,
            'customOrder': 0,
            'enabled': True,
            'enabledCookieJar': False,
            'ruleSearch': {
                'bookList': '',  # 需要用户补充
                'name': '',
                'author': '',
                'kind': '',
                'lastChapter': '',
                'bookUrl': '',
                'coverUrl': ''
            },
            'ruleBookInfo': {
                'name': og_tags.get('og:novel:book_name', ''),
                'author': og_tags.get('og:novel:author', ''),
                'coverUrl': og_tags.get('og:image', ''),
                'intro': og_tags.get('og:description', ''),
                'kind': '',
                'lastChapter': og_tags.get('og:novel:last_chapter_name', ''),
                'tocUrl': ''
            },
            'ruleToc': {
                'chapterList': '',
                'chapterName': '',
                'chapterUrl': '',
                'nextTocUrl': ''
            },
            'ruleContent': {
                'content': '',
                'nextContentUrl': ''
            },
            'exploreUrl': '',
            'weight': 0,
            'respondTime': 180000,
            'lastUpdateTime': int(time.time() * 1000)
        }
        
        # 如果有发现规则
        if explore_links:
            explore_rules = []
            for link in explore_links[:10]:
                # 转换为相对路径并支持分页
                url = link['url']
                # 替换末尾数字为{{page}}
                url = re.sub(r'\d+(\.html?)(/)?$', r'{{page}}\1\2', url)
                explore_rules.append(f"{link['title']}::{url}")
            
            source['exploreUrl'] = ','.join(explore_rules)
            source['enabledExplore'] = True
        
        return source
    
    def run(self):
        """运行分析"""
        print("=" * 70)
        print("快速搜索地址提取工具")
        print("=" * 70)
        print(f"目标网站: {self.url}")
        print()
        
        # 1. 获取页面
        html, charset = self.fetch_page()
        if not html:
            return None
        
        # 2. 分析表单
        search_results = self.analyze_forms(html)
        
        # 3. 分析发现规则
        explore_links = self.analyze_explore_links(html)
        
        # 4. 生成书源草稿
        draft = self.generate_book_source_draft(search_results, explore_links, charset)
        
        # 5. 输出结果
        print("\n" + "=" * 70)
        print("分析结果")
        print("=" * 70)
        
        if search_results:
            print(f"\n✓ 成功识别 {len(search_results)} 个搜索表单\n")
            
            for result in search_results:
                print(f"表单 {result['index']}:")
                print(f"  搜索字段: {result['search_field']}")
                print(f"  搜索地址: {result['search_url']}")
                print()
            
            if explore_links:
                print(f"✓ 发现规则 ({len(explore_links)} 个):")
                for link in explore_links[:5]:
                    print(f"  - {link['title']}: {link['url']}")
                print()
            
            if draft:
                print("✓ 书源草稿已生成")
                
                # 保存草稿
                timestamp = int(time.time())
                draft_file = Path(f'book_source_draft_{timestamp}.json')
                with open(draft_file, 'w', encoding='utf-8') as f:
                    json.dump([draft], f, ensure_ascii=False, indent=2)
                
                print(f"  草稿文件: {draft_file}")
                print()
                print("⚠️  注意: 书源草稿需要您补充以下内容:")
                print("  1. ruleSearch 的所有规则")
                print("  2. ruleToc 的所有规则")
                print("  3. ruleContent 的所有规则")
                print()
                
            return {
                'search_results': search_results,
                'explore_links': explore_links,
                'draft': draft
            }
        else:
            print("\n✗ 未找到搜索表单")
            print("\n建议:")
            print("  1. 检查URL是否正确")
            print("  2. 确认网站是否有搜索功能")
            print("  3. 尝试使用浏览器开发者工具手动分析")
            return None


def main():
    if len(sys.argv) < 2:
        print("用法: python quick_search_url_extractor.py <URL>")
        print("示例: python quick_search_url_extractor.py https://www.example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    
    extractor = QuickSearchUrlExtractor(url)
    result = extractor.run()
    
    if result:
        print("=" * 70)
        print("分析完成!")
        print("=" * 70)
    else:
        print("=" * 70)
        print("分析失败")
        print("=" * 70)
        sys.exit(1)


if __name__ == '__main__':
    main()
