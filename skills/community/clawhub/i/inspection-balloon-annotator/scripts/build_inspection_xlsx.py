# -*- coding: utf-8 -*-
"""Step 4: 生成检验表 Excel(内嵌气泡图 + 未注公差基准)。
用法: python build_inspection_xlsx.py <items.json> <ballooned.png> <out.xlsx>
        [--title "XX 尺寸与形位公差检验记录表"] [--no-embed]

items.json 结构:
{
  "title": "电磁阀尾座  尺寸与形位公差检验记录表",
  "info": [["零件名称","电磁阀尾座","图号","MEST-F800-18a"], ...],
  "items": [
    {"no":1,"view":"俯视图","item":"尺寸 19 ±0.1","basic":"19","upper":"+0.10",
     "lower":"-0.10","tol":"0.20","gauge":"数显卡尺","method":"图纸标注公差","level":"B"},
    ...
    {"no":"43","view":"其他","item":"外观质量", ...}
  ]
}
level: A=关键(红) / B=重要(黄) / C=一般(绿)
"""
import argparse, json, os, tempfile
from PIL import Image
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage

F_HDR   = Font(name='微软雅黑', size=10, bold=True, color='FFFFFF')
F_TITLE = Font(name='微软雅黑', size=16, bold=True, color='1F3864')
F_INFO  = Font(name='微软雅黑', size=10, bold=True)
F_TXT   = Font(name='微软雅黑', size=10)
F_SM    = Font(name='微软雅黑', size=9)
F_SEC   = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')
FILL_TITLE = PatternFill('solid', fgColor='D9E1F2')
FILL_HDR   = PatternFill('solid', fgColor='4472C4')
FILL_INFO  = PatternFill('solid', fgColor='F2F2F2')
FILL_A     = PatternFill('solid', fgColor='FFC7CE')
FILL_B     = PatternFill('solid', fgColor='FFEB9C')
FILL_C     = PatternFill('solid', fgColor='E2EFDA')
FILL_SEC   = PatternFill('solid', fgColor='7F7F7F')
thin = Side(style='thin', color='808080')
BORD = Border(left=thin, right=thin, top=thin, bottom=thin)
CEN = Alignment(horizontal='center', vertical='center', wrap_text=True)
LEFT = Alignment(horizontal='left', vertical='center', wrap_text=True)
HDRS = ["序号\n(气泡)","视图/剖视","检验项目(图纸标注)","基本尺寸","上偏差","下偏差",
        "公差带/公差值","检验量具·检具","检验方法·说明","重要度","实测值1","实测值2","实测值3","判定"]


