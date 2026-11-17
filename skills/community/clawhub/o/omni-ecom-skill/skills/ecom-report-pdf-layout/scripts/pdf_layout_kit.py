# -*- coding: utf-8 -*-
"""
标准电商经营诊断报告版式 · 排版工具包
=====================================
把 reportlab 中文 PDF 的三条铁律固化成可复用模块，避免每次重写样式。

三条铁律（写死在本模块，勿覆盖）：
  1. 正文 alignment=TA_LEFT + firstLineIndent=20，严禁 TA_JUSTIFY
  2. PageBreak 全文 0~1 个（本模块不提供 PageBreak 封装，需要时自己 import）
  3. 图表高宽比 CHART_RATIO=0.38，允许 0.35~0.40，禁止 0.5+

用法：
    from pdf_layout_kit import *
    doc = build_doc(resolve_out_path(PDF_PATH), title='XX店铺X月经营分析报告')
    story = [
        Paragraph('示例店铺 6 月经营分析报告', styles['DocTitle']),
        Paragraph('报告期：20XX年6月 ｜ 生成日期：20XX-07-05 ｜ 数据源：平台原始导出', styles['DocMeta']),
        section_title('一', '经营总览'),
        body('本月 GMV 120万元，净销售参考值 84万元；具体口径见证据附录。'),
        judge('退款对销售质量有显著影响，正式归因需结合订单期口径复核。'),
        make_table(rows, col_widths=[5*cm, 3.5*cm, 3.5*cm, 3.5*cm], first_col_left=True),
        *chart(os.path.join(CHART_DIR, 'gmv_trend.png'), caption='图1 月度GMV与净支付趋势'),
    ]
    doc.build(story)
    verify_pdf(doc.filename)
"""
import os
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
    KeepTogether, HRFlowable,
)

__all__ = [
    'styles', 'colors', 'cm', 'A4', 'Paragraph', 'Spacer', 'Table', 'TableStyle',
    'Image', 'KeepTogether', 'HRFlowable',
    'DARK', 'GRAY', 'LIGHT_GRAY', 'MID_GRAY', 'ACCENT', 'UP_GOOD', 'DOWN_BAD', 'BG_JUDGE',
    'CHART_W', 'CHART_RATIO', 'CONTENT_W', 'MAX_PAGES',
    'build_doc', 'resolve_out_path', 'verify_pdf',
    'section_title', 'subsection_title', 'body', 'body_left', 'small',
    'judge', 'finding', 'advice', 'chart', 'make_table',
    'change_html', 'pct_change_html', 'money_change_html',
    'fmt_money', 'fmt_wan', 'fmt_pct', 'fmt_num',
    'setup_matplotlib_cn',
]

# ---------------------------------------------------------------------------
# 字体注册（Windows）
# ---------------------------------------------------------------------------
_FONT_YAHEI = r'C:\Windows\Fonts\msyh.ttc'
_FONT_SIMHEI = r'C:\Windows\Fonts\simhei.ttf'

pdfmetrics.registerFont(TTFont('YaHei', _FONT_YAHEI, subfontIndex=0))
pdfmetrics.registerFont(TTFont('YaHei-Bold', _FONT_YAHEI, subfontIndex=1))
pdfmetrics.registerFont(TTFont('SimHei', _FONT_SIMHEI))

# ---------------------------------------------------------------------------
# 调色板（定版，勿改）
# ---------------------------------------------------------------------------
DARK = colors.HexColor('#333333')
GRAY = colors.HexColor('#666666')
LIGHT_GRAY = colors.HexColor('#F5F5F5')
MID_GRAY = colors.HexColor('#DDDDDD')
ACCENT = colors.HexColor('#2E5AAC')
UP_GOOD = colors.HexColor('#52C41A')     # 好 = 绿
DOWN_BAD = colors.HexColor('#FF4D4F')    # 坏 = 红
BG_JUDGE = colors.HexColor('#F2F2F2')

# ---------------------------------------------------------------------------
# 版面常量
# ---------------------------------------------------------------------------
MARGIN_LR = 2.5 * cm
MARGIN_TB = 2.0 * cm
CONTENT_W = A4[0] - MARGIN_LR * 2          # 16cm
CHART_W = 15.5 * cm                         # 图表宽度
CHART_RATIO = 0.38                          # 铁律 3：0.35~0.40
MAX_PAGES = 17                              # 交付物标准：页数上限

