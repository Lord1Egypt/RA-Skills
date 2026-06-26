#!/usr/bin/env python3
"""
kb-rst2md.py — RST → Markdown 转换器（增强版 v2）
处理：代码块、表格、指令、 admonition、图片链接
"""

import os
import sys
import re

def process_directives(text):
    """处理 RST 指令（directives）"""
    lines = text.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 跳过 image/figure 指令（整块缩进内容）
        if stripped.startswith('.. image::') or stripped.startswith('.. figure::'):
            # 跳过整块（所有缩进行）
            i += 1
            while i < len(lines):
                if not lines[i].strip():  # 空行
                    i += 1
                    continue
                if lines[i].startswith(' ') or lines[i].startswith('\t'):  # 缩进的行属于 directive
                    i += 1
                    continue
                break  # 非缩进行 = directive 结束
            continue
        
        # 跳过 include 指令
        if stripped.startswith('.. include::'):
            i += 1
            continue
        
        # 跳过 only 指令
        if stripped.startswith('.. only::'):
            i += 1
            continue
        
        # 跳过 .. |xxx| replace 指令
        if '|replace|' in stripped and 'replace::' in stripped:
            i += 1
            continue
        
        # 处理 code-block
        if '.. code-block::' in stripped:
            lang_match = re.search(r'code-block::\s*(\w+)', stripped)
            lang = lang_match.group(1) if lang_match else ''
            result.append(f'```{lang}')
            i += 1
            # 收集代码内容（缩进的行）
            while i < len(lines):
                code_line = lines[i]
                if code_line.strip() == '':
                    result.append('')
                    i += 1
                    continue
                # 非缩进且非空行 = 代码块结束
                if not lines[i].startswith(' ') and not lines[i].startswith('\t') and not lines[i].strip().startswith('#'):
                    if lines[i].strip() and not lines[i].strip().startswith('..'):
                        break
                # 去除缩进
                code = lines[i]
                if code.startswith(' ' * 4):
                    code = code[4:]
                elif code.startswith(' ' * 3):
                    code = code[3:]
                elif code.startswith(' ' * 2):
                    code = code[2:]
                elif code.startswith('\t'):
                    code = code[1:]
                result.append(code.rstrip())
                i += 1
            result.append('```')
            continue
        
        # 处理 .. note:: .. tip:: .. warning::
        note_match = re.search(r'\.\. (note|tip|warning|important|caution)::?\s*(.*)', stripped)
        if note_match:
            note_type = note_match.group(1).title()
            note_title = note_match.group(2).strip()
            
            if note_title:
                result.append(f'> **{note_type}: {note_title}**')
            else:
                result.append(f'> **{note_type}**')
            
            i += 1
            # 收集内容（缩进的行）
            while i < len(lines):
                content = lines[i]
                # 非缩进 = 结束
                if content.strip() == '':
                    result.append('')
                    i += 1
                    continue
                if not lines[i].startswith(' ') and not lines[i].startswith('\t'):
                    break
                # 去除缩进
                c = lines[i]
                for _ in range(4):
                    if c.startswith(' '):
                        c = c[1:]
                if c.startswith('\t'):
                    c = c[1:]
                result.append(c.rstrip())
                i += 1
            continue
        
        # 处理 .. |xxx| 字段列表
        if re.match(r'\s*\|.+\|\s*\w+::', stripped):
            i += 1
            continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)

