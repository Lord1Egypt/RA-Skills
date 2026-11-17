# -*- coding: utf-8 -*-
"""ZHC JSON 桥后端 BRIDGE-1.0

形态：常驻进程，一行一报文。
  stdin  每行一个请求 JSON：{"版本":"1.0","模块":"表","方法":"导出csv","参数":{...}}
  stdout 每行一个响应 JSON：{"成功":true,"结果":...} 或 {"成功":false,"错误":{"码":"B003","信息":"..."}}

铁律：本进程只做「结构化 IR 落地」，不参与编译，不影响 .zc → exe 链路。
缺依赖不算崩溃，按 B003 回错，让 ZHC 侧走降级路径。
"""
import io
import json
import os
import sys
import traceback

版本 = "1.0"
协议版本 = "1.0"


# ---------------- 响应构造 ----------------
def ok(结果):
    return {"成功": True, "结果": 结果}


def err(码, 信息):
    return {"成功": False, "错误": {"码": 码, "信息": 信息}}


# ---------------- 表 IR 校验 ----------------
def _取表(参数):
    """从参数里取表 IR，并做白名单校验；不合格返回 (None, 错误响应)。"""
    表 = 参数.get("表")
    if not isinstance(表, dict):
        return None, err("B004", "参数校验失败：缺少 表")
    列 = 表.get("列")
    行 = 表.get("行")
    if not isinstance(列, list) or not isinstance(行, list):
        return None, err("B004", "参数校验失败：表 必须含 列 与 行 两个数组")
    列名 = []
    for c in 列:
        if not isinstance(c, dict) or "名" not in c or "类型" not in c:
            return None, err("B004", "参数校验失败：列元素必须含 名 与 类型")
        列名.append(str(c["名"]))
    for r in 行:
        if not isinstance(r, list):
            return None, err("B004", "参数校验失败：行元素必须是数组")
        if len(r) != len(列名):
            return None, err("B004", "参数校验失败：某行元素个数与列数不一致")
    return (列名, [c.get("类型") for c in 列], 行), None


def _取路径(参数, 默认后缀):
    路径 = 参数.get("路径")
    if not 路径:
        return None, err("B004", "参数校验失败：缺少 路径")
    路径 = os.path.abspath(str(路径))
    目录 = os.path.dirname(路径)
    if 目录 and not os.path.isdir(目录):
        try:
            os.makedirs(目录, exist_ok=True)
        except OSError as e:
            return None, err("B005", "写盘失败：目录不可创建（%s）" % e)
    if not os.path.splitext(路径)[1]:
        路径 += 默认后缀
    return 路径, None


def _查可写(路径):
    """目标不可写时提前报 B005，不让 open 抛到外层。"""
    目录 = os.path.dirname(路径) or "."
    if not os.access(目录, os.W_OK):
        return err("B005", "写盘失败：目录只读（%s）" % 目录)
    if os.path.exists(路径) and not os.access(路径, os.W_OK):
        return err("B005", "写盘失败：文件只读（%s）" % 路径)
    return None


def _单元文本(v):
    """产物里的单元格文本口径：空→""，布尔→true/false（与 JSON 一致，
    否则 csv 会被 python 写成 True/False，反向读取就比对不上）。"""
    if v is None:
        return ""
    if v is True:
        return "true"
    if v is False:
        return "false"
    return str(v)