# ---------------------------------------------------------------------------
# 样式表
# ---------------------------------------------------------------------------
styles = getSampleStyleSheet()

_STYLE_DEFS = [
    dict(name='DocTitle', fontName='YaHei-Bold', fontSize=22, leading=28,
         textColor=DARK, alignment=TA_LEFT, spaceAfter=4),
    dict(name='DocMeta', fontName='YaHei', fontSize=10, leading=14,
         textColor=GRAY, alignment=TA_LEFT, spaceAfter=18),
    dict(name='Section', fontName='YaHei-Bold', fontSize=15, leading=22,
         textColor=DARK, alignment=TA_LEFT, spaceBefore=18, spaceAfter=8),
    dict(name='SubSection', fontName='YaHei-Bold', fontSize=11.5, leading=17,
         textColor=DARK, alignment=TA_LEFT, spaceBefore=10, spaceAfter=5),
    # 铁律 1：正文 TA_LEFT + 首行缩进 20，严禁 TA_JUSTIFY
    dict(name='Body', fontName='YaHei', fontSize=10, leading=16,
         textColor=DARK, alignment=TA_LEFT, firstLineIndent=20, spaceAfter=6),
    dict(name='BodyLeft', fontName='YaHei', fontSize=10, leading=16,
         textColor=DARK, alignment=TA_LEFT, spaceAfter=5),
    dict(name='Small', fontName='YaHei', fontSize=9, leading=13,
         textColor=GRAY, alignment=TA_LEFT, spaceAfter=4),
    dict(name='Caption', fontName='YaHei', fontSize=9, leading=13,
         textColor=GRAY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10),
    dict(name='Judge', fontName='YaHei-Bold', fontSize=10, leading=16,
         textColor=DARK, alignment=TA_LEFT, spaceAfter=2),
    dict(name='TableHeader', fontName='YaHei-Bold', fontSize=9.5, leading=14,
         textColor=DARK, alignment=TA_CENTER),
    dict(name='TableCell', fontName='YaHei', fontSize=9.5, leading=14,
         textColor=DARK, alignment=TA_CENTER),
    dict(name='TableCellLeft', fontName='YaHei', fontSize=9.5, leading=14,
         textColor=DARK, alignment=TA_LEFT),
]
for _d in _STYLE_DEFS:
    if _d['name'] not in styles:
        styles.add(ParagraphStyle(**_d))


# ---------------------------------------------------------------------------
# 文档构建
# ---------------------------------------------------------------------------
def build_doc(out_path, title='电商经营分析报告', author=''):
    """A4 纵向，标准边距。out_path 建议先过 resolve_out_path()。

    author 默认留空（PDF 属性不写入任何机构名）。如需署名，由调用方显式传入
    自己的机构/团队名称，例如 build_doc(path, author='XX咨询')。
    """
    return SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=MARGIN_LR, rightMargin=MARGIN_LR,
        topMargin=MARGIN_TB, bottomMargin=MARGIN_TB,
        title=title, author=author,
    )


def resolve_out_path(path):
    """目标 PDF 被阅读器占用时自动追加 _vX.Y 后缀，返回可写路径。"""
    def _writable(p):
        if not os.path.exists(p):
            d = os.path.dirname(p) or '.'
            os.makedirs(d, exist_ok=True)
            return True
        try:
            with open(p, 'a+b'):
                return True
        except (PermissionError, OSError):
            return False

    if _writable(path):
        return path

    root, ext = os.path.splitext(path)
    m = re.search(r'_v(\d+)\.(\d+)$', root)
    if m:
        base, major, minor = root[:m.start()], int(m.group(1)), int(m.group(2))
    else:
        base, major, minor = root, 2, 3
    for _ in range(200):
        minor += 1
        cand = '%s_v%d.%d%s' % (base, major, minor, ext)
        if _writable(cand):
            print('[INFO] 原路径被占用，改写入：%s' % cand)
            return cand
    raise IOError('无法找到可写的输出路径：%s' % path)


