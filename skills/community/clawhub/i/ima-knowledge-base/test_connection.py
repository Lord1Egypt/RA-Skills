#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMA 知识库连接测试脚本
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ima_sdk import IMAKnowledgeBase

def main():
    print("=" * 60)
    print("IMA 知识库 OpenAPI 连接测试")
    print("=" * 60)
    
    # 从配置文件读取
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    
    if os.path.exists(config_file):
        import json
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        client_id = config.get("client_id", "")
        api_key = config.get("api_key", "")
    else:
        # 从环境变量读取
        client_id = os.getenv("IMA_CLIENT_ID", "77d00affff7e596998dbcaaae338b3c1")
        api_key = os.getenv("IMA_API_KEY", "6KH6W9lJFWu6yGduCrlooPN6MaPv+pV89DJl/Asd+upvLIyZQCNeaocyMVqJ8tiEuRmiFWi9CA==")
    
    print(f"\nClient ID: {client_id[:20]}...")
    print(f"API Key: {api_key[:20]}...")
    
    ima = IMAKnowledgeBase(client_id, api_key)
    
    # 测试1: 创建笔记
    print("\n[测试 1/3] 创建笔记...")
    result = ima.create_note(
        title="IMA 知识库集成测试",
        content="""# IMA 知识库集成测试

恭喜！Agent 已成功打通 IMA 知识库。

## 功能列表

- ✅ 创建笔记
- ✅ 读取笔记
- ✅ 追加内容
- ✅ 自动保存对话记录

## 下一步

1. 配置自动保存对话记录到知识库
2. 实现知识库检索增强回答
3. 配置定期任务同步摘要

---
测试时间：2026年5月7日
"""
    )
    print(f"结果: {result}")
    
    if result.get("code") != 0:
        print(f"❌ 创建失败: {result.get('msg')}")
        return False
    
    note_id = result["data"]["note_id"]
    print(f"✅ 创建成功，笔记ID: {note_id}")
    
    # 测试2: 读取笔记
    print("\n[测试 2/3] 读取笔记内容...")
    note = ima.get_note(note_id)
    if note.get("code") == 0:
        print(f"✅ 读取成功")
        print(f"内容预览: {note['data']['content'][:100]}...")
    else:
        print(f"❌ 读取失败: {note.get('msg')}")
        return False
    
    # 测试3: 追加内容
    print("\n[测试 3/3] 追加内容...")
    append_result = ima.append_note(
        note_id,
        "\n\n## 测试追加\n\n这是通过 API 追加的内容。\n\n- 追加成功\n- 功能正常"
    )
    if append_result.get("code") == 0:
        print("✅ 追加成功")
    else:
        print(f"❌ 追加失败: {append_result.get('msg')}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！IMA 知识库已成功打通。")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
