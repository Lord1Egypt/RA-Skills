#!/usr/bin/env python3
"""
Markdown 转 Markmap HTML 思维导图生成器
支持输出 PDF 格式

该模块提供了将 Markdown 文档转换为交互式思维导图的功能，
可以输出 HTML 格式的思维导图，并可选地生成 PDF 版本。

用法：
    python tools/markmap_generator.py --file input.md --output output.html
    python tools/markmap_generator.py --file input.md --output output.html --pdf output.pdf
"""

from typing import Dict, List, Union, Optional
import argparse
import html
import os
import re


def is_table_row(line: str) -> bool:
    """
    检测是否为表格行
    
    Args:
        line (str): 待检测的行
        
    Returns:
        bool: 如果是表格行则返回True，否则返回False
    """
    line = line.strip()
    if not line.startswith('|') or not line.endswith('|'):
        return False
    
    # 检查是否有至少两个 | 符号
    if line.count('|') < 2:
        return False
    
    return True


def is_table_separator(line: str) -> bool:
    """
    检测是否为表格分隔行
    
    Args:
        line (str): 待检测的行
        
    Returns:
        bool: 如果是表格分隔行则返回True，否则返回False
    """
    line = line.strip()
    if not line.startswith('|') or not line.endswith('|'):
        return False
    
    # 移除首尾的 | 并去除空格
    cells = [cell.strip() for cell in line[1:-1].split('|')]
    
    # 检查是否每个单元格都是由 - 组成的分隔线
    for cell in cells:
        if cell and not re.match(r'^[-: ]+$', cell):
            return False
    
    return True


def clean_markdown_formatting(text: str) -> str:
    """
    清理 Markdown 格式标记（如 **加粗**、*斜体*等）
    
    Args:
        text (str): 待清理的文本
        
    Returns:
        str: 清理后的文本
    """
    # 去掉 ** 加粗标记
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # 去掉 * 斜体标记
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    # 去掉 __ 下划线标记
    text = re.sub(r'__(.+?)__', r'\1', text)
    # 去掉 _ 斜体标记
    text = re.sub(r'_(.+?)_', r'\1', text)
    return text


def parse_table_to_nodes(table_lines: List[str]) -> List[Dict[str, Union[str, List[Dict]]]]:
    """
    将表格内容转换为思维导图节点
    
    Args:
        table_lines (List[str]): 表格的所有行
        
    Returns:
        List[Dict[str, Union[str, List[Dict]]]]: 表格转换后的节点列表
    """
    nodes = []
    
    # 找到表头和数据行
    header_line = None
    separator_line_idx = -1
    
    for i, line in enumerate(table_lines):
        if is_table_separator(line):
            separator_line_idx = i
            header_line = table_lines[i-1] if i > 0 else None
            break
    
    if header_line is None:
        # 如果没有找到分隔行，假设第一行是表头
        header_line = table_lines[0]
        separator_line_idx = 1
    
    # 解析表头（清理格式标记）
    headers = [clean_markdown_formatting(h.strip()) for h in header_line.split('|')[1:-1]]
    
    # 解析数据行
    data_start_idx = separator_line_idx + 1
    for i in range(data_start_idx, len(table_lines)):
        data_line = table_lines[i].strip()
        if is_table_row(data_line):
            row_cells = [clean_markdown_formatting(cell.strip()) for cell in data_line.split('|')[1:-1]]
            
            if len(row_cells) >= 2:  # 至少要有两列才能生成主节点
                # 创建主节点：第一列 + 第二列（如果存在）
                if len(row_cells) >= 2:
                    main_content = f"{row_cells[0]} ({row_cells[1]})"
                else:
                    main_content = row_cells[0]
                
                main_node = {"content": html.escape(main_content), "children": []}
                
                # 将其余列作为子节点
                for j in range(2, len(row_cells)):
                    if j < len(headers):
                        child_content = f"{headers[j]}: {row_cells[j]}" if headers[j] else row_cells[j]
                    else:
                        child_content = row_cells[j]
                    
                    child_node = {"content": html.escape(child_content), "children": []}
                    main_node["children"].append(child_node)
                
                nodes.append(main_node)
            elif len(row_cells) == 1:  # 只有一列的情况
                main_node = {"content": html.escape(row_cells[0]), "children": []}
                nodes.append(main_node)
    
    return nodes


