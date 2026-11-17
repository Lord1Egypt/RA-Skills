#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_term_consistency.py — 多文档术语一致性检查（v6.6.0 新增；pp.py term-project）

真实场景：学位论文/课题组报告=多个章节文件。term_check 单文件查「是否符合标准库」，
查不了「同一概念在不同章节写法是否一致」——第 2 章写「类风湿关节炎」、第 5 章写
「类风湿性关节炎」，查重之外的全稿统一全靠人工。本工具对**一个目录**的全部文稿：

  1. 逐文件跑术语检查（引擎与 term_check 同源）→ 每文件非标准用法清单
  2. 跨文件写法矩阵：同一库内概念在各文件分别用了哪种写法（标准名/哪个别名）
  3. 不一致清单：出现 ≥2 种写法的概念 + 统一建议（以库标准名为准）

诚实边界（固定）：一致性维度只覆盖**术语库内概念**——库外自由写法本工具不可见
（可配合 term_check --neologism 的词典外新造词提示）；统一建议以库标准名为准，
最终取舍由作者决定。零依赖（标准库）；输出 JSON/文本/HTML 三形态。
用法:
  python3 scripts/pp_term_consistency.py 章节目录/ --json
  python3 scripts/pp_term_consistency.py 章节目录/ --html matrix.html
  python3 scripts/pp.py term-project 章节目录/
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from term_check import load_terminology  # noqa: E402 引擎同源（词典加载）

_INTEGRITY = ("学术诚信：本工具供作者自查与统一写作用语，统一建议以术语库标准名为准、"
              "由作者定夺；一致性维度只覆盖库内概念。")

# 与 term_check.check_terms 同源的排除规则（保持行为一致）
_SINGLE_SUFFIXES = ("家", "刊", "报", "类", "系", "学")
_DERIVATION_SUFFIXES = ("学家", "学会", "学分", "学科", "科学",
                        "分会", "中心", "专科", "科室", "研究",
                        "学院", "医院", "医师", "杂志", "手册",
                        "主任", "教授", "学系", "理论")
_PRECEDING_NAME_CHARS = ("国", "华", "洲", "际", "盟")


_TERMS_CACHE = {}


def scan_usages(text, bank_path=None):
    """单遍最长优先收集库内概念的全部写法命中 → [(写法, 标准名, 位置, 摘录)]。

    与 term_check.check_terms 的候选/裁决逻辑同源（标准词+别名一次收集、
    长者优先认领区间、派生词与机构名排除）；本函数额外保留标准词命中，
    供跨文件写法矩阵统计。v7.1.0: bank_path（项目自定义词表）按路径缓存。"""
    global _TERMS_CACHE
    key = bank_path or ""
    if key not in _TERMS_CACHE:
        _TERMS_CACHE[key] = load_terminology(bank_path)
    terms_db = _TERMS_CACHE[key]
    if not terms_db:
        return []
    standard_terms = {}
    for key, entry in terms_db.items():
        std = entry["standard"]
        standard_terms.setdefault(std, entry)
    candidates = []
    for std_name in standard_terms:
        for m in re.finditer(re.escape(std_name), text):
            candidates.append((m.start(), m.start() + len(std_name), std_name,
                               std_name, False))
    for alias_lower, entry in terms_db.items():
        std_name = entry["standard"]
        if alias_lower == std_name.lower():
            continue
        if re.fullmatch(r"[a-zA-Z]+", alias_lower):
            pattern = r"(?<![a-zA-Z])" + re.escape(alias_lower) + r"(?![a-zA-Z])"
        else:
            pattern = re.escape(alias_lower)
        for m in re.finditer(pattern, text, re.IGNORECASE):
            candidates.append((m.start(), m.start() + len(alias_lower),
                               std_name, m.group(0), True))
    candidates.sort(key=lambda c: (-(c[1] - c[0]), c[0], c[4]))
    usages = []
    claimed = set()
    for pos, end, std_name, surface, is_alias in candidates:
        if any(s <= pos < e or s < end <= e for s, e in claimed):
            continue
        rest = text[end:end + 4]
        if is_alias and rest and (any(rest.startswith(s) for s in _DERIVATION_SUFFIXES)
                                  or rest[:1] in _SINGLE_SUFFIXES):
            continue
        if is_alias and rest.startswith("会") and pos > 0 \
                and text[pos - 1] in _PRECEDING_NAME_CHARS:
            continue
        claimed.add((pos, end))
        ctx = text[max(0, pos - 12):min(len(text), end + 12)].replace("\n", " ")
        usages.append({"surface": surface, "standard": std_name,
                       "is_standard": not is_alias, "position": pos,
                       "context": ctx[:60]})
    usages.sort(key=lambda u: u["position"])
    return usages