def verify_pdf(path, max_pages=MAX_PAGES):
    """生成后自检：页数、空白页、中文渲染。缺库时降级为提示。"""
    ok = True
    try:
        import pymupdf as fitz
    except ImportError:
        print('[WARN] 未安装 pymupdf，跳过版式自检')
        return None

    doc = fitz.open(path)
    n = doc.page_count
    print('[CHECK] 总页数：%d（上限 %d）' % (n, max_pages))
    if n > max_pages:
        ok = False
        print('[FAIL] 页数超标，请压缩图表尺寸或合并同类章节')

    blanks = []
    for i, page in enumerate(doc, 1):
        text = page.get_text().strip()
        imgs = page.get_images(full=True)
        if len(text) < 30 and not imgs:
            blanks.append(i)
    if blanks:
        ok = False
        print('[FAIL] 疑似空白页：%s → 检查是否滥用 PageBreak（铁律 2）' % blanks)
    else:
        print('[CHECK] 无空白页')

    sample = doc[min(1, n - 1)].get_text()
    if sample and not re.search(r'[\u4e00-\u9fff]', sample):
        ok = False
        print('[FAIL] 未抽到中文，字体注册可能失败')
    doc.close()
    print('[RESULT] %s' % ('版式自检通过' if ok else '版式自检未通过，需修正'))
    return ok


# ---------------------------------------------------------------------------
# 数字格式化（货币一律用「元」，禁用 ¥）
# ---------------------------------------------------------------------------
def fmt_money(x, digits=2):
    return '%s元' % format(round(float(x), digits), ',.%df' % digits)


def fmt_wan(x, digits=2):
    return '%.*f万元' % (digits, float(x) / 10000.0)


def fmt_pct(x, digits=2):
    return '%.*f%%' % (digits, float(x))


def fmt_num(x):
    return format(int(round(float(x))), ',d')


# ---------------------------------------------------------------------------
# 涨跌着色
# ---------------------------------------------------------------------------
def _cname(color):
    return '#' + color.hexval().replace('0x', '')[-6:]


def change_html(current, previous, inverse=False, digits=1, unit='pct', style='TableCell'):
    """
    绿涨红跌箭头。
    inverse=True → 越低越好（退款率/跳失率/退货率/获客成本）
    unit='pct'   → 百分点差 ↑2.3pp（率类指标）
    unit='num'   → 相对变化 ↓18.5%（量类指标）
    """
    st = styles[style]
    if previous in (None, 0):
        return Paragraph('-', st)
    delta = (current - previous) if unit == 'pct' else (current - previous) / abs(previous) * 100.0
    if abs(delta) < 0.001:
        return Paragraph('<font color="#999999">—</font>', st)
    is_up = delta > 0
    good = (is_up and not inverse) or (not is_up and inverse)
    color = UP_GOOD if good else DOWN_BAD
    arrow = '↑' if is_up else '↓'
    suffix = 'pp' if unit == 'pct' else '%'
    txt = '%s%.*f%s' % (arrow, digits, abs(delta), suffix)
    return Paragraph('<font color="%s"><b>%s</b></font>' % (_cname(color), txt), st)


def pct_change_html(current, previous, inverse=False, digits=1):
    """量类指标相对变化（GMV / 访客 / 订单）。"""
    return change_html(current, previous, inverse=inverse, digits=digits, unit='num')


def money_change_html(current, previous, digits=1):
    return change_html(current, previous, inverse=False, digits=digits, unit='num')


# ---------------------------------------------------------------------------
# 结构元素
# ---------------------------------------------------------------------------
def section_title(num, title):
    """章节标题：section_title('一', '经营总览')"""
    return Paragraph('%s、%s' % (num, title), styles['Section'])


def subsection_title(num, title):
    """子节标题：subsection_title(1, '流量结构')"""
    return Paragraph('%s. %s' % (num, title), styles['SubSection'])


def body(text):
    """正文段落（自动首行缩进 2 字符）"""
    return Paragraph(text, styles['Body'])


def body_left(text):
    """不缩进的正文（列表项、说明）"""
    return Paragraph(text, styles['BodyLeft'])


def small(text):
    """脚注 / 口径说明"""
    return Paragraph(text, styles['Small'])


