#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MD to PDF Converter
将 Markdown 文件转换为 PDF 文件（支持中文）

用法:
    python md_to_pdf.py <input.md> [output.pdf]

参数:
    input   - 输入 Markdown 文件路径（必需）
    output  - 输出 PDF 文件路径（可选，默认与输入文件同名同目录）

依赖:
    pip install markdown reportlab
"""

import sys
import os
import re
import markdown
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


# 开源字体目录（优先）和系统字体路径（备用）
_SCRIPT_DIR = Path(__file__).resolve().parent
_FONTS_DIR = _SCRIPT_DIR.parent / 'fonts'

# 开源字体文件名
_NOTO_SERIF_SC = 'NotoSerifSC-Regular.ttf'   # 思源宋体 - 正文
_NOTO_SANS_SC_BOLD = 'NotoSansSC-Bold.ttf'   # 思源黑体 - 标题

# 系统字体备用路径（覆盖 macOS / Linux / Windows 主流中文字体安装位置）
# 顺序原则：每平台从最常见的现代字体排到兜底字体
_SYSTEM_FONT_PATHS = {
    'regular': [
        # --- macOS（现代 → 旧版）---
        '/System/Library/Fonts/PingFang.ttc',                    # 苹方（macOS 10.11+ 默认）
        '/System/Library/Fonts/STHeiti Light.ttc',               # 华文黑体细
        '/System/Library/Fonts/Hiragino Sans GB.ttc',            # 冬青黑体简中
        '/System/Library/Fonts/Supplemental/Songti.ttc',         # 宋体（macOS 10.14+）
        '/Library/Fonts/Songti.ttc',                             # 宋体（旧位置）
        '/System/Library/Fonts/STSong.ttf',                      # 华文宋体（已从新版 macOS 移除）
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',  # Arial Unicode 兜底
        # --- Linux ---
        '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/noto-cjk/NotoSerifCJK-Regular.ttc',
        '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',          # 文泉驿正黑
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',        # 文泉驿微米黑
        '/usr/share/fonts/truetype/arphic/uming.ttc',            # AR PL UMing
        # --- Windows ---
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'msyh.ttc'),   # 微软雅黑
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'simsun.ttc'), # 中易宋体
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'simkai.ttf'), # 楷体
    ],
    'bold': [
        # --- macOS ---
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Medium.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        '/System/Library/Fonts/Supplemental/Songti.ttc',
        '/Library/Fonts/Songti.ttc',
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
        # --- Linux ---
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        # --- Windows ---
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'msyhbd.ttc'), # 微软雅黑 Bold
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'msyh.ttc'),
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'simhei.ttf'), # 黑体
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'simsun.ttc'),
    ],
}

# 最终兜底：扫描标准字体目录，按文件名匹配 CJK 关键字
_FONT_SCAN_DIRS = [
    '/System/Library/Fonts',
    '/System/Library/Fonts/Supplemental',
    '/Library/Fonts',
    os.path.expanduser('~/Library/Fonts'),
    '/usr/share/fonts',
    '/usr/local/share/fonts',
    os.path.expanduser('~/.fonts'),
    os.path.expanduser('~/.local/share/fonts'),
    os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts'),
]

_CJK_FONT_KEYWORDS = (
    'noto', 'cjk', 'pingfang', 'heiti', 'songti', 'hiragino',
    'simsun', 'simhei', 'simkai', 'simfang', 'msyh', 'yahei', 'yuanti',
    'wqy', 'uming', 'ukai', 'stsong', 'stheiti', 'stkaiti', 'stfangsong',
    'sourcehan', 'source han', 'fandolsong', 'fandolhei',
)

# 注册字体状态
_fonts_registered = False
_font_regular = None
_font_bold = None


def _has_cjk_glyphs(font_name):
    """验证已注册的字体是否真正包含 CJK 字形。

    有些字体文件（如特定 TTC subfontIndex）能被 reportlab 成功注册，
    但实际不含中文字形，渲染时会产生黑色方框。此函数通过检查常用汉字
    的字形映射来排除这类"假阳性"字体。
    """
    try:
        font = pdfmetrics.getFont(font_name)
        # 方式一：直接检查 cmap（最可靠）
        face = getattr(font, 'face', None)
        if face is not None:
            cmap = getattr(face, 'charToGlyph', None)
            if cmap is not None:
                # 测试 4 个高频汉字：中(U+4E2D) 文(U+6587) 字(U+5B57) 体(U+4F53)
                test_codepoints = [0x4E2D, 0x6587, 0x5B57, 0x4F53]
                hits = sum(1 for cp in test_codepoints if cmap.get(cp, 0) != 0)
                return hits >= 2
        # 方式二：fallback 到 stringWidth（cmap 不可用时）
        width = pdfmetrics.stringWidth('中文', font_name, 12)
        return width > 1
    except Exception:
        return False


def _try_register(name, path):
    """尝试注册单个字体文件并验证 CJK 字形。

    TTC 文件依次尝试 subfontIndex 0-9，每个 index 注册成功后都会
    验证是否包含 CJK 字形，不包含则继续尝试下一个 index。
    """
    if not path or not os.path.exists(path):
        return False
    try:
        if path.lower().endswith('.ttc'):
            last_err = None
            for idx in range(10):
                try:
                    pdfmetrics.registerFont(TTFont(name, path, subfontIndex=idx))
                    if _has_cjk_glyphs(name):
                        return True
                    # 注册成功但无 CJK 字形，继续尝试下一个 subfontIndex
                except Exception as e:
                    last_err = e
                    continue
            print(f"  字体不可用 {os.path.basename(path)}: 所有 subfontIndex(0-9) 均无 CJK 字形或注册失败")
            return False
        else:
            pdfmetrics.registerFont(TTFont(name, path))
            if _has_cjk_glyphs(name):
                return True
            print(f"  字体不含 CJK 字形，跳过: {os.path.basename(path)}")
            return False
    except Exception as e:
        print(f"  字体注册失败 {os.path.basename(path)}: {e}")
        return False


def _build_candidate_list(local_filename, system_paths):
    """构建候选字体路径列表（不去重，按优先级排列）。"""
    candidates = []
    # 第一层：本地开源字体
    local_path = _FONTS_DIR / local_filename
    if local_path.exists():
        candidates.append(str(local_path))
    # 第二层：显式系统路径
    for p in system_paths:
        if p and os.path.exists(p):
            candidates.append(p)
    return candidates


def _scan_fonts_dirs():
    """扫描标准字体目录，按文件名中的 CJK 关键字返回候选字体路径列表。"""
    candidates = []
    seen = set()
    for d in _FONT_SCAN_DIRS:
        if not d or not os.path.isdir(d):
            continue
        try:
            for root, _dirs, files in os.walk(d):
                for fname in files:
                    low = fname.lower()
                    if not low.endswith(('.ttf', '.otf', '.ttc')):
                        continue
                    if not any(k in low for k in _CJK_FONT_KEYWORDS):
                        continue
                    full = os.path.join(root, fname)
                    if full not in seen:
                        seen.add(full)
                        candidates.append(full)
        except (OSError, PermissionError):
            continue
    return candidates


def _try_register_first(font_name, local_filename, system_paths, scanned_candidates=None):
    """依次尝试注册候选字体，返回首个注册成功的路径。全部失败返回 None。

    策略：先试本地字体 + 显式系统路径清单；全部失败再试 scanned_candidates（目录扫描结果）。
    """
    # 第一、二层
    for path in _build_candidate_list(local_filename, system_paths):
        if _try_register(font_name, path):
            return path
    # 第三层：目录扫描兜底
    if scanned_candidates:
        for path in scanned_candidates:
            if _try_register(font_name, path):
                print(f"  通过目录扫描命中字体: {path}")
                return path
    return None


def register_system_fonts():
    """注册中文字体。

    策略（三级降级 + 逐个尝试注册 + 双向兜底）：
      1. 依次尝试本地 fonts/ 下的开源字体、显式系统路径、目录扫描结果，
         **每个候选路径都实际尝试 registerFont**，某个路径注册失败则继续下一个；
      2. regular / bold 双向兜底：任一字重注册成功即可支撑另一字重；
      3. 全部失败才退回 Helvetica（中文将渲染为方块）。
    """
    global _fonts_registered, _font_regular, _font_bold

    if _fonts_registered:
        return _font_regular, _font_bold

    # 预先扫描字体目录（供两个字重共享）
    scanned = _scan_fonts_dirs()

    # 为 bold 扫描结果排序：优先文件名带粗体关键字的
    bold_hints = ('bold', 'heavy', 'black', 'medium', 'msyhbd', 'simhei')
    scanned_bold = sorted(scanned, key=lambda p: (
        0 if any(h in os.path.basename(p).lower() for h in bold_hints) else 1
    ))

    # 逐个尝试注册——每个候选路径都会实际调用 registerFont，失败则自动跳到下一个
    regular_path = _try_register_first('CJKRegular', _NOTO_SERIF_SC, _SYSTEM_FONT_PATHS['regular'], scanned)
    bold_path = _try_register_first('CJKBold', _NOTO_SANS_SC_BOLD, _SYSTEM_FONT_PATHS['bold'], scanned_bold)

    # 双向兜底：一个字重注册失败时复用另一个
    if regular_path and not bold_path:
        if _try_register('CJKBold', regular_path):
            bold_path = regular_path
    if bold_path and not regular_path:
        if _try_register('CJKRegular', bold_path):
            regular_path = bold_path

    # 设置最终字体名
    if regular_path:
        _font_regular = 'CJKRegular'
        print(f"已注册正文字体: {regular_path}")
    else:
        _font_regular = 'Helvetica'
        print("警告: 未找到可用中文正文字体，使用 Helvetica（中文将显示为方块）")
        print(f"  修复建议: python scripts/download_fonts.py  或手动将 TTF/OTF 放入 {_FONTS_DIR}")

    if bold_path:
        _font_bold = 'CJKBold'
        print(f"已注册标题字体: {bold_path}")
    else:
        _font_bold = 'Helvetica-Bold'
        print("警告: 未找到可用中文标题字体，使用 Helvetica-Bold")

    pdfmetrics.registerFontFamily(
        'ChineseFont',
        normal=_font_regular,
        bold=_font_bold,
        italic=_font_regular,
        boldItalic=_font_bold,
    )
    _fonts_registered = True
    return _font_regular, _font_bold


def contains_cjk(text):
    """检测文本是否包含中日韩文字"""
    for char in text:
        if '\u4e00' <= char <= '\u9fff':  # 中文
            return True
        if '\u3040' <= char <= '\u309f':  # 日文平假名
            return True
        if '\u30a0' <= char <= '\u30ff':  # 日文片假名
            return True
        if '\uac00' <= char <= '\ud7af':  # 韩文
            return True
    return False


def add_page_number(canvas_obj, doc):
    """添加页码到页面底部居中"""
    canvas_obj.saveState()
    font_name = _font_regular if _font_regular else 'Helvetica'
    canvas_obj.setFont(font_name, 10)
    page_num = canvas_obj.getPageNumber()
    text = f"- {page_num} -"
    canvas_obj.drawCentredString(A4[0] / 2, 15 * mm, text)
    canvas_obj.restoreState()


def get_styles(has_cjk=True):
    """获取文档样式"""
    regular_font, bold_font = register_system_fonts() if has_cjk else ('Helvetica', 'Helvetica-Bold')

    # 行间距增加20%: 14 * 1.2 = 17
    line_spacing = 17
    # 段间距增加30%: 3 * 1.3 = 4
    para_spacing = 4

    styles = getSampleStyleSheet()

    # 深灰色颜色定义
    dark_gray = colors.HexColor('#666666')

    # 主标题样式 - 28pt 居中，使用 Bold 字重
    styles.add(ParagraphStyle(
        name='MainTitle',
        fontName=bold_font,
        fontSize=28,
        leading=line_spacing,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.black,
    ))

    # 一级标题 - 18pt，使用 Bold 字重
    styles.add(ParagraphStyle(
        name='Heading1CN',
        fontName=bold_font,
        fontSize=18,
        leading=line_spacing,
        spaceBefore=10,
        spaceAfter=10,
        textColor=colors.black,
    ))

    # 二级标题 - 14pt，使用 Bold 字重
    styles.add(ParagraphStyle(
        name='Heading2CN',
        fontName=bold_font,
        fontSize=14,
        leading=line_spacing,
        spaceBefore=8,
        spaceAfter=6,
        textColor=colors.black,
    ))

    # 三级标题 - 12pt，使用 Bold 字重
    styles.add(ParagraphStyle(
        name='Heading3CN',
        fontName=bold_font,
        fontSize=12,
        leading=line_spacing,
        spaceBefore=10,
        spaceAfter=6,
        textColor=colors.black,
    ))

    # 正文样式 - 12pt，使用 Regular 字重
    styles.add(ParagraphStyle(
        name='BodyCN',
        fontName=regular_font,
        fontSize=12,
        leading=line_spacing,
        alignment=TA_JUSTIFY,
        spaceBefore=para_spacing,
        spaceAfter=para_spacing,
        textColor=colors.black,
    ))

    # 执行摘要正文样式 - 带首行缩进两个汉字
    styles.add(ParagraphStyle(
        name='BodyIndentCN',
        fontName=regular_font,
        fontSize=12,
        leading=line_spacing,
        alignment=TA_JUSTIFY,
        spaceBefore=para_spacing,
        spaceAfter=para_spacing,
        textColor=colors.black,
        firstLineIndent=24,  # 首行缩进两个汉字
    ))

    # 列表项样式 - 正文颜色，使用 bullet
    styles.add(ParagraphStyle(
        name='ListItemCN',
        fontName=regular_font,
        fontSize=12,
        leading=line_spacing,
        alignment=TA_JUSTIFY,
        spaceBefore=para_spacing,
        spaceAfter=para_spacing,
        textColor=colors.black,
        leftIndent=12,  # 文本缩进一个汉字
        bulletIndent=0,  # 圆点位置
        bulletFontName=regular_font,
        bulletFontSize=18,
    ))

    # 列表项样式 - 深灰色
    styles.add(ParagraphStyle(
        name='ListItemGray',
        fontName=regular_font,
        fontSize=12,
        leading=line_spacing,
        alignment=TA_JUSTIFY,
        spaceBefore=para_spacing,
        spaceAfter=para_spacing,
        textColor=dark_gray,
        leftIndent=12,
        bulletIndent=0,
        bulletFontName=regular_font,
        bulletFontSize=18,
    ))

    # 列表项样式 - 尾注
    styles.add(ParagraphStyle(
        name='ListItemFootnote',
        fontName=regular_font,
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        spaceBefore=4,
        spaceAfter=4,
        textColor=colors.black,
        leftIndent=12,
        bulletIndent=0,
        bulletFontName=regular_font,
        bulletFontSize=14,
    ))

    # 深灰色正文样式（用于原文链接和评估）
    styles.add(ParagraphStyle(
        name='BodyGray',
        fontName=regular_font,
        fontSize=12,
        leading=line_spacing,
        alignment=TA_JUSTIFY,
        spaceBefore=para_spacing,
        spaceAfter=para_spacing,
        textColor=dark_gray,
    ))

    # 引用样式（一级标题下的说明文字）- 浅灰色背景
    styles.add(ParagraphStyle(
        name='QuoteCN',
        fontName=regular_font,
        fontSize=12,
        leading=line_spacing,
        leftIndent=0,
        rightIndent=0,
        spaceBefore=6,
        spaceAfter=6,
        textColor=colors.black,
        backColor=colors.HexColor('#f0f0f0'),
        borderPadding=8,
    ))

    # 代码样式
    styles.add(ParagraphStyle(
        name='CodeCN',
        fontName='Courier',
        fontSize=10,
        leading=line_spacing,
        leftIndent=10,
        rightIndent=10,
        spaceBefore=10,
        spaceAfter=10,
        backColor=colors.HexColor('#f5f5f5'),
        textColor=colors.black,
    ))

    # 尾注样式 - 左对齐
    styles.add(ParagraphStyle(
        name='FootnoteCN',
        fontName=regular_font,
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        spaceBefore=4,
        spaceAfter=4,
        textColor=colors.black,
    ))

    return styles, regular_font, bold_font


def create_bold_paragraph(text, style, font_regular, font_bold):
    """创建粗体段落，使用字体切换方式"""
    # 对于标题，使用 bold 字体
    return Paragraph(text, style)


def parse_md_content(md_content: str):
    """解析 Markdown 内容，返回结构化数据"""
    lines = md_content.split('\n')
    elements = []

    current_table = []
    in_table = False
    in_code_block = False
    code_content = []

    for line in lines:
        # 处理代码块
        if line.strip().startswith('```'):
            if in_code_block:
                in_code_block = False
                elements.append(('code', '\n'.join(code_content)))
                code_content = []
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_content.append(line)
            continue

        # 处理表格
        if '|' in line and not line.strip().startswith('#'):
            if line.strip().startswith('|---') or line.strip().startswith('|:'):
                continue  # 跳过表格分隔行
            cells = [c.strip() for c in line.strip('|').split('|')]
            if in_table:
                current_table.append(cells)
            else:
                in_table = True
                current_table = [cells]
            continue
        elif in_table:
            elements.append(('table', current_table))
            current_table = []
            in_table = False

        # 处理标题
        if line.strip().startswith('#'):
            level = 0
            stripped = line.strip()
            while stripped.startswith('#'):
                level += 1
                stripped = stripped[1:]
            title = stripped.strip()
            elements.append(('heading', level, title))
            continue

        # 处理列表
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            elements.append(('list_item', line.strip()[2:]))
            continue

        if re.match(r'^\d+\.\s', line.strip()):
            elements.append(('list_item', re.sub(r'^\d+\.\s', '', line.strip())))
            continue

        # 处理引用
        if line.strip().startswith('>'):
            elements.append(('quote', line.strip()[1:].strip()))
            continue

        # 处理分隔线
        if line.strip() == '---' or line.strip() == '***':
            elements.append(('separator', None))
            continue

        # 处理普通文本
        if line.strip():
            elements.append(('paragraph', line.strip()))

    # 处理末尾表格
    if in_table and current_table:
        elements.append(('table', current_table))

    return elements


def create_pdf_from_elements(elements, output_file, has_cjk=True):
    """从解析的元素创建 PDF"""
    styles, base_font, bold_font = get_styles(has_cjk)

    doc = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        leftMargin=21*mm,
        rightMargin=21*mm,
        topMargin=15*mm,
        bottomMargin=20*mm,  # 增加底部边距以容纳页码
    )

    story = []

    # 用于追踪是否处于附录部分
    in_appendix = False
    # 用于追踪是否紧跟在二级标题之后（用于引用块背景）
    after_heading2 = False
    # 二级标题计数器
    heading2_counter = 0
    # 是否处于执行摘要部分
    in_executive_summary = False

    # 中文数字
    chinese_numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
                       '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十']

    for elem in elements:
        elem_type = elem[0]

        if elem_type == 'heading':
            level, title = elem[1], elem[2]
            # 处理标题中的格式标记
            title = re.sub(r'\*{2}(.*?)\*{2}', r'<b>\1</b>', title)  # **bold**
            title = re.sub(r'\*(.*?)\*', r'<i>\1</i>', title)  # *italic*
            title = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', title)  # `code`

            # 检测是否进入附录部分
            if '附录' in title:
                in_appendix = True
            elif level == 2 and not title.startswith('附录'):
                in_appendix = False

            # 二级标题后标记，用于后续引用块处理
            after_heading2 = (level == 2)

            # 检测是否进入/退出执行摘要部分
            if level == 2 and '执行摘要' in title:
                in_executive_summary = True
            elif level == 2 and '执行摘要' not in title:
                in_executive_summary = False

            if level == 1:
                story.append(Paragraph(title, styles['MainTitle']))
                story.append(Spacer(1, 10))
            elif level == 2:
                # 判断是否为执行摘要（不参与排序）
                if '执行摘要' in title:
                    story.append(Paragraph(title, styles['Heading1CN']))
                    story.append(Spacer(1, 6))
                else:
                    # 其他二级标题：去掉emoji符号，添加中文序号
                    clean_title = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', title).strip()
                    heading2_counter += 1
                    if heading2_counter <= len(chinese_numbers):
                        numbered_title = f"{chinese_numbers[heading2_counter-1]}、{clean_title}"
                    else:
                        numbered_title = f"{heading2_counter}、{clean_title}"
                    story.append(Paragraph(numbered_title, styles['Heading1CN']))
                    story.append(Spacer(1, 6))
            elif level == 3:
                story.append(Spacer(1, 12))  # 三级标题上方增加空行
                story.append(Paragraph(title, styles['Heading2CN']))
                after_heading2 = False  # 三级标题后不再是二级标题紧跟状态
            elif level == 4:
                story.append(Paragraph(title, styles['Heading3CN']))
                after_heading2 = False
            else:
                story.append(Paragraph(title, styles['BodyCN']))
                after_heading2 = False

        elif elem_type == 'paragraph':
            text = elem[1]
            # 处理格式标记
            text = re.sub(r'\*{2}(.*?)\*{2}', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
            text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<link href="\2">\1</link>', text)

            # 检测尾注行（斜体标记的特殊说明）
            if text.startswith('- *') or text.startswith('• *'):
                story.append(Paragraph(text, styles['FootnoteCN']))
            elif in_executive_summary:
                # 执行摘要段落使用首行缩进
                story.append(Paragraph(text, styles['BodyIndentCN']))
            else:
                story.append(Paragraph(text, styles['BodyCN']))
            after_heading2 = False

        elif elem_type == 'list_item':
            text = elem[1]

            # 先检测尾注行（在格式转换之前检测）
            is_footnote = text.startswith('*') and ('本' in text or '数据来源' in text or 'industry-intelligence' in text or 'skill' in text)

            # 处理格式标记
            text = re.sub(r'\*{2}(.*?)\*{2}', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)

            # 检测原文链接和评估行，使用深灰色样式
            if text.startswith('**原文链接**') or text.startswith('**评估**'):
                story.append(Paragraph(text, styles['ListItemGray'], bulletText='•'))
            # 尾注行使用 FootnoteCN 样式
            elif is_footnote:
                story.append(Paragraph(text, styles['ListItemFootnote'], bulletText='•'))
            else:
                story.append(Paragraph(text, styles['ListItemCN'], bulletText='•'))
            after_heading2 = False

        elif elem_type == 'quote':
            text = elem[1]
            text = re.sub(r'\*{2}(.*?)\*{2}', r'<b>\1</b>', text)
            # 二级标题下的引用块使用带浅灰色背景的样式
            if after_heading2:
                story.append(Paragraph(text, styles['QuoteCN']))
            else:
                story.append(Paragraph(text, styles['BodyCN']))
            after_heading2 = False

        elif elem_type == 'code':
            code = elem[1]
            # 简化代码显示
            code = code.replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(f"<font face='Courier'>{code}</font>", styles['CodeCN']))
            after_heading2 = False

        elif elem_type == 'table':
            table_data = elem[1]
            if table_data:
                # 处理表格内容：去掉 ** 标记
                processed_data = []
                for row_idx, row in enumerate(table_data):
                    processed_row = []
                    for cell in row:
                        # 去掉 ** 加粗标记
                        cell_text = re.sub(r'\*{2}(.*?)\*{2}', r'\1', cell)
                        processed_row.append(cell_text)
                    processed_data.append(processed_row)

                # 判断是否为附录表格
                is_appendix_table = in_appendix

                # 创建表格，附录表格拉宽到正文两端
                if is_appendix_table:
                    # 计算表格宽度：A4宽度减去左右边距
                    table_width = A4[0] - 42*mm
                    col_count = len(processed_data[0]) if processed_data else 1
                    col_width = table_width / col_count
                    t = Table(processed_data, colWidths=[col_width] * col_count)
                else:
                    t = Table(processed_data)

                # 基础表格样式
                table_style = [
                    ('FONTNAME', (0, 0), (-1, -1), base_font),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ]

                # 附录表格：所有列居中
                if is_appendix_table:
                    table_style.append(('ALIGN', (0, 0), (-1, -1), 'CENTER'))
                else:
                    # 普通表格：第一列左对齐，其他列居中
                    table_style.append(('ALIGN', (0, 0), (0, -1), 'LEFT'))
                    table_style.append(('ALIGN', (1, 0), (-1, -1), 'CENTER'))

                t.setStyle(TableStyle(table_style))
                story.append(t)
                story.append(Spacer(1, 12))
            after_heading2 = False

        elif elem_type == 'separator':
            story.append(Spacer(1, 15))
            after_heading2 = False

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


def md_to_pdf(input_path: str, output_path: str = None) -> str:
    """
    将 Markdown 文件转换为 PDF

    Args:
        input_path: 输入 Markdown 文件路径
        output_path: 输出 PDF 文件路径（可选）

    Returns:
        输出 PDF 文件路径
    """
    input_file = Path(input_path)

    # 检查输入文件是否存在
    if not input_file.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    # 确定输出路径
    if output_path is None:
        output_file = input_file.with_suffix('.pdf')
    else:
        output_file = Path(output_path)

    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 读取 Markdown 内容
    print(f"读取文件: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 检测是否包含 CJK 字符
    has_cjk = contains_cjk(md_content)
    if has_cjk:
        print("检测到中日韩文字，启用 CJK 字体支持")

    # 解析 Markdown 内容
    print("解析 Markdown...")
    elements = parse_md_content(md_content)

    # 创建 PDF
    print("生成 PDF...")
    create_pdf_from_elements(elements, output_file, has_cjk)

    print(f"PDF 已生成: {output_file}")
    return str(output_file)


def main():
    """命令行入口"""
    args = sys.argv[1:]

    # 字体自检子命令：不转换文件，仅打印检测结果并退出
    if args and args[0] in ('--check-fonts', 'check-fonts'):
        print("=== 字体环境自检 / Font environment check ===")
        print(f"本地字体目录: {_FONTS_DIR}")
        if _FONTS_DIR.exists():
            local = sorted(p.name for p in _FONTS_DIR.iterdir()
                           if p.suffix.lower() in ('.ttf', '.otf', '.ttc'))
            print(f"  本地字体文件: {local if local else '(空)'}")
        else:
            print("  本地字体目录不存在")
        regular, bold = register_system_fonts()
        print(f"\n最终选定:")
        print(f"  正文字体: {regular}")
        print(f"  标题字体: {bold}")
        if regular == 'Helvetica':
            print("\n❌ 未命中任何中文字体，中文将渲染为方块。")
            print("   修复方式（任选其一）:")
            print("   1) python scripts/download_fonts.py  — 下载开源思源字体")
            print(f"   2) 手动下载 TTF/OTF 放入 {_FONTS_DIR}")
            print("   3) 在系统层面安装任意 CJK 字体（Noto CJK / 微软雅黑 / 苹方等）")
            sys.exit(2)
        print("\n✅ 中文字体可用。")
        sys.exit(0)

    if len(args) < 1:
        print(__doc__)
        print("错误: 缺少输入文件参数")
        print("\n示例:")
        print("  python md_to_pdf.py input.md")
        print("  python md_to_pdf.py input.md output.pdf")
        print("  python md_to_pdf.py --check-fonts")
        sys.exit(1)

    input_path = args[0]
    output_path = args[1] if len(args) > 1 else None

    try:
        result = md_to_pdf(input_path, output_path)
        print(f"\n✅ 转换成功: {result}")
    except FileNotFoundError as e:
        print(f"\n❌ 文件错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 转换失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()