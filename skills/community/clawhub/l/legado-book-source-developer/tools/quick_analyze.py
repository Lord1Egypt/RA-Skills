#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速网站分析工具 - 增强版 v2.1
用于快速分析网站结构、编码和搜索接口
优化：自动存储HTML到html_storage，输出符合JSON格式的书源
"""

import sys
import io
import json
import re
import time
import hashlib
from urllib.parse import urlparse, urljoin
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"错误: 缺少依赖库 - {e}")
    print("请运行: pip install requests beautifulsoup4")
    sys.exit(1)

# 默认请求头
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


class HTMLStorage:
    """HTML存储管理器 - 存储到references/html_storage"""

    def __init__(self, storage_dir='references/html_storage'):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def generate_hash(self, url):
        """根据URL生成唯一哈希值"""
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def save_html(self, url, content, page_type='page'):
        """
        保存HTML到storage目录

        Args:
            url: 原始URL
            content: HTML内容
            page_type: 页面类型 (home, search, detail, toc, content)

        Returns:
            dict: 包含文件路径和元数据的字典
        """
        file_hash = self.generate_hash(url)
        html_filename = self.storage_dir / f"{file_hash}.html"
        meta_filename = self.storage_dir / f"{file_hash}.meta.json"

        # 保存HTML文件
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(content)

        # 生成元数据
        metadata = {
            'url': url,
            'size': len(content),
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'page_type': page_type,
            'storage_path': str(html_filename.relative_to(self.storage_dir.parent))
        }

        # 保存元数据JSON
        with open(meta_filename, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        return {
            'hash': file_hash,
            'html_file': str(html_filename),
            'meta_file': str(meta_filename),
            'metadata': metadata
        }


class QuickAnalyzer:
    """快速网站分析器"""

    def __init__(self, base_url, storage_dir='references/html_storage', headers=None):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or DEFAULT_HEADERS
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.storage = HTMLStorage(storage_dir)

        self.info = {
            'base_url': base_url,
            'encoding': None,
            'charset': None,
            'html_files': {},
            'js_files': {},
            'search_patterns': [],
            'detected_selectors': {},
            'book_source_draft': None
        }

    def detect_encoding(self):
        """检测网站编码并保存首页"""
        print("=" * 70)
        print("步骤 1：检测网站编码并保存首页")
        print("=" * 70)

        try:
            response = self.session.get(self.base_url, timeout=15)
            print(f"✓ 状态码: {response.status_code}")
            print(f"✓ 响应编码: {response.encoding}")
            print(f"✓ Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"✓ 实际编码: {response.apparent_encoding}")
            print(f"✓ 页面长度: {len(response.text)} 字符")

            # 确定最终编码
            content_type = response.headers.get('Content-Type', '')
            charset_match = re.search(r'charset=([^\s;]+)', content_type, re.I)
            
            if charset_match:
                detected_charset = charset_match.group(1).lower()
            else:
                detected_charset = response.apparent_encoding

            self.info['encoding'] = detected_charset
            self.info['charset'] = detected_charset

            # 保存首页到html_storage
            saved = self.storage.save_html(self.base_url, response.text, page_type='home')
            self.info['html_files']['home'] = saved
            print(f"✓ 首页已保存: {saved['html_file']}")
            print(f"✓ 元数据: {saved['meta_file']}")

            return response.text

        except Exception as e:
            print(f"✗ 错误: {e}")
            raise

    def find_javascript_files(self, html):
        """查找并保存JavaScript文件"""
        print("\n" + "=" * 70)
        print("步骤 2：查找JavaScript文件")
        print("=" * 70)

        soup = BeautifulSoup(html, 'html.parser')
        scripts = soup.find_all('script')

        js_urls = []
        for script in scripts:
            if script.get('src'):
                src = script.get('src')
                # 转换为绝对URL
                absolute_url = urljoin(self.base_url, src)
                js_urls.append(absolute_url)

        print(f"✓ 找到 {len(js_urls)} 个外部JavaScript文件")

        # 下载并保存JS文件
        for i, js_url in enumerate(js_urls[:10], 1):  # 只下载前10个
            try:
                print(f"  [{i}/{min(len(js_urls), 10)}] 下载: {js_url}")
                response = self.session.get(js_url, timeout=10)
                js_content = response.text

                # 保存JS文件
                js_hash = hashlib.md5(js_url.encode('utf-8')).hexdigest()
                js_filename = self.storage.storage_dir / f"{js_hash}.js"
                
                with open(js_filename, 'w', encoding='utf-8') as f:
                    f.write(js_content)

                # 保存元数据
                meta_filename = self.storage.storage_dir / f"{js_hash}.js.meta.json"
                metadata = {
                    'url': js_url,
                    'type': 'javascript',
                    'size': len(js_content),
                    'timestamp': time.time(),
                    'datetime': datetime.now().isoformat(),
                    'storage_path': str(js_filename.relative_to(self.storage.storage_dir.parent))
                }

                with open(meta_filename, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)

                self.info['js_files'][js_url] = {
                    'file': str(js_filename),
                    'meta': str(meta_filename)
                }

                print(f"      ✓ 已保存: {js_filename.name}")

            except Exception as e:
                print(f"      ✗ 下载失败: {e}")

        return js_urls

    def analyze_search_patterns(self, html):
        """分析搜索接口模式"""
        print("\n" + "=" * 70)
        print("步骤 3：分析搜索接口模式")
        print("=" * 70)

        soup = BeautifulSoup(html, 'html.parser')
        patterns = []

        # 查找搜索表单
        search_forms = soup.find_all('form')
        print(f"✓ 找到 {len(search_forms)} 个表单")

        for form in search_forms:
            form_action = form.get('action', '')
            if 'search' in form_action.lower() or 's.' in form_action:
                absolute_url = urljoin(self.base_url, form_action)
                method = form.get('method', 'GET').upper()

                print(f"\n  表单: {absolute_url}")
                print(f"    方法: {method}")

                inputs = form.find_all('input')
                params = []
                for inp in inputs:
                    name = inp.get('name', '')
                    inp_type = inp.get('type', 'text')
                    if name:
                        params.append({
                            'name': name,
                            'type': inp_type
                        })
                        print(f"    参数: {name} ({inp_type})")

                patterns.append({
                    'type': 'form',
                    'url': absolute_url,
                    'method': method,
                    'params': params
                })

        # 查找搜索链接
        search_links = soup.find_all('a', href=re.compile(r'search|s\.'))
        if search_links:
            print(f"\n✓ 找到 {len(search_links)} 个搜索相关链接")
            for link in search_links[:5]:  # 只显示前5个
                href = link.get('href', '')
                text = link.get_text(strip=True)
                absolute_url = urljoin(self.base_url, href)
                patterns.append({
                    'type': 'link',
                    'url': absolute_url,
                    'text': text
                })
                print(f"  链接: {text} -> {absolute_url}")

        self.info['search_patterns'] = patterns
        return patterns

    def analyze_html_structure(self, html):
        """分析HTML结构并推断选择器"""
        print("\n" + "=" * 70)
        print("步骤 4：分析HTML结构")
        print("=" * 70)

        soup = BeautifulSoup(html, 'html.parser')
        detected = {}

        # 常见的书籍列表选择器
        book_list_selectors = [
            '.book-list', '.result-list', '.search-result',
            'ul.hot_sale', '#sitebox dl', '#content .list li'
        ]

        for selector in book_list_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"✓ 找到书籍列表: {selector} ({len(elements)} 个)")
                detected['bookList'] = selector

                # 分析第一个书籍项的结构
                first_item = elements[0]
                print(f"\n  第一个书籍项的结构:")
                print(f"  {first_item.prettify()[:500]}...")

                # 尝试推断各个字段的选择器
                title_selectors = ['.title', 'h3', 'h4', 'a', '.name']
                for title_sel in title_selectors:
                    title = first_item.select_one(title_sel)
                    if title:
                        print(f"  ✓ 书名选择器: {selector} {title_sel}@text")
                        detected['name'] = title_sel
                        break

                author_selectors = ['.author', '.writer', '.by', 'p:nth-child(2)']
                for author_sel in author_selectors:
                    author = first_item.select_one(author_sel)
                    if author:
                        print(f"  ✓ 作者选择器: {selector} {author_sel}@text")
                        detected['author'] = author_sel
                        break

                cover_selectors = ['img', '.cover img', '.book-cover']
                for cover_sel in cover_selectors:
                    cover = first_item.select_one(cover_sel)
                    if cover:
                        # 检查懒加载
                        if cover.get('data-original'):
                            print(f"  ✓ 封面选择器: {selector} {cover_sel}@data-original||{cover_sel}@src")
                            detected['coverUrl'] = f"{cover_sel}@data-original||{cover_sel}@src"
                        else:
                            print(f"  ✓ 封面选择器: {selector} {cover_sel}@src")
                            detected['coverUrl'] = f"{cover_sel}@src"
                        break

                link_selectors = ['a', 'a[href]']
                for link_sel in link_selectors:
                    link = first_item.select_one(link_sel)
                    if link:
                        print(f"  ✓ 链接选择器: {selector} {link_sel}@href")
                        detected['bookUrl'] = link_sel
                        break

                break

        self.info['detected_selectors'] = detected
        return detected

    def generate_book_source_json(self):
        """生成符合标准格式的书源JSON"""
        print("\n" + "=" * 70)
        print("步骤 5：生成书源JSON")
        print("=" * 70)

        # 基础信息
        parsed_url = urlparse(self.base_url)
        book_source_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        book_source_name = f"示例书源_{parsed_url.netloc.replace('.', '_')}"

        # 构建searchUrl
        search_patterns = self.info.get('search_patterns', [])
        if search_patterns:
            pattern = search_patterns[0]
            if pattern['type'] == 'form':
                search_url = f"{pattern['url']}"
                # 添加参数配置
                config = {}
                if pattern['method'] != 'GET':
                    config['method'] = pattern['method']
                if self.info.get('charset') == 'gbk':
                    config['charset'] = 'gbk'
                if config:
                    search_url = f"{search_url},{json.dumps(config)}"
            else:
                search_url = pattern['url']
        else:
            # 默认搜索URL
            search_url = "/search?q={{key}}"
            if self.info.get('charset') == 'gbk':
                search_url = f"{search_url},{{\"charset\":\"gbk\"}}"

        # 获取检测到的选择器
        selectors = self.info.get('detected_selectors', {})

        # 构建书源JSON - 严格符合Legado格式
        book_source = {
            "bookSourceUrl": book_source_url,
            "bookSourceName": book_source_name,
            "bookSourceType": 0,
            "bookSourceGroup": "默认分组",
            "enabled": True,
            "enabledExplore": True,
            "enabledCookieJar": True,
            "loginUrl": "",
            "loginUi": "",
            "loginCheckJs": "",
            "concurrentRate": "",
            "header": json.dumps(DEFAULT_HEADERS, ensure_ascii=False),
            "searchUrl": search_url,
            "exploreUrl": "",
            "ruleSearch": {
                "bookList": selectors.get('bookList', '.book-list'),
                "name": selectors.get('name', '.title@text'),
                "author": selectors.get('author', '.author@text'),
                "kind": "",
                "wordCount": "",
                "lastChapter": "",
                "intro": "",
                "coverUrl": selectors.get('coverUrl', 'img@src'),
                "bookUrl": selectors.get('bookUrl', 'a@href')
            },
            "ruleBookInfo": {
                "name": "",
                "author": "",
                "kind": "",
                "wordCount": "",
                "lastChapter": "",
                "intro": "",
                "coverUrl": "",
                "init": ""
            },
            "ruleToc": {
                "chapterList": "",
                "chapterName": "",
                "chapterUrl": "",
                "formatJs": "",
                "nextTocUrl": ""
            },
            "ruleContent": {
                "content": "",
                "replaceRegex": "",
                "imageStyle": "",
                "imageDecode": "",
                "webJs": "",
                "nextContentUrl": "",
                "title": ""
            },
            "ruleExplore": {},
            "ruleReview": {},
            "bookSourceComment": f"由quick_analyze.py自动生成\\nURL: {self.base_url}\\n编码: {self.info.get('encoding', 'UTF-8')}",
            "variableComment": "{}"
        }

        self.info['book_source_draft'] = book_source

        # 保存书源JSON到文件
        output_file = f"book_source_{int(time.time())}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump([book_source], f, ensure_ascii=False, indent=2)

        print(f"\n✓ 书源JSON已生成: {output_file}")
        print(f"\n书源信息:")
        print(f"  书源名称: {book_source['bookSourceName']}")
        print(f"  书源URL: {book_source['bookSourceUrl']}")
        print(f"  搜索URL: {book_source['searchUrl']}")
        print(f"  编码: {self.info.get('encoding', 'UTF-8')}")

        return book_source, output_file

    def save_analysis_report(self):
        """保存分析报告"""
        print("\n" + "=" * 70)
        print("步骤 6：保存分析报告")
        print("=" * 70)

        report = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'base_url': self.base_url,
            'encoding': self.info.get('encoding'),
            'charset': self.info.get('charset'),
            'html_files': {k: v['html_file'] if isinstance(v, dict) else v for k, v in self.info.get('html_files', {}).items()},
            'js_files_count': len(self.info.get('js_files', {})),
            'search_patterns': self.info.get('search_patterns', []),
            'detected_selectors': self.info.get('detected_selectors', {}),
            'book_source_draft': self.info.get('book_source_draft')
        }

        report_file = f"analysis_report_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"✓ 分析报告已保存: {report_file}")
        print(f"\n报告内容:")
        print(f"  编码: {report['encoding']}")
        print(f"  HTML文件: {len(report['html_files'])} 个")
        print(f"  JS文件: {report['js_files_count']} 个")
        print(f"  搜索模式: {len(report['search_patterns'])} 个")
        print(f"  检测到的选择器: {len(report['detected_selectors'])} 个")

        return report_file

    def run(self):
        """执行完整分析流程"""
        print("\n" + "=" * 70)
        print("Legado 书源快速分析工具 v2.1")
        print("=" * 70)
        print(f"目标网站: {self.base_url}")
        print(f"存储目录: {self.storage.storage_dir.absolute()}")
        print("=" * 70 + "\n")

        try:
            # 步骤1: 检测编码并保存首页
            html = self.detect_encoding()

            # 步骤2: 查找JS文件
            self.find_javascript_files(html)

            # 步骤3: 分析搜索模式
            self.analyze_search_patterns(html)

            # 步骤4: 分析HTML结构
            self.analyze_html_structure(html)

            # 步骤5: 生成书源JSON
            book_source, output_file = self.generate_book_source_json()

            # 步骤6: 保存分析报告
            report_file = self.save_analysis_report()

            print("\n" + "=" * 70)
            print("✓ 分析完成！")
            print("=" * 70)
            print(f"\n生成的文件:")
            print(f"  1. 书源JSON: {output_file}")
            print(f"  2. 分析报告: {report_file}")
            print(f"  3. HTML文件: references/html_storage/*.html")
            print(f"  4. JS文件: references/html_storage/*.js")
            print(f"\n下一步:")
            print(f"  1. 查看生成的书源JSON: cat {output_file}")
            print(f"  2. 根据实际情况修改规则")
            print(f"  3. 导入Legado测试")

            return book_source, output_file

        except Exception as e:
            print(f"\n✗ 分析失败: {e}")
            import traceback
            traceback.print_exc()
            return None, None


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python quick_analyze.py <URL>")
        print("示例: python quick_analyze.py https://www.example.com")
        sys.exit(1)

    url = sys.argv[1]
    analyzer = QuickAnalyzer(url)
    analyzer.run()


if __name__ == "__main__":
    main()
