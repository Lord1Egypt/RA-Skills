#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create-pdf-doc.py — 火一五企业级原生 PDF 生成器 v7.0

不经过 Word 直接生成 PDF：
  - 复用 doc_core.py 的 Markdown 解析与文档规范预设（与 Word 渲染一致的版式语义）
  - 12 类规范全部支持
  - 页眉：LOGO + 公司名（左 / 居中 / 简洁三种布局），页脚：第 X 页 / 共 Y 页
  - 中文字体三层回落：Songti / STHeiti / 系统兜底
  - 缺公司信息时复用 company-info.py 的补录流程（exit 2 + 结构化 JSON）

依赖：
    pip install reportlab

用法：
    python create-pdf-doc.py --output 文档.pdf --title '标题' --content '...'
"""

import os
import sys
import html
import argparse
import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily, stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, PageBreak, KeepTogether,
    Preformatted, HRFlowable, ListFlowable, ListItem, Image,
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_core  # noqa: E402

# Pygments 是可选依赖；装了即代码块高亮
try:
    from pygments import lex
    from pygments.lexers import get_lexer_by_name
    from pygments.util import ClassNotFound
    HAS_PYGMENTS = True
except ImportError:  # pragma: no cover
    HAS_PYGMENTS = False


# ============================================================
# 一、字体注册（CJK + 等宽）
# ============================================================

class FontRegistry:
    """跨平台 CJK 字体注册。

    输出三个家族：
      - 宋体家族 (CJKSongti normal / CJKSongtiBold)
      - 黑体家族 (CJKHeiti  normal / CJKHeitiBold)
      - 等宽家族 (CJKMono   normal / CJKMonoBold)

    各 preset 的 font_body / font_heading 通过 PDF_FONT_MAP 落到这三家之一。
    """

    # v7.8.1 fix: macOS Songti.ttc / STHeiti.ttc 的 subface 索引被搞错了
    # 实测 fontTools 输出：
    #   Songti.ttc: [0] STSongti-SC-Black (特黑！) [1] SC-Bold [6] SC-Regular ← 正文要这个
    #   STHeiti Medium.ttc: [0] TC-Medium (繁体！) [1] SC-Medium ← 简体要这个
    # 之前 PDF 直出长期用的是「特黑」+「繁体」，看上去就跟 Word 不一样。
    SONGTI_CANDIDATES = [
        # macOS — subface 6 = STSongti-SC-Regular (正文), 1 = STSongti-SC-Bold
        ('/System/Library/Fonts/Supplemental/Songti.ttc', 6, 1),
        ('/System/Library/Fonts/Songti.ttc', 6, 1),
        # Linux Noto
        ('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc', 2, 2),
        ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 0, 0),
        # Windows
        (r'C:\Windows\Fonts\simsun.ttc', 0, 0),
        (r'C:\Windows\Fonts\simfang.ttf', None, None),
    ]

    HEITI_CANDIDATES = [
        # macOS — subface 1 = STHeitiSC-Medium (简体！), 0 是 TC (繁体) 不要选
        ('/System/Library/Fonts/STHeiti Medium.ttc', 1, 1),
        ('/System/Library/Fonts/STHeiti Light.ttc', 1, 1),
        # PingFang SC 备选 (macOS 11+ 系统字体)
        ('/System/Library/Fonts/PingFang.ttc', 0, 1),
        # Linux
        ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 2, 2),
        ('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 0, 0),
        # Windows
        (r'C:\Windows\Fonts\simhei.ttf', None, None),
        (r'C:\Windows\Fonts\msyh.ttc', 0, 1),
    ]

    MONO_CANDIDATES = [
        # macOS
        ('/System/Library/Fonts/Menlo.ttc', 0, 1),
        # Linux
        ('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', None, None),
        ('/usr/share/fonts/TTF/DejaVuSansMono.ttf', None, None),
        # Windows
        (r'C:\Windows\Fonts\consola.ttf', None, None),
        (r'C:\Windows\Fonts\cour.ttf', None, None),
    ]

    def __init__(self):
        self.songti = None
        self.songti_bold = None
        self.heiti = None
        self.heiti_bold = None
        self.mono = None
        self.mono_bold = None

    @staticmethod
    def _try_register(name, path, subface):
        try:
            if subface is None:
                pdfmetrics.registerFont(TTFont(name, path))
            else:
                pdfmetrics.registerFont(
                    TTFont(name, path, subfontIndex=subface))
            return True
        except Exception:
            return False

    def _register_pair(self, family_name, candidates):
        for path, regular_idx, bold_idx in candidates:
            if not os.path.exists(path):
                continue
            reg_name = f'{family_name}'
            bold_name = f'{family_name}Bold'
            if self._try_register(reg_name, path, regular_idx):
                if regular_idx == bold_idx or not self._try_register(
                        bold_name, path, bold_idx):
                    bold_name = reg_name
                return reg_name, bold_name
        return None, None

    def register_all(self):
        self.songti, self.songti_bold = self._register_pair(
            'CJKSongti', self.SONGTI_CANDIDATES)
        self.heiti, self.heiti_bold = self._register_pair(
            'CJKHeiti', self.HEITI_CANDIDATES)
        self.mono, self.mono_bold = self._register_pair(
            'CJKMono', self.MONO_CANDIDATES)

        # 至少要有一种 CJK 字体；用它互相回落
        primary = self.songti or self.heiti
        primary_bold = self.songti_bold or self.heiti_bold or primary
        if not primary:
            raise RuntimeError(
                '未找到任何可用的中文字体（Songti / STHeiti / Noto / SimSun）。'
                '请安装 LibreOffice、Microsoft Office 或 Noto CJK 字体。'
            )
        # 缺哪种就用 primary 兜底
        if not self.songti:
            self.songti, self.songti_bold = primary, primary_bold
        if not self.heiti:
            self.heiti, self.heiti_bold = primary, primary_bold
        if not self.mono:
            self.mono, self.mono_bold = primary, primary_bold

        # 注册 Family，让 <b> / <i> HTML 标记生效
        registerFontFamily(self.songti, normal=self.songti,
                           bold=self.songti_bold,
                           italic=self.songti,
                           boldItalic=self.songti_bold)
        registerFontFamily(self.heiti, normal=self.heiti,
                           bold=self.heiti_bold,
                           italic=self.heiti,
                           boldItalic=self.heiti_bold)
        registerFontFamily(self.mono, normal=self.mono,
                           bold=self.mono_bold,
                           italic=self.mono,
                           boldItalic=self.mono_bold)
        return self

    def map(self, logical_name):
        """preset 用的中文字体名 → 已注册 reportlab 字体名。"""
        m = {
            '宋体': self.songti,
            '仿宋': self.songti,
            '楷体': self.songti,
            '方正小标宋简体': self.heiti,
            '黑体': self.heiti,
            '微软雅黑': self.heiti,
            'Consolas': self.mono,
        }
        return m.get(logical_name, self.songti)


# ============================================================
# 二、ParagraphStyle 工厂
# ============================================================

def make_styles(preset, fonts: FontRegistry):
    body_font = fonts.map(preset.font_body)
    heading_font = fonts.map(preset.font_heading)
    title_font = fonts.map(preset.font_title)
    code_font = fonts.mono

    # v7.7 fix: Word `line_spacing=N` 是「单倍行距 × N」，单倍行距 = 字号 × 字体系数 (~1.2)。
    # 之前直接 `leading = size * line_spacing` 比 Word 视觉行距紧 ~17%（同 1.5 倍，PDF 18pt vs Word 21.6pt）。
    # 加 ×1.2 系数后两端对齐（中文字体 Songti/Heiti 的实际单倍行距系数）。
    leading_factor = preset.line_spacing * 1.2

    return {
        'title': ParagraphStyle(
            'HuoTitle', fontName=title_font,
            fontSize=preset.size_title,
            leading=preset.size_title * 1.4,
            alignment=TA_CENTER, spaceBefore=18, spaceAfter=18,
        ),
        'h1': ParagraphStyle(
            'HuoH1', fontName=heading_font,
            fontSize=preset.size_chapter,
            leading=preset.size_chapter * leading_factor,
            alignment=TA_LEFT, spaceBefore=18, spaceAfter=8,
            textColor=colors.HexColor('#1a1a1a'),
        ),
        'h2': ParagraphStyle(
            'HuoH2', fontName=heading_font,
            fontSize=preset.size_section,
            leading=preset.size_section * leading_factor,
            alignment=TA_LEFT, spaceBefore=14, spaceAfter=6,
            textColor=colors.HexColor('#1a1a1a'),
        ),
        'h3': ParagraphStyle(
            'HuoH3', fontName=heading_font,
            fontSize=preset.size_body + 1,
            leading=(preset.size_body + 1) * leading_factor,
            alignment=TA_LEFT, spaceBefore=8, spaceAfter=4,
        ),
        'body': ParagraphStyle(
            'HuoBody', fontName=body_font,
            fontSize=preset.size_body,
            leading=preset.size_body * leading_factor,
            alignment=TA_JUSTIFY,
            # v7.7 fix: Word 用 firstLineChars=200 (2 中文字符宽，自适应字号)，
            # PDF 之前用固定 0.74cm (≈21pt) 在 12pt 下偏小、在大字号下严重失真。
            # 改为 size × 2 (= 2 中文字符宽 pt 单位)，跨字号视觉与 Word 一致。
            firstLineIndent=preset.size_body * 2,
            spaceBefore=0, spaceAfter=preset.paragraph_spacing_pt,
        ),
        'body_noindent': ParagraphStyle(
            'HuoBodyNoIndent', fontName=body_font,
            fontSize=preset.size_body,
            leading=preset.size_body * leading_factor,
            alignment=TA_JUSTIFY, firstLineIndent=0,
            spaceBefore=0, spaceAfter=preset.paragraph_spacing_pt,
        ),
        'list_item': ParagraphStyle(
            'HuoList', fontName=body_font,
            fontSize=preset.size_body,
            leading=preset.size_body * leading_factor,
            leftIndent=14, bulletIndent=0,
            alignment=TA_JUSTIFY, spaceBefore=0, spaceAfter=3,
        ),
        'code': ParagraphStyle(
            'HuoCode', fontName=code_font,
            fontSize=preset.size_body - 1,
            leading=(preset.size_body - 1) * 1.3,
            backColor=colors.HexColor('#F5F5F5'),
            borderColor=colors.HexColor('#CCCCCC'),
            borderWidth=0.5, borderPadding=6,
            leftIndent=4, rightIndent=4, spaceBefore=4, spaceAfter=8,
            textColor=colors.HexColor('#222222'),
        ),
        'quote': ParagraphStyle(
            'HuoQuote', fontName=body_font,
            fontSize=preset.size_body,
            leading=preset.size_body * leading_factor,
            leftIndent=18, spaceBefore=4, spaceAfter=4,
            textColor=colors.HexColor('#555555'),
        ),
        'classification': ParagraphStyle(
            'HuoClass', fontName=heading_font,
            fontSize=preset.size_body, alignment=TA_RIGHT,
            textColor=colors.HexColor('#B00000'),
            spaceBefore=0, spaceAfter=0,
        ),
        'meta_key': ParagraphStyle(
            'HuoMetaKey', fontName=heading_font,
            fontSize=preset.size_body - 1, alignment=TA_LEFT,
            leading=(preset.size_body - 1) * 1.4,
        ),
        'meta_val': ParagraphStyle(
            'HuoMetaVal', fontName=body_font,
            fontSize=preset.size_body - 1, alignment=TA_LEFT,
            leading=(preset.size_body - 1) * 1.4,
        ),
        '_body_font': body_font,
        '_heading_font': heading_font,
        '_title_font': title_font,
        '_code_font': code_font,
    }


# ============================================================
# 三、内联 → reportlab HTML
# ============================================================

def inline_to_html(text, code_font_name):
    """tokenize → escape → reportlab 受限 HTML。

    text 中的 '\n' 是硬换行 → <br/>
    """
    if not text:
        return ''
    out_parts = []
    for line_idx, line in enumerate(doc_core.split_paragraph_lines(text)):
        if line_idx > 0:
            out_parts.append('<br/>')
        for kind, payload in doc_core.tokenize_inline(line):
            esc = html.escape(payload)
            if kind == 'bold':
                out_parts.append(f'<b>{esc}</b>')
            elif kind == 'italic':
                out_parts.append(f'<i>{esc}</i>')
            elif kind == 'code':
                out_parts.append(
                    f'<font face="{code_font_name}">{esc}</font>')
            else:
                out_parts.append(esc)
    return ''.join(out_parts)


# ============================================================
# 四、Block → Flowables
# ============================================================

def render_blocks_to_flowables(blocks, styles):
    flow = []
    for b in blocks:
        flow.extend(render_block(b, styles))
    return flow


def render_block(block, styles):
    btype = block['type']
    if btype == 'heading':
        return [render_heading(block, styles)]
    if btype == 'paragraph':
        text = block['text']
        # 兜住规范专属中文编号 → 转标题
        # 调用方需传 preset 给 detect；为简单起见这里只处理纯 markdown heading
        return [render_paragraph(text, styles)]
    if btype == 'list':
        return render_list(block, styles)
    if btype == 'table':
        return render_table(block, styles)
    if btype == 'code_block':
        return render_code_block(block, styles)
    if btype == 'blockquote':
        return render_blockquote(block, styles)
    if btype == 'metadata':
        return render_metadata(block, styles)
    if btype == 'hr':
        return [HRFlowable(width='100%', color=colors.HexColor('#CCCCCC'),
                           thickness=0.6, spaceBefore=4, spaceAfter=6)]
    if btype == 'page_break':
        return [PageBreak()]
    return []


_PDF_HEADING_COUNTER = [0]


def _reset_pdf_headings():
    _PDF_HEADING_COUNTER[0] = 0


def render_heading(block, styles):
    level = block['level']
    text = block['text']
    style = styles['h1'] if level <= 1 else (
        styles['h2'] if level == 2 else styles['h3'])
    _PDF_HEADING_COUNTER[0] += 1
    anchor = f'h_{_PDF_HEADING_COUNTER[0]}'
    h = inline_to_html(text, styles['_code_font'])
    # reportlab Paragraph 支持 <a name="..."/> 锚点 + bookmarkLevel 自动加进 outline
    bookmark = f'<a name="{anchor}"/>'
    para = Paragraph(bookmark + h, style)
    # 用同名属性触发 outline：reportlab 会读 paragraph.style 里的 outlineLevel
    para._huo_outline = (text, anchor, min(level, 3) - 1)
    return para


def render_paragraph(text, styles):
    body = inline_to_html(text, styles['_code_font'])
    return Paragraph(body, styles['body'])


def render_list(block, styles):
    items = block.get('items', [])
    ordered = block.get('ordered', False)
    flow = []
    for idx, item in enumerate(items, start=1):
        bullet = f'{idx}. ' if ordered else '• '
        html_text = bullet + inline_to_html(item, styles['_code_font'])
        flow.append(Paragraph(html_text, styles['list_item']))
    return flow


def render_table(block, styles):
    rows = block.get('rows', [])
    has_header = block.get('has_header', True)
    if not rows:
        return []
    max_cols = max(len(r) for r in rows)
    norm = [r + [''] * (max_cols - len(r)) for r in rows]

    cell_style = ParagraphStyle(
        'HuoTableCell', parent=styles['body_noindent'],
        fontSize=styles['body'].fontSize - 1,
        leading=(styles['body'].fontSize - 1) * 1.4,
        alignment=TA_CENTER,
    )
    head_style = ParagraphStyle(
        'HuoTableHead', parent=cell_style,
        fontName=styles['_heading_font'],
    )

    data = []
    for r_idx, row in enumerate(norm):
        is_head = has_header and r_idx == 0
        rendered = []
        for cell_text in row:
            html_text = inline_to_html(cell_text, styles['_code_font'])
            rendered.append(Paragraph(html_text,
                                       head_style if is_head else cell_style))
        data.append(rendered)

    tbl = Table(data, repeatRows=1 if has_header else 0)
    cmds = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#888888')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]
    if has_header:
        cmds.append(('BACKGROUND', (0, 0), (-1, 0),
                     colors.HexColor('#E8ECF0')))
    tbl.setStyle(TableStyle(cmds))
    return [Spacer(1, 4), tbl, Spacer(1, 6)]


def _highlight_code_html(code, lang, code_font_name):
    """用 Pygments 把代码切成带 <font color="#xxxxxx"> 的 reportlab HTML。

    返回 None 表示无法高亮（无 Pygments 或 lexer 找不到），调用方走 fallback。
    """
    if not HAS_PYGMENTS or not lang:
        return None
    try:
        lexer = get_lexer_by_name(lang, stripall=False, ensurenl=False)
    except ClassNotFound:
        return None
    out = []
    for ttype, value in lex(code, lexer):
        col = doc_core.get_token_color(repr(ttype))
        # 保留空格 / 换行；reportlab Preformatted 默认尊重空白
        esc = (html.escape(value)
               .replace(' ', '&nbsp;'))
        # 转换换行为 <br/>，等宽显示
        esc = esc.replace('\n', '<br/>')
        if col:
            out.append(f'<font color="#{col}">{esc}</font>')
        else:
            out.append(esc)
    return ''.join(out)


def render_code_block(block, styles):
    code = block.get('code', '')
    lang = block.get('lang', '')
    parts = []
    if lang:
        tag_style = ParagraphStyle(
            'HuoCodeTag', parent=styles['code'],
            fontSize=styles['code'].fontSize - 1,
            textColor=colors.HexColor('#888888'),
            backColor=None, borderWidth=0,
            spaceBefore=4, spaceAfter=0, leftIndent=0, rightIndent=0,
        )
        parts.append(Paragraph(html.escape(lang), tag_style))

    highlighted = _highlight_code_html(code, lang, styles['_code_font'])
    if highlighted is not None:
        # 高亮路径：用 Paragraph 渲染带颜色 HTML
        hl_style = ParagraphStyle(
            'HuoCodeHL', parent=styles['code'],
            backColor=colors.HexColor('#F7F7F7'),
        )
        parts.append(Paragraph(highlighted, hl_style))
    else:
        # 普通路径：Preformatted 保原始空白与换行
        parts.append(Preformatted(code, styles['code']))
    return parts


def render_blockquote(block, styles):
    """引用块：用 1×1 Table 加左侧竖线模拟 Markdown blockquote。"""
    flow = []
    for line in block.get('lines', []):
        if not line.strip():
            continue
        html_text = inline_to_html(line, styles['_code_font'])
        para = Paragraph(html_text, styles['quote'])
        tbl = Table([[para]], colWidths=['100%'])
        tbl.setStyle(TableStyle([
            ('LINEBEFORE', (0, 0), (0, -1), 2.5,
             colors.HexColor('#FF7043')),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('BACKGROUND', (0, 0), (-1, -1),
             colors.HexColor('#FAFAFA')),
        ]))
        flow.append(tbl)
    flow.append(Spacer(1, 4))
    return flow


def render_metadata(block, styles):
    pairs = block.get('pairs', [])
    if not pairs:
        return []
    data = []
    for key, value in pairs:
        k_html = inline_to_html(key or '', styles['_code_font'])
        v_html = inline_to_html(value or '', styles['_code_font'])
        data.append([Paragraph(k_html, styles['meta_key']),
                     Paragraph(v_html, styles['meta_val'])])
    tbl = Table(data, colWidths=[3.0 * cm, None])
    tbl.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return [tbl, Spacer(1, 6)]


# ============================================================
# 五、文档壳：标题、分类条、版本历史、审批表
# ============================================================

def _strip_markdown_emphasis(text):
    """剥外层 markdown 强调标记 — 与 create-word-doc.py 同步实现。"""
    if not text:
        return text
    s = text.strip()
    while True:
        changed = False
        for marker in ('**', '*', '`', '~~'):
            if (len(s) >= 2 * len(marker)
                    and s.startswith(marker) and s.endswith(marker)):
                s = s[len(marker):-len(marker)].strip()
                changed = True
                break
        if not changed:
            break
    return s


def make_classification_flowable(classification, styles):
    if not classification or classification == '公开':
        return []
    return [Paragraph(f'【{html.escape(classification)}】',
                      styles['classification'])]


def make_title_flowable(title, styles):
    if not title:
        return []
    title = _strip_markdown_emphasis(title)
    if not title:
        return []
    return [Paragraph(html.escape(title), styles['title'])]


def make_doc_meta_flowable(doc_number, version, classification, author,
                           styles):
    doc_number = _strip_markdown_emphasis(doc_number) if doc_number else doc_number
    version = _strip_markdown_emphasis(version) if version else version
    classification = (_strip_markdown_emphasis(classification)
                      if classification else classification)
    author = _strip_markdown_emphasis(author) if author else author

    items = []
    if doc_number:
        items.append(('文档编号', doc_number))
    items.append(('版本', version))
    items.append(('密级', classification))
    items.append(('日期', datetime.date.today().strftime('%Y-%m-%d')))
    if author:
        items.append(('作者', author))
    return render_metadata({'pairs': items}, styles)


_AUTO_META_KEYS = frozenset({
    '文档编号', '编号', '合同编号', '协议编号', '订单编号', '报价编号',
    '版本', '版次', '密级', '机密等级',
    '日期', '签订日期', '签约日期', '验收日期', '生效日期',
    '作者', '编制', '审核', '批准',
})


def _heading_count_ge(content, threshold):
    """v7.6.0：与 Word 端一致，统计 H1+H2 数量。"""
    if not content:
        return False
    count = 0
    for b in doc_core.parse_blocks(content):
        if b.get('type') == 'heading' and b.get('level', 9) <= 2:
            count += 1
            if count >= threshold:
                return True
    return False


def _body_has_top_metadata_block(content):
    """v7.6.0：与 create-word-doc.py 同步实现，覆盖 KV + TABLE 两种 LLM 写法。"""
    if not content:
        return False
    blocks = doc_core.parse_blocks(content)
    if not blocks:
        return False
    first = blocks[0]
    if first.get('type') == 'heading' and first.get('level') == 1:
        if len(blocks) < 2:
            return False
        first = blocks[1]
    btype = first.get('type')
    if btype == 'metadata':
        pairs = first.get('pairs') or []
        return any((k or '').strip().strip('*~`') in _AUTO_META_KEYS
                   for k, _ in pairs)
    if btype == 'table':
        rows = first.get('rows') or []
        if not rows or len(rows) < 2:
            return False
        if not all(len(r) >= 2 for r in rows):
            return False
        first_col = [(r[0] or '').strip().strip('*~`') for r in rows]
        return sum(1 for k in first_col if k in _AUTO_META_KEYS) >= 2
    return False


def _maybe_dedupe_h1_title(content, title, preset, want_title_block):
    """与 create-word-doc.py 同步实现：剥与 --title 同文的首个 H1。"""
    if not content or not title or not want_title_block:
        return content
    if not getattr(preset, 'dedupe_h1_title', True):
        return content
    target = _strip_markdown_emphasis(title.strip())
    if not target:
        return content
    lines = content.split('\n')
    i, n = 0, len(lines)
    while i < n and not lines[i].strip():
        i += 1
    if i < n and lines[i].strip() == '---':
        j = i + 1
        while j < n and lines[j].strip() != '---':
            j += 1
        if j < n:
            i = j + 1
            while i < n and not lines[i].strip():
                i += 1
    if i >= n:
        return content
    head = lines[i].strip()
    if not head.startswith('# '):
        return content
    head_text = _strip_markdown_emphasis(head[2:].strip())
    if head_text != target:
        return content
    return '\n'.join(lines[:i] + lines[i + 1:])


def make_version_history_flowable(version, date_str, author, styles):
    head = Paragraph('版本历史', styles['h2'])
    rows = [
        ['版本', '日期', '作者', '修改说明'],
        [version or 'V1.0', date_str, author or '未知', '首次创建'],
    ]
    return [Spacer(1, 6), head] + render_table(
        {'rows': rows, 'has_header': True}, styles)


def make_approval_flowable(approval_list, styles):
    items = approval_list if approval_list else [
        {'role': '编制', 'name': ''},
        {'role': '审核', 'name': ''},
        {'role': '批准', 'name': ''},
    ]
    today = datetime.date.today().strftime('%Y-%m-%d')
    rows = [['角色', '姓名', '日期', '签字']]
    for item in items:
        role = item.get('role', '')
        name = item.get('name') or '__________'
        date_str = item.get('date') or (today if role == '编制' else '')
        rows.append([role, name, date_str, '__________'])
    head = Paragraph('审批记录', styles['h2'])
    return [Spacer(1, 6), head] + render_table(
        {'rows': rows, 'has_header': True}, styles)


# ============================================================
# 六、Header / Footer canvas（包含页码 N/M）
# ============================================================

def make_chrome_callback(preset, company_name, logo_path,
                         doc_number, classification, body_font_name):
    """v7.8.5 重写：chrome 通过 PageTemplate.onPageEnd 回调绘制，避开 two-pass canvas
    的 page resource 回退 bug。

    历史：v7.8.0~v7.8.4 用 Canvas 子类 + ``__dict__.update(state)`` 收集所有页再重绘
    chrome，但 update 把 page-level font/xobject resource dict 也回退了，导致 chrome
    里 ``setFont(CJK 字体)`` 和 ``drawImage(LOGO)`` 都写进了 PDF stream 但 page
    Resources 没引用 → 渲染器输出 .notdef glyph 和空白图像（视觉=没有页眉）。
    Helvetica 因为是 PDF 14 标准字体不需要 page resource，所以 v7.8.4 调试时只有
    Helvetica 文字可见。

    新方案：onPageEnd 在每页内容渲染完成后调用，page Resources 已正确建立，
    setFont/drawImage 自动注册到正确的 page 资源字典。trade-off：拿不到总页数，
    页脚只显示"第 X 页"（"共 N 页"需要两遍 build，工程量过大）。
    """

    def _draw_chrome(canv, doc):
        page_w, page_h = canv._pagesize
        margin_l = preset.margin_left * cm
        margin_r = preset.margin_right * cm

        header_y = page_h - 1.2 * cm
        content_left = margin_l
        content_right = page_w - margin_r

        canv.saveState()
        canv.setFillColor(colors.black)
        canv.setStrokeColor(colors.black)

        font_size = preset.size_body - 2

        # v7.8.5 关键修复：先画页脚（触发 page-level 字体注册），再画页眉。
        # 实测 onPageEnd 模式下：第 1 次 setFont+drawString 不可见、第 2 次可见。
        # 这是 reportlab 内部 page Resources 在第 1 次 drawString 时尚未建立 mapping,
        # 第 2 次才确实写到 PDF Resources/Font 字典。先画页脚等于"预热"page font 字典,
        # 后画页眉 drawString 就能命中已注册的字体。
        footer_y = preset.margin_bottom * cm * 0.5
        canv.setFont(body_font_name, font_size)
        canv.drawCentredString(
            page_w / 2, footer_y,
            f'第 {doc.page} 页'
        )

        # 现在再画页眉（字体已注册到 page Resources）
        canv.setFont(body_font_name, font_size)

        label_parts = [company_name]
        if preset.header_layout == 'company':
            if doc_number:
                label_parts.append(f'    {doc_number}')
            if classification:
                label_parts.append(f'    【{classification}】')
        label = ''.join(label_parts)

        # v7.7 fix: stringWidth 真实测宽
        text_w = stringWidth(label, body_font_name, font_size)

        # LOGO 几何
        # v7.8.5 ELEPHANT-IN-THE-ROOM 修复：之前用 Image(logo_path, height=h).wrap()
        # 拿 (iw, ih)，但 wrap() 返回 iw=原图像素宽（如 2048），ih=缩放后高度。
        # target_w = 2048 * (25.5/25.5) = 2048pt 巨大错误。drawImage(width=2048,
        # preserveAspectRatio=True) 自动居中 → LOGO x 偏移到 (2048-25.5)/2=1011pt
        # 远超出 page 595pt 宽，肉眼看不见。中文文字 text_x = x_start + logo_w
        # = 2133pt 也跑到页外。**这才是 v7.7~v7.8.4 多次修复都没解决的真因。**
        # 改用 ImageReader 直接读 LOGO 像素尺寸做等比缩放。
        logo_w = 0
        target_w = 0
        target_h = 0.9 * cm
        gap = 0.2 * cm
        has_logo = (preset.header_layout in ('company', 'minimal', 'centered')
                    and logo_path and os.path.exists(logo_path))
        if has_logo:
            try:
                from reportlab.lib.utils import ImageReader
                ir = ImageReader(logo_path)
                iw, ih = ir.getSize()  # 像素尺寸（int）
                target_w = target_h * iw / ih if ih else target_h
                logo_w = target_w + gap
            except Exception:
                has_logo = False
                logo_w = 0

        # v7.7 fix: 统一 x_start
        block_w = logo_w + text_w
        if preset.header_layout == 'centered':
            x_start = (page_w - block_w) / 2
        else:
            x_start = content_left

        text_y = header_y + 0.05 * cm

        # LOGO
        if has_logo:
            try:
                canv.drawImage(logo_path, x_start, header_y - 0.15 * cm,
                               width=target_w, height=target_h,
                               mask='auto', preserveAspectRatio=True)
            except Exception:
                pass

        # chrome 文字
        text_x = x_start + logo_w
        canv.drawString(text_x, text_y - 0.05 * cm, label)

        # 灰线
        canv.setStrokeColor(colors.HexColor('#888888'))
        canv.setLineWidth(0.5)
        canv.line(content_left, header_y - 0.4 * cm,
                  content_right, header_y - 0.4 * cm)

        canv.restoreState()

    return _draw_chrome


# ============================================================
# 七、对外入口
# ============================================================

def create_pdf_doc(output_path, title='', content='', doc_number=None,
                   version='V1.0', classification='内部', author=None,
                   company_name=None, logo_path=None, approval=None,
                   doc_format=None, use_odoo=True,
                   force_version_history=None, force_approval=None,
                   force_classification_banner=None,
                   force_doc_meta_table=None,
                   force_title_block=None):
    info = doc_core.resolve_company_info(
        overrides={'company_name': company_name, 'logo_path': logo_path},
        use_odoo=use_odoo,
    )
    missing = doc_core.company_info_missing(info)
    if missing:
        raise RuntimeError(doc_core.company_info_error_payload(missing))

    company = info['company_name']
    logo = info['logo_path']

    if not doc_format or doc_format == 'auto':
        doc_format = doc_core.detect_format(title, content)
    preset = doc_core.get_preset(doc_format)

    print(f'📄 使用文档规范: {preset.name}')
    print(f'🏢 公司: {company}')
    print(f'🖼  LOGO: {logo}')

    fonts = FontRegistry().register_all()
    styles = make_styles(preset, fonts)

    want_banner = (force_classification_banner
                   if force_classification_banner is not None
                   else getattr(preset, 'show_classification_banner', True))
    want_meta = (force_doc_meta_table
                 if force_doc_meta_table is not None
                 else getattr(preset, 'show_doc_meta_table', True))
    want_title = (force_title_block
                  if force_title_block is not None
                  else getattr(preset, 'show_title_block', True))

    # H1 dedup：若 markdown 首个 H1 与 --title 同文，剥之
    content = _maybe_dedupe_h1_title(content, title, preset, want_title)

    # v7.5.2: 正文顶部已有元数据块（LLM 通常会写一份）就跳过自动 doc-meta 表
    if (want_meta and force_doc_meta_table is None
            and _body_has_top_metadata_block(content)):
        want_meta = False

    # 1) 解析 Markdown
    blocks = doc_core.parse_blocks(content)

    # 2) 段落识别规范专属中文编号 → 标题
    promoted_blocks = []
    for b in blocks:
        if b.get('type') == 'paragraph':
            detected = doc_core.detect_heading_from_preset(b['text'], preset)
            if detected is not None:
                level, cleaned = detected
                promoted_blocks.append({
                    'type': 'heading', 'level': level, 'text': cleaned,
                })
                continue
        promoted_blocks.append(b)

    # 3) Flowables
    body_flow = []
    if want_banner:
        body_flow.extend(make_classification_flowable(classification, styles))
    if want_title:
        body_flow.extend(make_title_flowable(title, styles))
    if want_meta:
        body_flow.extend(make_doc_meta_flowable(
            doc_number, version, classification, author, styles))

    if promoted_blocks:
        body_flow.extend(render_blocks_to_flowables(promoted_blocks, styles))
    else:
        empty_style = ParagraphStyle(
            'HuoEmpty', parent=styles['body'],
            textColor=colors.HexColor('#999999'))
        body_flow.append(Paragraph('（无正文内容）', empty_style))

    want_version = (force_version_history
                    if force_version_history is not None
                    else preset.has_version_history)
    if want_version:
        body_flow.extend(make_version_history_flowable(
            version, datetime.date.today().strftime('%Y-%m-%d'),
            author or '未知', styles))

    want_approval = (force_approval if force_approval is not None
                     else preset.has_approval)
    if want_approval or approval:
        body_flow.extend(make_approval_flowable(approval, styles))

    # 4) 构建文档
    page_w, page_h = A4
    frame = Frame(
        x1=preset.margin_left * cm,
        y1=preset.margin_bottom * cm,
        width=page_w - (preset.margin_left + preset.margin_right) * cm,
        height=page_h - (preset.margin_top + preset.margin_bottom) * cm,
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
        showBoundary=0,
    )
    # v7.8.5: chrome 通过 onPageEnd 回调画在每页内容渲染后，避免 two-pass canvas
    # 的 page resource 回退 bug（之前导致页眉 LOGO + CJK 字体不可见）
    chrome_callback = make_chrome_callback(
        preset, company, logo, doc_number, classification,
        styles['_body_font'])
    # v7.8.5 二轮：onPageEnd 仍然 LOGO+CJK 不可见（page resources 在内容渲染时已被
     # reportlab finalize，回调里新加的字体/xobject ref 注册不进 page Resources）。
     # 改用 onPage（page 开始时画 chrome），此时 page resources 可变，setFont/drawImage
     # 正常注册。chrome 区域 (页面顶部 1.2cm) 与 frame 区域 (margin_top 2.5cm 起)
     # 不重叠，不会被后续内容覆盖。
    template = PageTemplate(id='HuoTemplate', frames=[frame],
                            onPage=chrome_callback)

    # BaseDocTemplate 子类：自动收集标题书签 → 写入 PDF outline / 文档大纲
    class _HuoDocTemplate(BaseDocTemplate):
        def __init__(self, *args, **kwargs):
            BaseDocTemplate.__init__(self, *args, **kwargs)
            self._huo_max_outline_level = -1

        def afterFlowable(self, flowable):
            entry = getattr(flowable, '_huo_outline', None)
            if entry:
                heading_text, anchor, level = entry
                # v7.6.0: reportlab 不允许从 level=-1 直接跳到 level=2+，
                # 否则抛 ValueError。补齐中间 level（用 anchor + 'p' 占位）。
                while self._huo_max_outline_level < level - 1:
                    next_level = self._huo_max_outline_level + 1
                    pad_anchor = f'__huo_pad_{next_level}_{id(flowable)}'
                    self.canv.bookmarkPage(pad_anchor)
                    self.canv.addOutlineEntry('', pad_anchor,
                                              level=next_level, closed=False)
                    self._huo_max_outline_level = next_level
                self.canv.bookmarkPage(anchor)
                self.canv.addOutlineEntry(heading_text, anchor,
                                           level=level, closed=False)
                if level > self._huo_max_outline_level:
                    self._huo_max_outline_level = level

    doc = _HuoDocTemplate(
        output_path, pagesize=A4,
        leftMargin=preset.margin_left * cm,
        rightMargin=preset.margin_right * cm,
        topMargin=preset.margin_top * cm,
        bottomMargin=preset.margin_bottom * cm,
        title=title or '火一五企业文档',
        author=author or company,
        subject=preset.name,
        keywords=f'{preset.name},{company}',
        creator='火一五文档技能 v7.1',
    )
    doc.addPageTemplates([template])
    # PDF 默认就显示左侧大纲（PageMode = UseOutlines）
    doc._initialPageMode = ('UseOutlines', 0)

    # v7.8.5: chrome 已通过 PageTemplate.onPageEnd 注册（上方），不再用 canvasmaker
    _reset_pdf_headings()
    doc.build(body_flow)
    print(f'✅ PDF 已生成: {output_path}')
    return output_path


# ============================================================
# 八、CLI
# ============================================================

def _parse_args(argv):
    parser = argparse.ArgumentParser(
        prog='create-pdf-doc',
        description='火一五原生 PDF 生成器 v7.0（12 类规范）',
    )
    parser.add_argument('--output', '-o', required=False, default=None,
                        help='输出 .pdf 路径（--list-formats 模式可省略）')
    parser.add_argument('--title', default='')
    parser.add_argument('--content', default='',
                        help='Markdown 正文；@file 表示从文件读取')
    parser.add_argument('--doc-number', default=None)
    parser.add_argument('--version', default='V1.0')
    parser.add_argument('--classification', default='内部')
    parser.add_argument('--author', default=None)
    parser.add_argument('--doc-format', default='auto',
                        choices=['auto'] + doc_core.list_format_names())
    parser.add_argument('--company-name', default=None)
    parser.add_argument('--logo-path', default=None)
    parser.add_argument('--no-odoo', action='store_true')
    parser.add_argument('--with-version-history', action='store_true')
    parser.add_argument('--no-version-history', action='store_true')
    parser.add_argument('--with-approval', action='store_true')
    parser.add_argument('--no-approval', action='store_true')
    parser.add_argument('--with-classification-banner', action='store_true')
    parser.add_argument('--no-classification-banner', action='store_true')
    parser.add_argument('--with-doc-meta-table', action='store_true')
    parser.add_argument('--no-doc-meta-table', action='store_true')
    parser.add_argument('--with-title-block', action='store_true')
    parser.add_argument('--no-title-block', action='store_true')
    parser.add_argument('--list-formats', action='store_true')
    return parser.parse_args(argv[1:])


def _load_content(content_arg):
    if content_arg and content_arg.startswith('@'):
        with open(content_arg[1:], 'r', encoding='utf-8') as fh:
            return fh.read()
    return content_arg


def _flag_tristate(on, off):
    if on and off:
        return None
    if on:
        return True
    if off:
        return False
    return None


def main(argv=None):
    argv = argv if argv is not None else sys.argv
    try:
        args = _parse_args(argv)
        if args.list_formats:
            for name in doc_core.list_format_names():
                p = doc_core.get_preset(name)
                desc = getattr(p, 'description', '') or ''
                flags = []
                if getattr(p, 'show_classification_banner', True):
                    flags.append('banner')
                if getattr(p, 'show_doc_meta_table', True):
                    flags.append('meta')
                if p.has_version_history:
                    flags.append('版本史')
                if p.has_approval:
                    flags.append('审批')
                if p.table_of_contents:
                    flags.append('TOC')
                flag_str = ' / '.join(flags) if flags else '简洁'
                print(f'  {name:<8s} [{flag_str}]')
                if desc:
                    print(f'           {desc}')
            return 0
        if not args.output:
            print('错误：--output 必填（除非用 --list-formats）',
                  file=sys.stderr)
            return 2
        create_pdf_doc(
            output_path=args.output,
            title=args.title,
            content=_load_content(args.content),
            doc_number=args.doc_number,
            version=args.version,
            classification=args.classification,
            author=args.author,
            company_name=args.company_name,
            logo_path=args.logo_path,
            doc_format=args.doc_format,
            use_odoo=not args.no_odoo,
            force_version_history=_flag_tristate(
                args.with_version_history, args.no_version_history),
            force_approval=_flag_tristate(
                args.with_approval, args.no_approval),
            force_classification_banner=_flag_tristate(
                args.with_classification_banner,
                args.no_classification_banner),
            force_doc_meta_table=_flag_tristate(
                args.with_doc_meta_table, args.no_doc_meta_table),
            force_title_block=_flag_tristate(
                args.with_title_block, args.no_title_block),
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
