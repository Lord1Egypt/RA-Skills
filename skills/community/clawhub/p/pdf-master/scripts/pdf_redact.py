#!/usr/bin/env python3
r"""pdf_redact.py — 密文级敏感信息删除：真删底层对象 + 双引擎验证 + 删除证书（能力 #25）

流程：--scan 预览 → 用户确认 → --apply 执行 → 自动验证 → 出具证书
用法：
  python3 pdf_redact.py in.pdf --scan                      # 预览命中（不修改）
  python3 pdf_redact.py in.pdf --apply out.pdf --cert cert.json
  python3 pdf_redact.py in.pdf --apply out.pdf --regex "\d{17}[\dXx]" --types idcard,phone
"""
import argparse, datetime, hashlib, json, os, re, sys

# 手机号/银行卡带环视，避免误伤身份证号内部数字段
PRESETS = {
    "idcard": (r"(?<![\dXx])\d{17}[\dXx](?![\dXx])", "身份证号"),
    "phone": (r"(?<!\d)1[3-9]\d{9}(?!\d)", "手机号"),
    "bankcard": (r"(?<!\d)\d{16,19}(?!\d)", "银行卡号"),
    "email": (r"[\w.+-]+@[\w-]+\.[\w.-]+", "邮箱"),
}

def find_spans(text, patterns):
    """按 patterns 顺序优先去重匹配，返回 [(start,end,type,raw)]，区间不重叠。"""
    spans, occupied = [], []
    for label, pat in patterns:
        for m in re.finditer(pat, text):
            s, e = m.span()
            if any(s < oe and e > os_ for os_, oe in occupied):
                continue  # 已被更高优先级规则覆盖
            occupied.append((s, e))
            spans.append((s, e, label, m.group()))
    return spans

def scan_hits(path, patterns):
    import fitz
    doc = fitz.open(path)
    hits = []
    for pno in range(doc.page_count):
        for s, e, label, raw in find_spans(doc[pno].get_text(), patterns):
            hits.append({"page": pno + 1, "type": label,
                         "value": raw[:4] + "****" + raw[-2:], "raw": raw})
    doc.close()
    return hits

def verify(path, patterns):
    """双引擎验证：PyMuPDF + pdfplumber 全文提取，0 命中才通过。"""
    import fitz, pdfplumber
    texts = []
    with fitz.open(path) as d:
        texts.append("\n".join(p.get_text() for p in d))
    with pdfplumber.open(path) as d:
        texts.append("\n".join((p.extract_text() or "") for p in d.pages))
    residuals = []
    for engine, text in zip(["pymupdf", "pdfplumber"], texts):
        for s, e, label, raw in find_spans(text, patterns):
            residuals.append({"engine": engine, "type": label, "hit": raw})
    return residuals

def main():
    ap = argparse.ArgumentParser(description="密文级敏感信息删除")
    ap.add_argument("pdf")
    ap.add_argument("--scan", action="store_true", help="仅预览命中，不修改")
    ap.add_argument("--apply", metavar="OUT", help="执行删除并另存 OUT")
    ap.add_argument("--types", default="idcard,phone,bankcard,email",
                    help="预设类型，逗号分隔：idcard,phone,bankcard,email")
    ap.add_argument("--regex", action="append", help="自定义正则（可多次）")
    ap.add_argument("--cert", metavar="CERT.json", help="删除证书输出路径")
    a = ap.parse_args()
    patterns = [(PRESETS[t][1], PRESETS[t][0]) for t in a.types.split(",") if t in PRESETS]
    patterns += [("自定义", r) for r in (a.regex or [])]
    if not patterns:
        sys.exit("❌ 无有效删除规则")
    hits = scan_hits(a.pdf, patterns)
    if a.scan or not a.apply:
        print(f"📋 删除预览：共 {len(hits)} 处命中（未修改文件）")
        for h in hits[:50]:
            print(f"   第{h['page']}页 [{h['type']}] {h['value']}")
        if len(hits) > 50:
            print(f"   …另 {len(hits)-50} 处略")
        print("确认无误后执行：--apply out.pdf --cert cert.json")
        return
    import fitz
    doc = fitz.open(a.pdf)
    for pno in range(doc.page_count):
        page = doc[pno]
        raws = {raw for _, _, _, raw in find_spans(page.get_text(), patterns)}
        for raw in raws:
            for rect in page.search_for(raw):
                page.add_redact_annot(rect)
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)
    doc.save(a.apply, garbage=4, deflate=True)
    doc.close()
    residuals = verify(a.apply, patterns)
    status = "通过（0 残留）" if not residuals else f"发现 {len(residuals)} 处残留"
    cert = {
        "证书类型": "密文级删除证书",
        "源文件": os.path.basename(a.pdf),
        "源文件SHA256": hashlib.sha256(open(a.pdf, "rb").read()).hexdigest(),
        "输出文件": a.apply,
        "输出SHA256": hashlib.sha256(open(a.apply, "rb").read()).hexdigest(),
        "删除时间": datetime.datetime.now().isoformat(timespec="seconds"),
        "删除规则": [t for t, _ in patterns],
        "命中并删除": len(hits),
        "验证方式": "PyMuPDF + pdfplumber 双引擎全文提取扫描 + 正则二次扫描",
        "验证结果": status,
        "残留明细": residuals[:20],
    }
    cert_path = a.cert or os.path.splitext(a.apply)[0] + "_删除证书.json"
    with open(cert_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, ensure_ascii=False, indent=2)
    if residuals:
        print(f"⚠️ 验证发现残留 {len(residuals)} 处！详见证书。请检查是否为图片内文字（需走图像修复）")
        sys.exit(3)
    print(f"✅ 已彻底删除 {len(hits)} 处，双引擎验证 0 命中")
    print(f"📜 删除证书：{cert_path}")

if __name__ == "__main__":
    main()
