#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMA Cookie 获取与验证 - 最简3步完成

## 方案一：Playwright自动获取（推荐，如果云电脑有界面）

```bash
python ./skills/ima_knowledge_base/get_ima_cookie_playwright.py
```

## 方案二：手动获取（3步完成）

### 第1步：打开IMA并登录
访问 https://ima.qq.com ，用微信扫码登录

### 第2步：打开开发者工具（F12）
- 切换到 Network（网络）标签
- 刷新页面
- 点击任意一个请求（如 get_home_page_data）

### 第3步：复制Cookie
- 在右侧 Request Headers 中找到 Cookie 字段
- 复制全部内容（很长的一串）

### 然后运行验证：
```bash
cd ./skills/ima_knowledge_base
python test_cookie.py "粘贴你的Cookie"
```

---

## Cookie 格式示例
IMA-TOKEN=eyJhbGc...;其他参数=xxx;...

## 验证成功后，Cookie会自动保存到 ~/.hermes/.env
"""

import requests
import json
import re
import sys
from pathlib import Path


class IMACookieValidator:
    """IMA Cookie 验证器"""
    
    BASE_URL = "https://ima.qq.com"
    ENV_FILE = Path.home() / ".hermes" / ".env"
    
    def __init__(self, cookie_str: str = None):
        self.cookie_str = cookie_str or self.load_from_env()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'From_browser_ima': '1',
            'Extension_version': '999.999.999',
            'Referer': 'https://ima.qq.com/wikis',
            'x-ima-bkn': '212004022',
            'x-ima-cookie': '',
            'accept': 'application/json',
        }
    
    def load_from_env(self) -> str:
        """从环境变量加载Cookie"""
        if self.ENV_FILE.exists():
            content = self.ENV_FILE.read_text()
            match = re.search(r'IMA_COOKIE=["\'](.+?)["\']', content)
            if match:
                return match.group(1)
        
        # 尝试从环境变量读取
        import os
        return os.environ.get('IMA_COOKIE', '')
    
    def validate_format(self) -> bool:
        """验证Cookie格式"""
        if not self.cookie_str:
            print("❌ Cookie为空")
            return False
        
        if 'IMA-TOKEN=' not in self.cookie_str:
            print("❌ Cookie中未找到 IMA-TOKEN")
            print("   请确保复制了完整的Cookie字符串")
            return False
        
        print(f"✓ Cookie格式正确 ({len(self.cookie_str)} 字符)")
        return True
    
    def test_home_page_data(self) -> dict:
        """测试获取首页数据（知识库列表）"""
        self.headers['x-ima-cookie'] = self.cookie_str
        
        url = f"{self.BASE_URL}/cgi-bin/knowledge_tab_reader/get_home_page_data"
        payload = {
            "knowledge_base_id": "",
            "need_folder_number": True,
            "need_default_cover": False
        }
        
        print(f"\n📡 测试接口: get_home_page_data")
        print(f"   URL: {url}")
        
        try:
            resp = requests.post(url, headers=self.headers, json=payload, timeout=30)
            print(f"   状态码: {resp.status_code}")
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('ret') == 0:
                    print("   ✅ 接口调用成功！")
                    return data.get('data', {})
                else:
                    print(f"   ❌ 接口返回错误: {data.get('msg')}")
                    return None
            else:
                print(f"   ❌ HTTP错误: {resp.text[:200]}")
                return None
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
            return None
    
    def test_note_search(self) -> bool:
        """测试笔记搜索"""
        self.headers['x-ima-cookie'] = self.cookie_str
        
        url = f"{self.BASE_URL}/cgi-bin/note/search_note_book"
        payload = {
            "search_type": 0,
            "query_info": {"title": "测试"},
            "start": 0,
            "end": 5
        }
        
        print(f"\n📡 测试接口: search_note_book")
        
        try:
            resp = requests.post(url, headers=self.headers, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('ret') == 0:
                    print("   ✅ 笔记搜索可用！")
                    return True
            
            print(f"   ⚠️  笔记搜索返回: {resp.text[:200]}")
            return False
            
        except Exception as e:
            print(f"   ⚠️  笔记搜索异常: {e}")
            return False
    
    def save_to_env(self) -> bool:
        """保存Cookie到.env"""
        if not self.ENV_FILE.exists():
            self.ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
            self.ENV_FILE.write_text('')
        
        content = self.ENV_FILE.read_text()
        
        if 'IMA_COOKIE=' in content:
            content = re.sub(r'IMA_COOKIE=["\'].*?["\']', f'IMA_COOKIE="{self.cookie_str}"', content)
        else:
            content += f'\nIMA_COOKIE="{self.cookie_str}"\n'
        
        self.ENV_FILE.write_text(content)
        print(f"\n💾 Cookie已保存到: {self.ENV_FILE}")
        return True
    
    def print_knowledge_bases(self, data: dict):
        """打印知识库列表"""
        if not data:
            return
        
        print("\n" + "=" * 60)
        print("📚 你的 IMA 知识库")
        print("=" * 60)
        
        # 个人知识库
        personal = data.get('main_knowledge_base_info', {})
        if personal:
            print(f"\n👤 【个人知识库】")
            print(f"   名称: {personal.get('name', '未命名')}")
            print(f"   ID: {personal.get('id', 'N/A')}")
        
        # 订阅的知识库
        followed = data.get('followed_knowledge_base', [])
        if followed:
            print(f"\n📋 【订阅的知识库】({len(followed)} 个)")
            for kb in followed[:10]:  # 只显示前10个
                print(f"   • {kb.get('name', '未命名')}")
                print(f"     ID: {kb.get('id')}")
        
        # 最近公开知识库
        recent = data.get('recent_public_knowledge_base', [])
        if recent:
            print(f"\n🌐 【最近公开知识库】({len(recent)} 个)")
            for kb in recent[:5]:
                print(f"   • {kb.get('name', '未命名')}")
        
        print()


def main():
    print("=" * 70)
    print("IMA Cookie 验证工具")
    print("=" * 70)
    
    # 获取Cookie
    cookie = None
    if len(sys.argv) > 1:
        cookie = sys.argv[1]
    else:
        # 尝试从环境变量读取
        import os
        cookie = os.environ.get('IMA_COOKIE')
        if cookie:
            print("\n📋 从环境变量加载Cookie")
    
    validator = IMACookieValidator(cookie)
    
    # 验证格式
    if not validator.validate_format():
        print("\n" + "=" * 70)
        print("❌ Cookie无效")
        print("=" * 70)
        print("\n请按以下步骤获取Cookie：")
        print("1. 打开 https://ima.qq.com 并登录")
        print("2. 按 F12 -> Network -> 刷新页面")
        print("3. 点击任意请求 -> Headers -> 复制 Cookie")
        print("\n然后运行：")
        print(f"  python {sys.argv[0]} \"你的_Cookie\"")
        sys.exit(1)
    
    # 测试接口
    data = validator.test_home_page_data()
    validator.test_note_search()
    
    if data:
        validator.print_knowledge_bases(data)
        validator.save_to_env()
        
        print("\n" + "=" * 70)
        print("🎉 验证成功！")
        print("=" * 70)
        print("\n可用功能：")
        print("  ✓ 获取知识库列表")
        print("  ✓ 搜索笔记")
        print("  ✓ 订阅知识库操作（需要知识库ID）")
    else:
        print("\n❌ 接口测试失败，Cookie可能已过期")


if __name__ == "__main__":
    main()
