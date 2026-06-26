#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出所有已保存的颜文字"""

import json
import os

def list_kaomojis():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'kaomojis.json')
    
    if not os.path.exists(json_path):
        print("暂无颜文字数据")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = data.get('items', [])
    
    if not items:
        print("暂无颜文字数据")
        return
    
    print(f"共有 {len(items)} 个颜文字：\n")
    
    for i, item in enumerate(items, 1):
        kaomoji = item.get('kaomoji', '')
        meaning = item.get('meaning', '')
        usage = ', '.join(item.get('usage', []))
        tone = ', '.join(item.get('tone', []))
        
        print(f"{i}. {kaomoji}")
        print(f"   含义: {meaning}")
        print(f"   场景: {usage}")
        print(f"   语气: {tone}")
        print()

if __name__ == '__main__':
    list_kaomojis()
