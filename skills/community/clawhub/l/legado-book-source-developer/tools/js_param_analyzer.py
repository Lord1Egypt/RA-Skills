#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JavaScript参数分析工具
用于分析和提取JavaScript中的参数生成逻辑
"""

import sys
import io
import re
import json
from urllib.parse import urlparse, urljoin

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"错误: 缺少依赖库 - {e}")
    print("请运行: pip install requests beautifulsoup4")
    sys.exit(1)


class JSParamAnalyzer:
    """JavaScript参数分析器"""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.js_functions = {}
        self.api_endpoints = []
        self.param_generators = {}

    def extract_javascript_from_html(self, html):
        """从HTML中提取所有JavaScript代码"""
        print("=" * 70)
        print("步骤 1：从HTML中提取JavaScript")
        print("=" * 70)

        soup = BeautifulSoup(html, 'html.parser')
        scripts = soup.find_all('script')

        all_js = []

        # 外部JS文件
        external_js = []
        for script in scripts:
            src = script.get('src')
            if src:
                external_js.append(urljoin(self.base_url, src))

        print(f"✓ 找到 {len(external_js)} 个外部JS文件")

        # 内联脚本
        inline_scripts = []
        for script in scripts:
            if script.string and script.string.strip():
                inline_scripts.append(script.string)

        print(f"✓ 找到 {len(inline_scripts)} 个内联脚本")

        return external_js, inline_scripts

    def download_and_analyze_js(self, js_urls):
        """下载并分析JS文件"""
        print("\n" + "=" * 70)
        print("步骤 2：下载并分析JavaScript文件")
        print("=" * 70)

        for i, js_url in enumerate(js_urls, 1):
            print(f"\n[{i}/{len(js_urls)}] 分析: {js_url}")

            try:
                response = self.session.get(js_url, timeout=15)
                js_content = response.text

                # 保存JS文件
                filename = js_url.split('/')[-1]
                if not filename.endswith('.js'):
                    filename += '.js'
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(js_content)
                print(f"  ✓ 已保存: {filename} ({len(js_content)} 字符)")

                # 分析JS内容
                self.analyze_js_functions(js_content, filename)
                self.find_api_endpoints(js_content, filename)
                self.find_param_generators(js_content, filename)

            except Exception as e:
                print(f"  ✗ 下载失败: {str(e)[:100]}")

    def analyze_js_functions(self, js_content, filename):
        """分析JavaScript中的函数"""
        
        # 查找函数定义
        function_patterns = [
            r'function\s+(\w+)\s*\(',
            r'(\w+)\s*:\s*function\s*\(',
            r'const\s+(\w+)\s*=\s*\(',
            r'let\s+(\w+)\s*=\s*\(',
            r'var\s+(\w+)\s*=\s*function\s*\('
        ]

        functions = []
        for pattern in function_patterns:
            matches = re.findall(pattern, js_content)
            functions.extend(matches)

        if functions:
            print(f"  • 找到 {len(set(functions))} 个函数")
            
            # 查找与搜索相关的函数
            search_related = [f for f in set(functions) 
                           if any(keyword in f.lower() 
                                for keyword in ['search', 'ajax', 'fetch', 'api', 'query', 'get'])]
            
            if search_related:
                print(f"    搜索相关函数: {', '.join(search_related[:10])}")
                self.js_functions[filename] = search_related

    def find_api_endpoints(self, js_content, filename):
        """查找API端点"""
        
        api_patterns = [
            r'["\']([^"\']*\/(?:api|ajax|search|query)[^"\']*)["\']',
            r'url\s*[:=]\s*["\']([^"\']+)["\']',
            r'baseURL\s*[:=]\s*["\']([^"\']+)["\']',
            r'apiUrl\s*[:=]\s*["\']([^"\']+)["\']',
            r'endpoint\s*[:=]\s*["\']([^"\']+)["\']',
            r'fetch\s*\(\s*["\']([^"\']+)["\']',
            r'\.get\s*\(\s*["\']([^"\']+)["\']',
            r'\.post\s*\(\s*["\']([^"\']+)["\']'
        ]

        endpoints = []
        for pattern in api_patterns:
            matches = re.findall(pattern, js_content, re.IGNORECASE)
            endpoints.extend(matches)

        if endpoints:
            # 去重
            unique_endpoints = list(set(endpoints))
            print(f"  • 找到 {len(unique_endpoints)} 个可能的API端点")
            
            # 优先显示包含search/api/关键词的
            priority_endpoints = [e for e in unique_endpoints 
                               if any(kw in e.lower() for kw in ['search', 'api', 'ajax', 'query'])]
            
            if priority_endpoints:
                print(f"    优先端点: {', '.join(priority_endpoints[:5])}")
                self.api_endpoints.extend(priority_endpoints)
            else:
                print(f"    其他端点: {', '.join(unique_endpoints[:5])}")

    def find_param_generators(self, js_content, filename):
        """查找参数生成逻辑"""
        
        # 查找加密/签名相关代码
        encrypt_patterns = [
            r'function\s+(\w*[Ee]ncrypt\w*)\s*\(',
            r'function\s+(\w*[Ss]ign\w*)\s*\(',
            r'function\s+(\w*[Hh]ash\w*)\s*\(',
            r'function\s+(\w*[Tt]oken\w*)\s*\(',
            r'(?:const|let|var)\s+(\w*[Ee]ncrypt\w*)\s*=',
            r'(?:const|let|var)\s+(\w*[Ss]ign\w*)\s*=',
            r'(?:const|let|var)\s+(\w*[Tt]oken\w*)\s*='
        ]

        param_funcs = []
        for pattern in encrypt_patterns:
            matches = re.findall(pattern, js_content)
            param_funcs.extend(matches)

        if param_funcs:
            print(f"  • 找到 {len(set(param_funcs))} 个参数生成相关函数:")
            for func in set(param_funcs)[:5]:
                print(f"    - {func}")
                self.param_generators[filename] = self.param_generators.get(filename, []) + [func]

        # 查找常用的加密库
        crypto_libraries = [
            'crypto-js',
            'md5',
            'sha',
            'aes',
            'des',
            'rsa'
        ]

        for lib in crypto_libraries:
            if lib.lower() in js_content.lower():
                print(f"  • 可能使用的加密库: {lib}")

    def extract_search_logic(self, js_content, filename):
        """提取搜索相关逻辑"""
        
        print(f"\n  搜索逻辑分析:")
        
        # 查找搜索函数调用
        search_call_patterns = [
            r'(?:search|query)\s*\([^)]*\)',
            r'fetch\s*\([^)]*search[^)]*\)',
            r'ajax\s*\([^)]*search[^)]*\)'
        ]

        for pattern in search_call_patterns:
            matches = re.findall(pattern, js_content, re.IGNORECASE)
            if matches:
                print(f"    • 找到搜索调用:")
                for match in matches[:3]:
                    print(f"      {match[:100]}")

    def generate_analysis_report(self):
        """生成分析报告"""
        print("\n" + "=" * 70)
        print("参数分析报告")
        print("=" * 70)

        print(f"\n网站: {self.base_url}")

        if self.js_functions:
            print(f"\n找到的搜索相关函数:")
            for filename, funcs in self.js_functions.items():
                print(f"  {filename}: {', '.join(funcs)}")

        if self.api_endpoints:
            print(f"\n找到的API端点:")
            for i, endpoint in enumerate(set(self.api_endpoints), 1):
                print(f"  {i}. {endpoint}")

        if self.param_generators:
            print(f"\n找到的参数生成函数:")
            for filename, funcs in self.param_generators.items():
                print(f"  {filename}: {', '.join(funcs)}")

        # 保存报告
        report = {
            'website': self.base_url,
            'search_functions': self.js_functions,
            'api_endpoints': list(set(self.api_endpoints)),
            'param_generators': self.param_generators
        }

        with open('js_param_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 详细报告已保存: js_param_report.json")

        # 提供建议
        print("\n" + "=" * 70)
        print("下一步建议")
        print("=" * 70)

        if not self.api_endpoints:
            print("\n⚠️  未找到明显的API端点")
            print("   建议:")
            print("   1. 使用浏览器开发者工具的Network面板")
            print("   2. 执行搜索操作，查看实际发出的请求")
            print("   3. 复制cURL并提供给分析工具")
        else:
            print("\n✓ 找到可能的API端点")
            print("   建议:")
            print("   1. 使用requests库测试这些端点")
            print("   2. 分析必需的参数")
            print("   3. 查看参数生成函数的实现")

        if self.param_generators:
            print("\n✓ 找到参数生成函数")
            print("   建议:")
            print("   1. 查看这些函数的具体实现")
            print("   2. 确定是否可以在Python中实现")
            print("   3. 或使用webView执行JavaScript")

    def analyze_curl_command(self, curl_command):
        """分析cURL命令，提取请求信息"""
        print("\n" + "=" * 70)
        print("分析cURL命令")
        print("=" * 70)

        # 提取URL
        url_match = re.search(r"curl\s+['\"]?([^'\"]+)['\"]?", curl_command)
        if url_match:
            print(f"URL: {url_match.group(1)}")

        # 提取方法
        method = 'GET'
        if '-X POST' in curl_command or '--request POST' in curl_command:
            method = 'POST'
        print(f"Method: {method}")

        # 提取请求头
        headers = {}
        header_pattern = r'-H\s+[\'\"]([^\'=]+):\s*([^\'\"]+)[\'\"]'
        for match in re.finditer(header_pattern, curl_command):
            key = match.group(1)
            value = match.group(2)
            headers[key] = value

        if headers:
            print(f"\nHeaders:")
            for key, value in headers.items():
                print(f"  {key}: {value}")

        # 提取数据
        data_pattern = r'--data-?[a-z]*\s+[\'\"]([^\'\"]+)[\'\"]|-d\s+[\'\"]([^\'\"]+)[\'\"]'
        data_match = re.search(data_pattern, curl_command)
        if data_match:
            data = data_match.group(1) or data_match.group(2)
            print(f"\nData: {data}")

            # 尝试解析JSON数据
            if data.startswith('{'):
                try:
                    json_data = json.loads(data)
                    print(f"\nJSON参数:")
                    for key, value in json_data.items():
                        print(f"  {key}: {value}")
                except:
                    pass


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python js_param_analyzer.py <选项>")
        print("\n选项:")
        print("  --analyze <URL>      分析网站的JavaScript")
        print("  --curl <命令>        分析cURL命令")
        print("\n示例:")
        print("  python js_param_analyzer.py --analyze https://www.example.com")
        print("  python js_param_analyzer.py --curl 'curl http://example.com...'")
        sys.exit(1)

    option = sys.argv[1]

    try:
        if option == '--analyze':
            if len(sys.argv) < 3:
                print("错误: 需要提供网站URL")
                sys.exit(1)

            url = sys.argv[2]
            print(f"分析网站: {url}\n")

            analyzer = JSParamAnalyzer(url)

            # 获取首页HTML
            response = analyzer.session.get(url, timeout=15)
            html = response.text

            # 保存首页
            with open('home.html', 'w', encoding='utf-8') as f:
                f.write(html)

            # 提取JS
            external_js, inline_scripts = analyzer.extract_javascript_from_html(html)

            # 下载并分析
            analyzer.download_and_analyze_js(external_js[:5])  # 只分析前5个

            # 生成报告
            analyzer.generate_analysis_report()

        elif option == '--curl':
            if len(sys.argv) < 3:
                print("错误: 需要提供cURL命令")
                sys.exit(1)

            curl_command = ' '.join(sys.argv[2:])
            analyzer = JSParamAnalyzer('unknown')
            analyzer.analyze_curl_command(curl_command)

        else:
            print(f"错误: 未知选项 {option}")
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
