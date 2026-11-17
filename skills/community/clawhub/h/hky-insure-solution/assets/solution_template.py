# -*- coding: utf-8 -*-
"""
养老与传承风险解决方案 · 暖黄 docx 生成器（零第三方依赖，仅用 Python 标准库）

复用 hky-insure-risk-report 的「暖黄 1.0 版」配色。
替换顶部 DATA 字典为本客户内容，运行 `python solution_template.py`
即可产出 `养老与传承风险解决方案.docx`。

零依赖说明：部分运行环境无法安装 lxml / python-docx，故直接用
zipfile + xml.etree 构造 OOXML，保证 skill 在任意环境可独立运行。
"""

import os
import zipfile
import xml.etree.ElementTree as ET

# ----------------------------- 配色（暖黄 1.0 版） -----------------------------
C_PRIMARY = "A06A30"      # 主色：章节标题/表头/底线
C_TITLE = "8B5A2B"        # 深色主标题
C_ACCENT = "E07A30"       # 强调色：副标题/信息框左边线
C_BODY = "4A3525"         # 正文
C_GRAY = "8C7A6A"         # 暖灰：日期/小字
C_HEADER_FILL = "A06A30"  # 表头填充
C_ZEBRA = "FFF8F0"        # 斑马行
C_INFO_FILL = "FDF3E6"    # 信息框填充
FONT = "Microsoft YaHei"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XS = "http://www.w3.org/XML/1998/namespace"

ET.register_namespace("w", W)
ET.register_namespace("xml", "http://www.w3.org/XML/1998/namespace")

# ----------------------------- 底层 XML 助手 -----------------------------
def q(tag):
    return "{%s}%s" % (W, tag)

def A(**kwargs):
    return {q(k): str(v) for k, v in kwargs.items()}

def el(tag, attrs=None, text=None):
    e = ET.Element(q(tag))
    if attrs:
        for k, v in attrs.items():
            e.set(k, v)
    if text is not None:
        e.text = text
    return e

def run(text, bold=False, color=C_BODY, size=20, italic=False):
    r = el("r")
    rpr = el("rPr")
    rpr.append(el("rFonts", A(ascii=FONT, eastAsia=FONT, hAnsi=FONT)))
    if bold:
        rpr.append(el("b"))
    if italic:
        rpr.append(el("i"))
    rpr.append(el("color", A(val=color)))
    rpr.append(el("sz", A(val=str(size))))
    rpr.append(el("szCs", A(val=str(size))))
    r.append(rpr)
    t = el("t")
    t.text = text
    r.append(t)
    return r

def paragraph(runs, style=None, align=None, after=120):
    p = el("p")
    ppr = el("pPr")
    has = False
    if style:
        ppr.append(el("pStyle", A(val=style)))
        has = True
    if align:
        ppr.append(el("jc", A(val=align)))
        has = True
    if after is not None:
        ppr.append(el("spacing", A(after=str(after))))
        has = True
    if has:
        p.append(ppr)
    for rn in (runs or []):
        p.append(rn)
    return p

def heading(text, level=2):
    sizes = {1: 36, 2: 24, 3: 18}
    colors = {1: C_TITLE, 2: C_PRIMARY, 3: C_ACCENT}
    return paragraph([run(text, bold=True, color=colors.get(level, C_PRIMARY),
                          size=sizes.get(level, 24))], after=140)

def body_text(text, color=C_BODY, size=20, bold=False, align=None, after=100):
    return paragraph([run(text, color=color, size=size, bold=bold)], align=align, after=after)

def bullets(items, color=C_BODY, size=20):
    out = []
    for it in items:
        out.append(paragraph([run("● " + it, color=color, size=size)], after=60))
    return out

def page_break():
    p = el("p")
    r = el("r")
    r.append(el("br", A(type="page")))
    p.append(r)
    return p

def star(n):
    return "★" * max(0, min(5, n))

