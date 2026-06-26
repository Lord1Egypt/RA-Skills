#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
璃幽小说章节整理工具
用于整理小说文件，生成目录和统计信息

用法：
    python organize-novel.py --input "E:\璃幽\06_璃幽小说\" --output "E:\璃幽\06_璃幽小说\目录.md"
"""

import argparse
import re
from pathlib import Path
from datetime import datetime


def parse_chapter_info(file_path: Path) -> dict:
    """从文件解析章节信息"""
    content = file_path.read_text(encoding='utf-8')
    
    # 尝试从文件名提取章节号
    filename = file_path.stem
    chapter_match = re.search(r'(?:第|chapter|ep|episode)[\s_-]*(\d+)', filename, re.IGNORECASE)
    chapter_num = chapter_match.group(1) if chapter_match else "?"
    
    # 尝试从内容提取标题
    title_match = re.search(r'^#\s*(?:第\d+章\s*)?[#*\s]*(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filename
    
    # 统计字数
    char_count = len(content)
    word_count = len(re.findall(r'[\u4e00-\u9fff]', content))  # 中文字数
    
    # 提取创建日期（如果有）
    date_match = re.search(r'\*\*创作日期：\*\*\s*(\d{4}-\d{2}-\d{2})', content)
    create_date = date_match.group(1) if date_match else file_path.stat().st_mtime
    
    return {
        'chapter': chapter_num,
        'title': title,
        'file': file_path,
        'chars': char_count,
        'words': word_count,
        'date': create_date
    }


def scan_novel_directory(input_dir: Path) -> list:
    """扫描小说目录"""
    chapters = []
    
    # 查找所有 markdown 文件
    for file in input_dir.glob("*.md"):
        # 跳过目录文件
        if "目录" in file.name or "README" in file.name:
            continue
        
        try:
            info = parse_chapter_info(file)
            chapters.append(info)
        except Exception as e:
            print(f"⚠ 读取失败 {file.name}: {e}")
    
    # 按章节号排序
    chapters.sort(key=lambda x: (
        int(x['chapter']) if x['chapter'].isdigit() else 999,
        x['title']
    ))
    
    return chapters


def generate_toc(chapters: list, output_path: Path):
    """生成目录"""
    total_words = sum(ch['words'] for ch in chapters)
    total_chars = sum(ch['chars'] for ch in chapters)
    
    toc = f"""# 璃幽小说目录

**最后更新：** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**总章节数：** {len(chapters)} 章  
**总字数：** {total_words:,} 字（中文）/ {total_chars:,} 字符（总计）

---

## 📖 章节列表

| 章节 | 标题 | 字数 | 创建日期 |
|------|------|------|----------|
"""
    
    for ch in chapters:
        # 格式化日期
        if isinstance(ch['date'], (int, float)):
            date_str = datetime.fromtimestamp(ch['date']).strftime('%Y-%m-%d')
        else:
            date_str = ch['date']
        
        toc += f"| 第{ch['chapter']}章 | [{ch['title']}]({ch['file'].name}) | {ch['words']:,} | {date_str} |\n"
    
    toc += f"""
---

## 📊 统计信息

- **总章节数：** {len(chapters)} 章
- **总字数：** {total_words:,} 字（中文）
- **总字符：** {total_chars:,} 字符
- **平均每章：** {total_words // len(chapters) if chapters else 0:,} 字

---

## 📝 创作进度

### 最近更新的 5 章

"""
    
    # 按修改时间排序，显示最近更新的
    recent = sorted(chapters, key=lambda x: x['file'].stat().st_mtime, reverse=True)[:5]
    for i, ch in enumerate(recent, 1):
        mod_time = datetime.fromtimestamp(ch['file'].stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        toc += f"{i}. **第{ch['chapter']}章** {ch['title']} - 更新于 {mod_time}\n"
    
    toc += f"""
---

## 🎯 创作目标

- [ ] 下一章节规划：
- [ ] 本月目标： 章
- [ ] 当前进度：{len(chapters)} 章

---

_「每个故事都是一次治愈。」_  
_—— 璃幽 🌸_

---

**自动生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**工具版本：** v0.1.0
"""
    
    # 写入文件
    output_path.write_text(toc, encoding='utf-8')
    print(f"✓ 目录已生成：{output_path}")


def main():
    parser = argparse.ArgumentParser(description="璃幽小说章节整理工具")
    parser.add_argument("--input", type=str, required=True, help="小说目录路径")
    parser.add_argument("--output", type=str, help="输出文件路径（可选）")
    parser.add_argument("--stats", action="store_true", help="只显示统计信息")
    
    args = parser.parse_args()
    
    input_dir = Path(args.input)
    
    if not input_dir.exists():
        print(f"❌ 目录不存在：{input_dir}")
        return
    
    # 扫描章节
    print(f"📚 扫描目录：{input_dir}")
    chapters = scan_novel_directory(input_dir)
    
    if not chapters:
        print("⚠ 未找到章节文件")
        return
    
    # 显示统计
    total_words = sum(ch['words'] for ch in chapters)
    print(f"\n📊 统计信息:")
    print(f"  总章节数：{len(chapters)} 章")
    print(f"  总字数：{total_words:,} 字")
    print(f"  平均每章：{total_words // len(chapters):,} 字")
    
    if args.stats:
        return
    
    # 生成目录
    output_path = Path(args.output) if args.output else input_dir / "目录.md"
    generate_toc(chapters, output_path)
    
    # 显示章节列表
    print(f"\n📖 章节列表:")
    for ch in chapters[:10]:  # 只显示前 10 章
        print(f"  第{ch['chapter']}章：{ch['title']} ({ch['words']:,}字)")
    
    if len(chapters) > 10:
        print(f"  ... 还有 {len(chapters) - 10} 章")


if __name__ == "__main__":
    main()
