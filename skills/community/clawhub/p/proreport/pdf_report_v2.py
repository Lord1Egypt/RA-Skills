"""PDF 报告生成器 - 对标 2222策略评估报告风格"""
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, HRFlowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

from .config import COLORS, hex_to_rgb, CTA_MARKET_AVG, CTA_TOP

# 注册中文字体
try:
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    _CN_FONT = "STSong-Light"
except:
    _CN_FONT = "Helvetica"

# 颜色常量
_PRIMARY = colors.HexColor(COLORS.PRIMARY)
_SECONDARY = colors.HexColor(COLORS.SECONDARY)
_ACCENT = colors.HexColor(COLORS.ACCENT)
_WHITE = colors.white
_LIGHT_BG = colors.HexColor(COLORS.LIGHT_BG)
_GREEN = colors.HexColor(COLORS.POSITIVE)
_RED = colors.HexColor(COLORS.NEGATIVE)
_BORDER = colors.HexColor(COLORS.BORDER)

PAGE_W, PAGE_H = A4


def _make_styles():
    """创建所有段落样式"""
    _DARK_TEXT = colors.HexColor("#1F2328")  # 近黑但不刺眼
    _SUB_TEXT = colors.HexColor("#57606A")   # 副文本石墨灰

    styles = {}
    styles["cover_title"] = ParagraphStyle(
        "cover_title", fontName=_CN_FONT, fontSize=30, leading=40,
        textColor=_WHITE, alignment=TA_CENTER, spaceAfter=14,
    )
    styles["cover_subtitle"] = ParagraphStyle(
        "cover_subtitle", fontName=_CN_FONT, fontSize=16, leading=22,
        textColor=colors.HexColor("#C0C8D4"), alignment=TA_CENTER, spaceAfter=8,
    )
    styles["cover_info"] = ParagraphStyle(
        "cover_info", fontName=_CN_FONT, fontSize=12, leading=18,
        textColor=colors.HexColor("#D0D8E4"), alignment=TA_CENTER, spaceAfter=6,
    )
    styles["h1"] = ParagraphStyle(
        "h1", fontName=_CN_FONT, fontSize=18, leading=28,
        textColor=_PRIMARY, spaceBefore=22, spaceAfter=6,
    )
    styles["h2"] = ParagraphStyle(
        "h2", fontName=_CN_FONT, fontSize=13, leading=20,
        textColor=_PRIMARY, spaceBefore=14, spaceAfter=8,
        # 左侧蓝色竖线效果
        borderColor=_PRIMARY, borderWidth=2.5,
        borderPadding=(4, 0, 4, 8),  # top, right, bottom, left
        leftIndent=10,
    )
    styles["h3"] = ParagraphStyle(
        "h3", fontName=_CN_FONT, fontSize=11, leading=17,
        textColor=_PRIMARY, spaceBefore=10, spaceAfter=6,
        leftIndent=6,
    )
    styles["body"] = ParagraphStyle(
        "body", fontName=_CN_FONT, fontSize=10, leading=18,
        textColor=_DARK_TEXT, alignment=TA_JUSTIFY, spaceAfter=8,
        firstLineIndent=20,
    )
    styles["body_no_indent"] = ParagraphStyle(
        "body_no_indent", fontName=_CN_FONT, fontSize=10, leading=18,
        textColor=_DARK_TEXT, alignment=TA_LEFT, spaceAfter=6,
    )
    styles["caption"] = ParagraphStyle(
        "caption", fontName=_CN_FONT, fontSize=9, leading=14,
        textColor=_SUB_TEXT, alignment=TA_CENTER, spaceAfter=12,
    )
    styles["disclaimer"] = ParagraphStyle(
        "disclaimer", fontName=_CN_FONT, fontSize=8, leading=12,
        textColor=_SUB_TEXT, alignment=TA_CENTER, spaceBefore=6,
    )
    styles["metric_value"] = ParagraphStyle(
        "metric_value", fontName=_CN_FONT, fontSize=24, leading=30,
        textColor=_ACCENT, alignment=TA_CENTER,
    )
    styles["metric_label"] = ParagraphStyle(
        "metric_label", fontName=_CN_FONT, fontSize=10, leading=14,
        textColor=colors.HexColor("#D0D8E4"), alignment=TA_CENTER,
    )
    return styles