def clean_rst_markup(text):
    """清理 RST 标记"""
    
    # guilabel → **粗体**
    text = re.sub(r':guilabel:`([^`]+)`', r'**\1**', text)
    
    # icon → [图标名]
    text = re.sub(r':icon:`([^`]+)`', r'[\1]', text)
    
    # menuselection → **粗体**（替换箭头）
    text = re.sub(r':menuselection:`([^`]+)`', 
                  lambda m: '**' + m.group(1).replace(' --> ', ' → ').replace('-->', ' → ') + '**', text)
    
    # ref → 纯文本
    text = re.sub(r':ref:`([^`]+?)`', r'\1', text)
    text = re.sub(r':ref:`([^`<]+)\s*<([^`]+)>`', r'[\1](\2)', text)
    
    # doc → 纯文本
    text = re.sub(r':doc:`([^`]+?)`', r'\1', text)
    text = re.sub(r':doc:`([^`<]+)\s*<([^`]+)>`', r'[\1](\2)', text)
    
    # abbr
    text = re.sub(r':abbr:`([^`<]+)\s*<([^`]+)>`', r'\1 (\2)', text)
    text = re.sub(r':abbr:`([^`]+)`', r'\1', text)
    
    # 要点标记
    text = re.sub(r'\*\*(.+?)\*\*', r'**\1**', text)
    text = re.sub(r'\*(.+?)\*', r'*\1*', text)
    
    # 链接
    text = re.sub(r'`([^<]+?) <([^>]+)>`__?', r'[\1](\2)', text)
    text = re.sub(r'`([^<]+?) <([^>]+)>`_', r'[\1](\2)', text)
    
    # literal (单反引号)
    text = re.sub(r'``([^`]+)``', r'`\1`', text)
    
    return text

def process_tables(text):
    """处理表格（支持复杂网格表格）"""
    lines = text.split('\n')
    result = []
    i = 0
    
    def is_table_row(line):
        """检测是否是表格行（包含 | 但不是分隔行）"""
        stripped = line.strip()
        if not stripped or '|' not in stripped:
            return False
        # 分隔行如 +---+---+---+
        if re.match(r'^\+[-=+:]+\+$', stripped.replace(' ', '')):
            return False
        return True
    
    def parse_table_row(line):
        """解析表格行，返回单元格列表"""
        cells = [c.strip() for c in line.split('|')[1:-1]]
        return cells
    
    def count_cols(line):
        """计算表格列数"""
        stripped = line.strip()
        # 去掉首尾的 |
        if stripped.startswith('|'):
            stripped = stripped[1:]
        if stripped.endswith('|'):
            stripped = stripped[:-1]
        return stripped.count('|') + 1
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 检测表格开始（边框行）
        if re.match(r'^\+[-=+:]+\+$', stripped.replace(' ', '')):
            # 收集整个表格
            table_rows = []
            col_count = 0
            
            # 跳过头部边框
            i += 1
            
            # 收集所有行直到非表格行
            while i < len(lines):
                line_i = lines[i]
                stripped_i = line_i.strip()
                
                # 表格结束
                if not stripped_i or (not '|' in stripped_i and not re.match(r'^\+[-=+:]+\+$', stripped_i.replace(' ', ''))):
                    break
                
                # 分隔行（如 +============+==================================+）
                if re.match(r'^\+[-=+:]+\+$', stripped_i.replace(' ', '')):
                    i += 1
                    continue
                
                # 数据行
                if '|' in stripped_i:
                    cells = parse_table_row(stripped_i)
                    table_rows.append(cells)
                    if col_count == 0:
                        col_count = len(cells)
                
                i += 1
            
            # 输出 Markdown 表格
            if table_rows:
                # 找到表头行（第一个非空行）
                header_idx = 0
                for idx, row in enumerate(table_rows):
                    if any(c.strip() for c in row):
                        header_idx = idx
                        break
                
                # 表头
                header = table_rows[header_idx]
                # 补齐列数
                while len(header) < col_count:
                    header.append('')
                result.append('| ' + ' | '.join(header) + ' |')
                # 分隔行
                result.append('|' + '|'.join([' --- ' for _ in range(col_count)]) + '|')
                
                # 数据行（跳过表头）
                for row in table_rows[header_idx + 1:]:
                    if any(c.strip() for c in row):
                        # 补齐列数
                        while len(row) < col_count:
                            row.append('')
                        result.append('| ' + ' | '.join(row) + ' |')
            continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)