# ---------------- 方法：表 ----------------
def 表_导出csv(参数):
    解, e = _取表(参数)
    if e:
        return e
    列名, 类型, 行 = 解
    路径, e = _取路径(参数, ".csv")
    if e:
        return e
    e = _查可写(路径)
    if e:
        return e
    import csv
    try:
        with io.open(路径, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(列名)
            for r in 行:
                w.writerow([_单元文本(v) for v in r])
    except OSError as ex:
        return err("B005", "写盘失败：%s" % ex)
    return ok({"路径": 路径, "行数": len(行), "列数": len(列名), "字节": os.path.getsize(路径)})


def 表_导出xlsx(参数):
    """xlsx 一律用标准库 zipfile 直写 OOXML 最小集，不依赖 openpyxl。
    理由：桥是可选能力，越少外部依赖，降级触发面越小；本机断网也能出产物。"""
    解, e = _取表(参数)
    if e:
        return e
    列名, 类型, 行 = 解
    路径, e = _取路径(参数, ".xlsx")
    if e:
        return e
    e = _查可写(路径)
    if e:
        return e
    try:
        _写xlsx(路径, 列名, 类型, 行, str(参数.get("工作表") or "数据"))
    except OSError as ex:
        return err("B005", "写盘失败：%s" % ex)
    return ok({"路径": 路径, "行数": len(行), "列数": len(列名), "字节": os.path.getsize(路径)})


def _列号(idx):
    """0 -> A, 25 -> Z, 26 -> AA"""
    s = ""
    idx += 1
    while idx:
        idx, r = divmod(idx - 1, 26)
        s = chr(65 + r) + s
    return s


def _xesc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def _xlsx单元格(ref, v, 类型):
    if v is None or v == "":
        return ""
    t = str(类型 or "文本")
    if t == "逻辑":
        try:
            b = 1 if (v is True or str(v).lower() in ("真", "true", "1")) else 0
        except Exception:
            b = 0
        return '<c r="%s" t="b"><v>%d</v></c>' % (ref, b)
    if t in ("整数", "浮点"):
        try:
            num = float(v) if t == "浮点" else int(v)
        except (TypeError, ValueError):
            return '<c r="%s" t="inlineStr"><is><t>%s</t></is></c>' % (ref, _xesc(v))
        if t == "浮点":
            return '<c r="%s"><v>%s</v></c>' % (ref, repr(float(v)))
        return '<c r="%s"><v>%d</v></c>' % (ref, num)
    return '<c r="%s" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, _xesc(v))


def _写xlsx(路径, 列名, 类型, 行, 表名):
    import zipfile
    rows = []
    rows.append("<row r=\"1\">" + "".join(
        _xlsx单元格(_列号(i) + "1", n, "文本") for i, n in enumerate(列名)) + "</row>")
    for ri, r in enumerate(行, start=2):
        cells = []
        for ci, v in enumerate(r):
            cells.append(_xlsx单元格(_列号(ci) + str(ri), v, 类型[ci] if ci < len(类型) else "文本"))
        rows.append('<row r="%d">%s</row>' % (ri, "".join(cells)))
    sheet = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
             '<sheetData>%s</sheetData></worksheet>' % "".join(rows))
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
          '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
          '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>')
    wb = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
          '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          '<sheets><sheet name="%s" sheetId="1" r:id="rId1"/></sheets></workbook>' % _xesc(表名[:31]))
    wbrels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
              '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
              '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
              '</Relationships>')
    with zipfile.ZipFile(路径, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", wb)
        z.writestr("xl/_rels/workbook.xml.rels", wbrels)
        z.writestr("xl/worksheets/sheet1.xml", sheet)


# ---------------- 方法：文档 ----------------
def 文档_导出docx(参数):
    """docx 同样零第三方依赖：zipfile 直写 OOXML 最小集（段落 + 表格）。"""
    解, e = _取表(参数)
    if e:
        return e
    列名, 类型, 行 = 解
    路径, e = _取路径(参数, ".docx")
    if e:
        return e
    e = _查可写(路径)
    if e:
        return e
    try:
        _写docx(路径, 参数.get("标题"), 参数.get("段落") or [], 列名, 行)
    except OSError as ex:
        return err("B005", "写盘失败：%s" % ex)
    return ok({"路径": 路径, "行数": len(行), "列数": len(列名), "字节": os.path.getsize(路径)})


def _wesc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def _w段(text, 加粗=False, 字号半磅=None):
    rpr = ""
    if 加粗 or 字号半磅:
        rpr = "<w:rPr>" + ("<w:b/>" if 加粗 else "")
        if 字号半磅:
            rpr += '<w:sz w:val="%d"/>' % 字号半磅
        rpr += "</w:rPr>"
    return ('<w:p><w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>' % (rpr, _wesc(text)))


def _w单元格(text, 加粗=False):
    return "<w:tc><w:p><w:r>%s<w:t xml:space=\"preserve\">%s</w:t></w:r></w:p></w:tc>" % (
        "<w:rPr><w:b/></w:rPr>" if 加粗 else "", _wesc(text))


def _写docx(路径, 标题, 段落, 列名, 行):
    import zipfile
    body = []
    if 标题:
        body.append(_w段(标题, 加粗=True, 字号半磅=32))
    for p in 段落:
        body.append(_w段(p))
    if 列名:
        borders = ('<w:tblPr><w:tblBorders>'
                   + "".join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="auto"/>' % k
                             for k in ("top", "left", "bottom", "right", "insideH", "insideV"))
                   + '</w:tblBorders></w:tblPr>')
        trs = ["<w:tr>" + "".join(_w单元格(n, 加粗=True) for n in 列名) + "</w:tr>"]
        for r in 行:
            trs.append("<w:tr>" + "".join(_w单元格(_单元文本(v)) for v in r) + "</w:tr>")
        body.append("<w:tbl>" + borders + "".join(trs) + "</w:tbl>")
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           '<w:body>%s<w:sectPr/></w:body></w:document>' % "".join(body))
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>')
    with zipfile.ZipFile(路径, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)


