#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 IMA 知识库测试脚本

使用方法：
1. 从浏览器获取 Cookie
2. 运行脚本：python test_knowledge_base.py "你的_Cookie_字符串"
"""

import requests
import json
import sys

def test_ima_knowledge_base(cookie_str: str):
    """测试 IMA 知识库接口"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Content-Type': 'application/json',
        'From_browser_ima': '1',
        'Extension_version': '999.999.999',
        'Referer': 'https://ima.qq.com/wikis',
        'x-ima-bkn': '212004022',
        'x-ima-cookie': cookie_str,
        'accept': 'application/json',
    }
    
    url = "https://ima.qq.com/cgi-bin/knowledge_tab_reader/get_home_page_data"
    payload = {
        "knowledge_base_id": "",
        "need_folder_number": True,
        "need_default_cover": False
    }
    
    print("=" * 60)
    print("IMA 知识库测试")
    print("=" * 60)
    
    # 检查 Cookie
    if 'IMA-TOKEN=' not in cookie_str:
        print("\n❌ 错误：Cookie 中未找到 IMA-TOKEN！")
        print("   请确保复制了完整的 Cookie 字符串")
        return False
    
    print("\n✓ Cookie 检查通过（包含 IMA-TOKEN）")
    
    # 发送请求
    print(f"\n请求 URL: {url}")
    print("正在请求知识库列表...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"\n响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('ret') == 0:
                print("\n✅ Cookie 有效！成功获取知识库数据")
                
                # 解析知识库列表
                kb_data = data.get('data', {})
                
                print("\n" + "=" * 60)
                print("📚 你的 IMA 知识库列表")
                print("=" * 60)
                
                # 个人知识库
                personal = kb_data.get('main_knowledge_base_info')
                if personal:
                    print(f"\n👤 【个人知识库】")
                    print(f"   名称: {personal.get('name')}")
                    print(f"   ID: {personal.get('id')}")
                
                # 订阅的知识库
                followed = kb_data.get('followed_knowledge_base', [])
                if followed:
                    print(f"\n📋 【订阅的知识库】({len(followed)} 个)")
                    for i, kb in enumerate(followed, 1):
                        print(f"   {i}. {kb.get('name')}")
                        print(f"      ID: {kb.get('id')}")
                
                # 最近访问的公开知识库
                recent = kb_data.get('recent_public_knowledge_base', [])
                if recent:
                    print(f"\n🌐 【最近公开知识库】({len(recent)} 个)")
                    for i, kb in enumerate(recent, 1):
                        print(f"   {i}. {kb.get('name')}")
                        print(f"      ID: {kb.get('id')}")
                
                # 完整响应（用于调试）
                print("\n" + "=" * 60)
                print("📝 完整响应数据（调试用）：")
                print("=" * 60)
                print(json.dumps(data, ensure_ascii=False, indent=2))
                
                return True
            else:
                print(f"\n❌ 接口返回错误: {data.get('msg', '未知错误')}")
                print(f"   完整响应: {json.dumps(data, ensure_ascii=False)}")
                return False
        else:
            print(f"\n❌ HTTP 错误: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ 请求出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("IMA 知识库 Cookie 测试工具")
        print("=" * 60)
        print("\n使用方法：")
        print(f"  python {sys.argv[0]} \"你的_Cookie_字符串\"")
        print("\n获取 Cookie 的方法：")
        print("  1. 用浏览器登录 https://ima.qq.com")
        print("  2. 按 F12 打开开发者工具")
        print("  3. 切换到 Network 标签，刷新页面")
        print("  4. 找到任意请求，复制 Request Headers 中的 Cookie")
        print("\n注意：Cookie 必须包含 IMA-TOKEN=...")
        return
    
    cookie_str = sys.argv[1]
    test_ima_knowledge_base(cookie_str)


if __name__ == "__main__":
    main()