def parse_markdown_to_tree(markdown_text: str) -> Dict[str, Union[str, List[Dict]]]:
    """
    将 Markdown 文本转换为树形结构
    
    Args:
        markdown_text (str): 输入的 Markdown 文本
        
    Returns:
        Dict[str, Union[str, List[Dict]]]: 表示思维导图结构的字典
    """
    lines = markdown_text.strip().split('\n')
    root = {"content": "思维导图", "children": []}
    stack = [(0, root)]
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue
        
        # 检查是否为表格行
        if is_table_row(line) and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            # 收集整个表格（包括表头、分隔行和数据行）
            table_lines = [line]
            j = i + 1
            while j < len(lines):
                next_line = lines[j].rstrip()
                if is_table_row(next_line) or is_table_separator(next_line):
                    table_lines.append(next_line)
                    j += 1
                else:
                    break
            
            # 将表格转换为节点并添加到当前层级
            table_nodes = parse_table_to_nodes(table_lines)
            current_level = 3  # 表格内容的默认层级
            
            # 添加表格节点到当前栈顶元素
            parent = stack[-1][1]
            for node in table_nodes:
                parent["children"].append(node)
            
            # 跳过已处理的表格行
            i = j
            continue
        
        indent = len(line) - len(line.lstrip())
        stripped = line.lstrip()
        
        level = 0
        content = stripped
        
        if stripped.startswith('# '):
            level = 1
            content = stripped[2:]
        elif stripped.startswith('## '):
            level = 2
            content = stripped[3:]
        elif stripped.startswith('### '):
            level = 3
            content = stripped[4:]
        elif stripped.startswith('#### '):
            level = 4
            content = stripped[5:]
        elif stripped.startswith('- ') or stripped.startswith('* '):
            content = stripped[2:]
            if indent == 0:
                level = 3
            elif indent <= 2:
                level = 4
            else:
                level = 5
        else:
            # 非表格非标题非列表的普通文本行，跳过
            i += 1
            continue
        
        content = content.strip()
        if not content:
            i += 1
            continue
        
        new_node = {"content": html.escape(content), "children": []}
        
        while len(stack) > 1 and stack[-1][0] >= level:
            stack.pop()
        
        parent = stack[-1][1]
        parent["children"].append(new_node)
        stack.append((level, new_node))
        
        i += 1
    
    return root


def dict_to_js_json(d: Dict[str, Union[str, List[Dict]]]) -> str:
    """
    将字典转换为 JavaScript 对象字符串
    
    Args:
        d (Dict[str, Union[str, List[Dict]]]): 表示节点的字典
        
    Returns:
        str: JavaScript 对象表示的字符串
    """
    content = d.get("content", "").replace("\\", "\\\\").replace("'", "\\'")
    children = d.get("children", [])
    
    if children:
        children_str = ",".join(dict_to_js_json(c) for c in children)
        return f"{{'content': '{content}', 'children': [{children_str}]}}"
    else:
        return f"{{'content': '{content}', 'children': []}}"


def generate_markmap_html(title: str, markdown_content: str) -> str:
    """
    生成 Markmap HTML
    
    Args:
        title (str): 思维导图标题
        markdown_content (str): Markdown 内容
        
    Returns:
        str: 生成的 HTML 字符串
    """
    root_data = parse_markdown_to_tree(markdown_content)
    
    if not root_data.get("content"):
        root_data["content"] = title
    
    root_json = dict_to_js_json(root_data)
    
    return f'''<!doctype html>
<html>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{html.escape(title)} - 思维导图</title>
<style>
* {{ margin: 0; padding: 0; }}
html {{ font-family: ui-sans-serif, system-ui, sans-serif; }}
#mindmap {{ display: block; width: 100vw; height: 100vh; }}
.markmap-dark {{ background: #27272a; color: white; }}
</style>
<link rel="stylesheet" href="https://unpkg.com/markmap-toolbar@0.18.12/dist/style.css">
</head>
<body>
<svg id="mindmap"></svg>
<script src="https://unpkg.com/d3@7.9.0/dist/d3.min.js"></script>
<script src="https://unpkg.com/markmap-view@0.18.12/dist/browser/index.js"></script>
<script src="https://unpkg.com/markmap-toolbar@0.18.12/dist/index.js"></script>
<script>(r => {{ setTimeout(r); }})(function renderToolbar() {{
  const {{ markmap, mm }} = window;
  const {{ el }} = markmap.Toolbar.create(mm);
  el.setAttribute('style', 'position:absolute;bottom:20px;right:20px');
  document.body.append(el);
}})</script>
<script>((getMarkmap, getOptions, root2, jsonOptions) => {{
  const markmap = getMarkmap();
  window.mm = markmap.Markmap.create("svg#mindmap", (getOptions || markmap.deriveOptions)(jsonOptions), root2);
  if (window.matchMedia("(prefers-color-scheme: dark)").matches) {{
    document.documentElement.classList.add("markmap-dark");
  }}
}})(() => window.markmap,null,{root_json},{{}})</script>
</body>
</html>'''


