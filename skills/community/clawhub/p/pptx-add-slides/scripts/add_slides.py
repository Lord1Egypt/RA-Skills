#!/usr/bin/env python3
"""
pptx-add-slides — 在已有 PPTX 中新增幻灯片，通过克隆 slide XML 模板保持风格一致。

核心策略：
1. 将 PPTX 作为 zip 打开
2. 读取模板页的完整 slide XML（ppt/slides/slideN.xml）
3. 提取所有 <a:t> 文本节点，构建文本索引映射
4. 根据用户提供的内容替换文本节点
5. 创建新 slide XML，复制关系文件
6. 更新 [Content_Types].xml、presentation.xml.rels、presentation.xml
7. 写回 zip 输出

用法示例：
    python3 add_slides.py \
        --source input.pptx --output output.pptx \
        --template-page 5 --insert-after 2 \
        --pages '[{"title":"新标题","content":["点1","点2","点3"],"footer":"总结"}]'
"""

import argparse
import copy
import json
import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


# ── 工具函数 ──────────────────────────────────────────────

NS = {
    'a':   'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r':   'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p':   'http://schemas.openxmlformats.org/presentationml/2006/main',
    'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
    'mc':  'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'ct':  'http://schemas.openxmlformats.org/package/2006/content-types',
    'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def qn(tag: str) -> str:
    """解析形如 'a:t' 的标签为 Clark notation 全限定名。"""
    if ':' in tag:
        prefix, local = tag.split(':', 1)
        return '{%s}%s' % (NS[prefix], local)
    return tag


def sorted_slide_indices(zf: zipfile.ZipFile) -> list:
    """返回 zip 内所有 slideN.xml 的页码（int），升序排列。"""
    indices = []
    for name in zf.namelist():
        m = re.match(r'ppt/slides/slide(\d+)\.xml', name)
        if m:
            indices.append(int(m.group(1)))
    return sorted(indices)


def slide_path(n: int) -> str:
    return f'ppt/slides/slide{n}.xml'

def slide_rels_path(n: int) -> str:
    return f'ppt/slides/_rels/slide{n}.xml.rels'


def get_max_slide_id(pres_xml: str) -> int:
    """从 presentation.xml 中获取当前最大的 slide id。"""
    root = ET.fromstring(pres_xml)
    ids = []
    for sld in root.iter(qn('p:sldId')):
        ids.append(int(sld.attrib['id']))
    return max(ids) if ids else 256


def get_next_rId(rels_xml: str) -> int:
    """从 rels XML 中获取下一个可用的 rId 编号。"""
    root = ET.fromstring(rels_xml)
    max_id = 0
    for rel in root:
        rid = rel.attrib.get('Id', '')
        m = re.match(r'rId(\d+)', rid)
        if m:
            max_id = max(max_id, int(m.group(1)))
    return max_id + 1


def extract_text_nodes(slide_xml: str) -> list:
    """提取 slide XML 中所有 <a:t> 元素的文本列表（按文档顺序），返回 [(element, current_text), ...]"""
    root = ET.fromstring(slide_xml)
    nodes = []
    for t_elem in root.iter(qn('a:t')):
        nodes.append((t_elem, t_elem.text or ''))
    return nodes


def replace_texts(slide_xml: str, replacements: list) -> str:
    """
    替换 slide XML 中的文本节点。
    replacements: [(old_text_substring, new_text), ...]
    按顺序匹配节点，每个节点文本若包含 old_text_substring 则整段替换为 new_text。
    如果 replacements 数量少于文本节点数，多余的节点保持不变。
    """
    root = ET.fromstring(slide_xml)
    text_nodes = [(elem, elem.text or '') for elem in root.iter(qn('a:t'))]

    # 按顺序匹配：每个 replacement 匹配下一个未使用的文本节点
    repl_idx = 0
    used = set()
    for i, (elem, current) in enumerate(text_nodes):
        if repl_idx >= len(replacements):
            break
        old_substr, new_str = replacements[repl_idx]
        if old_substr in current:
            elem.text = new_str
            used.add(i)
            repl_idx += 1

    return ET.tostring(root, encoding='unicode')


def build_replacements(page_type: str, data: dict, text_nodes: list) -> list:
    """
    根据页面类型和内容数据，构建替换列表。
    返回 [(old_text, new_text), ...]，按模板中文本节点顺序。
    """
    current_texts = [text for _, text in text_nodes]
    repl = []

    if page_type == 'content':
        # 典型结构: title → subtitle → content bullets... → footer
        title = data.get('title', '')
        subtitle = data.get('subtitle', '')
        bullets = data.get('content', [])
        footer = data.get('footer', '')
        desc = data.get('desc', '')

        # 按顺序匹配：找到标题节点、副标题节点、要点节点、底部节点
        # 启发式：正文页通常第一个非空文本是标题，最后一个是底部
        non_empty = [(i, t) for i, t in enumerate(current_texts) if t.strip()]

        idx = 0
        if title and idx < len(non_empty):
            repl.append((non_empty[idx][1], title))
            idx += 1
        if subtitle and idx < len(non_empty):
            repl.append((non_empty[idx][1], subtitle))
            idx += 1
        if desc and idx < len(non_empty):
            repl.append((non_empty[idx][1], desc))
            idx += 1

        # 要点：每个 bullet 替换一个文本节点
        for bullet in bullets:
            if idx < len(non_empty):
                repl.append((non_empty[idx][1], bullet))
                idx += 1
            else:
                break

        # 底部总结
        if footer and idx < len(non_empty):
            repl.append((non_empty[idx][1], footer))

    elif page_type == 'section':
        # 分隔页结构：section_number → title → desc
        section_number = data.get('section_number', '')
        title = data.get('title', '')
        desc = data.get('desc', '')

        non_empty = [(i, t) for i, t in enumerate(current_texts) if t.strip()]
        idx = 0
        if section_number and idx < len(non_empty):
            repl.append((non_empty[idx][1], section_number))
            idx += 1
        if title and idx < len(non_empty):
            repl.append((non_empty[idx][1], title))
            idx += 1
        if desc and idx < len(non_empty):
            repl.append((non_empty[idx][1], desc))

    return repl


def update_content_types(ct_xml: str, slide_num: int) -> str:
    """在 [Content_Types].xml 中为新 slide 添加 Override。"""
    root = ET.fromstring(ct_xml)
    part_name = f'/ppt/slides/slide{slide_num}.xml'
    # 检查是否已存在
    for ov in root:
        if ov.attrib.get('PartName') == part_name:
            return ET.tostring(root, encoding='unicode')
    override = ET.SubElement(root, qn('ct:Override'))
    override.set('PartName', part_name)
    override.set('ContentType', 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml')
    return ET.tostring(root, encoding='unicode')


def add_slide_to_presentation(pres_xml: str, slide_num: int, rId: str) -> str:
    """在 presentation.xml 的 sldIdLst 中添加新 slide 引用。"""
    root = ET.fromstring(pres_xml)
    sld_id_lst = root.find(qn('p:sldIdLst'))
    if sld_id_lst is None:
        # 创建
        sld_id_lst = ET.SubElement(root, qn('p:sldIdLst'))

    new_id = get_max_slide_id(pres_xml) + 1
    sld_id = ET.SubElement(sld_id_lst, qn('p:sldId'))
    sld_id.set('id', str(new_id))
    sld_id.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', rId)

    return ET.tostring(root, encoding='unicode')


def add_rels_entry(rels_xml: str, rId: str, target: str) -> str:
    """在 rels XML 中添加一条 Relationship。"""
    root = ET.fromstring(rels_xml)
    rel = ET.SubElement(root, qn('rel:Relationship'))
    rel.set('Id', rId)
    rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide')
    rel.set('Target', target)
    return ET.tostring(root, encoding='unicode')


# ── 主流程 ────────────────────────────────────────────────

def process(source_path: str, output_path: str, template_page: int,
            insert_after: int, page_type: str, pages_data: list):
    """
    核心处理函数。

    Args:
        source_path:   原 PPTX 路径
        output_path:   输出 PPTX 路径
        template_page: 模板页码（1-based，指原 PPT 中的位置）
        insert_after:  新页插入位置（在指定页码之后，0 表示最前面）
        page_type:     页面类型（content / section）
        pages_data:    页面内容列表，每项为一个 dict
    """
    # 复制源文件到输出
    shutil.copy2(source_path, output_path)

    # 以 zip 模式读写
    with zipfile.ZipFile(output_path, 'r') as zf:
        all_files = {name: zf.read(name) for name in zf.namelist()}

    # 读取模板页
    template_xml_str = all_files[slide_path(template_page)].decode('utf-8')
    template_rels_str = all_files.get(slide_rels_path(template_page), b'')

    # 读取关键配置文件
    pres_xml_str = all_files['ppt/presentation.xml'].decode('utf-8')
    pres_rels_str = all_files['ppt/_rels/presentation.xml.rels'].decode('utf-8')
    ct_xml_str = all_files['[Content_Types].xml'].decode('utf-8')

    # 获取现有 slide 编号
    existing = sorted_slide_indices(zf)
    next_slide = max(existing) + 1 if existing else 1

    # 计算插入位置：需要知道 insert_after 对应哪个 slide 编号
    # existing 是当前 zip 内的 slide 编号列表，按页码顺序
    # insert_after 是用户视角的页码（1-based），需要找到 insert_after 对应的 slide 编号
    # 然后再决定新 slide 的编号和 sldIdLst 中的位置

    # 读取 presentation.xml 中的 slide 顺序
    pres_root = ET.fromstring(pres_xml_str)
    sld_id_lst = pres_root.find(qn('p:sldIdLst'))
    slide_order = []
    if sld_id_lst is not None:
        for sld in sld_id_lst:
            rid = sld.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', '')
            slide_order.append(rid)

    # 从 rels 中解析 rId -> slide 编号映射
    rels_root = ET.fromstring(pres_rels_str)
    rid_to_target = {}
    for rel in rels_root:
        rid = rel.attrib.get('Id', '')
        target = rel.attrib.get('Target', '')
        rid_to_target[rid] = target

    # 确定新页面序列：在指定的 insert_after 页之后插入新页
    # slide_order 是当前 rId 序列，按页码排列
    insert_pos = insert_after  # 在 insert_after 个 slide 之后
    # 0 表示最前面

    # 为每个新页处理
    current_slide_num = next_slide
    next_rid = get_next_rId(pres_rels_str)

    for page_data in pages_data:
        # 提取模板文本节点
        text_nodes = extract_text_nodes(template_xml_str)

        # 构建替换列表
        replacements = build_replacements(page_type, page_data, text_nodes)

        # 替换文本
        new_slide_xml = replace_texts(template_xml_str, replacements)

        # 新 slide 编号
        sn = current_slide_num
        current_slide_num += 1

        # 更新内容类型
        ct_xml_str = update_content_types(ct_xml_str, sn)

        # 新 rId
        new_rid = f'rId{next_rid}'
        next_rid += 1

        # 更新 presentation.xml.rels
        pres_rels_str = add_rels_entry(pres_rels_str, new_rid, f'slides/slide{sn}.xml')

        # 更新 presentation.xml 的 slide 顺序
        pres_root2 = ET.fromstring(pres_xml_str)
        sld_lst = pres_root2.find(qn('p:sldIdLst'))
        if sld_lst is None:
            sld_lst = ET.SubElement(pres_root2, qn('p:sldIdLst'))

        # 计算插入位置（在 sldIdLst 中）
        insert_idx = min(insert_pos + (pages_data.index(page_data)), len(list(sld_lst)))

        new_sld_id = ET.Element(qn('p:sldId'))
        new_sld_id.set('id', str(get_max_slide_id(pres_xml_str) + 1 + pages_data.index(page_data)))
        new_sld_id.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', new_rid)

        sld_list = list(sld_lst)
        sld_lst.clear()
        for i, existing_sld in enumerate(sld_list):
            if i == insert_idx:
                sld_lst.append(new_sld_id)
            sld_lst.append(existing_sld)
        if insert_idx >= len(sld_list):
            sld_lst.append(new_sld_id)

        pres_xml_str = ET.tostring(pres_root2, encoding='unicode')

        # 存入新文件
        all_files[slide_path(sn)] = new_slide_xml.encode('utf-8')
        if template_rels_str:
            # 复制 rels 文件（保持图片等资源引用）
            all_files[slide_rels_path(sn)] = template_rels_str

    # 更新配置
    all_files['ppt/presentation.xml'] = pres_xml_str.encode('utf-8')
    all_files['ppt/_rels/presentation.xml.rels'] = pres_rels_str.encode('utf-8')
    all_files['[Content_Types].xml'] = ct_xml_str.encode('utf-8')

    # 写回 zip
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf_out:
        for name, data in all_files.items():
            zf_out.writestr(name, data)


def main():
    parser = argparse.ArgumentParser(description='在 PPTX 中新增幻灯片并保持风格一致')
    parser.add_argument('--source', required=True, help='原 PPTX 文件路径')
    parser.add_argument('--output', required=True, help='输出 PPTX 文件路径')
    parser.add_argument('--template-page', type=int, required=True, help='模板页码（1-based）')
    parser.add_argument('--insert-after', type=int, default=0, help='插入位置（在第几页之后，0=最前面）')
    parser.add_argument('--page-type', default='content', choices=['content', 'section', 'cover'],
                        help='页面类型')
    parser.add_argument('--pages', default='[]', help='页面内容 JSON 数组')
    parser.add_argument('--pages-config', default=None,
                        help='混合类型完整配置 JSON（优先级高于 --pages）')

    args = parser.parse_args()

    if args.pages_config:
        configs = json.loads(args.pages_config)
        # 按 insert_after 排序
        configs.sort(key=lambda c: c.get('insert_after', 0))

        # 分组处理：相同 template 和 type 的一起处理
        groups = {}
        for cfg in configs:
            key = (cfg.get('template', args.template_page), cfg.get('type', args.page_type))
            if key not in groups:
                groups[key] = []
            groups[key].append(cfg)

        # 逐组处理（简化：先全部处理第一个模板，再处理后续）
        current_source = args.source
        temp_files = []
        for (tmpl, ptype), cfgs in groups.items():
            temp_out = args.output.replace('.pptx', f'_tmp_{tmpl}_{ptype}.pptx')
            temp_files.append(temp_out)
            pages = [c['data'] for c in cfgs]
            insert_after = cfgs[0].get('insert_after', 0)
            process(current_source, temp_out, tmpl, insert_after, ptype, pages)
            current_source = temp_out

        # 最终输出
        if temp_files:
            shutil.copy2(temp_files[-1], args.output)
            # 清理临时文件
            for tf in temp_files:
                try:
                    os.remove(tf)
                except OSError:
                    pass
    else:
        pages = json.loads(args.pages)
        process(args.source, args.output, args.template_page,
                args.insert_after, args.page_type, pages)

    print(f'Done. Output: {args.output}')


if __name__ == '__main__':
    main()
