#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMA /cgi-bin/ 端点批量测试脚本

测试所有已知的 /cgi-bin/ 接口可用性
"""

import requests
import json
import re
import sys
from pathlib import Path


class IMAEndpointTester:
    """IMA 端点测试器"""
    
    BASE_URL = "https://ima.qq.com"
    ENV_FILE = Path.home() / ".hermes" / ".env"
    
    # 已知的 /cgi-bin/ 端点
    ENDPOINTS = [
        {
            'name': 'get_home_page_data',
            'path': '/cgi-bin/knowledge_tab_reader/get_home_page_data',
            'method': 'POST',
            'body': {
                "knowledge_base_id": "",
                "need_folder_number": True,
                "need_default_cover": False
            },
            'desc': '获取首页数据（知识库列表）'
        },
        {
            'name': 'search_note_book',
            'path': '/cgi-bin/note/search_note_book',
            'method': 'POST',
            'body': {
                "search_type": 0,
                "query_info": {"title": "测试"},
                "start": 0,
                "end": 5
            },
            'desc': '搜索笔记'
        },
        {
            'name': 'get_note_content',
            'path': '/cgi-bin/note/get_note_content',
            'method': 'POST',
            'body': {
                "doc_id": "test",
                "need_format": True
            },
            'desc': '获取笔记内容'
        },
        {
            'name': 'save_note',
            'path': '/cgi-bin/note/save_note',
            'method': 'POST',
            'body': {
                "doc_id": "",
                "content": "# 测试笔记\n\n内容",
                "title": "测试"
            },
            'desc': '保存笔记'
        },
        {
            'name': 'assistant_qa',
            'path': '/cgi-bin/assistant/qa',
            'method': 'POST',
            'body': {
                "query": "你好",
                "knowledge_base_id": ""
            },
            'desc': '知识库问答'
        },
        {
            'name': 'get_knowledge_base_info',
            'path': '/cgi-bin/knowledge_tab_reader/get_knowledge_base_info',
            'method': 'POST',
            'body': {
                "knowledge_base_id": ""
            },
            'desc': '获取知识库详情'
        },
        {
            'name': 'list_knowledge_bases',
            'path': '/cgi-bin/knowledge_tab_reader/list_knowledge_bases',
            'method': 'POST',
            'body': {
                "page": 1,
                "page_size": 20
            },
            'desc': '列出知识库'
        },
        {
            'name': 'search_knowledge',
            'path': '/cgi-bin/knowledge_tab_reader/search_knowledge',
            'method': 'POST',
            'body': {
                "query": "测试",
                "knowledge_base_id": ""
            },
            'desc': '搜索知识库内容'
        },
        {
            'name': 'get_folder_list',
            'path': '/cgi-bin/knowledge_tab_reader/get_folder_list',
            'method': 'POST',
            'body': {
                "knowledge_base_id": "",
                "parent_folder_id": ""
            },
            'desc': '获取文件夹列表'
        },
        {
            'name': 'create_folder',
            'path': '/cgi-bin/knowledge_tab_reader/create_folder',
            'method': 'POST',
            'body': {
                "knowledge_base_id": "",
                "name": "新文件夹",
                "parent_folder_id": ""
            },
            'desc': '创建文件夹'
        },
    ]
    
    def __init__(self, cookie_str: str = None):
        self.cookie = cookie_str or self.load_cookie()
        self.results = []
        
    def load_cookie(self) -> str:
        """加载Cookie"""
        if self.ENV_FILE.exists():
            content = self.ENV_FILE.read_text()
            match = re.search(r'IMA_COOKIE=["\'](.+?)["\']', content)
            if match:
                return match.group(1)
        return ''
    
    def get_headers(self) -> dict:
        """获取请求头"""
        return {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'From_browser_ima': '1',
            'Extension_version': '999.999.999',
            'Referer': 'https://ima.qq.com/wikis',
            'x-ima-bkn': '212004022',
            'x-ima-cookie': self.cookie,
            'accept': 'application/json',
        }
    
    def test_endpoint(self, endpoint: dict) -> dict:
        """测试单个端点"""
        url = f"{self.BASE_URL}{endpoint['path']}"
        
        result = {
            'name': endpoint['name'],
            'path': endpoint['path'],
            'desc': endpoint['desc'],
            'status': 'untested',
            'ret': None,
            'msg': '',
            'data_preview': ''
        }
        
        try:
            resp = requests.post(
                url,
                headers=self.get_headers(),
                json=endpoint.get('body', {}),
                timeout=15
            )
            
            result['http_status'] = resp.status_code
            
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    result['ret'] = data.get('ret')
                    result['msg'] = data.get('msg', '')
                    
                    if data.get('ret') == 0:
                        result['status'] = '✅ 可用'
                        # 预览数据
                        if 'data' in data:
                            if isinstance(data['data'], dict):
                                keys = list(data['data'].keys())[:5]
                                result['data_preview'] = f"keys: {keys}"
                            elif isinstance(data['data'], list):
                                result['data_preview'] = f"list[{len(data['data'])}]"
                            else:
                                result['data_preview'] = str(data['data'])[:100]
                    else:
                        result['status'] = '⚠️ 返回错误'
                        
                except json.JSONDecodeError:
                    result['status'] = '⚠️ 非JSON响应'
                    result['data_preview'] = resp.text[:100]
            else:
                result['status'] = f'❌ HTTP {resp.status_code}'
                
        except Exception as e:
            result['status'] = f'❌ {type(e).__name__}'
            result['msg'] = str(e)[:50]
        
        return result
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("IMA /cgi-bin/ 端点批量测试")
        print("=" * 80)
        
        if not self.cookie:
            print("\n❌ 未找到 Cookie，请先运行：")
            print("   python test_cookie.py \"你的_Cookie\"")
            return
        
        print(f"\n📋 测试 {len(self.ENDPOINTS)} 个端点...\n")
        
        available = []
        
        for ep in self.ENDPOINTS:
            result = self.test_endpoint(ep)
            self.results.append(result)
            
            # 打印结果
            status_icon = '✅' if '可用' in result['status'] else ('⚠️' if '⚠️' in result['status'] else '❌')
            print(f"{status_icon} {result['name']:<30} {result['status']}")
            
            if '可用' in result['status']:
                available.append(result)
        
        # 汇总
        print("\n" + "=" * 80)
        print("📊 测试结果汇总")
        print("=" * 80)
        
        print(f"\n✅ 可用接口 ({len(available)}/{len(self.ENDPOINTS)}):")
        for r in available:
            print(f"   • {r['name']}: {r['desc']}")
            if r.get('data_preview'):
                print(f"     数据: {r['data_preview']}")
        
        print(f"\n❌ 不可用/错误接口:")
        for r in self.results:
            if '可用' not in r['status']:
                print(f"   • {r['name']}: {r['status']} - {r['msg']}")
        
        return available
    
    def save_results(self):
        """保存测试结果"""
        output = {
            'available': [
                {
                    'name': r['name'],
                    'path': r['path'],
                    'desc': r['desc'],
                    'data_preview': r.get('data_preview', '')
                }
                for r in self.results if '可用' in r['status']
            ],
            'unavailable': [
                {
                    'name': r['name'],
                    'path': r['path'],
                    'status': r['status'],
                    'msg': r['msg']
                }
                for r in self.results if '可用' not in r['status']
            ]
        }
        
        output_file = Path(__file__).parent / 'endpoints_available.json'
        output_file.write_text(json.dumps(output, ensure_ascii=False, indent=2))
        print(f"\n💾 结果已保存到: {output_file}")


def main():
    tester = IMAEndpointTester()
    
    if len(sys.argv) > 1:
        tester.cookie = sys.argv[1]
    
    available = tester.run_all_tests()
    tester.save_results()
    
    if available:
        print("\n🎉 发现可用接口！请更新 README_KnowledgeBase.md")


if __name__ == "__main__":
    main()