# ---------------- 方法：页面 ----------------
def 页面_导出html(参数):
    """响应式静态页：只用流体排版，不写像素断点，导出物不含 script。"""
    解, e = _取表(参数)
    if e:
        return e
    列名, 类型, 行 = 解
    路径, e = _取路径(参数, ".html")
    if e:
        return e
    e = _查可写(路径)
    if e:
        return e
    标题 = str(参数.get("标题") or "ZHC 数据页")
    esc = lambda s: (str(s).replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;").replace('"', "&quot;"))
    头 = "".join("<th>%s</th>" % esc(n) for n in 列名)
    体 = []
    for r in 行:
        体.append("<tr>" + "".join("<td>%s</td>" % esc(_单元文本(v)) for v in r) + "</tr>")
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>
:root{--fg:#1c1c1e;--bg:#fff;--line:#d8d8dc;--head:#f4f4f6}
*{box-sizing:border-box}
body{margin:0;padding:clamp(1rem,3vw,2.5rem);font:clamp(0.95rem,1.6vw,1.05rem)/1.6 system-ui,"Microsoft YaHei",sans-serif;color:var(--fg);background:var(--bg)}
h1{font-size:clamp(1.4rem,3.2vw,2.1rem);margin:0 0 1rem}
.wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%%;min-width:min(100%%,32rem)}
th,td{border:1px solid var(--line);padding:clamp(.4rem,1vw,.7rem);text-align:left}
th{background:var(--head);font-weight:600;position:sticky;top:0}
tbody tr:nth-child(even){background:#fafafb}
</style>
</head>
<body>
<h1>%s</h1>
<div class="wrap">
<table>
<thead><tr>%s</tr></thead>
<tbody>%s</tbody>
</table>
</div>
</body>
</html>
""" % (esc(标题), esc(标题), 头, "".join(体))
    try:
        io.open(路径, "w", encoding="utf-8", newline="\n").write(html)
    except OSError as ex:
        return err("B005", "写盘失败：%s" % ex)
    return ok({"路径": 路径, "行数": len(行), "列数": len(列名), "字节": os.path.getsize(路径)})


def 桥_版本(参数):
    return ok({"协议": 协议版本, "实现": "python", "Python": sys.version.split()[0],
                   "第三方依赖": 0, "产物格式": sorted({m + "." + f for (m, f) in 方法表})})


# ---------------- 注册表 ----------------
方法表 = {
    ("表", "导出csv"): 表_导出csv,
    ("表", "导出xlsx"): 表_导出xlsx,
    ("文档", "导出docx"): 文档_导出docx,
    ("页面", "导出html"): 页面_导出html,
    ("桥", "版本"): 桥_版本,
}


def 处理(请求):
    if not isinstance(请求, dict):
        return err("B002", "报文非法：请求必须是 JSON 对象")
    if str(请求.get("版本") or "") != 协议版本:
        return err("B002", "报文非法：版本必须是 %s" % 协议版本)
    模块 = str(请求.get("模块") or "")
    方法 = str(请求.get("方法") or "")
    参数 = 请求.get("参数")
    if 参数 is None:
        参数 = {}
    if not isinstance(参数, dict):
        return err("B004", "参数校验失败：参数必须是 JSON 对象")
    fn = 方法表.get((模块, 方法))
    if fn is None:
        return err("B001", "后端不存在：%s.%s" % (模块, 方法))
    try:
        return fn(参数)
    except Exception as ex:  # 后端内部异常一律转成响应，不允许把栈打到 stdout
        sys.stderr.write(traceback.format_exc())
        return err("B005", "写盘失败：后端异常（%s）" % ex)


def main():
    # 一律二进制按行读写，避免 Windows 文本模式把 \r\n 或 \x1a 当结束符
    inp = sys.stdin.buffer
    out = sys.stdout.buffer
    for raw in inp:
        line = raw.strip()
        if not line:
            continue
        try:
            # 用 utf-8-sig：上游偶尔带 BOM（PowerShell 管道、记事本另存），不该因此判报文非法
            请求 = json.loads(line.decode("utf-8-sig"))
        except ValueError as ex:
            响应 = err("B002", "报文非法：%s" % ex)
        else:
            响应 = 处理(请求)
        out.write((json.dumps(响应, ensure_ascii=False) + "\n").encode("utf-8"))
        out.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