def _header_footer(canvas, doc, strategy_name, report_date):
    """页眉页脚"""
    canvas.saveState()
    # 页眉蓝条
    canvas.setFillColor(_PRIMARY)
    canvas.rect(0, PAGE_H - 20 * mm, PAGE_W, 20 * mm, fill=1, stroke=0)
    canvas.setFillColor(_WHITE)
    canvas.setFont(_CN_FONT, 8.5)
    canvas.drawString(20 * mm, PAGE_H - 14 * mm, f"{strategy_name} 策略评估报告")
    canvas.drawRightString(PAGE_W - 20 * mm, PAGE_H - 14 * mm,
                          f"报告日期：{report_date}")
    # 页眉下装饰线（双线：粗蓝+细金）
    canvas.setStrokeColor(_PRIMARY)
    canvas.setLineWidth(1.5)
    canvas.line(20 * mm, PAGE_H - 22 * mm, PAGE_W - 20 * mm, PAGE_H - 22 * mm)
    canvas.setStrokeColor(_ACCENT)
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, PAGE_H - 23.5 * mm, PAGE_W - 20 * mm, PAGE_H - 23.5 * mm)
    # 页脚：页码 + 细线
    canvas.setStrokeColor(colors.HexColor("#D1D9E0"))
    canvas.setLineWidth(0.3)
    canvas.line(20 * mm, 18 * mm, PAGE_W - 20 * mm, 18 * mm)
    canvas.setFillColor(colors.HexColor("#57606A"))
    canvas.setFont(_CN_FONT, 8)
    canvas.drawCentredString(PAGE_W / 2, 12 * mm, f"第 {doc.page} 页")
    canvas.restoreState()


def _make_kv_table(data: list[tuple], col_widths=None):
    """创建键值对信息表"""
    if col_widths is None:
        col_widths = [80, 150, 80, 150]

    table_data = []
    for row in data:
        styled = []
        for i, cell in enumerate(row):
            if i % 2 == 0:
                styled.append(Paragraph(f"<b>{cell}</b>",
                    ParagraphStyle("kv", fontName=_CN_FONT, fontSize=10, textColor=_WHITE)))
            else:
                styled.append(Paragraph(str(cell),
                    ParagraphStyle("kv", fontName=_CN_FONT, fontSize=10)))
        table_data.append(styled)

    t = Table(table_data, colWidths=col_widths)
    style_cmds = [
        ("GRID", (0, 0), (-1, -1), 0.5, _BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]
    for row_idx in range(len(table_data)):
        for col_idx in range(0, len(table_data[row_idx]), 2):
            style_cmds.append(("BACKGROUND", (col_idx, row_idx), (col_idx, row_idx), _PRIMARY))
    t.setStyle(TableStyle(style_cmds))
    return t


def _make_data_table(headers: list, rows: list, col_widths=None, highlight_col=None):
    """创建数据表格，最后一列自动左对齐（适合评价说明等长文本列）"""
    styled_headers = [Paragraph(f"<b>{h}</b>",
        ParagraphStyle("th", fontName=_CN_FONT, fontSize=9.5, textColor=_WHITE, alignment=TA_CENTER))
        for h in headers]
    ncols = len(headers)
    styled_rows = []
    for row in rows:
        styled = []
        for col_idx, cell in enumerate(row):
            # 最后一列左对齐（适合长文本），其他列居中
            align = TA_LEFT if col_idx == ncols - 1 and ncols >= 4 else TA_CENTER
            styled.append(Paragraph(str(cell),
                ParagraphStyle("td", fontName=_CN_FONT, fontSize=9, alignment=align)))
        styled_rows.append(styled)

    table_data = [styled_headers] + styled_rows
    t = Table(table_data, colWidths=col_widths)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), _PRIMARY),
        ("GRID", (0, 0), (-1, -1), 0.4, _BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), _LIGHT_BG))
    t.setStyle(TableStyle(style_cmds))
    return t


def _chart_block(story, S, title, chart_path, caption, width=470, height=260):
    """将章节小标题+图表+说明打包为 KeepTogether，防止分页。
    如果图表太高超过页面可用高度（约680pt），自动缩放。
    """
    MAX_H = 420  # 留给标题+说明的空间后，图表最大高度
    if height > MAX_H:
        scale = MAX_H / height
        width, height = int(width * scale), MAX_H
    elements = []
    if title:
        elements.append(Paragraph(title, S["h2"]))
    elements.append(Image(chart_path, width=width, height=height))
    elements.append(Paragraph(caption, S["caption"]))
    story.append(KeepTogether(elements))


