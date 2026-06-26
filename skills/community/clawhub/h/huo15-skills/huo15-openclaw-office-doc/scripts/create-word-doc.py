#!/usr/bin/env python3
"""
create-word-doc.py - 企业级 Word 文档生成器 v3.0（WPS/Word 双兼容）

格式标准：
  - 页面边距：上 3.7cm，下 3.5cm，左 2.8cm，右 2.6cm
  - 标题层次：章=黑体/小二/加粗，节=楷体/三号/加粗，条=仿宋/四号/加粗
  - 正文：仿宋/小四/首行缩进2字符/1.5倍行距
  - 页眉：LOGO + 公司名称 + 文档编号 + 密级
  - 页脚：居中，"第 X 页 / 共 Y 页"
  - 版本历史表：自动生成
  - 审批签字区：可选

用法：
    python create-word-doc.py <输出路径> [标题] [正文] [编号] [版本] [密级]
"""

import sys
import os
import re
import ssl
import json
import datetime
import urllib.request
import xmlrpc.client
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ============== 企业公文格式常量 ==============
MARGIN_TOP = 3.7
MARGIN_BOTTOM = 3.5
MARGIN_LEFT = 2.8
MARGIN_RIGHT = 2.6

# 字体（WPS 和 Word 都支持）
FONT_BODY = '仿宋'
FONT_HEADING_CHAPTER = '黑体'      # 章：黑体
FONT_HEADING_SECTION = '楷体'     # 节：楷体
FONT_HEADING_ARTICLE = '仿宋'     # 条：仿宋
FONT_HEADER = '黑体'
FONT_FOOTER = '仿宋'

# 字号（pt）
SIZE_CHAPTER = 16     # 章：一级标题，黑体 16pt 加粗
SIZE_SECTION = 14    # 节：二级标题，楷体 14pt 加粗
SIZE_ARTICLE = 12    # 条：三级标题，仿宋 12pt 加粗
SIZE_BODY = 12       # 正文：仿宋 12pt
SIZE_TITLE = 22      # 文档标题：黑体 22pt 加粗
SIZE_HEADER = 10.5
SIZE_FOOTER = 10.5
SIZE_TABLE_HEADER = 10.5
SIZE_TABLE_BODY = 10.5

# 行距
LINE_SPACING = 1.5

# 首行缩进（2个中文字符约 0.74cm）
FIRST_LINE_INDENT = Cm(0.74)

# 表格斑马条纹颜色（浅灰）
TABLE_ROW_EVEN_COLOR = RGBColor(0xF2, 0xF2, 0xF2)

# ============== 公司信息 ==============
USER_HOME = os.path.expanduser("~")
LOGO_DIR = os.path.join(USER_HOME, ".huo15", "assets")
DEFAULT_LOGO_PATH = os.path.join(LOGO_DIR, "logo.png")
FALLBACK_LOGO_URL = 'https://tools.huo15.com/uploads/images/system/logo-colours.png'
DEFAULT_COMPANY_NAME = '青岛火一五信息科技有限公司'


def get_company_info():
    """从公司系统获取公司信息和 LOGO"""
    info = {'company_name': DEFAULT_COMPANY_NAME, 'logo_path': None}

    if os.path.exists(DEFAULT_LOGO_PATH) and os.path.getsize(DEFAULT_LOGO_PATH) > 1000:
        info['logo_path'] = DEFAULT_LOGO_PATH
        return info

    try:
        creds_file = os.path.join(
            os.path.expanduser('~/.openclaw/agents'),
            os.environ.get('OC_AGENT_ID', 'main'),
            'odoo_creds.json'
        )
        if os.path.exists(creds_file):
            with open(creds_file) as f:
                creds = json.load(f)

            cfg_file = os.path.expanduser('~/.openclaw/openclaw.json')
            if os.path.exists(cfg_file):
                with open(cfg_file) as f:
                    cfg = json.load(f)
                    odoo_env = cfg.get('skills', {}).get('entries', {}).get('huo15-odoo', {}).get('env', {})
                    url = odoo_env.get('ODOO_URL', 'https://huihuoyun.huo15.com')
                    db = odoo_env.get('ODOO_DB', 'huo15_prod')

                user = creds.get('user', '')
                password = creds.get('password', '')
                if user and password:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=ctx)
                    uid = common.authenticate(db, user, password, {})
                    if uid:
                        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=ctx)
                        data = models.execute_kw(db, uid, password, 'res.company',
                            'search_read', [[('id', '=', 1)]], {'fields': ['name', 'logo'], 'limit': 1})
                        if data:
                            info['company_name'] = data[0].get('name', DEFAULT_COMPANY_NAME)
                            logo_id = data[0].get('logo')
                            if logo_id:
                                _download(f'{url}/web/image/res.company/{logo_id}/logo', DEFAULT_LOGO_PATH)
                                if os.path.exists(DEFAULT_LOGO_PATH):
                                    info['logo_path'] = DEFAULT_LOGO_PATH
    except Exception as e:
        print(f"获取公司信息失败: {e}")

    if not info['logo_path']:
        _download(FALLBACK_LOGO_URL, DEFAULT_LOGO_PATH)
        if os.path.exists(DEFAULT_LOGO_PATH):
            info['logo_path'] = DEFAULT_LOGO_PATH

    return info