def cell(text, fill, color, bold, ncol):
    tc = el("tc")
    tcpr = el("tcPr")
    tcpr.append(el("tcW", A(w=str(int(5000 / ncol)), type="pct")))
    if fill:
        tcpr.append(el("shd", A(val="clear", color="auto", fill=fill)))
    tc.append(tcpr)
    tc.append(paragraph([run(text, bold=bold, color=color, size=18)], after=20))
    return tc

def table(headers, rows, zebra=True, header_fill=C_HEADER_FILL):
    ncol = max(1, len(headers))
    tbl = el("tbl")
    tblpr = el("tblPr")
    tblpr.append(el("tblStyle", A(val="TableGrid")))
    tblpr.append(el("tblW", A(w="5000", type="pct")))
    borders = el("tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        borders.append(el(edge, A(val="single", sz="4", space="0", color="auto")))
    tblpr.append(borders)
    tbl.append(tblpr)
    grid = el("tblGrid")
    for _ in range(ncol):
        grid.append(el("gridCol", A(w=str(int(9000 / ncol)))))
    tbl.append(grid)
    # 表头
    tr = el("tr")
    for h in headers:
        tr.append(cell(h, header_fill, "FFFFFF", True, ncol))
    tbl.append(tr)
    # 数据行
    for i, row in enumerate(rows):
        tr = el("tr")
        fill = C_ZEBRA if (zebra and i % 2 == 1) else None
        for val in row:
            tr.append(cell(val, fill, C_BODY, False, ncol))
        tbl.append(tr)
    return tbl

def info_box(title, lines):
    tc = el("tc")
    tcpr = el("tcPr")
    tcpr.append(el("tcW", A(w="5000", type="pct")))
    tcpr.append(el("shd", A(val="clear", color="auto", fill=C_INFO_FILL)))
    borders = el("tcBorders")
    borders.append(el("left", A(val="single", sz="24", space="0", color=C_ACCENT)))
    tcpr.append(borders)
    tc.append(tcpr)
    tc.append(paragraph([run(title, bold=True, color=C_ACCENT, size=18)], after=40))
    for ln in lines:
        tc.append(paragraph([run(ln, color=C_BODY, size=18)], after=40))
    tbl = el("tbl")
    tblpr = el("tblPr")
    tblpr.append(el("tblW", A(w="5000", type="pct")))
    tbl.append(tblpr)
    grid = el("tblGrid")
    grid.append(el("gridCol", A(w="9000")))
    tbl.append(grid)
    tr = el("tr")
    tr.append(tc)
    tbl.append(tr)
    return tbl

# ----------------------------- 组装文档 -----------------------------
def build(data):
    body = el("body")

    # 封面
    body.append(paragraph(
        [run(data["client"] + " · 养老与传承风险解决方案", bold=True, color=C_TITLE, size=36)],
        align="center", after=120))
    body.append(paragraph(
        [run(data.get("slogan", "守你的财富，护你的晚年，承你的心"), color=C_ACCENT, size=20)],
        align="center", after=120))
    body.append(paragraph(
        [run(data.get("salutation", "亲启"), bold=True, color=C_PRIMARY, size=24)],
        align="center", after=80))
    body.append(paragraph(
        [run(data.get("disclaimer",
                      "本报告仅供" + data["client"] + "个人参考使用，不构成具体投资或保险购买建议。"),
             color=C_GRAY, size=16)], align="center", after=60))
    body.append(paragraph(
        [run(data.get("date", "2026 年 8 月"), color=C_GRAY, size=16)], align="center"))
    body.append(page_break())

    # 关于本方案
    body.append(heading("关于本方案", 2))
    if data.get("basis"):
        body.append(body_text(data["basis"]))
    if data.get("structure"):
        body.append(body_text("方案结构：" + data["structure"]))
    if data.get("conclusion"):
        body.append(info_box("核心结论", [data["conclusion"]]))
    body.append(page_break())

    # 一、健康状况更新
    body.append(heading("一、健康状况更新（沟通确认）", 2))
    if data.get("health_note"):
        body.append(body_text(data["health_note"]))
    if data.get("health_table"):
        body.append(table(data["health_table"][0], data["health_table"][1]))
    if data.get("health_advice"):
        body.append(body_text("投保建议：" + data["health_advice"]))
    body.append(page_break())

    # 解决方案一~四（人·权·财）
    nums = ["二", "三", "四", "五"]
    sub = ["一", "二", "三", "四"]
    for i, sol in enumerate(data.get("solutions", [])):
        title = "%s、解决方案%s：%s" % (nums[i], sub[i], sol["title"])
        if sol.get("tag"):
            title += "【%s】" % sol["tag"]
        body.append(heading(title, 2))
        if sol.get("gap"):
            body.append(body_text("（一）现状与缺口", color=C_ACCENT, size=18, bold=True))
            body.append(table(sol["gap"][0], sol["gap"][1]))
        if sol.get("direction"):
            body.append(body_text("（二）解决方向", color=C_ACCENT, size=18, bold=True))
            body.append(table(sol["direction"][0], sol["direction"][1]))
        if sol.get("details"):
            body.append(body_text("（三）沟通确认的关键细节", color=C_ACCENT, size=18, bold=True))
            for p in bullets(sol["details"]):
                body.append(p)
        if sol.get("next"):
            body.append(info_box("下一步行动", [sol["next"]]))
        body.append(page_break())

    # 条件章节（按需）
    for cond in data.get("conditional", []):
        body.append(heading(cond["title"], 2))
        if cond.get("body"):
            body.append(body_text(cond["body"]))
        if cond.get("bullets"):
            for p in bullets(cond["bullets"]):
                body.append(p)
        body.append(page_break())

    # 风险—解决方案对照总表
    body.append(heading("风险—解决方案对照总表", 2))
    if data.get("compare"):
        body.append(table(data["compare"][0], data["compare"][1]))
    body.append(page_break())

    # 行动优先级与时间轴
    body.append(heading("行动优先级与时间轴", 2))
    if data.get("timeline"):
        body.append(table(data["timeline"][0], data["timeline"][1]))
    body.append(page_break())

    # 保险产品配置计划（预留页）
    body.append(heading("九、保险产品配置计划（预留页）", 2))
    body.append(body_text(
        "说明：以下页面为产品计划预留区，在完成产品筛选和演示后，由顾问填入具体产品名称、"
        "保额、保费、起领金额等详细信息。客户签字确认后作为正式配置记录。本次仅列类别与空白表，不填具体产品。"))
    for prod in data.get("products", []):
        body.append(body_text(prod["name"], bold=True, color=C_PRIMARY, size=18))
        headers = prod["headers"]
        blank = [["" for _ in headers] for _ in range(prod.get("blank_rows", 1))]
        body.append(table(headers, blank))
    body.append(page_break())

    # 结语 + 落款
    body.append(heading("十、结语", 2))
    if data.get("ending"):
        for p in bullets(data["ending"]):
            body.append(p)
    body.append(paragraph([run("敬呈", color=C_BODY, size=20)], after=40))
    body.append(paragraph([run(data.get("date", "2026 年 8 月"), color=C_GRAY, size=16)], after=40))
    if data.get("adviser"):
        body.append(paragraph([run(data["adviser"] + " 敬呈", bold=True, color=C_PRIMARY, size=18)]))

    # 页面设置
    sect = el("sectPr")
    sect.append(el("pgSz", A(w="11906", h="16838")))
    sect.append(el("pgMar", A(top="1134", right="1134", bottom="1134", left="1134",
                                 header="720", footer="720", gutter="0")))
    body.append(sect)

    doc = el("document")
    doc.append(body)
    return doc

# ----------------------------- 静态包部件 -----------------------------
CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''

RELS_ROOT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Microsoft YaHei" w:eastAsia="Microsoft YaHei" w:hAnsi="Microsoft YaHei"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders>
<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
</w:tblBorders></w:tblPr></w:style>
</w:styles>'''

CORE = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>养老与传承风险解决方案</dc:title>
<dc:creator>清流计划</dc:creator>
<dcterms:created xsi:type="dcterms:W3CDTF">2026-08-01T00:00:00Z</dcterms:created>
<dcterms:modified xsi:type="dcterms:W3CDTF">2026-08-01T00:00:00Z</dcterms:modified>
</cp:coreProperties>'''

APP = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<Application>Microsoft Office Word</Application>
</Properties>'''

def write_docx(doc_element, out_path):
    xml = ET.tostring(doc_element, encoding="unicode")
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + xml
    parts = {
        "[Content_Types].xml": CONTENT_TYPES,
        "_rels/.rels": RELS_ROOT,
        "word/document.xml": xml,
        "word/styles.xml": STYLES,
        "word/_rels/document.xml.rels": DOC_RELS,
        "docProps/core.xml": CORE,
        "docProps/app.xml": APP,
    }
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, content in parts.items():
            data = content.encode("utf-8") if isinstance(content, str) else content
            z.writestr(name, data)
    return out_path

# ----------------------------- 示例 DATA（替换为本客户内容） -----------------------------
DATA = {
    "client": "示例女士",
    "slogan": "守你的财富，护你的晚年，承你的心",
    "salutation": "亲启",
    "disclaimer": "本报告仅供示例女士个人参考使用，不构成具体投资或保险购买建议。",
    "date": "2026 年 8 月",
    "adviser": "清流计划",
    "basis": "本方案在首次深度面谈与《第一版报告信息补充》的基础上编制，是一份由风险分析报告延伸出的行动指南。方案聚焦于如何一步步解决已识别的风险，而非停留在风险描述层面。",
    "structure": "① 医疗品质保障 ② 养老现金流方案 ③ 应急保值优化 ④ 传承与监护安排 ⑤ 保险产品配置计划（预留，待确认后填入）",
    "conclusion": "当前最关键的行动是——先补全健康保障（重疾险重投 + 中高端医疗），同时落地养老年金方案。",
    "health_note": "以下健康信息将直接影响投保选择和健康告知，须在投保前如实核对。",
    "health_table": [
        ["检查项目", "结果", "风险评估", "对保险的影响"],
        ["高血脂", "已知指标，经治疗后恢复正常", "低-中度", "须如实告知；多数重疾/医疗可承保"],
        ["血管局部斑块/轻度狭窄", "检出，有遗传倾向，已治疗", "低-中度", "须告知；建议投保前做预核保"],
        ["家族病史", "高血脂、心脑血管病", "中（遗传倾向）", "整体核保更严格，宜尽早投保"],
    ],
    "health_advice": "整体健康状况可控，仍处投保黄金窗口。主要关注高血脂与血管斑块的告知方式，建议在投保前先做「预核保」。",
    "solutions": [
        {
            "title": "医疗品质保障", "tag": "最优先",
            "gap": [["保障层级", "具体情况", "覆盖范围", "缺口"],
                    ["社保医保", "含长护险", "普通部基础医疗", "DRG 后自费增多"],
                    ["重疾险", "曾被误导退保，当前无", "—", "★ 缺口：无定额给付"]],
            "direction": [["工具", "作用", "操作建议"],
                          ["重疾险（重投）", "重大疾病一次性定额给付", "尽快重投，趁窗口期"],
                          ["中高端医疗险", "严重疾病可入特需/国际部", "对比产品，优先预核保"]],
            "details": ["重疾 vs 医疗：重疾为一次性给付，与医疗险报销不重复。",
                        "DRG 下：院外康复、护理、收入中断不报销，正是重疾险价值。",
                        "0 免赔：可报销医保剩余部分，填补小额自费缺口。"],
            "next": "提交健康资料 → 确认承保条件 → 签单。",
        },
        {
            "title": "养老现金流方案", "tag": "第二优先",
            "gap": [["维度", "现状", "建议", "判断"],
                    ["社保替代率", "仅靠社保，替代率有限", "转职工社保", "仍须补充商业养老金"]],
            "direction": [["笔钱", "金额", "工具类型", "特点"],
                          ["① 养老年金", "150 万", "养老年金（固定为主）", "60/65 岁起月领≥1 万"],
                          ["② 增额终身寿", "50 万", "增额终身寿险", "减保领取，应急储备"]],
            "details": ["年金核心价值不是收益率最高，而是活多久领多久 + 按月到账 + 心理安全感。",
                        "利率窗口提示：普通型预定利率上限已降至 2.0%。"],
            "next": "出具产品计划书演示，客户决策后配置。",
        },
        {
            "title": "应急保值与存量优化",
            "gap": [["工具", "判断", "建议定位"],
                    ["银行存款/理财", "灵活性好", "保持少量现金应急"],
                    ["增额终身寿", "锁定+减保", "应急储备主力"]],
            "direction": [["工具", "判断", "建议定位"],
                          ["年金", "强制储蓄+终身", "养老现金流底盘"]],
            "details": ["资源优先向健康险和年金倾斜，存量优化随信托架构确定后统筹。"],
            "next": "待信托架构确定后统筹存量。",
        },
        {
            "title": "传承与监护安排",
            "gap": [["家庭成员", "法律身份与风险", "遗嘱/隔离安排"],
                    ["父亲", "第一顺序法定继承人", "立遗嘱排除父亲"],
                    ["本人", "资金决策人", "立遗嘱指定流向+意定监护"]],
            "direction": [["安排", "作用", "操作建议"],
                          ["遗嘱", "锁死资产流向", "尽早订立并公证"],
                          ["意定监护", "补监护真空", "先建认知，后期敲定"]],
            "details": ["关系断联 ≠ 法律关系消失，须用遗嘱锁死流向。",
                        "意定监护可后期再做，先建立认知。"],
            "next": "推进遗嘱订立，意定监护后期安排。",
        },
    ],
    "conditional": [
        {"title": "六、港险规划结论",
         "body": "从资金使用上看，这笔钱的规划目的不是增值多少，而是确定性的现金流。",
         "bullets": ["客户无外币使用场景，港险复利优势不明显。",
                     "结论：本次不建议通过港险规划，资金在国内做好稳定担保。"]},
    ],
    "compare": [
        ["序号", "风险", "紧迫度", "解决方案", "状态"],
        ["1", "重疾退保缺口", star(5), "重疾险重投 + 中高端医疗", "最紧迫·待执行"],
        ["2", "200 万拆分执行", star(4), "150 万年金 + 50 万增额寿", "方向明确"],
        ["3", "遗嘱/继承真空", star(3), "立遗嘱排除父亲", "待安排"],
        ["4", "港险错配", star(1), "不做港险，国内稳定担保", "已收敛"],
    ],
    "timeline": [
        ["时间", "行动", "负责方", "备注"],
        ["近期（本月内）", "① 重疾险重投核保 ② 中高端医疗预核保", "协助", "健康保障是地基"],
        ["短期（1–2 月）", "200 万落地 + 社保转职工", "出具计划书", "年金建议生日前配完"],
        ["中期（3–6 月）", "婚前财产隔离 + 意定监护认知", "法务+顾问", "不急于敲定"],
        ["长期（年度复盘）", "产品利益复盘 + 信托架构评估", "定期回访", "长期跟踪"],
    ],
    "products": [
        {"name": "产品一：健康保障（重疾险 + 中高端医疗）",
         "headers": ["被保人", "保障计划", "保险期间", "交费期间", "保障额度", "首年保费"],
         "blank_rows": 1},
        {"name": "产品二：养老年金（60/65 岁起领）",
         "headers": ["被保人", "保障计划", "保险期间", "交费期间", "保障额度", "首年保费"],
         "blank_rows": 1},
        {"name": "产品三：增额终身寿（应急储备）",
         "headers": ["被保人", "保障计划", "保险期间", "交费期间", "保障额度", "首年保费"],
         "blank_rows": 1},
    ],
    "ending": ["医疗：不追求最贵，但要在关键时刻「有选择权」。",
               "养老金：不仅是补缺口，而是让退休生活有品质、有尊严。",
               "应急：已经有了准备，不需要过度配置。",
               "传承：把资产流向用遗嘱锁死，不给法定继承留漏洞。",
               "监护：认知先行，后期再把决策权交给信任的人。"],
}

# ----------------------------- 入口 -----------------------------
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "养老与传承风险解决方案.docx")
    doc = build(DATA)
    write_docx(doc, out)
    print("已生成：", out)
