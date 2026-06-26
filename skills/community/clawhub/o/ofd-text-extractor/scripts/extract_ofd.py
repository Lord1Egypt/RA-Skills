#!/usr/bin/env python3
"""
OFD 文本提取脚本 - 支持模板页和字符级位置
从 OFD 文件中提取文本内容，保留位置信息
"""

import sys
import io

# 设置 UTF-8 输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

# OFD 命名空间
OFD_NS = {"ofd": "http://www.ofdspec.org/2016"}


def extract_ofd(ofd_path: str, show_characters: bool = False, output_path: str = None) -> Dict:
    """
    从 OFD 文件提取文本和位置信息

    Args:
        ofd_path: OFD 文件路径
        show_characters: 是否显示字符级位置
        output_path: 输出 JSON 路径（可选）

    Returns:
        dict: 包含提取结果的字典
    """
    ofd_path = Path(ofd_path)
    if not ofd_path.exists():
        raise FileNotFoundError(f"文件不存在: {ofd_path}")

    result = {
        "file": ofd_path.name,
        "pages": []
    }

    # 解压 OFD（本质是 ZIP）
    with zipfile.ZipFile(ofd_path, 'r') as zf:
        # 第一步：解析 Document.xml 获取模板页映射
        template_map = extract_template_map(zf)
        print(f"  Found {len(template_map)} template pages")

        # 第二步：查找所有页面内容文件
        content_files = sorted([
            name for name in zf.namelist()
            if 'Pages/Page_' in name and name.endswith('/Content.xml')
        ])

        for page_path in content_files:
            page_result = extract_page(zf, page_path, template_map, show_characters)
            result["pages"].append(page_result)

    # 输出到文件
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {output_path}")

    return result


def extract_template_map(zf: zipfile.ZipFile) -> Dict[str, str]:
    """解析 Document.xml 获取模板页映射"""
    template_map = {}

    # 查找 Document.xml
    doc_paths = [n for n in zf.namelist() if n.endswith('/Document.xml')]
    if not doc_paths:
        return template_map

    doc_path = doc_paths[0]
    doc_content = zf.read(doc_path).decode('utf-8')

    # 解析模板页映射：TemplatePage ID="1" BaseLoc="Tpls/Tpl_0/Content.xml"
    pattern = r'<ofd:TemplatePage\s+ID="(\d+)"\s+BaseLoc="([^"]+)"'
    matches = re.findall(pattern, doc_content)

    for tpl_id, base_loc in matches:
        tpl_path = base_loc.replace('/', '/')
        if tpl_path in zf.namelist():
            template_map[tpl_id] = tpl_path

    return template_map


def extract_page(zf: zipfile.ZipFile, page_path: str, template_map: Dict[str, str], include_chars: bool) -> Dict:
    """
    从单个页面提取文本（含模板页）

    Args:
        zf: ZipFile 对象
        page_path: 页面 Content.xml 路径
        template_map: 模板页映射
        include_chars: 是否包含字符级位置

    Returns:
        dict: 页面提取结果
    """
    content_xml = zf.read(page_path).decode('utf-8')

    # 获取页面索引
    page_match = re.search(r'Page_(\d+)', page_path)
    page_index = int(page_match.group(1)) if page_match else 0

    # 提取页面尺寸
    size_match = re.search(r'PhysicalBox>([\d. ]+)<', content_xml)
    page_size = {}
    if size_match:
        nums = size_match.group(1).strip().split()
        if len(nums) >= 4:
            page_size = {"width": float(nums[2]), "height": float(nums[3])}

    page_texts = []
    template_texts = []
    used_templates = []

    # 查找页面中引用的模板
    template_refs = re.findall(r'Template[^>]*TemplateID="(\d+)"', content_xml)

    for tpl_id in template_refs:
        if tpl_id not in used_templates and tpl_id in template_map:
            used_templates.append(tpl_id)
            tpl_path = template_map[tpl_id]

            print(f"    [Page {page_index+1}] Load template Tpl_{tpl_id}")
            tpl_content = zf.read(tpl_path).decode('utf-8')
            tpl_texts = extract_text_objects(tpl_content, f"template_{tpl_id}", include_chars)
            template_texts.extend(tpl_texts)

    # 提取页面自身的文本内容
    page_texts = extract_text_objects(content_xml, "page", include_chars)

    return {
        "pageIndex": page_index,
        "pageSize": page_size,
        "pageTexts": page_texts,
        "templateTexts": template_texts,
        "usedTemplates": used_templates
    }


