#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_gap.py — 将"公司现有文档集"与所选 ISO 标准的条款要求进行差距分析。
泛化版本：标准条款、关键审核点（高压线）、必需程序列表全部来自
knowledge/<standard>_framework.json 与 knowledge/<standard>_templates.json。

用法:
  python analyze_gap.py <docs_dir> --standard iso9001 [--json] [--out report.md]
"""
import sys, os, re, json, argparse, glob

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
KNOWLEDGE_DIR = os.path.join(SKILL_DIR, "knowledge")

def load_json(name):
    path = os.path.join(KNOWLEDGE_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_json_fallback(name):
    """加载某标准专属 JSON；缺失时回退到 generic_mss_* 兜底，再缺失返回空结构。"""
    path = os.path.join(KNOWLEDGE_DIR, name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    if name.endswith("_framework.json"):
        fb = os.path.join(KNOWLEDGE_DIR, "generic_mss_framework.json")
    else:
        fb = os.path.join(KNOWLEDGE_DIR, "generic_mss_templates.json")
    if os.path.exists(fb):
        print(f"[INFO] 标准文件 {name} 缺失，使用通用兜底: {os.path.basename(fb)}")
        with open(fb, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"templates": []} if name.endswith("_templates.json") else {}

def collect_text(docs_dir):
    texts = []
    for fp in glob.glob(os.path.join(docs_dir, "**", "*"), recursive=True):
        if os.path.isfile(fp) and fp.lower().endswith((".docx", ".doc", ".txt", ".md")):
            try:
                if fp.lower().endswith((".docx", ".doc")):
                    import zipfile
                    if fp.lower().endswith(".docx"):
                        z = zipfile.ZipFile(fp)
                        t = z.read("word/document.xml").decode("utf-8", "ignore")
                        t = re.sub(r"<[^>]+>", " ", t)
                    else:
                        t = open(fp, "r", encoding="utf-8", errors="ignore").read()
                else:
                    t = open(fp, "r", encoding="utf-8", errors="ignore").read()
                texts.append((os.path.basename(fp), t))
            except Exception:
                continue
    return texts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docs_dir")
    ap.add_argument("--standard", default="iso9001")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()

    fw = load_json_fallback(f"{args.standard}_framework.json")
    tpl = load_json_fallback(f"{args.standard}_templates.json")

    docs = collect_text(args.docs_dir)
    if not docs:
        print(f"[WARN] 目录 {args.docs_dir} 下未找到可解析文档。")
        return

    corpus = "\n".join(t for _, t in docs)
    doc_names = [n for n, _ in docs]

    # 必需程序覆盖
    required = fw.get("required_procedures", [])
    proc_present, proc_missing = [], []
    for p in required:
        # 用程序名关键词 + 条款号在语料中匹配
        kws = [p.get("name", "")] + p.get("match_keywords", [])
        hit = any((k and k in corpus) for k in kws) or any(
            (p.get("clause", "") and p.get("clause", "") in t) for _, t in docs)
        (proc_present if hit else proc_missing).append(p)

    # 关键审核点（高压线）覆盖
    hv = fw.get("high_voltage_lines", [])
    hv_covered, hv_missing = [], []
    for item in hv:
        kws = item.get("keywords_zh", []) + item.get("keywords_en", [])
        hit = any(k and k in corpus for k in kws)
        (hv_covered if hit else hv_missing).append(item)

    # 模板成熟度（知识库已备模板：专属 + 通用兜底）
    tmpl_ids = {t.get("id") for t in tpl.get("templates", [])}
    try:
        gen_tpl = load_json_fallback("generic_mss_templates.json").get("templates", [])
        tmpl_ids |= {t.get("id") for t in gen_tpl}
    except Exception:
        pass
    tmpl_for_missing = [p for p in proc_missing if p.get("id") in tmpl_ids]

    report = {
        "standard": args.standard,
        "standard_name": fw.get("standard"),
        "analyzed_docs": doc_names,
        "procedures_total": len(required),
        "procedures_present": len(proc_present),
        "procedures_missing": len(proc_missing),
        "high_voltage_total": len(hv),
        "high_voltage_covered": len(hv_covered),
        "high_voltage_missing": len(hv_missing),
        "missing_procedures": [
            {"id": p.get("id"), "name": p.get("name"), "clause": p.get("clause"), "priority": p.get("priority")}
            for p in proc_missing
        ],
        "missing_high_voltage": [
            {"id": h.get("id"), "name": h.get("name_zh") or h.get("name_en"),
             "description": h.get("description_zh") or h.get("description_en")}
            for h in hv_missing
        ],
        "auto_generatable": [
            {"id": p.get("id"), "name": p.get("name"), "clause": p.get("clause")}
            for p in tmpl_for_missing
        ],
    }

    if args.json or args.out:
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                if args.out.endswith(".json"):
                    f.write(json.dumps(report, ensure_ascii=False, indent=2))
                else:
                    f.write(render_md(report, fw))
            print(f"[OK] 差距分析报告已写入: {args.out}")
        else:
            print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_md(report, fw))

def render_md(r, fw):
    L = []
    L.append(f"# {r['standard_name']} 体系差距分析报告\n")
    L.append(f"- 分析文档数：{len(r['analyzed_docs'])}（{', '.join(r['analyzed_docs'])}）")
    L.append(f"- 必需程序覆盖：{r['procedures_present']}/{r['procedures_total']}")
    L.append(f"- 关键审核点覆盖：{r['high_voltage_covered']}/{r['high_voltage_total']}\n")
    if r["missing_procedures"]:
        L.append("## 一、缺失的必需程序（需补建）")
        for p in r["missing_procedures"]:
            tag = "【高】" if p.get("priority") == "high" else "【中】" if p.get("priority") == "medium" else "【低】"
            L.append(f"- {tag} {p.get('id')} {p.get('name')}（条款 {p.get('clause')}）")
        L.append("")
    if r["missing_high_voltage"]:
        L.append("## 二、关键审核点风险（高压线缺失，重点整改）")
        for h in r["missing_high_voltage"]:
            L.append(f"- **{h.get('name')}**：{h.get('description')}")
        L.append("")
    if r["auto_generatable"]:
        L.append("## 三、可一键生成的文件（本技能已备模板）")
        for p in r["auto_generatable"]:
            L.append(f"- {p.get('id')} {p.get('name')} → `generate_document.py --standard {r['standard']} --type {p.get('id')}`")
        L.append("")
    L.append("> 建议优先补齐【高】优先级程序与全部关键审核点，再开展内审与管理评审。")
    return "\n".join(L)

if __name__ == "__main__":
    main()
