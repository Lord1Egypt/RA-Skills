#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_docx.py — 解析公司现有体系文档（.docx/.doc/.txt/.md），提取结构化信息。
泛化版本：关键审核点（高压线）与条款映射来自 knowledge/<standard>_framework.json，
做到"换标准只换 JSON，脚本零改动"。

用法:
  python parse_docx.py <input_file> --standard iso9001 [--json] [--out out.json]
"""
import sys, os, re, json, argparse

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "knowledge")

def load_framework(standard_id):
    """加载某标准的 framework；专属文件缺失时自动回退到通用 Annex SL 兜底框架。"""
    path = os.path.join(KNOWLEDGE_DIR, f"{standard_id}_framework.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    fallback = os.path.join(KNOWLEDGE_DIR, "generic_mss_framework.json")
    if os.path.exists(fallback):
        print(f"[INFO] 标准 {standard_id} 暂无专属框架，使用通用 Annex SL 兜底框架。")
        with open(fallback, "r", encoding="utf-8") as f:
            return json.load(f)
    raise SystemExit(f"[ERROR] 找不到标准框架文件: {path}\n"
                     f"        可用标准请查看 knowledge/standard_index.json")

def read_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt" or ext == ".md":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    if ext in (".docx", ".doc"):
        return read_office(path, ext)
    raise SystemExit(f"[ERROR] 不支持的文件类型: {ext}")

def read_office(path, ext):
    try:
        if ext == ".docx":
            import zipfile
            z = zipfile.ZipFile(path)
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
            xml = re.sub(r"<w:p[ >]", "\n", xml)
            xml = re.sub(r"<w:tr[ >]", "\n", xml)
            xml = re.sub(r"<[^>]+>", "", xml)
            xml = xml.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&nbsp;", " ")
            return xml
        else:  # .doc 采用最朴素文本抽取（兼容优先）
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()
            # 去除二进制噪音，保留可见中文/英文/标点
            return re.sub(r"[^\u4e00-\u9fffA-Za-z0-9\s\.\,\，\。\、\：\:\;\；\（\）\(\)\%\/\-\—]", "", raw)
    except Exception as e:
        return f"[WARN] 无法解析 Office 文件: {e}"

def extract_headings(text):
    lines = [l.strip() for l in text.split("\n")]
    headings = []
    for l in lines:
        if not l:
            continue
        # 形如 "1. 目的" / "3.2 职责" / "一、范围"
        if re.match(r"^(\d+(\.\d+)*|[一二三四五六七八九十]+)[、．.\s]", l) and len(l) <= 40:
            headings.append(l)
    return headings

def extract_responsibilities(text):
    pats = [
        r"([\u4e00-\u9fff]{2,}(部|中心|组|经理|负责人|主管|工程师|小组|成员|部门|委员会|全员|员工|管理层)[\s\S]{0,80}?负责[\s\S]{0,120}?)[\n。；;]",
        r"职责[\s\S]{0,400}?",
    ]
    found = []
    for p in pats:
        for m in re.finditer(p, text):
            seg = m.group(0).replace("\n", " ").strip()
            if 4 < len(seg) < 200:
                found.append(seg)
    return list(dict.fromkeys(found))[:15]

def extract_process_steps(text):
    steps = re.findall(r"(\d+[\.、]\s*[\u4e00-\u9fff][^\n]{1,60})", text)
    steps = [s.strip() for s in steps]
    return list(dict.fromkeys(steps))[:25]

def extract_records(text):
    recs = re.findall(r"((?:《|〔|\[|<)?[^\n，。；;]{1,30}?(?:记录|清单|台账|报告|表|单|档案|台账|日志|档案)(?:》|〕|\]|>)?)", text)
    return list(dict.fromkeys([r.strip() for r in recs]))[:20]

def map_clauses(text, framework):
    """根据框架里的 clause_keywords 把文档命中到条款。"""
    mapping = framework.get("clause_keywords", {})
    found = []
    for clause, kws in mapping.items():
        for kw in kws:
            if kw and kw in text:
                if clause not in found:
                    found.append(clause)
                break
    return found

def detect_high_voltage(text, framework):
    """根据框架里的高压线 keywords 检测覆盖情况。"""
    hv = framework.get("high_voltage_lines", [])
    covered, missing = [], []
    for item in hv:
        kws = item.get("keywords_zh", []) + item.get("keywords_en", [])
        hit = any(k and k in text for k in kws)
        entry = {"id": item.get("id"), "name": item.get("name_zh") or item.get("name_en")}
        (covered if hit else missing).append(entry)
    return covered, missing

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_file")
    ap.add_argument("--standard", default="iso9001", help="标准 ID，例如 iso9001 / iso14001 / iso45001 / iso27001 / iso20000")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出")
    ap.add_argument("--out", help="输出文件路径")
    args = ap.parse_args()

    framework = load_framework(args.standard)
    text = read_text(args.input_file)
    result = {
        "standard": args.standard,
        "standard_name": framework.get("standard", args.standard),
        "source_file": os.path.basename(args.input_file),
        "char_count": len(text),
        "headings": extract_headings(text),
        "responsibilities": extract_responsibilities(text),
        "process_steps": extract_process_steps(text),
        "records": extract_records(text),
        "clauses_covered": map_clauses(text, framework),
        "high_voltage_covered": detect_high_voltage(text, framework)[0],
        "high_voltage_missing": detect_high_voltage(text, framework)[1],
    }
    if args.json or args.out:
        out = json.dumps(result, ensure_ascii=False, indent=2)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(out)
            print(f"[OK] 结构化结果已写入: {args.out}")
        else:
            print(out)
    else:
        print(f"=== 文档结构化解析（标准：{framework.get('standard')}）===")
        print(f"字符数: {result['char_count']}")
        print(f"\n[标题] 命中 {len(result['headings'])} 个")
        for h in result["headings"][:20]:
            print(f"  - {h}")
        print(f"\n[职责] 命中 {len(result['responsibilities'])} 条")
        for r in result["responsibilities"][:8]:
            print(f"  - {r}")
        print(f"\n[流程步骤] 命中 {len(result['process_steps'])} 条")
        for s in result["process_steps"][:12]:
            print(f"  - {s}")
        print(f"\n[记录表单] 命中 {len(result['records'])} 个")
        for r in result["records"][:10]:
            print(f"  - {r}")
        print(f"\n[条款覆盖] {result['clauses_covered']}")
        print(f"\n[关键审核点-已覆盖] {[x['name'] for x in result['high_voltage_covered']]}")
        print(f"[关键审核点-缺失]   {[x['name'] for x in result['high_voltage_missing']]}")

if __name__ == "__main__":
    main()