def build(items, img_path, out, title, wb=None, embed_img=True):
    if wb is None:
        wb = Workbook()
        ws = wb.active
    else:
        ws = wb.create_sheet("检验记录表")
    ws.title = "检验记录表"
    ws.merge_cells('A1:N1'); ws['A1'] = title
    ws['A1'].font = F_TITLE; ws['A1'].fill = FILL_TITLE; ws['A1'].alignment = CEN
    ws.row_dimensions[1].height = 30

    r = 2
    for row in items.get("info", []):
        spans = [('A', 'B'), ('C', 'G'), ('H', 'I'), ('J', 'N')]
        for (c1, c2), v, islab in zip(spans, row, [True, False, True, False]):
            ws.merge_cells(f'{c1}{r}:{c2}{r}')
            cc = ws[f'{c1}{r}']; cc.value = v
            cc.font = F_INFO if islab else F_TXT
            cc.fill = FILL_INFO if islab else PatternFill('solid', fgColor='FFFFFF')
            cc.alignment = CEN
        for col in range(1, 15):
            ws.cell(r, col).border = BORD
        r += 1

    hr = r + 1
    for i, h in enumerate(HDRS, 1):
        cc = ws.cell(hr, i, h); cc.font = F_HDR; cc.fill = FILL_HDR; cc.alignment = CEN; cc.border = BORD
    ws.row_dimensions[hr].height = 40

    rr = hr + 1
    for d in items.get("items", []):
        vals = [d.get("no"), d.get("view"), d.get("item"), d.get("basic"), d.get("upper"),
                d.get("lower"), d.get("tol"), d.get("gauge"), d.get("method"), d.get("level"),
                "", "", "", ""]
        for i, v in enumerate(vals, 1):
            cc = ws.cell(rr, i, v)
            cc.font = F_TXT if i != 1 else F_INFO
            cc.alignment = CEN if i in (1,2,4,5,6,7,10,11,12,13,14) else LEFT
            cc.border = BORD
        lv = str(d.get("level", "C")).upper()[:1]
        ws.cell(rr, 10).fill = {'A': FILL_A, 'B': FILL_B, 'C': FILL_C}.get(lv, FILL_C)
        rr += 1

    rr += 1
    ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=14)
    cc = ws.cell(rr, 1, "检验结论：□ 合格    □ 让步接收    □ 不合格(退回)        检验员：____________   审核：____________   日期：____________")
    cc.font = F_INFO; cc.alignment = LEFT; cc.border = BORD
    ws.row_dimensions[rr].height = 26
    for i, w in enumerate([7,12,30,11,9,9,13,20,26,8,9,9,9,9], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = f'A{hr+1}'

    # Sheet2 气泡图
    ws2 = wb.create_sheet("标注图纸(气泡图)")
    ws2.cell(1, 1, title.replace("检验记录表", "") + "— 气泡标注图").font = F_TITLE
    ws2.merge_cells('A1:H1')
    ws2.cell(2, 1, "说明：图中红色编号气泡与《检验记录表》序号一一对应；气泡引线指向对应尺寸/公差标注。").font = F_SM
    ws2.merge_cells('A2:H2')
    if embed_img and img_path and os.path.exists(img_path):
        thumb = os.path.join(tempfile.gettempdir(), f"_balloon_embed_{os.getpid()}.png")
        im = Image.open(img_path)
        im.resize((2400, int(2400 * im.height / im.width)), Image.LANCZOS).save(thumb)
        ws2.add_image(XLImage(thumb), 'A4')
        ws2.column_dimensions['A'].width = 4
        ws2.row_dimensions[4].height = 900

    # Sheet3 未注公差基准
    ws3 = wb.create_sheet("未注公差基准")
    ws3.column_dimensions['A'].width = 22
    for c in 'BCDEFGH':
        ws3.column_dimensions[c].width = 12
    ws3.column_dimensions['H'].width = 16
    ws3.cell(1, 1, "未注公差基准值(依据图纸技术要求)").font = F_TITLE
    ws3.merge_cells('A1:H1')

    def sec(r0, text):
        ws3.merge_cells(start_row=r0, start_column=1, end_row=r0, end_column=8)
        cc = ws3.cell(r0, 1, text); cc.font = F_SEC; cc.fill = FILL_SEC; cc.alignment = LEFT
        return r0 + 1

    def table(r0, ttl, headers, rows):
        if ttl:
            ws3.merge_cells(start_row=r0, start_column=1, end_row=r0, end_column=len(headers))
            cc = ws3.cell(r0, 1, ttl); cc.font = F_INFO; cc.fill = FILL_INFO; cc.alignment = LEFT; cc.border = BORD
            r0 += 1
        for i, h in enumerate(headers, 1):
            cc = ws3.cell(r0, i, h); cc.font = F_HDR; cc.fill = FILL_HDR; cc.alignment = CEN; cc.border = BORD
        r0 += 1
        for rw in rows:
            for i, v in enumerate(rw, 1):
                cc = ws3.cell(r0, i, v); cc.font = F_TXT; cc.alignment = CEN; cc.border = BORD
            r0 += 1
        return r0 + 1

    r3 = 3
    r3 = sec(r3, "一、未注线性尺寸极限偏差  GB/T1804-2000 f级(精密)")
    r3 = table(r3, "", ["基本尺寸分段/mm","0.5~3",">3~6",">6~30",">30~120",">120~400",">400~1000"],
               [["极限偏差 ± /mm","0.05","0.05","0.1","0.15","0.2","0.3"]])
    r3 = sec(r3, "二、未注倒圆半径与倒角高度极限偏差  GB/T1804-2000 f级")
    r3 = table(r3, "", ["基本尺寸分段/mm","0.5~3",">3~6",">6~30",">30"],
               [["极限偏差 ± /mm","0.2","0.5","1","2"]])
    r3 = sec(r3, "三、未注角度尺寸极限偏差  GB/T1804-2000 f级")
    r3 = table(r3, "", ["角度短边长度/mm","≤10",">10~50",">50~120",">120~400",">400"],
               [["极限偏差","±1°","±30′","±20′","±10′","±5′"]])
    r3 = sec(r3, "四、未注形位公差值  GB/T1184-1996 H级")
    r3 = table(r3, "4.1 直线度、平面度 (单位 mm)",
               ["基本长度/mm","≤10",">10~30",">30~100",">100~300",">300~1000"],
               [["H级公差值","0.02","0.05","0.1","0.2","0.3"]])
    r3 = table(r3, "4.2 垂直度 / 对称度 (单位 mm)",
               ["基本长度/mm","≤100",">100~300",">300~1000",">1000"],
               [["垂直度 H","0.2","0.3","0.4","0.5"], ["对称度 H","0.5","0.6","0.8","1"]])
    r3 = table(r3, "4.3 圆跳动 (单位 mm)", ["等级","H","K","L"], [["公差值","0.1","0.2","0.5"]])

    explicit = items.get("explicit")
    if explicit:
        r3 = sec(r3, "五、图纸明确标注的尺寸/形位公差(优先于未注公差)")
        for rw in explicit:
            for i, v in enumerate(rw, 1):
                cc = ws3.cell(r3, i, v)
                cc.font = F_HDR if rw is explicit[0] else F_TXT
                cc.fill = FILL_HDR if rw is explicit[0] else PatternFill('solid', fgColor='FFFFFF')
                cc.alignment = CEN; cc.border = BORD
            r3 += 1

    if out:
        wb.save(out)
    return wb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items"); ap.add_argument("png"); ap.add_argument("out")
    ap.add_argument("--title", default=None)
    a = ap.parse_args()
    items = json.load(open(a.items, encoding="utf-8"))
    title = a.title or items.get("title", "尺寸与形位公差检验记录表")
    build(items, a.png, a.out, title)
    print("OK saved:", a.out)


if __name__ == "__main__":
    main()