def extract_text_objects(content: str, source: str, include_chars: bool) -> List[Dict]:
    """从 XML 内容中提取所有文本对象"""
    texts = []

    # 使用正则表达式匹配 TextObject
    text_object_pattern = r'<ofd:TextObject[^>]*ID="(\d+)"[^>]*>([\s\S]*?)</ofd:TextObject>'
    text_object_matches = re.finditer(text_object_pattern, content)

    idx = 0
    for to_match in text_object_matches:
        object_id = to_match.group(1)
        object_content = to_match.group(2)

        # 提取 Boundary 属性
        boundary = {"x": 0, "y": 0, "width": 0, "height": 0}
        boundary_match = re.search(r'Boundary="([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)"', to_match.group(0))
        if boundary_match:
            boundary = {
                "x": float(boundary_match.group(1)),
                "y": float(boundary_match.group(2)),
                "width": float(boundary_match.group(3)),
                "height": float(boundary_match.group(4))
            }

        # 提取 TextCode 信息
        textcode_pattern = r'<ofd:TextCode\s+X="([\d.]+)"\s+Y="([\d.]+)"(?:\s+DeltaX="([^"]*)")?\s*>([\s\S]*?)</ofd:TextCode>'
        tc_matches = re.finditer(textcode_pattern, object_content)

        for tc in tc_matches:
            start_x = float(tc.group(1))
            start_y = float(tc.group(2))
            delta_x_str = tc.group(3) or ""
            text_content = tc.group(4)

            # 解析 DeltaX 间距数组
            delta_x_values = []
            if delta_x_str.strip():
                for x in delta_x_str.strip().split():
                    if x:
                        # 只保留有效的数字字符
                        cleaned = re.sub(r'[^0-9.\-]', '', x)
                        if cleaned and re.match(r'^[\d.\-]+$', cleaned):
                            delta_x_values.append(float(cleaned))

            text_obj = {
                "id": f"{source}_{idx}",
                "objectId": object_id,
                "text": text_content,
                "x": start_x,
                "y": start_y,
                "boundary": boundary,
                "source": source
            }

            # 计算字符位置
            if include_chars:
                characters = calculate_char_positions(text_content, start_x, start_y, delta_x_values)
                text_obj["characters"] = characters

            texts.append(text_obj)
            idx += 1

    return texts


def calculate_char_positions(text: str, start_x: float, start_y: float, delta_x: List[float]) -> List[Dict]:
    """计算每个字符的精确位置"""
    characters = []
    char_x = start_x

    for i, char in enumerate(text):
        char_pos = {
            "char": char,
            "x": round(char_x, 4),
            "y": start_y,
            "index": i
        }
        characters.append(char_pos)

        # 计算下一个字符的X位置
        if i < len(delta_x):
            char_x += delta_x[i]
        elif delta_x:
            char_x += delta_x[-1]

    return characters


def print_result(result: Dict, show_chars: bool):
    """打印提取结果（格式化输出）"""
    print("")
    print(f"文件: {result['file']}")
    print("=" * 60)

    for page in result['pages']:
        print(f"\n第 {page['pageIndex'] + 1} 页:")
        if page.get('pageSize'):
            print(f"  页面尺寸: {page['pageSize'].get('width')} x {page['pageSize'].get('height')} mm")
        if page.get('usedTemplates'):
            print(f"  模板: {', '.join(page['usedTemplates'])}")
        print("-" * 40)

        # 合并所有文本
        all_texts = []
        for t in page.get('templateTexts', []):
            t['isTemplate'] = True
            all_texts.append(t)
        for t in page.get('pageTexts', []):
            t['isTemplate'] = False
            all_texts.append(t)

        # 按位置排序
        sorted_texts = sorted(all_texts, key=lambda t: (t['y'], t['x']))

        for t in sorted_texts:
            prefix = "[T]" if t['isTemplate'] else "   "
            text_to_show = t['text'][:50] + "..." if len(t['text']) > 50 else t['text']

            print(f"  {prefix} [{t['x']:.3f}, {t['y']:.3f}] {text_to_show}")

            # 显示字符位置
            if show_chars and 'characters' in t and t['characters']:
                char_positions = [f"{c['char']}@{round(c['x'], 3)}" for c in t['characters']]
                print(f"      CHARS: {', '.join(char_positions)}")

        page_count = len(page.get('pageTexts', []))
        template_count = len(page.get('templateTexts', []))
        print(f"  (页面: {page_count}, 模板: {template_count})")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python extract_ofd.py <ofd_file> [--show-chars] [--output <output_json>]")
        sys.exit(1)

    ofd_file = sys.argv[1]
    output_file = None
    show_chars = False

    # 解析参数
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    if '--show-chars' in sys.argv:
        show_chars = True

    print("正在提取 OFD 文本（含模板页）...")

    try:
        result = extract_ofd(ofd_file, show_chars, output_file)
        print_result(result, show_chars)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
