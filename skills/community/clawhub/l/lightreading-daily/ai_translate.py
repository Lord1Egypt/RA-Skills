# -*- coding: utf-8 -*-
"""
AI 翻译助手 - 将 today_en.txt 翻译成中文并保存到 today_cn.txt
由 AI 调用执行翻译任务
"""

import os
import sys

def load_english():
    """加载英文内容"""
    en_file = os.path.join(os.path.dirname(__file__), 'today_en.txt')
    if not os.path.exists(en_file):
        print("错误：未找到 today_en.txt")
        print("请先运行 push_wechat.py 抓取英文内容")
        return None
    
    with open(en_file, 'r', encoding='utf-8') as f:
        return f.read()

def save_chinese(content):
    """保存中文翻译"""
    cn_file = os.path.join(os.path.dirname(__file__), 'today_cn.txt')
    with open(cn_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("中文翻译已保存到：{}".format(cn_file))

def main():
    print("=" * 60)
    print("AI 翻译助手 - LightReading 每日推送")
    print("=" * 60)
    
    # 加载英文内容
    english = load_english()
    if not english:
        return 1
    
    print("\n[英文原文]")
    print("-" * 60)
    print(english[:500] + "..." if len(english) > 500 else english)
    print("-" * 60)
    
    print("\n请 AI 将上述英文内容翻译成中文，然后调用 save_chinese() 保存")
    print("\n示例：")
    print("  translated = translate(english)  # AI 翻译")
    print("  save_chinese(translated)         # 保存到文件")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