def _callout(label, text):
    inner = Paragraph('<b>%s：</b>%s' % (label, text), styles['BodyLeft'])
    t = Table([[inner]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_JUDGE),
        ('BOX', (0, 0), (-1, -1), 0.5, MID_GRAY),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


def judge(text):
    """经营判断 callout（定性判断，每章最多 1 条）"""
    return _callout('经营判断', text)


def finding(text):
    """关键发现 callout（数据层面异常/亮点）"""
    return _callout('关键发现', text)


def advice(idx, goal, actions, metrics, owner=None, deadline=None, acceptance=None, stop=None):
    """
    行动建议：目标 / 动作 / 观察指标，并可选负责人 / 时间 / 验收 / 停止条件。
    actions 可以是 str 或 list[str]
    """
    if isinstance(actions, (list, tuple)):
        actions = ' '.join('%s%s' % ('①②③④⑤⑥⑦⑧⑨'[i] if i < 9 else '·', a)
                           for i, a in enumerate(actions))
    items = [
        Paragraph('<b>建议%s</b>' % idx, styles['Judge']),
        Paragraph('<b>目标：</b>%s' % goal, styles['BodyLeft']),
        Paragraph('<b>动作：</b>%s' % actions, styles['BodyLeft']),
        Paragraph('<b>观察指标：</b>%s' % metrics, styles['BodyLeft']),
    ]
    if owner:
        items.append(Paragraph('<b>负责人：</b>%s' % owner, styles['BodyLeft']))
    if deadline:
        items.append(Paragraph('<b>时间：</b>%s' % deadline, styles['BodyLeft']))
    if acceptance:
        items.append(Paragraph('<b>验收标准：</b>%s' % acceptance, styles['BodyLeft']))
    if stop:
        items.append(Paragraph('<b>停止条件：</b>%s' % stop, styles['BodyLeft']))
    items.append(Spacer(1, 6))
    return KeepTogether(items)


def chart(path, width=CHART_W, ratio=CHART_RATIO, caption=None):
    """
    图表（铁律 3：高宽比 0.35~0.40）。返回 flowable 列表，用 *chart(...) 展开。
    """
    if not (0.35 <= ratio <= 0.40):
        raise ValueError('图表高宽比 %.2f 越界，必须在 0.35~0.40（铁律 3）' % ratio)
    items = []
    if os.path.exists(path):
        items.append(Image(path, width=width, height=width * ratio))
        if caption:
            items.append(Paragraph(caption, styles['Caption']))
    else:
        print('[WARN] 图表缺失：%s' % path)
        items.append(Paragraph('[图表缺失: %s]' % os.path.basename(path), styles['Small']))
    return items


def make_table(data, col_widths, header=True, align='center', first_col_left=False):
    """
    浅灰表头 + 细边框标准表。单元格自动 Paragraph 包裹。
    col_widths 合计应等于 CONTENT_W。
    """
    total = sum(col_widths)
    if abs(total - CONTENT_W) > 0.6 * cm:
        print('[WARN] 表格列宽合计 %.2fcm，正文宽 %.2fcm，可能溢出' % (total / cm, CONTENT_W / cm))

    cell_style = styles['TableCellLeft'] if align == 'left' else styles['TableCell']
    first_style = styles['TableCellLeft'] if first_col_left else cell_style

    rows = []
    for i, row in enumerate(data):
        r = []
        for j, val in enumerate(row):
            if isinstance(val, Paragraph):
                r.append(val)
            elif i == 0 and header:
                r.append(Paragraph(str(val), styles['TableHeader']))
            elif j == 0 and first_col_left:
                r.append(Paragraph(str(val), first_style))
            else:
                r.append(Paragraph(str(val), cell_style))
        rows.append(r)

    t = Table(rows, colWidths=col_widths, repeatRows=1 if header else 0)
    st = [
        ('FONTNAME', (0, 0), (-1, -1), 'YaHei'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, MID_GRAY),
    ]
    if header:
        st += [
            ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GRAY),
            ('FONTNAME', (0, 0), (-1, 0), 'YaHei-Bold'),
        ]
    t.setStyle(TableStyle(st))
    return t


# ---------------------------------------------------------------------------
# matplotlib 中文配置
# ---------------------------------------------------------------------------
def setup_matplotlib_cn():
    """
    图表字体用 SimHei；货币一律写「元」，禁用「¥」（黑体缺该字形会留空）。
    出图建议 figsize=(9, 3.4), dpi=160，与 CHART_RATIO=0.38 对应。
    """
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import font_manager, rcParams
    font_manager.fontManager.addfont(_FONT_SIMHEI)
    rcParams['font.sans-serif'] = ['SimHei']
    rcParams['axes.unicode_minus'] = False
    rcParams['figure.dpi'] = 160
    rcParams['savefig.bbox'] = 'tight'
    return rcParams