def _download(url, dest_path):
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        return
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"✓ LOGO 已下载: {dest_path}")
    except Exception as e:
        print(f"⚠ LOGO 下载失败: {e}")


def _set_font(run, font_name, size, bold=False, color=None):
    """设置中文字体（WPS/Word 双兼容）"""
    run.font.name = font_name
    rPr = run._element.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        run._element.insert(0, rPr)
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = color


def _add_border_bottom(paragraph):
    """给段落下方加细线"""
    pPr = paragraph._element.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        paragraph._element.insert(0, pPr)
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '000000')
    pBdr.append(bottom)
    pPr.append(pBdr)


def _set_cell_shading(cell, fill_color):
    """设置单元格背景色"""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_color)
    tcPr.append(shd)


def add_header(doc, logo_path, company_name, doc_number=None, classification=None):
    """页眉：LOGO + 公司名称 + 文档编号 + 密级，左对齐，底边细线"""
    section = doc.sections[0]
    header = section.header
    header.is_linked_to_previous = False

    for p in header.paragraphs:
        for r in p.runs:
            r.text = ''
    para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # LOGO
    if logo_path and os.path.exists(logo_path):
        try:
            run = para.add_run()
            run.add_picture(logo_path, height=Cm(1.0))
        except Exception as e:
            print(f"⚠ LOGO 添加失败: {e}")

    # 公司名称
    run = para.add_run(f' {company_name}')
    _set_font(run, FONT_HEADER, SIZE_HEADER)

    # 文档编号
    if doc_number:
        run = para.add_run(f'  {doc_number}')
        _set_font(run, FONT_HEADER, SIZE_HEADER)

    # 密级
    if classification:
        run = para.add_run(f'  【{classification}】')
        _set_font(run, FONT_HEADER, SIZE_HEADER, bold=True)

    _add_border_bottom(para)


def add_footer(doc):
    """页脚：居中，'第 X 页 / 共 Y 页'"""
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False

    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for r in para.runs:
        r.text = ''

    def add_text(text):
        r = para.add_run(text)
        _set_font(r, FONT_FOOTER, SIZE_FOOTER)
        return r

    def add_field(name):
        r = para.add_run()
        fc1 = OxmlElement('w:fldChar')
        fc1.set(qn('w:fldCharType'), 'begin')
        it = OxmlElement('w:instrText')
        it.set(qn('xml:space'), 'preserve')
        it.text = f' {name} '
        fc2 = OxmlElement('w:fldChar')
        fc2.set(qn('w:fldCharType'), 'end')
        r._element.clear()
        r._element.append(fc1)
        r._element.append(it)
        r._element.append(fc2)
        _set_font(r, FONT_FOOTER, SIZE_FOOTER)

    add_text('第 ')
    add_field('PAGE')
    add_text(' 页 / 共 ')
    add_field('NUMPAGES')
    add_text(' 页')


# ============== 段落样式定义 ==============

class ParagraphStyle:
    """段落样式配置"""
    def __init__(self, font, size, bold=False, indent=True,
                 alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                 space_before=0, space_after=6,
                 line_spacing=LINE_SPACING):
        self.font = font
        self.size = size
        self.bold = bold
        self.indent = indent
        self.alignment = alignment
        self.space_before = space_before
        self.space_after = space_after
        self.line_spacing = line_spacing

    def apply(self, p):
        """应用样式到段落"""
        p.alignment = self.alignment
        p.paragraph_format.line_spacing = self.line_spacing
        p.paragraph_format.space_before = Pt(self.space_before)
        p.paragraph_format.space_after = Pt(self.space_after)
        if self.indent:
            p.paragraph_format.first_line_indent = FIRST_LINE_INDENT
        else:
            p.paragraph_format.first_line_indent = Cm(0)


# 预定义样式
STYLE_CHAPTER = ParagraphStyle(FONT_HEADING_CHAPTER, SIZE_CHAPTER, bold=True,
                               indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
                               space_before=18, space_after=6)

