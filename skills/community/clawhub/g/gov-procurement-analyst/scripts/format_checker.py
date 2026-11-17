#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标书格式合规检查 · 10 项扫描（16.9，v5.5 扩容）

扫描项：
  1 页眉页脚  2 字体字号  3 页边距  4 目录结构  5 页码连续
  6 图表编号  7 行距段落  8 密封要求  9 签字盖章  10 投标函格式

依赖：python-docx（未安装时降级为「文本清单式检查」，输出 10 项待人工核对清单）

用法：
  python format_checker.py <标书.docx> [--rules rules.json] [--json]
"""

import argparse
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CHECK_ITEMS = [
    (1, "页眉页脚", "一般"),
    (2, "字体字号", "一般"),
    (3, "页边距", "一般"),
    (4, "目录结构", "低"),
    (5, "页码连续", "低"),
    (6, "图表编号", "低"),
    (7, "行距段落", "一般"),
    (8, "密封要求", "高"),
    (9, "签字盖章", "高"),
    (10, "投标函格式", "高"),
]

DEFAULT_RULES = {
    "font_name": "仿宋_GB2312",
    "font_size_pt": 16.0,
    "margin_top_cm": 2.54,
    "margin_bottom_cm": 2.54,
    "margin_left_cm": 3.0,
    "margin_right_cm": 2.0,
    "line_spacing": 1.5,
    "require_page_number": True,
    "require_toc": True,
}


def try_import_docx():
    try:
        import docx  # type: ignore

        return docx
    except Exception:
        return None


def fallback_check(doc_path, rules):
    """无 python-docx 时：输出 10 项待人工核对清单。"""
    results = []
    for no, name, risk in CHECK_ITEMS:
        results.append({
            "no": no, "item": name, "risk": risk, "state": "warn",
            "location": "全文", "current": "未自动检测（缺 python-docx）",
            "expected": "按招标文件格式要求人工核对",
            "note": "安装 python-docx 后可自动扫描：发送「安装python-docx」",
        })
    return results, False


def check_docx(doc_path, rules):
    docx = try_import_docx()
    if docx is None:
        return fallback_check(doc_path, rules)
    doc = docx.Document(doc_path)
    results = []

    def add(no, state, location, current, expected, note=""):
        item = next(n for n in CHECK_ITEMS if n[0] == no)
        results.append({"no": no, "item": item[1], "risk": item[2], "state": state,
                        "location": location, "current": current, "expected": expected, "note": note})

    # 1 页眉页脚
    try:
        headers = []
        for sec in doc.sections:
            headers.extend(p.text.strip() for p in sec.header.paragraphs if p.text.strip())
        if headers:
            add(1, "pass", "所有节页眉", "、".join(headers[:3]), "与招标文件指定一致")
        else:
            add(1, "warn", "所有节页眉", "未设置页眉", "按招标文件要求设置", "未明确要求时可不设")
    except Exception as exc:  # noqa: BLE001
        add(1, "warn", "页眉", "解析失败：%s" % exc, "人工核对")

    # 2 字体字号
    bad_fonts, bad_sizes = [], []
    for p in doc.paragraphs:
        for r in p.runs:
            if not r.text.strip():
                continue
            if r.font.name and r.font.name != rules["font_name"]:
                bad_fonts.append(r.font.name)
            if r.font.size and abs(r.font.size.pt - rules["font_size_pt"]) > 0.5:
                bad_sizes.append("%.1f" % r.font.size.pt)
    if not bad_fonts and not bad_sizes:
        add(2, "pass", "正文 run", "字体/字号统一", "仿宋_GB2312 三号（16pt）")
    else:
        add(2, "fail", "正文部分段落",
            "异常字体 %s；异常字号 %s" % (sorted(set(bad_fonts))[:3] or "-", sorted(set(bad_sizes))[:3] or "-"),
            "%s 三号（16pt）" % rules["font_name"])

    # 3 页边距
    try:
        sec = doc.sections[0]
        top = sec.top_margin.cm
        left = sec.left_margin.cm
        problems = []
        if abs(top - rules["margin_top_cm"]) > 0.05:
            problems.append("上边距 %.2fcm" % top)
        if abs(left - rules["margin_left_cm"]) > 0.05:
            problems.append("左边距 %.2fcm" % left)
        if problems:
            add(3, "fail", "第 1 节页面设置", "；".join(problems),
                "上 2.54cm / 左 3.0cm（装订线）")
        else:
            add(3, "pass", "第 1 节页面设置", "上 %.2fcm / 左 %.2fcm" % (top, left),
                "上 2.54cm / 左 3.0cm")
    except Exception as exc:  # noqa: BLE001
        add(3, "warn", "页面设置", "解析失败：%s" % exc, "人工核对")

    # 4 目录结构
    text_all = "\n".join(p.text for p in doc.paragraphs)
    has_toc_title = "目录" in text_all
    xml = doc.element.xml
    has_toc_field = "TOC" in xml or "fldChar" in xml
    if has_toc_title and has_toc_field:
        add(4, "pass", "目录", "含目录标题 + TOC 域", "含章节标题与页码")
    elif has_toc_title:
        add(4, "warn", "目录", "有目录标题但未见 TOC 域", "建议使用自动目录域")
    else:
        add(4, "warn", "目录", "未检测到目录", "含章节标题与页码")

    # 5 页码连续
    footer_text = " ".join(p.text.strip() for sec in doc.sections for p in sec.footer.paragraphs)
    if "PAGE" in xml or re.search(r"\d+", footer_text):
        add(5, "pass", "页脚", "检测到页码域/页码文本", "正文连续编号")
    elif rules.get("require_page_number"):
        add(5, "fail", "页脚", "未检测到页码", "正文连续页码")
    else:
        add(5, "pass", "页脚", "无页码（未强制）", "—")

    # 6 图表编号
    figs = re.findall(r"图\s*\d+\s*[-–]\s*\d+", text_all)
    tabs = re.findall(r"表\s*\d+\s*[-–]\s*\d+", text_all)
    if figs or tabs:
        add(6, "pass", "正文题注", "图 %d 处 / 表 %d 处" % (len(figs), len(tabs)), "按章连续编号")
    else:
        add(6, "warn", "正文题注", "未检测到「图X-Y / 表X-Y」编号", "按章连续编号（图3-1）")

    # 7 行距段落
    spacings = []
    for p in doc.paragraphs:
        ls = p.paragraph_format.line_spacing
        if ls:
            spacings.append(round(float(ls), 2))
    if spacings and all(abs(s - rules["line_spacing"]) < 0.05 for s in spacings):
        add(7, "pass", "段落行距", "统一 %.2f" % spacings[0], "%.1f 倍行距" % rules["line_spacing"])
    elif spacings and len(set(spacings)) == 1:
        add(7, "fail", "段落行距", "行距 %.2f，与要求不符" % spacings[0],
            "%.1f 倍行距" % rules["line_spacing"])
    elif spacings:
        add(7, "warn", "段落行距", "存在多种行距 %s" % sorted(set(spacings))[:3],
            "%.1f 倍行距统一" % rules["line_spacing"])
    else:
        add(7, "warn", "段落行距", "未显式设置行距", "%.1f 倍行距" % rules["line_spacing"])

    # 8 密封要求（关键词）
    kw_seal = [k for k in ("正本", "副本", "密封", "骑缝") if k in text_all]
    if kw_seal:
        add(8, "warn", "正文密封条款", "检测到关键词：%s" % "、".join(kw_seal),
            "正副本数量/密封方式符合招标文件要求", "需人工线下核对实体密封")
    else:
        add(8, "warn", "正文密封条款", "未检测到密封关键词", "按招标文件要求密封", "需人工线下核对")

    # 9 签字盖章
    kw_sign = [k for k in ("签字", "盖章", "公章", "法定代表人", "授权委托书") if k in text_all]
    if len(kw_sign) >= 2:
        add(9, "pass", "签字盖章位置", "检测到：%s" % "、".join(kw_sign), "法人签字 + 公章 + 授权委托书")
    elif kw_sign:
        add(9, "warn", "签字盖章位置", "仅检测到：%s" % "、".join(kw_sign), "法人签字 + 公章 + 骑缝章 + 授权委托书")
    else:
        add(9, "warn", "签字盖章位置", "未检测到签字盖章关键词", "法人签字 + 公章 + 授权委托书")

    # 10 投标函格式
    kw_bid = [k for k in ("投标函", "报价表", "投标总价", "法定代表人或授权代表") if k in text_all]
    if "投标函" in kw_bid and len(kw_bid) >= 2:
        add(10, "pass", "投标函", "检测到：%s" % "、".join(kw_bid), "投标函 + 报价表格式完整")
    elif kw_bid:
        add(10, "warn", "投标函", "仅检测到：%s" % "、".join(kw_bid), "投标函 + 报价表格式完整")
    else:
        add(10, "warn", "投标函", "未检测到投标函/报价表关键词", "投标函 + 报价表格式完整")

    results.sort(key=lambda r: r["no"])
    return results, True


def render(results, auto):
    passed = sum(1 for r in results if r["state"] == "pass")
    warned = sum(1 for r in results if r["state"] == "warn")
    failed = sum(1 for r in results if r["state"] == "fail")
    lines = []
    lines.append("标书格式合规检查报告（10 项）")
    lines.append("扫描方式：%s" % ("python-docx 自动扫描" if auto else "清单式（缺 python-docx，需人工核对）"))
    lines.append("结果：通过 %d / 警告 %d / 不通过 %d" % (passed, warned, failed))
    lines.append("")
    lines.append("整改清单（位置 + 现状 + 应改为）")
    for r in results:
        icon = {"pass": "通过", "warn": "警告", "fail": "不通过"}[r["state"]]
        lines.append("[%s] 第 %d 项 %s（风险：%s）" % (icon, r["no"], r["item"], r["risk"]))
        if r["state"] != "pass":
            lines.append("  位置：%s" % r["location"])
            lines.append("  现状：%s" % r["current"])
            lines.append("  应改为：%s" % r["expected"])
        if r.get("note"):
            lines.append("  备注：%s" % r["note"])
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="标书格式合规检查 10 项")
    ap.add_argument("docx")
    ap.add_argument("--rules")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(args.docx):
        raise SystemExit("文件不存在：%s" % args.docx)
    if not args.docx.lower().endswith((".docx", ".doc")):
        raise SystemExit("仅支持 .docx（PDF/图片请转换后再检查）")

    rules = dict(DEFAULT_RULES)
    if args.rules:
        with open(args.rules, encoding="utf-8") as fh:
            rules.update(json.load(fh))

    results, auto = check_docx(args.docx, rules)
    if args.json:
        print(json.dumps({"auto": auto, "results": results}, ensure_ascii=False, indent=2))
    else:
        print(render(results, auto))


if __name__ == "__main__":
    main()
