#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMA 知识库 Cookie 获取与测试脚本

使用方法：
1. 手动从浏览器获取 Cookie（推荐）
2. 运行测试脚本验证 Cookie 是否有效
"""

import requests
import json
import sys
from typing import Dict, Optional

# ============================================================
# 第一部分：手动获取 Cookie 的详细指南
# ============================================================

COOKIE_GUIDE = """
================================================================================
                            IMA Cookie 获取指南
================================================================================

方法一：手动从浏览器获取（推荐，最稳定）
--------------------------------------------------------------------------------

1. 打开 Chrome/Edge 浏览器，访问 https://ima.qq.com
2. 登录你的 IMA 账号（微信扫码或其他方式）
3. 按 F12 打开开发者工具
4. 切换到 "Network"（网络）标签页
5. 刷新页面，找到任意一个请求（比如 get_home_page_data）
6. 点击该请求，在 "Headers" 标签中找到 "Request Headers"
7. 复制 "Cookie" 字段的全部内容（很长的一串）

方法二：用浏览器开发者工具控制台获取
--------------------------------------------------------------------------------

1. 打开开发者工具 (F12)
2. 切换到 "Console"（控制台）标签
3. 输入：document.cookie
4. 复制输出的全部内容

需要提取的关键 Cookie：
- IMA-TOKEN=...
- ...其他 cookie

================================================================================
"""

# ============================================================
# 第二部分：Cookie 测试脚本
# ============================================================

class IMAKnowledgeBaseTester:
    """IMA 知识库 Cookie 测试器"""
    
    BASE_URL = "https://ima.qq.com"
    
    def __init__(self, cookie_str: str):
        self.cookie_str = cookie_str
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'From_browser_ima': '1',
            'Extension_version': '999.999.999',
            'Referer': 'https://ima.qq.com/wikis',
            'x-ima-bkn': '212004022',
            'x-ima-cookie': cookie_str,
            'accept': 'application/json',
            'cache-control': 'no-cache'
        }
    
    def test_cookie_validity(self) -> bool:
        """测试 Cookie 是否有效"""
        print("\n" + "="*60)
        print("测试 Cookie 有效性...")
        print("="*60)
        
        # 检查是否包含 IMA-TOKEN
        if 'IMA-TOKEN=' not in self.cookie_str:
            print("❌ Cookie 中未找到 IMA-TOKEN！请重新获取完整的 Cookie")
            return False
        
        print("✓ 包含 IMA-TOKEN")
        return True
    
    def get_knowledge_base_list(self) -> Optional[Dict]:
        """获取知识库列表"""
        url = f"{self.BASE_URL}/cgi-bin/knowledge_tab_reader/get_home_page_data"
        
        # 先获取个人知识库ID（可以先用空的试试）
        payload = {
            "knowledge_base_id": "",  # 空字符串应该返回个人信息和知识库列表
            "need_folder_number": True,
            "need_default_cover": False
        }
        
        print(f"\n请求 URL: {url}")
        print(f"请求体: {json.dumps(payload, ensure_ascii=False)}")
        
        try:
            response = self.session.post(url, headers=self.headers, json=payload, timeout=30)
            print(f"\n响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
                return data
            else:
                print(f"错误响应: {response.text}")
                return None
                
        except Exception as e:
            print(f"请求出错: {e}")
            return None
    
    def extract_knowledge_bases(self, response_data: Dict) -> list:
        """从响应中提取知识库列表"""
        kb_list = []
        
        try:
            # 根据 ima-cli 的结构提取
            if 'data' in response_data:
                data = response_data['data']
                
                # 个人知识库信息
                if 'main_knowledge_base_info' in data:
                    personal = data['main_knowledge_base_info']
                    kb_list.append({
                        'type': '个人知识库',
                        'id': personal.get('id'),
                        'name': personal.get('name'),
                        'icon': personal.get('icon')
                    })
                
                # 订阅的知识库
                if 'followed_knowledge_base' in data:
                    for kb in data['followed_knowledge_base']:
                        kb_list.append({
                            'type': '订阅知识库',
                            'id': kb.get('id'),
                            'name': kb.get('name'),
                            'icon': kb.get('icon')
                        })
                
                # 公开的知识库
                if 'recent_public_knowledge_base' in data:
                    for kb in data['recent_public_knowledge_base']:
                        kb_list.append({
                            'type': '公开知识库',
                            'id': kb.get('id'),
                            'name': kb.get('name'),
                            'icon': kb.get('icon')
                        })
                        
        except Exception as e:
            print(f"解析知识库列表时出错: {e}")
        
        return kb_list


def main():
    print(COOKIE_GUIDE)
    
    # 示例 Cookie（请替换为你的真实 Cookie）
    EXAMPLE_COOKIE = """
    请在这里粘贴你的 Cookie
    格式类似：IMA-TOKEN=xxx; other_cookie=yyy; ...
    """
    
    print("请将你的 IMA Cookie 粘贴到下方（替换示例内容）：")
    print("-" * 60)
    
    # 从命令行参数获取 Cookie，或者让用户输入
    if len(sys.argv) > 1:
        cookie_str = sys.argv[1]
    else:
        print("\n使用方法：")
        print(f"  python {sys.argv[0]} '你的_Cookie_字符串'")
        print("\n或者直接在脚本中修改 EXAMPLE_COOKIE 变量")
        print("\n" + "="*60)
        print("现在运行一个简单的测试来验证接口结构...")
        print("="*60)
        return
    
    # 创建测试器
    tester = IMAKnowledgeBaseTester(cookie_str)
    
    # 测试 Cookie 有效性
    if not tester.test_cookie_validity():
        print("\n❌ Cookie 无效，请重新获取")
        return
    
    # 获取知识库列表
    print("\n" + "="*60)
    print("尝试获取知识库列表...")
    print("="*60)
    
    response = tester.get_knowledge_base_list()
    
    if response and response.get('ret') == 0:
        print("\n✅ Cookie 有效！成功获取到数据")
        
        kb_list = tester.extract_knowledge_bases(response)
        
        if kb_list:
            print("\n" + "="*60)
            print("你的 IMA 知识库列表：")
            print("="*60)
            
            for i, kb in enumerate(kb_list, 1):
                print(f"\n{i}. [{kb['type']}] {kb['name']}")
                print(f"   ID: {kb['id']}")
        else:
            print("\n未找到知识库列表，请检查响应结构")
    else:
        print("\n❌ 获取知识库列表失败")
        if response:
            print(f"错误信息: {response.get('msg', '未知错误')}")


if __name__ == "__main__":
    main()
