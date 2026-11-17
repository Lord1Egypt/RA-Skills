#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_document.py — 依据标准模板生成体系文件（程序文件 / 质量手册 / 记录表单）。
泛化版本：模板来自 knowledge/<standard>_templates.json；高压线合规声明来自
knowledge/<standard>_framework.json。

用法:
  # 生成单个程序文件
  python generate_document.py --standard iso9001 --type QP-001 --org "示例科技有限公司"
  # 批量生成该标准全部模板
  python generate_document.py --standard iso14001 --type all --org "XX 公司" --out ./out
  # 双语
  python generate_document.py --standard iso9001 --type QP-001 --lang bilingual
"""
import sys, os, re, json, argparse, datetime

# 兼容 Windows GBK 控制台：将 stdout 设为 utf-8，避免 ✓ 等字符打印崩溃
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
KNOWLEDGE_DIR = os.path.join(SKILL_DIR, "knowledge")

def load_json(name):
    with open(os.path.join(KNOWLEDGE_DIR, name), "r", encoding="utf-8") as f:
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

def fill_vars(text, org, today, ver="A/0"):
    return (text.replace("{company}", org)
                .replace("{org}", org)
                .replace("{date}", today)
                .replace("{version}", ver)
                .replace("{today}", today))

def build_hv_block(framework):
    lines = []
    for hv in framework.get("high_voltage_lines", []):
        name = hv.get("name_zh") or hv.get("name_en")
        lines.append(f"### {name}")
        for stmt in hv.get("compliance_statement", []):
            lines.append(f"- {stmt}")
        lines.append("")
    return "\n".join(lines)

def render_template(tpl, framework, org, lang):
    today = datetime.date.today().isoformat()
    ver = "A/0"
    out = []
    title = tpl.get("name")
    if lang == "bilingual" and tpl.get("name_en"):
        title = f"{tpl.get('name')} / {tpl.get('name_en')}"
    out.append(f"# {title}")
    meta = tpl.get("meta") or {}
    out.append(f"- 文件编号：{tpl.get('id')}")
    out.append(f"- 对应条款：{tpl.get('clause')}")
    out.append(f"- 版本：{ver}    生效日期：{today}    编制单位：{org}")
    out.append("")
    for sec in tpl.get("sections", []):
        s_title = sec.get("title")
        if lang == "bilingual" and sec.get("title_en"):
            s_title = f"{sec.get('title')} / {sec.get('title_en')}"
        out.append(f"## {s_title}")
        content = fill_vars(sec.get("content", ""), org, today, ver)
        out.append(content)
        out.append("")
    # 关键审核点提示（高压线）
    if tpl.get("high_voltage_check"):
        keys = tpl["high_voltage_check"]
        if isinstance(keys, str):
            keys = [keys]
        out.append("## 关键审核点（审核员必查，请重点准备证据）")
        for k in keys:
            for hv in framework.get("high_voltage_lines", []):
                if hv.get("id") == k:
                    out.append(f"### {hv.get('name_zh') or hv.get('name_en')}")
                    for stmt in hv.get("compliance_statement", []):
                        out.append(f"- {stmt}")
                    out.append("")
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--standard", default="iso9001")
    ap.add_argument("--type", required=True, help="模板 ID，或 all 批量生成")
    ap.add_argument("--org", default="XX 公司", help="公司/组织名称")
    ap.add_argument("--lang", default="zh", choices=["zh", "bilingual"])
    ap.add_argument("--out", help="输出目录（type=all 时）或输出文件")
    args = ap.parse_args()

    tpl_file = f"{args.standard}_templates.json"
    framework = load_json_fallback(f"{args.standard}_framework.json")
    # 合并：标准专属模板 + 通用模板（按 id 去重，专属优先）
    std_tpls = load_json_fallback(tpl_file).get("templates", [])
    gen_tpls = load_json_fallback("generic_mss_templates.json").get("templates", [])
    by_id = {t.get("id"): t for t in gen_tpls}
    for t in std_tpls:
        by_id[t.get("id")] = t
    templates = list(by_id.values())

    if args.type == "all":
        out_dir = args.out or os.path.join(os.getcwd(), f"generated_{args.standard}")
        os.makedirs(out_dir, exist_ok=True)
        for t in templates:
            content = render_template(t, framework, args.org, args.lang)
            fn = os.path.join(out_dir, f"{t.get('id')}.md")
            with open(fn, "w", encoding="utf-8") as f:
                f.write(content)
        print(f"[OK] 已生成 {len(templates)} 份文件到: {out_dir}（含通用模板 {len(gen_tpls)} 份）")
        return

    t = next((x for x in templates if x.get("id") == args.type), None)
    if not t:
        avail = ", ".join(x.get("id") for x in templates)
        print(f"[ERROR] 找不到模板 ID={args.type}。可用: {avail}")
        return
    content = render_template(t, framework, args.org, args.lang)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] 已生成: {args.out}")
    else:
        print(content)

if __name__ == "__main__":
    main()