def process_lists(text):
    """处理列表"""
    lines = text.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        
        # 检测列表项
        list_match = re.match(r'^([\-\*])\s+(.+)$', line)
        if list_match:
            indent = len(line) - len(line.lstrip())
            prefix = '  ' * (indent // 4) + '- '
            result.append(prefix + list_match.group(2))
            in_list = True
            continue
        
        # 检测编号列表
        num_match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if num_match:
            indent = len(line) - len(line.lstrip())
            prefix = '  ' * (indent // 4) + f'{num_match.group(1)}. '
            result.append(prefix + num_match.group(2))
            in_list = True
            continue
        
        # 非列表行
        if in_list and stripped and not stripped.startswith('>'):
            result.append('')
        in_list = False
        result.append(line)
    
    return '\n'.join(result)

def fix_headers(text):
    """修复标题"""
    lines = text.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 检测 H1 上划线（===== at start）
        if re.match(r'^=+\s*', stripped) and i + 1 < len(lines):
            # 找到标题在下一行
            next_line = lines[i + 1].strip()
            if next_line and not next_line.startswith('#'):
                result.append(f"# {next_line}")
                i += 2  # 跳过上划线和标题
                continue
        
        # 检测 H1 下划线（===== at current, title is previous）
        if re.match(r'^=+$', stripped):
            if i > 0:
                prev_line = lines[i-1].strip()
                if prev_line and not prev_line.startswith('#'):
                    result[-1] = f"# {prev_line}"
                i += 1  # 跳过下划线
                continue
        
        # 检测 H2 下划线（-----）
        if re.match(r'^-+$', stripped):
            if i > 0:
                prev_line = lines[i-1].strip()
                if prev_line and not prev_line.startswith('#'):
                    result[-1] = f"## {prev_line}"
                i += 1  # 跳过下划线
                continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)

def rst_to_markdown(rst_content):
    """主转换函数"""
    
    # 1. 处理指令
    text = process_directives(rst_content)
    
    # 2. 处理表格
    text = process_tables(text)
    
    # 3. 清理 RST 标记
    text = clean_rst_markup(text)
    
    # 4. 处理列表
    text = process_lists(text)
    
    # 5. 修复标题
    text = fix_headers(text)
    
    # 6. 清理空行
    lines = text.split('\n')
    cleaned = []
    prev_empty = False
    
    for line in lines:
        is_empty = not line.strip()
        if is_empty:
            if not prev_empty:
                cleaned.append('')
            prev_empty = True
        else:
            cleaned.append(line)
            prev_empty = False
    
    return '\n'.join(cleaned)

def process_md(module_rst_path, module_name):
    """处理单个模块"""
    
    if not os.path.exists(module_rst_path):
        return None
    
    with open(module_rst_path, 'r', encoding='utf-8') as f:
        rst_content = f.read()
    
    # 提取子模块列表
    submodules = re.findall(r'^\s*([\w/]+)/(\w+)\s*$', rst_content, re.MULTILINE)
    
    # 转换为主 Markdown
    md = rst_to_markdown(rst_content)
    
    # 添加子模块索引
    if submodules:
        md += "\n\n## 子模块索引\n\n"
        for dir_path, filename in submodules[:15]:
            sub_rst = os.path.join(os.path.dirname(module_rst_path), dir_path, f"{filename}.rst")
            if os.path.exists(sub_rst):
                try:
                    with open(sub_rst, 'r', encoding='utf-8') as f:
                        sub_content = f.read(500)
                    
                    title_match = re.search(r'^([^\n=]+)\n[=\-]+\n', sub_content, re.MULTILINE)
                    sub_title = title_match.group(1).strip() if title_match else filename
                    md += f"- **{sub_title}**\n"
                except:
                    md += f"- {filename}\n"
    
    return md

def main():
    if len(sys.argv) < 2:
        print("用法: kb-rst2md.py <rst_file>", file=sys.stderr)
        sys.exit(1)
    
    rst_path = sys.argv[1]
    module_name = os.path.basename(os.path.dirname(rst_path))
    
    result = process_md(rst_path, module_name)
    
    if result:
        print(result)
    else:
        print(f"❌ 无法处理: {rst_path}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