def collect_files(d, recursive=False):
    it = d.rglob("*") if recursive else d.iterdir()
    return sorted(f for f in it
                  if f.is_file() and f.suffix.lower() in (".txt", ".md", ".docx")
                  and f.stat().st_size < 5 * 1024 * 1024)


def analyze(dir_path, recursive=False, bank_path=None):
    from docx_text import read_text_any
    files = collect_files(Path(dir_path), recursive)
    if len(files) < 2:
        print("目录内有效文稿不足 2 份（txt/md/docx）——跨文件一致性需要至少两份文稿。",
              file=sys.stderr)
        sys.exit(2)  # 退出码契约：输入错误=2
    per_file = []
    variant_map = {}  # standard → {surface → set(files)}
    for f in files:
        try:
            text = read_text_any(f)
        except Exception as e:
            per_file.append({"file": f.name, "error": str(e)[:120]})
            continue
        usages = scan_usages(text, bank_path)
        per_file.append({"file": f.name, "usages": usages,
                         "nonstandard": sum(1 for u in usages if not u["is_standard"])})
        for u in usages:
            variant_map.setdefault(u["standard"], {}).setdefault(u["surface"], set()).add(f.name)
    matrix = []
    for std in sorted(variant_map):
        variants = {s: sorted(fs) for s, fs in variant_map[std].items()}
        inconsistent = len(variants) > 1
        # 不一致时判定推荐写法：标准名在场→推荐标准名；否则推荐出现文件最多的写法
        if inconsistent:
            if std in variants:
                recommend, basis = std, "库标准名"
            else:
                recommend = max(variants, key=lambda s: len(variants[s]))
                basis = "出现文件最多（库标准名未出现）"
        else:
            recommend, basis = None, None
        matrix.append({"concept": std, "variants": variants,
                       "inconsistent": inconsistent,
                       "recommend": recommend, "basis": basis})
    n_incons = sum(1 for m in matrix if m["inconsistent"])
    return {"directory": str(dir_path), "files": [p["file"] for p in per_file],
            "per_file": per_file, "matrix": matrix,
            "aggregate": {"files": len(files),
                          "concepts_seen": len(matrix),
                          "inconsistent_concepts": n_incons,
                          "nonstandard_total": sum(p.get("nonstandard", 0)
                                                   for p in per_file)},
            "integrity_notice": _INTEGRITY}


def print_text(r):
    agg = r["aggregate"]
    print(f"多文档术语一致性: {agg['files']} 份文稿 ｜ 库内概念 {agg['concepts_seen']} 个"
          f" ｜ 跨文件不一致 {agg['inconsistent_concepts']} 个"
          f" ｜ 非标准用法合计 {agg['nonstandard_total']}")
    print("─" * 56)
    for m in r["matrix"]:
        if not m["inconsistent"]:
            continue
        vs = "；".join(f"「{s}」@ {','.join(fs)}" for s, fs in m["variants"].items())
        print(f"◆ {m['concept']}：{vs}")
        print(f"  建议统一为「{m['recommend']}」（依据：{m['basis']}）")
    if not agg["inconsistent_concepts"]:
        print("✓ 未发现跨文件写法不一致。")
    err = [p for p in r["per_file"] if "error" in p]
    for p in err:
        print(f"  [错误] {p['file']}: {p['error'][:50]}")
    print("─" * 56)
    print("边界：一致性只覆盖库内概念（库外写法不可见，可配合 term_check --neologism）；"
          "统一建议以库标准名为准，取舍由作者定夺。")