STYLE_SECTION = ParagraphStyle(FONT_HEADING_SECTION, SIZE_SECTION, bold=True,
                               indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
                               space_before=12, space_after=4)

STYLE_ARTICLE = ParagraphStyle(FONT_HEADING_ARTICLE, SIZE_ARTICLE, bold=True,
                                indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
                                space_before=6, space_after=3)

STYLE_BODY = ParagraphStyle(FONT_BODY, SIZE_BODY, bold=False,
                             indent=True, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                             space_before=0, space_after=6)

STYLE_EMPTY = ParagraphStyle(FONT_BODY, SIZE_BODY, bold=False,
                              indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
                              space_before=0, space_after=0)

STYLE_TABLE_CELL = ParagraphStyle(FONT_BODY, SIZE_TABLE_BODY, bold=False,
                                    indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
                                    space_before=2, space_after=2)

STYLE_TABLE_HEADER = ParagraphStyle(FONT_HEADING_CHAPTER, SIZE_TABLE_HEADER, bold=True,
                                      indent=False, alignment=WD_ALIGN_PARAGRAPH.CENTER,
                                      space_before=2, space_after=2)


def add_paragraph(doc, text, style):
    """添加段落并应用样式"""
    p = doc.add_paragraph()
    style.apply(p)
    if text:
        run = p.add_run(text)
        _set_font(run, style.font, style.size, style.bold)
    return p


def add_empty_line(doc):
    """添加空行"""
    add_paragraph(doc, '', STYLE_EMPTY)


# ============== 内容解析 ==============

def detect_paragraph_type(text):
    """
    检测段落类型
    返回：(类型, 清洗后的文本)
    类型: 'chapter', 'section', 'article', 'body', 'blank'
    """
    if not text or not text.strip():
        return 'blank', ''

    t = text.strip()

    # 一级标题：第X章、第X节、第X篇、第X款
    if re.match(r'^第[一二三四五六七八九十百千]+[章节篇款]', t):
        return 'chapter', re.sub(r'^第[一二三四五六七八九十百千]+[章节篇款]\s*', '', t)

    # 条（合同专用条款）：第X条
    if re.match(r'^第[一二三四五六七八九十百千零]+条', t):
        return 'article', re.sub(r'^第[一二三四五六七八九十百千零]+条\s*', '', t)

    # 二级标题：一、二、三、，. 等多种分隔符
    if re.match(r'^[一二三四五六七八九十百千]+[、．,，]', t):
        return 'section', re.sub(r'^[一二三四五六七八九十百千]+[、．,，]\s*', '', t)

    # 三级标题：（一）（二）（三）
    if re.match(r'^[（\(][一二三四五六七八九十百千]+[）\)]', t):
        return 'article', re.sub(r'^[（\(][一二三四五六七八九十百千]+[）\)]\s*', '', t)

    return 'body', _clean(t)


def _clean(text):
    """清除 markdown 符号"""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'^#+\s*', '', text)
    text = re.sub(r'^[-*+]\s+', '', text)
    text = re.sub(r'^\d+\.\s+', '', text)
    return text.strip()


def parse_table_lines(lines, start_idx):
    """解析连续表格行，返回结束索引"""
    table_lines = []
    i = start_idx
    while i < len(lines):
        t = lines[i].strip()
        if t.startswith('|'):
            # 跳过分割线
            if re.match(r'^[\|\-\s]+$', t):
                i += 1
                continue
            table_lines.append(t)
            i += 1
        else:
            break
    return table_lines, i


