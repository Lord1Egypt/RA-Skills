#!/usr/bin/env python3
"""
小说记忆文件压缩脚本

功能：
1. 合并早期章节概要
2. 清理已解决的伏笔
3. 精简人物描述
4. 控制文件总字数

使用：
    python3 compress_novel_memory.py <memory_file.md>
    python3 compress_novel_memory.py <memory_file.md> --keep-chapters 15
"""

import re
import sys
from pathlib import Path


def parse_memory_file(content: str) -> dict:
    """解析记忆文件为结构化数据"""
    sections = {
        'basic': '',
        'world': '',
        'characters': '',
        'chapters': [],
        'foreshadowing': '',
        'timeline': ''
    }
    
    # 提取各部分
    basic_match = re.search(r'## 基本信息\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if basic_match:
        sections['basic'] = basic_match.group(1).strip()
    
    world_match = re.search(r'## 世界观\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if world_match:
        sections['world'] = world_match.group(1).strip()
    
    characters_match = re.search(r'## 主要人物\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if characters_match:
        sections['characters'] = characters_match.group(1).strip()
    
    chapters_match = re.search(r'## 剧情概要\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if chapters_match:
        chapters_text = chapters_match.group(1)
        # 提取各章节
        # 支持多种章节格式：第X章：xxx、第X章: xxx、第X章 xxx
        chapter_pattern = r'### 第(\d+)章[：:\s](.*?)(?=### 第|\Z)'
        for match in re.finditer(chapter_pattern, chapters_text, re.DOTALL):
            ch_num = int(match.group(1))
            ch_content = match.group(2).strip()
            sections['chapters'].append({
                'num': ch_num,
                'content': ch_content[:200]  # 限制单章节长度
            })
    
    foreshadowing_match = re.search(r'## 伏笔追踪\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if foreshadowing_match:
        sections['foreshadowing'] = foreshadowing_match.group(1).strip()
    
    timeline_match = re.search(r'## 时间线\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if timeline_match:
        sections['timeline'] = timeline_match.group(1).strip()
    
    return sections


def compress_chapters(chapters: list, keep_recent: int = 15) -> tuple:
    """压缩章节：合并早期章节，保留近期章节"""
    if len(chapters) <= keep_recent:
        return chapters, None
    
    # 早期章节合并
    early_chapters = chapters[:-keep_recent]
    recent_chapters = chapters[-keep_recent:]
    
    # 合并早期章节为概要
    early_summary = f"第1-{early_chapters[-1]['num']}章概要：\n"
    key_events = []
    for ch in early_chapters[:10]:  # 只取前10个关键事件
        # 提取关键信息（第一句话）
        first_sentence = ch['content'].split('。')[0][:50]
        if first_sentence:
            key_events.append(f"- 第{ch['num']}章：{first_sentence}")
    
    early_summary += '\n'.join(key_events[:5])
    if len(key_events) > 5:
        early_summary += f"\n...共{len(early_chapters)}章"
    
    return recent_chapters, early_summary


def compress_foreshadowing(foreshadowing: str) -> str:
    """清理已解决的伏笔，只保留未解决的"""
    lines = foreshadowing.split('\n')
    unresolved = []
    resolved_count = 0
    
    for line in lines:
        if line.strip().startswith('- [x]'):
            resolved_count += 1
        elif line.strip().startswith('- [ ]'):
            unresolved.append(line)
    
    if resolved_count > 0:
        print(f"  清理了 {resolved_count} 个已解决的伏笔")
    
    return '\n'.join(unresolved) if unresolved else ''


def rebuild_memory_file(title: str, sections: dict, early_summary: str = None) -> str:
    """重建记忆文件"""
    output = f"# 《{title}》记忆文件\n\n"
    
    # 基本信息
    if sections['basic']:
        output += f"## 基本信息\n{sections['basic']}\n\n"
    
    # 世界观
    if sections['world']:
        output += f"## 世界观\n{sections['world']}\n\n"
    
    # 主要人物
    if sections['characters']:
        output += f"## 主要人物\n{sections['characters']}\n\n"
    
    # 剧情概要
    output += "## 剧情概要\n\n"
    if early_summary:
        output += f"### 早期章节\n{early_summary}\n\n"
    
    for ch in sections['chapters']:
        output += f"### 第{ch['num']}章\n{ch['content']}\n\n"
    
    # 伏笔追踪
    if sections['foreshadowing']:
        compressed = compress_foreshadowing(sections['foreshadowing'])
        if compressed:
            output += f"## 伏笔追踪\n{compressed}\n\n"
    
    # 时间线
    if sections['timeline']:
        output += f"## 时间线\n{sections['timeline']}\n"
    
    return output


def extract_title(content: str) -> str:
    """从文件中提取小说名"""
    match = re.search(r'# 《(.+?)》记忆文件', content)
    return match.group(1) if match else "未知小说"


def compress_memory_file(file_path: str, keep_chapters: int = 15):
    """主压缩函数"""
    path = Path(file_path)
    if not path.exists():
        print(f"错误：文件不存在 - {file_path}")
        return False
    
    content = path.read_text(encoding='utf-8')
    original_size = len(content)
    
    # 提取标题
    title = extract_title(content)
    print(f"正在压缩《{title}》记忆文件...")
    print(f"  原始大小：{original_size} 字")
    
    # 解析
    sections = parse_memory_file(content)
    chapter_count = len(sections['chapters'])
    print(f"  章节数：{chapter_count}")
    
    # 压缩章节
    recent_chapters, early_summary = compress_chapters(sections['chapters'], keep_chapters)
    sections['chapters'] = recent_chapters
    
    if early_summary:
        print(f"  合并了前 {chapter_count - keep_chapters} 章为概要")
    
    # 重建文件
    new_content = rebuild_memory_file(title, sections, early_summary)
    new_size = len(new_content)
    
    # 计算压缩率
    compression_ratio = (1 - new_size / original_size) * 100 if original_size > 0 else 0
    
    print(f"  压缩后大小：{new_size} 字")
    print(f"  压缩率：{compression_ratio:.1f}%")
    
    # 备份原文件
    backup_path = path.with_suffix('.md.bak')
    path.rename(backup_path)
    print(f"  原文件备份：{backup_path}")
    
    # 写入新文件
    path.write_text(new_content, encoding='utf-8')
    print(f"  新文件已保存：{path}")
    
    return True


def main():
    if len(sys.argv) < 2:
        print("用法：python3 compress_novel_memory.py <memory_file.md> [--keep-chapters N]")
        print("\n选项：")
        print("  --keep-chapters N  保留最近N章（默认15）")
        sys.exit(1)
    
    file_path = sys.argv[1]
    keep_chapters = 15
    
    # 解析参数
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == '--keep-chapters' and i + 1 < len(args):
            keep_chapters = int(args[i + 1])
    
    compress_memory_file(file_path, keep_chapters)


if __name__ == '__main__':
    main()