_CSS = """body{font-family:-apple-system,'PingFang SC',sans-serif;margin:24px;color:#222;max-width:1000px}
h1{font-size:20px}h2{font-size:16px;margin-top:24px}
table{border-collapse:collapse;width:100%;font-size:13px;margin-top:10px}
th,td{border:1px solid #ddd;padding:5px 8px;text-align:left;vertical-align:top}
th{background:#f5f5f5}.bad{background:#fdecea}.ok{background:#eef7ee}
.note{color:#777;font-size:12px;margin-top:14px}.decl{border:1px solid #e8d9a0;background:#fdf9ec;border-radius:6px;padding:10px 14px;font-size:13px}"""


def render_html(r, out_path):
    rows = []
    for m in r["matrix"]:
        if not m["inconsistent"]:
            continue
        cells = "".join(
            f"<td>{html.escape(s)}<br><span style='color:#888'>{html.escape(','.join(fs))}</span></td>"
            for s, fs in m["variants"].items())
        rows.append(f"<tr class='bad'><td><b>{html.escape(m['concept'])}</b></td>{cells}"
                    f"<td>统一为「{html.escape(m['recommend'])}」<br><span style='color:#888'>{html.escape(m['basis'])}</span></td></tr>")
    ok_rows = [m for m in r["matrix"] if not m["inconsistent"]]
    ok_html = ""
    if ok_rows:
        ok_html = ("<h2>一致概念（" + str(len(ok_rows)) + "）</h2><table><tr><th>概念</th><th>写法</th></tr>"
                   + "".join(f"<tr class='ok'><td>{html.escape(m['concept'])}</td>"
                             f"<td>{html.escape('／'.join(m['variants']))}</td></tr>" for m in ok_rows)
                   + "</table>")
    agg = r["aggregate"]
    out_path.write_text(
        f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><title>多文档术语一致性</title>
<style>{_CSS}</style></head><body>
<h1>多文档术语一致性报告</h1>
<p>{agg['files']} 份文稿 ｜ 库内概念 {agg['concepts_seen']} 个 ｜ 跨文件不一致 <b style="color:#c0392b">{agg['inconsistent_concepts']}</b> 个 ｜ 非标准用法合计 {agg['nonstandard_total']}</p>
<h2>跨文件不一致（{agg['inconsistent_concepts']}）</h2>
<table><tr><th>概念</th><th colspan="99">写法 @ 文件</th><th>统一建议</th></tr>
{''.join(rows) or '<tr><td colspan=3>✓ 未发现</td></tr>'}</table>
{ok_html}
<div class="decl" style="margin-top:18px">{_INTEGRITY}</div>
<p class="note">Paper Polisher Pro · 多文档术语一致性 · 诚信声明为报告组成部分</p>
</body></html>""", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="多文档术语一致性（跨文件写法矩阵+统一建议）")
    ap.add_argument("directory", help="章节目录（≥2 份 txt/md/docx）")
    ap.add_argument("--recursive", action="store_true", help="递归子目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON（stdout 或 --output）")
    ap.add_argument("--output", metavar="PATH", help="JSON 落盘路径")
    ap.add_argument("--html", metavar="PATH", help="HTML 矩阵报告落盘路径")
    ap.add_argument("--bank", metavar="PATH",
                    help="v7.1.0: 项目自定义术语库（JSON，格式同内置库）；与内置合并、同 cn 覆盖")
    a = ap.parse_args()
    d = Path(a.directory)
    if not d.is_dir():
        print(f"Error: not a directory: {a.directory}", file=sys.stderr)
        sys.exit(2)
    r = analyze(a.directory, a.recursive, bank_path=a.bank)
    if a.html:
        render_html(r, Path(a.html))
        print(f"HTML 矩阵报告: {a.html}", file=sys.stderr)
    if a.output:
        Path(a.output).write_text(json.dumps(r, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
        print(f"JSON 报告: {a.output}", file=sys.stderr)
    if a.json and not a.output:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif not a.output and not a.json:
        print_text(r)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
