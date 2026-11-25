#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Markdown → Word（info-collect-v3 附带工具，也可单独用）。

支持：# / ## / ### 标题、段落、- 与 1. 列表、| 表格 |、> 引用、行内 **粗体**、
      行内 `代码`、```代码块```。

依赖：**仅 Python 标准库**（zipfile + xml）。本脚本直接生成符合 OOXML 规范的
      .docx 文件，不需要安装任何第三方库。原实现基于第三方 Word 库，此处为
      **等价简化实现**：标题层级、段落、列表、表格、粗体、引用、代码块等
      常规排版保持一致（表格为真表格，Word 中可继续编辑）。

用法：python3 scripts/md_to_docx.py report.md --out report.docx [--title "情报整理报告"]
"""
import argparse
import re
import zipfile

# ---------- OOXML 常量 ----------
NS_W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
XML_HEAD = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

BODY_SZ = 21            # 10.5 pt（半磅）
H1_SZ, H2_SZ, H3_SZ = 32, 26, 23
TBL_SZ = 19             # 9.5 pt
CODE_SZ = 18            # 9 pt
FONT_BODY = "宋体"
FONT_HEAD = "黑体"
FONT_MONO = "Consolas"

CONTENT_TYPES = XML_HEAD + (
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '</Types>'
)

ROOT_RELS = XML_HEAD + (
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '</Relationships>'
)

DOC_RELS = XML_HEAD + (
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '</Relationships>'
)


def styles_xml():
    def head_style(sid, name, lvl, size):
        return (
            '<w:style w:type="paragraph" w:styleId="%s"><w:name w:val="%s"/>'
            '<w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
            '<w:pPr><w:keepNext/><w:outlineLvl w:val="%d"/></w:pPr>'
            '<w:rPr><w:rFonts w:ascii="%s" w:hAnsi="%s" w:eastAsia="%s"/>'
            '<w:b/><w:bCs/><w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr></w:style>'
            % (sid, name, lvl, FONT_HEAD, FONT_HEAD, FONT_HEAD, size, size)
        )

    return XML_HEAD + (
        '<w:styles ' + NS_W + '>'
        '<w:docDefaults><w:rPrDefault><w:rPr>'
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="' + FONT_BODY + '" w:cs="Times New Roman"/>'
        '<w:sz w:val="21"/><w:szCs w:val="21"/>'
        '</w:rPr></w:rPrDefault>'
        '<w:pPrDefault><w:pPr><w:spacing w:after="80" w:line="288" w:lineRule="auto"/></w:pPr></w:pPrDefault>'
        '</w:docDefaults>'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
        + head_style("Heading1", "heading 1", 0, H1_SZ)
        + head_style("Heading2", "heading 2", 1, H2_SZ)
        + head_style("Heading3", "heading 3", 2, H3_SZ)
        + '<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/>'
          '<w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:ind w:left="240"/></w:pPr>'
          '<w:rPr><w:color w:val="595959"/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr></w:style>'
        + '<w:style w:type="paragraph" w:styleId="CodeBlock"><w:name w:val="Code Block"/>'
          '<w:basedOn w:val="Normal"/><w:qFormat/>'
          '<w:pPr><w:shd w:val="clear" w:color="auto" w:fill="F5F5F5"/><w:spacing w:after="0"/></w:pPr>'
          '<w:rPr><w:rFonts w:ascii="' + FONT_MONO + '" w:hAnsi="' + FONT_MONO + '" w:eastAsia="' + FONT_BODY + '"/>'
          '<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>'
        '</w:styles>'
    )


# ---------- 基础构件 ----------
def xml_escape(text):
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def _run(text, bold=False, size=BODY_SZ, font=None, italic=False):
    rpr = []
    if font:
        rpr.append('<w:rFonts w:ascii="%s" w:hAnsi="%s" w:eastAsia="%s" w:cs="%s"/>'
                   % (font, font, font, font))
    if bold:
        rpr.append("<w:b/><w:bCs/>")
    if italic:
        rpr.append("<w:i/><w:iCs/>")
    rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size))
    return '<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % ("".join(rpr), xml_escape(text))


INLINE_RE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`)")


def _runs(text, size=BODY_SZ, bold=False, font=None):
    """把行内 **粗体** 与 `代码` 拆成多个 run。"""
    out = []
    for seg in INLINE_RE.split(text):
        if not seg:
            continue
        if seg.startswith("**") and seg.endswith("**") and len(seg) > 4:
            out.append(_run(seg[2:-2], bold=True, size=size, font=font))
        elif seg.startswith("`") and seg.endswith("`") and len(seg) > 2:
            out.append(_run(seg[1:-1], size=CODE_SZ, font=FONT_MONO))
        else:
            out.append(_run(seg, bold=bold, size=size, font=font))
    return "".join(out)


def _para(content_xml, style=None, align=None, indent=None, after=None, before=None):
    ppr = []
    if style:
        ppr.append('<w:pStyle w:val="%s"/>' % style)
    if before is not None or after is not None:
        sp = []
        if before is not None:
            sp.append('w:before="%d"' % before)
        if after is not None:
            sp.append('w:after="%d"' % after)
        ppr.append("<w:spacing %s/>" % " ".join(sp))
    if indent:
        ppr.append('<w:ind w:left="%d" w:hanging="%d"/>' % indent)
    if align:
        ppr.append('<w:jc w:val="%s"/>' % align)
    ppr_xml = "<w:pPr>%s</w:pPr>" % "".join(ppr) if ppr else ""
    return "<w:p>%s%s</w:p>" % (ppr_xml, content_xml)


def _split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _table(rows):
    """真表格：首行表头加底纹，网格线为单线。"""
    ncols = max(len(r) for r in rows)
    borders = "".join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/>' % s
                      for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    xml = ['<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders>%s</w:tblBorders>'
           '<w:tblLayout w:type="autofit"/></w:tblPr>' % borders]
    xml.append("<w:tblGrid>%s</w:tblGrid>" % "".join('<w:gridCol w:w="1800"/>' for _ in range(ncols)))
    for ri, row in enumerate(rows):
        cells = []
        for ci in range(ncols):
            val = row[ci] if ci < len(row) else ""
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="EDEDED"/>' if ri == 0 else ""
            tcpr = ('<w:tcPr><w:tcW w:w="0" w:type="auto"/>%s<w:vAlign w:val="center"/></w:tcPr>' % shd)
            cells.append("<w:tc>%s%s</w:tc>" % (tcpr, _para(_runs(val, size=TBL_SZ, bold=(ri == 0)))))
        trpr = "<w:trPr><w:tblHeader/></w:trPr>" if ri == 0 else ""
        xml.append("<w:tr>%s%s</w:tr>" % (trpr, "".join(cells)))
    xml.append("</w:tbl>")
    return "".join(xml)


# ---------- Markdown 解析 ----------
def parse_md(lines):
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue

        if s.startswith("```"):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            blocks.append(("code", buf))
            continue

        if s.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|?$", lines[i + 1].strip()):
            rows = [_split_row(s)]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(_split_row(lines[i]))
                i += 1
            blocks.append(("table", rows))
            continue

        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            blocks.append(("h", (len(m.group(1)), m.group(2).strip())))
            i += 1
            continue

        if s.startswith(">"):
            blocks.append(("quote", s.lstrip(">").strip()))
            i += 1
            continue

        m = re.match(r"^([-*]|\d+\.)\s+(.*)$", s)
        if m:
            blocks.append(("li", (m.group(1), m.group(2).strip())))
            i += 1
            continue

        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            blocks.append(("hr", None))
            i += 1
            continue

        blocks.append(("p", s))
        i += 1
    return blocks


def render(blocks, title=None):
    body = []
    for kind, payload in blocks:
        if kind == "h":
            lvl, text = payload
            if lvl == 1:
                if title:
                    text = title
                body.append(_para(_runs(text, size=H1_SZ, bold=True, font=FONT_HEAD),
                                  style="Heading1", align="center", before=240, after=240))
            elif lvl == 2:
                body.append(_para(_runs(text, size=H2_SZ, bold=True, font=FONT_HEAD),
                                  style="Heading2", before=200, after=120))
            else:
                body.append(_para(_runs(text, size=H3_SZ, bold=True, font=FONT_HEAD),
                                  style="Heading3", before=160, after=100))
        elif kind == "p":
            body.append(_para(_runs(payload), after=80))
        elif kind == "li":
            marker, text = payload
            prefix = "• " if marker in ("-", "*") else marker + " "
            body.append(_para(_runs(prefix + text), indent=(420, 210), after=40))
        elif kind == "quote":
            body.append(_para(_runs(payload, size=TBL_SZ), style="Quote", after=80))
        elif kind == "code":
            for ln in payload:
                body.append(_para(_run(ln if ln else " ", size=CODE_SZ, font=FONT_MONO),
                                  style="CodeBlock", after=0))
            body.append(_para("", after=80))
        elif kind == "table":
            body.append(_table(payload))
            body.append(_para("", after=80))
        elif kind == "hr":
            body.append(_para("", after=80))
    return "".join(body)


def write_docx(path, body_xml, title):
    parts = {
        "[Content_Types].xml": CONTENT_TYPES,
        "_rels/.rels": ROOT_RELS,
        "word/document.xml": XML_HEAD + (
            '<w:document ' + NS_W + '><w:body>' + body_xml +
            '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"'
            ' w:header="851" w:footer="992" w:gutter="0"/></w:sectPr>'
            '</w:body></w:document>'),
        "word/_rels/document.xml.rels": DOC_RELS,
        "word/styles.xml": styles_xml(),
        "docProps/core.xml": XML_HEAD + (
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"'
            ' xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"'
            ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>' + xml_escape(title) + '</dc:title>'
            '<dc:creator>skill-runtime</dc:creator>'
            '<cp:lastModifiedBy>skill-runtime</cp:lastModifiedBy>'
            '</cp:coreProperties>'),
    }
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data.encode("utf-8"))


def main():
    ap = argparse.ArgumentParser(description="Markdown → Word（纯标准库实现，无需第三方依赖）")
    ap.add_argument("md", help="输入 Markdown 文件路径")
    ap.add_argument("--out", required=True, help="输出 .docx 文件路径")
    ap.add_argument("--title", help="覆盖文档一级标题（可选）")
    a = ap.parse_args()

    with open(a.md, encoding="utf-8") as f:
        lines = f.read().split("\n")
    body = render(parse_md(lines), a.title)
    write_docx(a.out, body, a.title or "情报整理报告")
    print(f"已生成 {a.out}")


if __name__ == "__main__":
    main()
