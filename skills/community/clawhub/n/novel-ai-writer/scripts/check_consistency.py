#!/usr/bin/env python3
"""
逻辑一致性检查工具
用法：python3 check_consistency.py <file1.txt> [file2.txt] ...
"""

import sys
import re
from pathlib import Path

def extract_characters(text):
    """提取人物名字（简单实现，实际应该用NER）"""
    # 简单启发式：连续的中文2-4字，且首字母大写（如果有拼音）
    pattern = r'[\u4e00-\u9fff]{2,4}'
    matches = re.findall(pattern, text)
    # 去重，过滤常见非人名
    stopwords = {'什么', '怎么', '为什么', '但是', '因为', '所以', '可以', '已经'}
    characters = set(m for m in matches if m not in stopwords)
    return characters

def check_character_consistency(texts):
    """检查人物一致性（简单实现）"""
    print("🔍 检查人物一致性...")
    all_characters = set()
    for text in texts:
        chars = extract_characters(text)
        all_characters.update(chars)
    
    print(f"  发现人物：{', '.join(list(all_characters)[:10])}...")  # 只显示前10个
    print("  ⚠️  注意：此为简单实现，可能需要人工核对")
    return all_characters

def check_timeline_consistency(texts):
    """检查时间线一致性（简单实现）"""
    print("🔍 检查时间线一致性...")
    time_expressions = []
    for text in texts:
        # 查找时间表达
        patterns = [
            r'第[一二三四五六七八九十\d]+章',
            r'\d+天[前之]',
            r'\d+年[前之]',
            r'三[天年月]前',
            r'昨天|今天|明天',
        ]
        for p in patterns:
            matches = re.findall(p, text)
            time_expressions.extend(matches)
    
    if time_expressions:
        print(f"  发现时间表达：{time_expressions[:10]}...")
    else:
        print("  未发现明显时间表达")
    
    print("  ⚠️  注意：时间线检查需要人工核对章节顺序")
    return time_expressions

def check_item_consistency(texts):
    """检查物品一致性（简单实现）"""
    print("🔍 检查物品一致性...")
    # 查找可能的物品（带引号或特定动词后的名词）
    item_patterns = [
        r'["\']([^"\']+)["\']',  # 引号内的内容
        r'(拿起|放下|拿出|放入|拿着|握着)(了)?([\u4e00-\u9fff]{2,6})',
    ]
    
    items = set()
    for text in texts:
        for p in item_patterns:
            matches = re.findall(p, text)
            if isinstance(matches[0], tuple) if matches else False:
                items.update(m[2] for m in matches if len(m) > 2)
            else:
                items.update(matches)
    
    if items:
        print(f"  发现物品：{', '.join(list(items)[:10])}...")
        print("  ⚠️  注意：需要人工核对物品是否凭空出现/消失")
    else:
        print("  未检测到明显物品")
    
    return items

def main():
    if len(sys.argv) < 2:
        print("用法：python3 check_consistency.py <file1.txt> [file2.txt] ...")
        print("\n示例：")
        print("  python3 check_consistency.py chapter1.txt chapter2.txt chapter3.txt")
        sys.exit(1)
    
    files = sys.argv[1:]
    texts = []
    
    print(f"📂 读取 {len(files)} 个文件...")
    for f in files:
        path = Path(f)
        if not path.exists():
            print(f"  ⚠️  文件不存在：{f}")
            continue
        with open(path, 'r', encoding='utf-8') as fp:
            texts.append(fp.read())
    
    if not texts:
        print("❌ 没有成功读取任何文件")
        sys.exit(1)
    
    print(f"✅ 成功读取 {len(texts)} 个文件\n")
    
    # 执行检查
    print("=" * 50)
    print("开始逻辑一致性检查...")
    print("=" * 50 + "\n")
    
    characters = check_character_consistency(texts)
    print()
    
    timeline = check_timeline_consistency(texts)
    print()
    
    items = check_item_consistency(texts)
    print()
    
    # 输出总结
    print("=" * 50)
    print("检查完成！")
    print("=" * 50)
    print("\n⚠️  注意：此为辅助工具，结果需要人工核对")
    print("💡 建议：将输出结果作为线索，人工逐章检查")

if __name__ == '__main__':
    main()