def build_table(doc, table_lines, style_table_header=None):
    """将表格行数据写入 Word 表格（支持斑马条纹）"""
    rows_data = []
    for line in table_lines:
        cells = [c.strip() for c in line.strip('|').split('|')]
        rows_data.append(cells)

    if len(rows_data) < 2:
        return

    cols = len(rows_data[0])
    table = doc.add_table(rows=len(rows_data), cols=cols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for r, row in enumerate(rows_data):
        is_header = (r == 0)
        for c, text in enumerate(row):
            cell = table.rows[r].cells[c]
            cell.text = text

            # 单元格样式
            for para in cell.paragraphs:
                if is_header:
                    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in para.runs:
                        _set_font(run, FONT_HEADING_CHAPTER, SIZE_TABLE_HEADER, bold=True)
                else:
                    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in para.runs:
                        _set_font(run, FONT_BODY, SIZE_TABLE_BODY, bold=False)

            # 表头背景色
            if is_header:
                _set_cell_shading(cell, 'D9D9D9')
            elif r % 2 == 0:
                # 斑马条纹：偶数行浅灰
                _set_cell_shading(cell, 'F2F2F2')


# ============== 合同专用样式 ==============
# 合同正文：顶格（无缩进），左对齐，不加粗
STYLE_CONTRACT_BODY = ParagraphStyle(FONT_BODY, SIZE_BODY, bold=False,
                                       indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
                                       space_before=0, space_after=6,
                                       line_spacing=LINE_SPACING)

# 合同条款（第X条）：仿宋加粗，无缩进，左对齐
STYLE_CONTRACT_ARTICLE = ParagraphStyle(FONT_BODY, SIZE_BODY, bold=True,
                                        indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
                                        space_before=6, space_after=3,
                                        line_spacing=LINE_SPACING)

# 合同章（第X章）：黑体加粗，无缩进，左对齐
STYLE_CONTRACT_CHAPTER = ParagraphStyle(FONT_HEADING_CHAPTER, SIZE_CHAPTER, bold=True,
                                        indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
                                        space_before=18, space_after=6)

# 合同节（一、二、三、）：楷体加粗，无缩进，左对齐
STYLE_CONTRACT_SECTION = ParagraphStyle(FONT_HEADING_SECTION, SIZE_SECTION, bold=True,
                                         indent=False, alignment=WD_ALIGN_PARAGRAPH.LEFT,
                                         space_before=12, space_after=4)


def parse_content(doc, content, document_type='general'):
    """
    将纯文本内容解析并写入 Word
    document_type: 'contract' | 'report' | 'official' | 'general'
    """
    if not content:
        return

    # 根据文档类型选择样式集
    if document_type == 'contract':
        style_chapter = STYLE_CONTRACT_CHAPTER
        style_section = STYLE_CONTRACT_SECTION
        style_article = STYLE_CONTRACT_ARTICLE
        style_body = STYLE_CONTRACT_BODY
    else:
        # 报告/公文/通用：正文有缩进，两端对齐
        style_chapter = STYLE_CHAPTER
        style_section = STYLE_SECTION
        style_article = STYLE_ARTICLE
        style_body = STYLE_BODY

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]
        t = line.strip()

        # 空行
        if not t:
            add_empty_line(doc)
            i += 1
            continue

        # 表格行
        if t.startswith('|'):
            table_lines, i = parse_table_lines(lines, i)
            build_table(doc, table_lines)
            continue

        # 检测段落类型
        ptype, clean_text = detect_paragraph_type(t)

        if ptype == 'blank':
            add_empty_line(doc)
        elif ptype == 'chapter':
            add_paragraph(doc, t, style_chapter)
        elif ptype == 'section':
            add_paragraph(doc, t, style_section)
        elif ptype == 'article':
            add_paragraph(doc, t, style_article)
        else:  # body
            if clean_text:
                add_paragraph(doc, clean_text, style_body)
            else:
                add_empty_line(doc)

        i += 1


def add_version_history(doc, version='V1.0', date=None, author='未知'):
    """添加版本历史表"""
    if not date:
        date = datetime.date.today().strftime('%Y-%m-%d')

    add_empty_line(doc)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run('【版本历史】')
    _set_font(run, FONT_HEADING_SECTION, SIZE_SECTION, bold=True)
    p.paragraph_format.space_after = Pt(6)

    table_data = [
        '| 版本 | 日期 | 作者 | 修改内容 |',
        '|------|------|------|----------|',
        f'| {version} | {date} | {author} | 首次创建 |',
    ]
    build_table(doc, table_data)


def add_approval_block(doc, approval_list=None):
    """添加审批签字区"""
    if approval_list is None:
        approval_list = [
            {'role': '编制', 'name': ''},
            {'role': '审核', 'name': ''},
            {'role': '批准', 'name': ''},
        ]

    add_empty_line(doc)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run('【审批记录】')
    _set_font(run, FONT_HEADING_SECTION, SIZE_SECTION, bold=True)
    p.paragraph_format.space_after = Pt(6)

    today = datetime.date.today().strftime('%Y-%m-%d')

    # 构建表格数据
    header = '| 角色 | 姓名 | 日期 | 签字 |'
    separator = '|------|------|------|------|'
    rows = [header, separator]

    for item in approval_list:
        role = item.get('role', '')
        name = item.get('name', '__________')
        date_str = item.get('date', today if role == '编制' else '')
        sign = '__________' if not name else name
        rows.append(f'| {role} | {name or "__________"} | {date_str} | {sign} |')

    build_table(doc, rows)