def generate_pdf_from_html(html_path: str, pdf_path: str) -> bool:
    """
    从 HTML 生成 PDF（使用 Playwright）
    
    Args:
        html_path (str): HTML 文件路径
        pdf_path (str): 输出 PDF 路径
        
    Returns:
        bool: 是否成功生成 PDF
        
    Raises:
        ImportError: 当 Playwright 未安装时
    """
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{os.path.abspath(html_path)}")
            page.wait_for_timeout(2000)
            page.pdf(path=pdf_path, format='A4', landscape=True, print_background=True)
            browser.close()
        return True
    except ImportError:
        print("错误：缺少依赖包 'playwright'。")
        print("解决方法：运行 'pip install playwright' 安装依赖。")
        print("然后运行 'playwright install chromium' 安装浏览器。")
        return False
    except FileNotFoundError:
        print(f"错误：找不到文件 '{html_path}'。")
        print("请确保输入的 HTML 文件路径正确。")
        return False
    except Exception as e:
        print(f"PDF 生成失败: {e}")
        print("可能的原因：")
        print("- Playwright 浏览器未正确安装")
        print("- HTML 文件格式错误")
        print("- 权限不足或磁盘空间不够")
        print("解决方法：")
        print("- 确保已安装 Playwright 和 Chromium 浏览器")
        print("- 检查文件路径是否正确")
        print("- 确认有足够的磁盘空间")
        return False


def main() -> None:
    """
    主函数：解析命令行参数并执行转换过程
    """
    parser = argparse.ArgumentParser(
        description='Markdown 转 Markmap HTML 思维导图'
    )
    parser.add_argument(
        '--input', 
        type=str, 
        help='Markdown 内容'
    )
    parser.add_argument(
        '--file', 
        type=str, 
        help='Markdown 文件路径'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        required=True, 
        help='输出 HTML 文件路径'
    )
    parser.add_argument(
        '--title', 
        type=str, 
        default='思维导图', 
        help='标题'
    )
    parser.add_argument(
        '--pdf', 
        type=str, 
        help='输出 PDF 路径（可选）'
    )
    
    args = parser.parse_args()
    
    # 获取 Markdown 内容
    markdown_content = ""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        except FileNotFoundError:
            print(f"错误：找不到文件 '{args.file}'。")
            print("请检查文件路径是否正确。")
            return
        except UnicodeDecodeError:
            print(f"错误：无法解码文件 '{args.file}'。")
            print("请确保文件是 UTF-8 编码。")
            return
        except Exception as e:
            print(f"读取文件时发生错误: {e}")
            print("请检查文件权限和格式。")
            return
    elif args.input:
        markdown_content = args.input
    else:
        print("错误：请提供 --input 或 --file 参数")
        print("使用 --help 查看帮助信息。")
        return
    
    # 生成 HTML
    html_content = generate_markmap_html(args.title, markdown_content)
    
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            print(f"创建输出目录失败: {e}")
            print("请检查目录权限。")
            return
    
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html_content)
    except Exception as e:
        print(f"写入文件失败: {e}")
        print("请检查输出路径和权限。")
        return
    
    print(f"思维导图已生成: {args.output}")
    
    # 生成 PDF
    if args.pdf:
        if generate_pdf_from_html(args.output, args.pdf):
            print(f"PDF 已生成: {args.pdf}")
        else:
            print("PDF 生成失败，请检查错误信息。")


if __name__ == '__main__':
    main()