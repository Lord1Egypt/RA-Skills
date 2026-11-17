#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_document.py — 把公司现有文档自动转换为符合目标标准评价格式的体系文件。

流程：
  1. 复用 parse_docx 的抽取能力：从旧文档提取标题/职责/流程步骤/记录表单/条款覆盖；
  2. 模板匹配：按关键词与条款把旧文档匹配到最合适的标准模板（专属+通用合并后打分）；
  3. 内容回填：把旧文档的目的/职责/流程/记录内容填入标准模板对应章节；
     旧文档没有的章节保留模板默认内容并标注 [模板默认，请结合实际修订]；
  4. 输出：标准格式 Markdown（含文件编号、条款映射、关键审核点、转换溯源附录）。

用法:
  # 单文件转换（自动匹配模板）
  python convert_document.py 旧文档.docx --standard iso9001 --org "XX公司"
  # 指定目标模板
  python convert_document.py 旧文档.docx --standard iso22000 --template QP-HACCP --org "XX食品"
  # 批量转换目录下所有文档
  python convert_document.py ./docs --standard iso27001 --org "XX科技" --out ./converted
"""
import sys, os, re, json, argparse, datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "knowledge")
sys.path.insert(0, SCRIPT_DIR)

from parse_docx import (load_framework, read_text, extract_headings,
                        extract_responsibilities, extract_process_steps,
                        extract_records, map_clauses, detect_high_voltage)

SUPPORTED_EXT = (".docx", ".doc", ".txt", ".md")


def load_templates(standard_id):
    """加载标准专属模板 + 通用模板（按 id 去重，专属优先）。"""
    def _load(name):
        p = os.path.join(KNOWLEDGE_DIR, name)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f).get("templates", [])
        return []
    gen = _load("generic_mss_templates.json")
    std = _load(f"{standard_id}_templates.json")
    by_id = {t.get("id"): t for t in gen}
    for t in std:
        by_id[t.get("id")] = t
    return list(by_id.values())


def score_template(tpl, text, filename):
    """给模板与旧文档的匹配度打分：模板名/条款关键词命中 + 文件名相似。"""
    score = 0
    name = tpl.get("name", "")
    # 模板名逐词命中正文（按 2 字滑窗切词，覆盖"文件控制/内审/管理评审"等）
    words = [name[i:i+2] for i in range(len(name)-1)]
    hits = sum(1 for w in words if w and w in text)
    score += hits * 2
    # 文件名命中模板名核心词
    base = os.path.splitext(os.path.basename(filename))[0]
    core = re.sub(r"(控制)?(管理)?程序$", "", name)
    if core and (core in base or base in name):
        score += 30
    for w in set(words):
        if w in base:
            score += 6
    # 章节标题命中
    for sec in tpl.get("sections", []):
        st = re.sub(r"^\d+\s*", "", sec.get("title", ""))
        if st and st in text:
            score += 1
    return score


def pick_template(templates, text, filename):
    scored = sorted(((score_template(t, text, filename), t) for t in templates),
                    key=lambda x: -x[0])
    return scored[0][1], [(s, t.get("id"), t.get("name")) for s, t in scored[:3]]


def slice_source_sections(text):
    """按标题把旧文档切块，返回 {标题: 内容}。"""
    lines = text.split("\n")
    sections, cur_title, buf = {}, "_前言", []
    pat = re.compile(r"^(\d+(\.\d+)*|[一二三四五六七八九十]+)[、．.\s]\s*(\S.*)$")
    for l in lines:
        l = l.strip()
        m = pat.match(l)
        if m and len(l) <= 40:
            if buf:
                sections[cur_title] = "\n".join(buf).strip()
            cur_title, buf = l, []
        elif l:
            buf.append(l)
    if buf:
        sections[cur_title] = "\n".join(buf).strip()
    return sections


# 标准章节 → 旧文档章节标题的匹配关键词
SECTION_KEYS = {
    "目的": ["目的", "总则", "前言"],
    "适用范围": ["范围", "适用"],
    "职责": ["职责", "分工", "组织", "责任"],
    "工作程序": ["程序", "流程", "步骤", "要求", "内容", "控制", "方法", "实施", "过程"],
}


def match_source_content(sec_title, src_sections):
    """为标准模板章节找旧文档对应内容。"""
    clean = re.sub(r"^\d+\s*", "", sec_title)
    keys = []
    for k, kws in SECTION_KEYS.items():
        if k in clean:
            keys = kws
            break
    if not keys:
        keys = [clean]
    matched = []
    for title, content in src_sections.items():
        if any(k in title for k in keys):
            matched.append((title, content))
    return matched


def fill_vars(text, org, today, ver="A/0"):
    return (text.replace("{company}", org).replace("{org}", org)
                .replace("{date}", today).replace("{version}", ver)
                .replace("{today}", today))


def convert_one(src_path, standard, framework, templates, org, tpl_id=None):
    text = read_text(src_path)
    src_sections = slice_source_sections(text)
    if tpl_id:
        tpl = next((t for t in templates if t.get("id") == tpl_id), None)
        if not tpl:
            raise SystemExit(f"[ERROR] 找不到模板 ID={tpl_id}。可用: "
                             + ", ".join(t.get("id") for t in templates))
        top3 = [(0, tpl_id, tpl.get("name"))]
    else:
        base = os.path.basename(src_path)
        if "手册" in base or "manual" in base.lower():
            print(f"[提示] 「{base}」疑似体系手册，内容通常横跨多个程序文件。"
                  f"本次将匹配单一模板转换；建议按程序拆分转换，或用 --template 指定目标模板。")
        tpl, top3 = pick_template(templates, text, src_path)

    today = datetime.date.today().isoformat()
    ver = "A/0"
    clauses = map_clauses(text, framework)
    hv_cov, hv_miss = detect_high_voltage(text, framework)
    resp = extract_responsibilities(text)
    records = extract_records(text)

    out = []
    out.append(f"# {tpl.get('name')}")
    out.append(f"- 文件编号：{tpl.get('id')}    版本：{ver}    生效日期：{today}    编制单位：{org}")
    out.append(f"- 目标标准：{framework.get('standard', standard)}    对应条款：{tpl.get('clause')}")
    out.append(f"- 转换来源：{os.path.basename(src_path)}（自动转换，请人工复核）")
    out.append("")

    used_titles = set()
    for sec in tpl.get("sections", []):
        s_title = sec.get("title")
        out.append(f"## {s_title}")
        matched = match_source_content(s_title, src_sections)
        if matched:
            for title, content in matched:
                used_titles.add(title)
                out.append(content if title.startswith("_") else f"（源自原文「{title}」）\n{content}")
            # 职责章节额外并入正则抽取的职责句
            if "职责" in s_title and resp:
                extra = [r for r in resp if r not in "\n".join(c for _, c in matched)]
                if extra:
                    out.append("\n补充识别的职责条目：")
                    out.extend(f"- {r}" for r in extra[:8])
        else:
            if "职责" in s_title and resp:
                out.append("（原文未见独立职责章节，以下为自动识别的职责条目）")
                out.extend(f"- {r}" for r in resp[:8])
                out.append("> [自动识别内容——请人工核对并补充]")
            else:
                out.append(fill_vars(sec.get("content", ""), org, today, ver))
                out.append("> [模板默认内容——原文档未覆盖本章节，请结合实际修订]")
        out.append("")

    # 原文档中未映射进标准章节的剩余内容
    leftovers = {t: c for t, c in src_sections.items()
                 if t not in used_titles and not t.startswith("_") and c}
    if leftovers:
        out.append("## 附录A 原文档保留内容（未自动归类，请人工分配到相应章节）")
        for t, c in leftovers.items():
            out.append(f"### {t}")
            out.append(c)
            out.append("")

    # 记录表单
    if records:
        out.append("## 附录B 引用记录/表单清单（自动识别）")
        out.extend(f"- {r}" for r in records)
        out.append("")

    # 关键审核点
    keys = tpl.get("high_voltage_check") or []
    if isinstance(keys, str):
        keys = [keys]
    hv_lines = framework.get("high_voltage_lines", [])
    if keys:
        out.append("## 附录C 关键审核点（审核员必查，请重点准备证据）")
        for k in keys:
            for hv in hv_lines:
                if hv.get("id") == k:
                    out.append(f"### {hv.get('name_zh') or hv.get('name_en')}")
                    out.extend(f"- {s}" for s in hv.get("compliance_statement", []))
                    out.append("")

    # 转换溯源
    out.append("## 附录D 转换报告")
    out.append(f"- 匹配模板：{tpl.get('id')} {tpl.get('name')}"
               + ("" if tpl_id else f"（候选：{'; '.join(f'{i}:{n}(分{s})' for s, i, n in top3)}）"))
    out.append(f"- 原文条款覆盖：{', '.join(clauses) if clauses else '无'}")
    out.append(f"- 关键审核点已覆盖：{', '.join(x['name'] for x in hv_cov) if hv_cov else '无'}")
    out.append(f"- 关键审核点缺失：{', '.join(x['name'] for x in hv_miss) if hv_miss else '无'}")
    out.append("- 说明：标注 [模板默认内容] 的章节为原文档缺失部分，需人工补充实际做法。")
    return tpl, "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="旧文档文件或目录（.docx/.doc/.txt/.md）")
    ap.add_argument("--standard", default="iso9001", help="目标标准 ID，见 knowledge/standard_index.json")
    ap.add_argument("--template", help="指定目标模板 ID（缺省自动匹配）")
    ap.add_argument("--org", default="XX 公司", help="公司/组织名称")
    ap.add_argument("--out", help="输出文件（单文件）或输出目录（目录批量）")
    args = ap.parse_args()

    framework = load_framework(args.standard)
    templates = load_templates(args.standard)

    if os.path.isdir(args.input):
        files = [os.path.join(args.input, f) for f in sorted(os.listdir(args.input))
                 if f.lower().endswith(SUPPORTED_EXT)]
        if not files:
            raise SystemExit(f"[ERROR] 目录中没有可转换的文档: {args.input}")
        out_dir = args.out or os.path.join(os.getcwd(), f"converted_{args.standard}")
        os.makedirs(out_dir, exist_ok=True)
        for fp in files:
            tpl, content = convert_one(fp, args.standard, framework, templates,
                                       args.org, args.template)
            base = os.path.splitext(os.path.basename(fp))[0]
            fn = os.path.join(out_dir, f"{tpl.get('id')}_{base}.md")
            with open(fn, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[OK] {os.path.basename(fp)} -> {os.path.basename(fn)}（模板 {tpl.get('id')}）")
        print(f"[OK] 共转换 {len(files)} 份到: {out_dir}")
        return

    tpl, content = convert_one(args.input, args.standard, framework, templates,
                               args.org, args.template)
    if args.out and not args.out.lower().endswith(".md"):
        os.makedirs(args.out, exist_ok=True)
        base = os.path.splitext(os.path.basename(args.input))[0]
        args.out = os.path.join(args.out, f"{tpl.get('id')}_{base}.md")
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] 已转换（模板 {tpl.get('id')} {tpl.get('name')}）: {args.out}")
    else:
        print(content)


if __name__ == "__main__":
    main()