def add_classification_mark(doc, classification):
    """添加密级标识（页面顶部右侧）"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(f'【{classification}】')
    _set_font(run, FONT_BODY, SIZE_BODY, bold=True)
    p.paragraph_format.space_after = Pt(0)


def create_word_doc(output_path, title='', content='', doc_number=None, version='V1.0',
                    classification='内部', author=None, company_name=None,
                    logo_path=None, approval=None, footer_page=True, header_doc_number=True,
                    document_type='general'):
    """
    生成企业标准 Word 文档 v4.0

    参数:
        output_path: 输出文件路径（必需）
        title: 文档标题（可选）
        content: 正文内容（可选）
        doc_number: 文档编号（可选，自动生成）
        version: 版本号（可选，默认 V1.0）
        classification: 密级（可选，默认内部）
        author: 作者（可选）
        company_name: 公司名称（可选，默认自动获取）
        document_type: 文档类型（可选，默认 general）
            - 'contract': 合同格式（章/条结构，正文顶格无缩进）
            - 'report': 报告格式（一二三层级，正文首行缩进）
            - 'official': 公文格式（GB/T 9704-2012）
            - 'general': 通用格式（默认）
        logo_path: LOGO 路径（可选）
        approval: 审批人列表（可选）
            [{"role": "编制", "name": "赵博"}, {"role": "审核", "name": ""}, {"role": "批准", "name": ""}]
        footer_page: 页脚显示页码（默认 True）
        header_doc_number: 页眉显示文档编号（默认 True）
    """
    doc = Document()

    # 页面边距
    for sec in doc.sections:
        sec.top_margin = Cm(MARGIN_TOP)
        sec.bottom_margin = Cm(MARGIN_BOTTOM)
        sec.left_margin = Cm(MARGIN_LEFT)
        sec.right_margin = Cm(MARGIN_RIGHT)
        sec.header_distance = Cm(1.5)
        sec.footer_distance = Cm(1.5)

    # 公司信息
    info = get_company_info()
    logo = logo_path or info.get('logo_path')
    company = company_name or info.get('company_name', DEFAULT_COMPANY_NAME)

    # 合同类型：不加页眉页脚、不加密级、不加版本历史、不加审批区
    is_contract = (document_type == 'contract')

    # 页眉（合同用简化版：无密级徽章，但保留LOGO和公司名）
    header_doc_num = doc_number if header_doc_number else None
    if is_contract:
        add_header(doc, logo, company, header_doc_num, None)
    else:
        add_header(doc, logo, company, header_doc_num, classification)

    # 页脚
    if footer_page:
        add_footer(doc)

    # 默认样式
    style = doc.styles['Normal']
    style.font.name = FONT_BODY
    style.font.size = Pt(SIZE_BODY)

    # 密级标识（合同不加）
    if classification and classification != '公开' and not is_contract:
        add_classification_mark(doc, classification)

    # 合同标题：居中大二号字
    if title:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        _set_font(run, FONT_HEADING_CHAPTER, SIZE_TITLE, bold=True)
        p.paragraph_format.line_spacing = LINE_SPACING
        p.paragraph_format.space_after = Pt(18)

    # 合同不需要元数据行，直接跳到正文
    if not is_contract:
        # 元数据信息（编号、版本、密级、日期）
        meta_items = []
        if doc_number:
            meta_items.append(f'文档编号：{doc_number}')
        meta_items.append(f'版本：{version}')
        meta_items.append(f'密级：{classification}')
        today = datetime.date.today().strftime('%Y-%m-%d')
        meta_items.append(f'日期：{today}')
        if author:
            meta_items.append(f'作者：{author}')

        if meta_items:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(6)
            meta_text = '  |  '.join(meta_items)
            run = p.add_run(meta_text)
            _set_font(run, FONT_BODY, SIZE_BODY - 1)

        # 版本历史
        add_version_history(doc, version, today, author or '未知')

    # 正文
    today = datetime.date.today().strftime('%Y-%m-%d')
    parse_content(doc, content, document_type)

    # 审批签字区（合同不加，用正文里的签署栏）
    if not is_contract and approval is not None:
        add_approval_block(doc, approval)

    doc.save(output_path)
    print(f'✅ 文档已生成: {output_path}')
    return output_path


if __name__ == '__main__':
    args = sys.argv
    output = args[1] if len(args) > 1 else 'output.docx'
    title = args[2] if len(args) > 2 else ''
    content = args[3] if len(args) > 3 else ''
    doc_number = args[4] if len(args) > 4 else None
    version = args[5] if len(args) > 5 else 'V1.0'
    classification = args[6] if len(args) > 6 else '内部'

    create_word_doc(
        output_path=output,
        title=title,
        content=content,
        doc_number=doc_number,
        version=version,
        classification=classification
    )
