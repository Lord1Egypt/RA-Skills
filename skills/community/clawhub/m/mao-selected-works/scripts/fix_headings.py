#!/usr/bin/env python3
"""修复毛选Markdown文件中的标题层级问题。

问题：在"中国革命和中国共产党"等文章中，"一 地主阶级"、"二 资产阶级"等
应该是4级标题（####），但被错误地标记为2级标题（##）。

修复规则：
- 在"第X节"（3级标题）下的"一、二、三"等小节应该是4级标题
- 独立文章中的"一、二、三"等小节应该是3级标题
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

# 匹配中文数字（一到九十九）
CHINESE_NUMS = r'[一二三四五六七八九十百]+'

# 匹配模式：## 一　XXX 或 ## 一 XXX
HEADING_PATTERN = re.compile(
    r'^(##)\s+(' + CHINESE_NUMS + r')\s+'
)

def fix_heading_level(line: str, in_section: bool) -> tuple[str, bool]:
    """修复单行标题层级。
    
    Args:
        line: 当前行
        in_section: 是否在"第X节"内部
        
    Returns:
        (修复后的行, 更新后的in_section状态)
    """
    # 检测是否进入"第X节"（3级标题）
    if line.startswith('### ') and '第' in line and '节' in line:
        return line, True
    
    # 检测是否退出"第X节"（遇到新的2级标题）
    if line.startswith('## ') and not HEADING_PATTERN.match(line):
        return line, False
    
    # 修复"## 一 XXX" -> "#### 一 XXX"（如果在节内）
    match = HEADING_PATTERN.match(line)
    if match and in_section:
        return line.replace('## ', '#### ', 1), in_section
    
    # 修复"## 一 XXX" -> "### 一 XXX"（如果不在节内，是独立文章的小节）
    if match and not in_section:
        return line.replace('## ', '### ', 1), in_section
    
    return line, in_section

def fix_file(filepath: Path) -> bool:
    """修复单个文件的标题层级。
    
    Returns:
        是否进行了修改
    """
    content = filepath.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    fixed_lines = []
    in_section = False
    modified = False
    
    for line in lines:
        fixed_line, in_section = fix_heading_level(line, in_section)
        fixed_lines.append(fixed_line)
        if fixed_line != line:
            modified = True
            print(f"  {filepath.name}: {line.strip()} -> {fixed_line.strip()}")
    
    if modified:
        filepath.write_text('\n'.join(fixed_lines) + '\n', encoding='utf-8')
    
    return modified

def main():
    """主函数。"""
    if not DATA_DIR.exists():
        print(f"数据目录不存在: {DATA_DIR}")
        return
    
    files_fixed = 0
    for filepath in sorted(DATA_DIR.glob('*.md')):
        if filepath.name in {'SUMMARY.md', '目录.md'}:
            continue
        
        if fix_file(filepath):
            files_fixed += 1
    
    print(f"\n共修复 {files_fixed} 个文件")

if __name__ == '__main__':
    main()