def _safe_text(val) -> str:
    """将任意类型安全转为字符串。列表用换行连接，None返回空串。"""
    if val is None:
        return ""
    if isinstance(val, list):
        return "\n\n".join(str(item) for item in val if item)
    return str(val)


def _md_bold(text: str) -> str:
    """将 **加粗** 转为 reportlab 蓝色加粗标签"""
    import re
    return re.sub(r'\*\*(.+?)\*\*',
                  r'<b><font color="#1B3A5C">\1</font></b>', text)


def _render_markdown_text(story, text: str, S: dict):
    """将含 Markdown 格式的文本解析为 reportlab 段落序列。
    支持：### 三级标题、## 二级标题、**加粗**（蓝色）、\n\n 分段。
    """
    if not text:
        return
    lines = text.split("\n")
    buf = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if buf:
                story.append(Paragraph(_md_bold(" ".join(buf)), S["body"]))
                buf = []
            continue
        if stripped.startswith("### "):
            if buf:
                story.append(Paragraph(_md_bold(" ".join(buf)), S["body"]))
                buf = []
            story.append(Paragraph(stripped[4:], S["h3"]))
        elif stripped.startswith("## "):
            if buf:
                story.append(Paragraph(_md_bold(" ".join(buf)), S["body"]))
                buf = []
            story.append(Paragraph(stripped[3:], S["h2"]))
        else:
            buf.append(stripped)
    if buf:
        story.append(Paragraph(_md_bold(" ".join(buf)), S["body"]))


def generate_pdf(analysis: dict, content: dict, output_path: str = "output/report.pdf"):
    """生成 PDF 报告

    Parameters
    ----------
    analysis : dict
        JSON output from run_analysis.py (core_metrics, yearly, charts, etc.)
    content : dict
        AI-generated text content keyed by section name.
    output_path : str
        Destination path for the generated PDF.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    S = _make_styles()
    c = analysis.get("core_metrics", {})
    period = analysis.get("period", {})
    strategy_name = analysis.get("strategy_name", "未知策略")
    charts = analysis.get("charts", {})
    report_date = datetime.now().strftime("%Y年%m月%d日")

    story = []

    # ==================== 封面 ====================
    story.append(Spacer(1, 60 * mm))

    # 封面蓝色块（用 Table 模拟）
    cover_content = [
        [Paragraph(f"{strategy_name} 量化策略", S["cover_title"])],
        [Paragraph("运行情况综合评估报告", S["cover_title"])],
        [Spacer(1, 5 * mm)],
        [Paragraph("Comprehensive Performance Evaluation Report", S["cover_subtitle"])],
        [Spacer(1, 10 * mm)],
        [Paragraph(f"评估区间：{period.get('start', '')} 至 {period.get('end', '')}", S["cover_info"])],
        [Paragraph(f"运行天数：{period.get('trading_days', 0)} 个交易日", S["cover_info"])],
        [Spacer(1, 8 * mm)],
        [Paragraph(f"报告日期：{report_date}", S["cover_info"])],
    ]
    cover_table = Table(cover_content, colWidths=[PAGE_W - 60 * mm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), _PRIMARY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 10 * mm))

    # 核心指标卡片
    metrics_data = [
        [Paragraph("累计收益率", S["metric_label"]),
         Paragraph("年化收益率", S["metric_label"]),
         Paragraph("最大回撤", S["metric_label"]),
         Paragraph("夏普比率", S["metric_label"])],
        [Paragraph(f"<b>{c.get('cumulative_return', 0):.1%}</b>", S["metric_value"]),
         Paragraph(f"<b>{c.get('annualized_return', 0):.1%}</b>", S["metric_value"]),
         Paragraph(f"<b>{c.get('max_drawdown', 0):.1%}</b>",
            ParagraphStyle("mv", fontName=_CN_FONT, fontSize=22, leading=28,
                          textColor=_RED if c.get('max_drawdown', 0) < -0.15 else _ACCENT, alignment=TA_CENTER)),
         Paragraph(f"<b>{c.get('sharpe_ratio', 0):.2f}</b>", S["metric_value"])],
    ]
    metrics_table = Table(metrics_data, colWidths=[110, 110, 110, 110])
    metrics_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), _PRIMARY),
        ("BACKGROUND", (0, 1), (-1, 1), _LIGHT_BG),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, _BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph(
        "免责声明：本报告基于历史净值数据生成，所有分析结果仅供参考，不构成投资建议。过往业绩不代表未来表现。",
        S["disclaimer"]))

    story.append(PageBreak())

    # ==================== 目录 ====================
    story.append(Paragraph("目 录", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))
    toc_items = [
        ("一、执行摘要", ""),
        ("二、净值曲线分析（日/周/月/年）", ""),
        ("三、策略核心评估指标", ""),
        ("四、品种与板块分析", ""),
        ("五、回撤风险提示与处置建议", ""),
        ("六、每万元每日收益率分析", ""),
        ("七、月度收益率热力图", ""),
        ("八、滚动夏普比率分析", ""),
        ("九、与市场CTA策略同期表现对比", ""),
        ("十、综合评价与结论", ""),
        ("十一、策略改进建议", ""),
    ]
    for item, _ in toc_items:
        story.append(Paragraph(f"    {item}",
            ParagraphStyle("toc", fontName=_CN_FONT, fontSize=12, leading=26,
                          textColor=colors.black, leftIndent=40)))
    story.append(PageBreak())

    # ==================== 一、执行摘要 ====================
    story.append(Paragraph("一 执行摘要", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))

    story.append(Paragraph("1.1 策略基本信息", S["h2"]))
    story.append(_make_kv_table([
        ("策略名称", f"{strategy_name}量化策略", "数据来源", "每日净值交易记录"),
        ("评估区间", f"{period.get('start', '')} 至 {period.get('end', '')}", "交易日数", f"{period.get('trading_days', 0)} 个"),
        ("初始净值", f"{c.get('start_nav', 1):.4f}", "期末净值", f"{c.get('end_nav', 1):.4f}"),
        ("历史峰值", f"{c.get('peak_nav', 1):.4f}", "报告日期", report_date),
    ]))
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph("1.2 核心表现摘要", S["h2"]))
    story.append(Paragraph(_safe_text(content.get("executive_summary")), S["body"]))
    story.append(PageBreak())

    # ==================== 二、净值曲线分析 ====================
    story.append(Paragraph("二 净值曲线分析", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))

    if "nav_drawdown" in charts:
        _chart_block(story, S, "2.1 日净值曲线与回撤分析", charts["nav_drawdown"],
                     f"图2-1 策略日净值曲线及回撤走势（{period.get('start','')}—{period.get('end','')}）", height=280)
    _render_markdown_text(story, _safe_text(content.get("nav_daily_analysis")), S)

    if "weekly_nav" in charts:
        _chart_block(story, S, "2.2 周净值曲线分析", charts["weekly_nav"],
                     "图2-2 策略周净值曲线及周收益率分布", height=240)
    _render_markdown_text(story, _safe_text(content.get("nav_weekly_analysis")), S)

    if "monthly_nav" in charts:
        _chart_block(story, S, "2.3 月净值曲线分析", charts["monthly_nav"],
                     "图2-3 策略月净值曲线及月收益率分布", height=240)
    _render_markdown_text(story, _safe_text(content.get("nav_monthly_analysis")), S)

    if "yearly_bar" in charts:
        _chart_block(story, S, "2.4 年度净值走势与年化收益", charts["yearly_bar"],
                     "图2-4 年度净值走势与年度收益率对比", height=200)

    yearly_list = analysis.get("yearly", [])
    _render_markdown_text(story, _safe_text(content.get("nav_yearly_analysis")), S)

    story.append(PageBreak())

    # ==================== 三、策略核心评估指标 ====================
    story.append(Paragraph("三 策略核心评估指标", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))
    if "radar" in charts:
        _chart_block(story, S, "3.1 综合评分雷达图与指标总览", charts["radar"],
                     "图3-1 策略综合评分雷达图", width=260, height=260)
    story.append(Paragraph("3.2 核心指标深度解析", S["h2"]))
    ie = content.get("indicator_evaluations", {})
    if isinstance(ie, list): ie = {}
    indicator_names = ["年化收益率","年化波动率","最大回撤","夏普比率","卡玛比率","索提诺比率","日胜率","日盈亏比","最大连续亏损","日VaR(95%)"]
    indicator_values = [
        f"{c.get('annualized_return',0):.2%}", f"{c.get('annualized_volatility',0):.2%}",
        f"{c.get('max_drawdown',0):.2%}", f"{c.get('sharpe_ratio',0):.2f}",
        f"{c.get('calmar_ratio',0):.2f}", f"{c.get('sortino_ratio',0):.2f}",
        f"{c.get('daily_win_rate',0):.1%}", f"{c.get('daily_pnl_ratio',0):.2f}",
        f"{c.get('max_consecutive_loss_days',0)}天", f"{c.get('var_95',0):.2%}",
    ]
    indicator_benchmarks = ["≥15%","≤20%","≤-20%","≥1.0","≥1.5","≥1.5","≥50%","≥1.5","≤7天",">-3%"]
    indicators = [(n, v, b, ie.get(n, "-") or "-") for n, v, b in zip(indicator_names, indicator_values, indicator_benchmarks)]
    story.append(_make_data_table(["指标名称","策略值","行业基准","评价说明"], indicators, col_widths=[80,60,55,265]))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("3.3 分年度绩效归因", S["h2"]))
    yearly_rows = [[str(y.get("year","")), f"{y.get('return',0):.2%}", f"{y.get('volatility',0):.2%}",
        f"{y.get('sharpe',0):.2f}", f"{y.get('max_drawdown',0):.2%}", y.get("rating","")] for y in yearly_list]
    if yearly_rows:
        story.append(_make_data_table(["年份","年度收益率","年化波动率","夏普比率","最大回撤","综合评级"], yearly_rows, col_widths=[60,80,80,70,80,90]))
    story.append(PageBreak())

    # ==================== 四、品种与板块分析 ====================
    variety_metrics = analysis.get("variety_metrics", [])
    if variety_metrics:
        story.append(Paragraph("四 品种与板块分析", S["h1"]))
        story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))
        if "variety_top" in charts:
            _chart_block(story, S, "4.1 品种盈亏排名", charts["variety_top"], "图4-1 盈利/亏损 TOP 10 品种", height=240)
        _render_markdown_text(story, _safe_text(content.get("variety_analysis")), S)
        if "sector_bar" in charts:
            _chart_block(story, S, "4.2 板块分析", charts["sector_bar"], "图4-2 板块收益与胜率-夏普散点图", height=240)
        _render_markdown_text(story, _safe_text(content.get("sector_analysis")), S)
        story.append(PageBreak())

    # ==================== 五、回撤风险 ====================
    story.append(Paragraph("五 回撤风险提示与处置建议", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))
    if "drawdown_risk" in charts:
        _chart_block(story, S, None, charts["drawdown_risk"], "图5-1 回撤走势分级与回撤幅度分布统计", height=310)
    story.append(Spacer(1, 5 * mm))
    _render_markdown_text(story, _safe_text(content.get("drawdown_analysis")), S)
    story.append(Paragraph("5.1 回撤天数分布统计", S["h2"]))
    dd_dist = analysis.get("drawdown_distribution", None)
    if dd_dist:
        dd_dist_rows = [[row.get("level",""), row.get("range",""), str(row.get("days",0)), f"{row.get('pct',0):.1f}%", row.get("desc","")] for row in dd_dist]
        story.append(_make_data_table(["风险级别","回撤区间","持续天数","占总交易日比","说明"], dd_dist_rows, col_widths=[60,70,55,70,205]))
        story.append(Spacer(1, 5 * mm))
    drawdown_events = analysis.get("drawdown_events", [])
    if drawdown_events:
        story.append(Paragraph("5.2 历次显著回撤明细与处置建议", S["h2"]))
        dd_rows = [[e.get("start",""), e.get("end",""), str(e.get("duration",0)), f"{e.get('depth',0):.2%}", e.get("level",""), e.get("suggestion","")] for e in drawdown_events]
        story.append(_make_data_table(["开始日期","结束日期","持续(天)","最大深度","风险级别","处置建议"], dd_rows, col_widths=[70,70,50,60,50,160]))
    story.append(PageBreak())

    # ==================== 六、每万元收益 ====================
    story.append(Paragraph("六 每万元每日收益率分析", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))
    if "per_10k" in charts:
        _chart_block(story, S, None, charts["per_10k"], "图6-1 每万元每日收益率", height=350)
    story.append(Paragraph("6.1 资金效率核心指标", S["h2"]))
    per10k_data = analysis.get("per_10k", {})
    if per10k_data:
        cap_stats = [("日均每万元收益",f"{per10k_data.get('daily_avg',0):.2f} 元/万"),("年化每万元收益",f"{per10k_data.get('annual',0):.0f} 元/万"),("累计每万元收益",f"{per10k_data.get('cumulative',0):.0f} 元/万"),("单日最大盈利",f"+{per10k_data.get('max_profit',0):.0f} 元/万"),("单日最大亏损",f"{per10k_data.get('max_loss',0):.0f} 元/万")]
        story.append(_make_data_table(["指标","数值"], [[k,v] for k,v in cap_stats], col_widths=[160,160]))
    _render_markdown_text(story, _safe_text(content.get("per_10k_analysis")), S)
    story.append(PageBreak())

    # ==================== 七、月度收益率热力图 ====================
    story.append(Paragraph("七 月度收益率热力图", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))
    if "heatmap" in charts:
        _chart_block(story, S, None, charts["heatmap"], "图7-1 月度收益率热力图（绿色=正收益，红色=负收益）", height=280)
    _render_markdown_text(story, _safe_text(content.get("heatmap_analysis")), S)
    story.append(PageBreak())

    # ==================== 八、滚动夏普 ====================
    story.append(Paragraph("八 滚动夏普比率分析", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))
    if "rolling_sharpe" in charts:
        _chart_block(story, S, None, charts["rolling_sharpe"], "图8-1 滚动夏普比率走势及色温图", height=350)
    story.append(Paragraph("8.1 核心统计指标", S["h2"]))
    rs120_data = analysis.get("rolling_sharpe_120", {})
    if rs120_data:
        sharpe_stats = [("全期夏普比率",f"{c.get('sharpe_ratio',0):.2f}"),("120日Sharpe均值",f"{rs120_data.get('mean',0):.2f}"),("最新120日Sharpe",f"{rs120_data.get('latest',0):.2f}"),("Sharpe>0占比",f"{rs120_data.get('positive_pct',0):.1f}%"),("Sharpe>1占比",f"{rs120_data.get('gt1_pct',0):.1f}%")]
        story.append(_make_data_table(["指标","数值"], [[k,v] for k,v in sharpe_stats], col_widths=[160,160]))
    _render_markdown_text(story, _safe_text(content.get("rolling_sharpe_analysis")), S)
    story.append(PageBreak())

    # ==================== 九、CTA策略对比 ====================
    story.append(Paragraph("九 与市场CTA策略同期表现对比", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))
    story.append(Paragraph("9.1 横向对比分析", S["h2"]))
    def _rank(val, avg, top, lower_better=False):
        if lower_better: return "优秀" if val <= top else ("中上" if val <= avg else "一般")
        return "优秀" if val >= top else ("中上" if val >= avg else "一般")
    cmp_rows = [
        ("累计收益率", f"{c.get('cumulative_return',0):.1%}", f"~{CTA_MARKET_AVG['累计收益率']:.0%}", f"~{CTA_TOP['累计收益率']:.0%}", _rank(c.get('cumulative_return',0), CTA_MARKET_AVG['累计收益率'], CTA_TOP['累计收益率'])),
        ("年化收益率", f"{c.get('annualized_return',0):.1%}", f"~{CTA_MARKET_AVG['年化收益率']:.0%}", f"~{CTA_TOP['年化收益率']:.0%}", _rank(c.get('annualized_return',0), CTA_MARKET_AVG['年化收益率'], CTA_TOP['年化收益率'])),
        ("最大回撤", f"{c.get('max_drawdown',0):.1%}", f"~{CTA_MARKET_AVG['最大回撤']:.0%}", f"~{CTA_TOP['最大回撤']:.0%}", _rank(c.get('max_drawdown',0), CTA_MARKET_AVG['最大回撤'], CTA_TOP['最大回撤'], True)),
        ("夏普比率", f"{c.get('sharpe_ratio',0):.2f}", f"~{CTA_MARKET_AVG['夏普比率']:.1f}", f"~{CTA_TOP['夏普比率']:.1f}", _rank(c.get('sharpe_ratio',0), CTA_MARKET_AVG['夏普比率'], CTA_TOP['夏普比率'])),
    ]
    story.append(_make_data_table(["对比维度",f"本策略({strategy_name})","CTA市场均值","头部CTA策略","综合排名"], cmp_rows, col_widths=[80,90,90,90,90]))
    story.append(Spacer(1, 5 * mm))
    _render_markdown_text(story, _safe_text(content.get("cta_comparison")), S)
    story.append(PageBreak())

    # ==================== 十、综合评价与结论 ====================
    story.append(Paragraph("十 综合评价与结论", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))
    story.append(Paragraph("10.1 总体评价", S["h2"]))
    years = period.get("years", 0)
    eval_dims = [
        ("绝对收益能力", _eval_stars(c.get('annualized_return',0), [0.05,0.10,0.15,0.25]), f"累计{c.get('cumulative_return',0):.1%}，年化{c.get('annualized_return',0):.1%}"),
        ("风险控制能力", _eval_stars(-c.get('max_drawdown',0), [0.05,0.10,0.15,0.20]), f"最大回撤{c.get('max_drawdown',0):.1%}，夏普{c.get('sharpe_ratio',0):.2f}"),
        ("稳定性与一致性", _eval_stars(c.get('sortino_ratio',0), [0.3,0.6,1.0,1.5]), f"索提诺比率{c.get('sortino_ratio',0):.2f}"),
        ("可持续运营能力", _eval_stars(years, [1,2,3,4]), f"{years:.1f}年运行，具备持续运营基础"),
    ]
    story.append(_make_data_table(["评价维度","评级","核心评价"], eval_dims, col_widths=[100,80,280]))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("10.2 结论与展望", S["h2"]))
    conclusion_text = _safe_text(content.get("conclusion"))
    if not conclusion_text:
        conclusion_text = f"{strategy_name}量化策略自{period.get('start','')}启动至今，历经约{years:.0f}年市场周期检验，累计净值增长{c.get('cumulative_return',0):.1%}，年化收益{c.get('annualized_return',0):.1%}，是一个值得持续跟踪的量化策略。"
    _render_markdown_text(story, conclusion_text, S)
    story.append(PageBreak())

    # ==================== 十一、策略改进建议（最后一章） ====================
    story.append(Paragraph("十一 策略改进建议", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_PRIMARY, spaceAfter=10))
    story.append(Paragraph("基于上述全面分析，我们从多个维度提出策略优化改进建议：", S["body"]))
    story.append(Spacer(1, 3 * mm))
    suggestions = content.get("suggestions", [])
    if isinstance(suggestions, str):
        suggestions = [s.strip() for s in suggestions.split("\n") if s.strip()]
    for i, sug in enumerate(suggestions, 1):
        if not isinstance(sug, str) or len(sug) < 5: continue
        title, body = f"11.{i}", sug
        for sep in ["——", "：", ":"]:
            if sep in sug:
                parts = sug.split(sep, 1)
                title, body = f"11.{i} {parts[0].strip()}", parts[1].strip()
                break
        story.append(Paragraph(title, S["h2"]))
        # 用 _render_markdown_text 渲染正文，支持长文本分段和加粗
        _render_markdown_text(story, body, S)
        story.append(Spacer(1, 5 * mm))

    story.append(Spacer(1, 15 * mm))
    story.append(Paragraph(
        f"本报告由量化分析系统基于策略历史数据自动生成 | "
        f"报告日期：{report_date} | 数据截止：{period.get('end', '')}",
        S["disclaimer"]))
    story.append(Paragraph(
        "报告中CTA市场基准数据基于公开行业数据估算，仅供参考，不作为投资决策依据",
        S["disclaimer"]))

    # ==================== 构建 PDF ====================
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        topMargin=30 * mm, bottomMargin=20 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
    )

    def on_page(canvas, doc_):
        _header_footer(canvas, doc_, strategy_name, report_date)

    def on_first_page(canvas, doc_):
        pass  # 封面无页眉页脚

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_page)
    return output_path


def _eval_stars(val, thresholds):
    """根据阈值列表返回星级"""
    stars = 1
    for t in thresholds:
        if val >= t:
            stars += 1
    stars = min(5, stars)
    return "★" * stars + "☆" * (5 - stars)
