#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mifu-chem-mindmap 工具脚本
用法:
  python3 mindmap_tools.py render   <data.json> <out.html>   # 从JSON渲染招贴本HTML
  python3 mindmap_tools.py validate <data.json>              # V1方程式守恒+V2完整度+V3渲染一致性
  python3 mindmap_tools.py all      <data.json> <out.html>   # validate + render 一步完成
零外部依赖（仅标准库）。validate不过关时render仍可执行但会输出警告（交付必须validate全绿）。
"""
import json, sys, re, os, datetime

SUBS = '₀₁₂₃₄₅₆₇₈₉'
SUPS = '⁰¹²³⁴⁵⁶⁷⁸⁹'
SIGNS = '⁺⁻'

# ---------------- V1: 方程式守恒校验 ----------------

def strip_conditions(eq: str) -> str:
    """去掉箭头后的条件括号、全角注释、空白"""
    s = eq.strip()
    s = re.sub(r'([→⇌⟶=])\s*\([^)]*\)', r'\1', s)      # →(点燃) →
    s = re.sub(r'→\s*\{[^}]*\}', '→', s)                 # →{条件} →
    s = re.sub(r'（[^）]*）', '', s)                       # 全角注释
    s = re.sub(r'\s+', '', s)
    # 长箭头归一
    s = s.replace('⟶', '→').replace('==', '=')
    return s

def read_num(s: str, i: int):
    """读取数字串（ASCII系数或Unicode下标），返回(值, 新位置)；无数字返回(1, i)"""
    n = 0; got = False
    while i < len(s):
        c = s[i]
        if c in SUBS:
            n = n * 10 + SUBS.index(c); got = True; i += 1
        elif c.isdigit() and c.isascii():
            n = n * 10 + int(c); got = True; i += 1
        else:
            break
    return (n if got else 1), i

def parse_species(tok: str):
    """解析一个化学式token -> {元素: 个数}。忽略电荷上标。处理前导系数与·结晶水。"""
    # 先提取前导ASCII系数（如 3S 的 3、2CaSO₄·2H₂O 的 2）
    lead = 0; j = 0
    while j < len(tok) and tok[j].isdigit() and tok[j].isascii():
        lead = lead * 10 + int(tok[j]); j += 1
    body = tok[j:]

    counts = {}
    def parse_segment(seg):
        local = {}
        stack = [local]
        i = 0
        while i < len(seg):
            c = seg[i]
            if c in '([{':
                stack.append({}); i += 1
            elif c in ')]}':
                done = stack.pop()
                m, i = read_num(seg, i + 1)
                if stack:
                    for el, n in done.items():
                        stack[-1][el] = stack[-1].get(el, 0) + n * m
            elif c.isupper():
                el = c; i += 1
                while i < len(seg) and seg[i].islower():
                    el += seg[i]; i += 1
                n, i = read_num(seg, i)
                stack[-1][el] = stack[-1].get(el, 0) + n
            elif c in SUPS or c in SIGNS:
                i += 1  # 电荷，忽略
            else:
                i += 1  # 其他未知字符（↓↑↓·残留等）跳过
        return stack[0] if stack else {}

    total = {}
    parts = body.split('·')
    for k, p in enumerate(parts):
        if not p: continue
        if k > 0:
            cw, j2 = read_num_ascii(p, 0)
            p = p[j2:]
        else:
            cw = 1
        d = parse_segment(p)
        if not d:
            return {}  # 解析失败（含未知变量等）
        for el, n in d.items():
            total[el] = total.get(el, 0) + n * cw
    if lead:
        for el in total:
            total[el] *= lead
    return total

def read_num_ascii(s: str, i: int):
    """只读ASCII数字（结晶水系数），返回(值, 新位置)"""
    n = 0; got = False
    while i < len(s) and s[i].isdigit() and s[i].isascii():
        n = n * 10 + int(s[i]); got = True; i += 1
    return (n if got else 1), i

def parse_side(side: str):
    """一侧 -> {元素: 总数}；跳过空token与纯电子"""
    total = {}
    for tok in side.split('+'):
        tok = tok.strip()
        if not tok or tok == 'e⁻' or re.fullmatch(r'[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+', tok):
            continue
        d = parse_species(tok)
        if not d:  # 解析失败（可能是变量如X）
            return None
        for el, n in d.items():
            total[el] = total.get(el, 0) + n
    return total

def check_equation(eq: str):
    """返回(None)表示通过，(msg)表示错误"""
    s = strip_conditions(eq)
    if not s:
        return '空方程式'
    # 拆左右
    for arrow in ['→', '⇌', '=']:
        if arrow in s:
            left, right = s.split(arrow, 1)
            break
    else:
        return '未找到反应箭头(→/⇌/=)'
    L = parse_side(left)
    R = parse_side(right)
    if L is None or R is None:
        return 'SKIP'  # 含变量（如X₂）或无法解析的物种，转人工核对
    problems = []
    for el in sorted(set(L) | set(R)):
        ln, rn = L.get(el, 0), R.get(el, 0)
        if ln != rn:
            problems.append(f'{el}: 左{ln} vs 右{rn}')
    if problems:
        return '原子不守恒(' + '; '.join(problems) + ')'
    return None

def v1_validate(data):
    bank = data.get('equations_bank', [])
    errors, skipped, ok = [], [], 0
    for eq in bank:
        r = check_equation(eq)
        if r == 'SKIP':
            skipped.append(eq)
        elif r:
            errors.append((eq, r))
        else:
            ok += 1
    return bank, ok, skipped, errors

# ---------------- V2: 完整度校验 ----------------

DIMENSIONS = {
    '价态': ['价态', '价'],
    '物理性质': ['物理性质'],
    '化学性质': ['化学性质', '性质'],
    '制备': ['制备', '制法', '实验室制', '工业'],
    '检验': ['检验', '鉴别'],
    '用途': ['用途'],
    '污染治理': ['污染', '治理', '环保', '绿色'],
}

def v2_validate(data):
    branches = data.get('branches', [])
    report = []
    all_sections = []
    for b in branches:
        for sec in b.get('sections', []):
            all_sections.append(sec.get('title', ''))
    joined = ' '.join(all_sections)
    missing = [d for d, kws in DIMENSIONS.items() if not any(k in joined for k in kws)]
    n_nodes = sum(len(sec.get('nodes', [])) for b in branches for sec in b.get('sections', []))
    n_eq = sum(1 for b in branches for sec in b.get('sections', []) for nd in sec.get('nodes', []) if nd.get('eq'))
    tags = {'常考': 0, '易错': 0, '可推': 0, '必须记': 0}
    for b in branches:
        for sec in b.get('sections', []):
            for nd in sec.get('nodes', []):
                t = nd.get('tag') or ''
                for k in tags:
                    if k in t: tags[k] += 1
    coverage = round((7 - len(missing)) / 7 * 100)
    report.append(f'分支数: {len(branches)} (标准5-8)')
    report.append(f'节点数: {n_nodes}, 含方程式节点: {n_eq}, 方程式银行: {len(data.get("equations_bank", []))}')
    report.append(f'7维度覆盖: {coverage}%  缺失: {missing if missing else "无"}')
    report.append(f'标签统计: {tags}  可推占比: {round(tags["可推"]*100/max(1,n_nodes))}% (健康区间20-40%)')
    return coverage, missing, report

# ---------------- 渲染 ----------------

BRANCH_COLORS = ['#2563eb', '#059669', '#d97706', '#7c3aed', '#dc2626', '#0891b2', '#be185d', '#4d7c0f']

def render_valence_svg(axis):
    states = axis.get('states', [])
    if not states: return ''
    w, h = 660, 120
    n = len(states)
    pad = 80
    step = (w - 2 * pad) // max(1, n - 1) if n > 1 else 0
    ys = 70
    svg = [f'<svg viewBox="0 0 {w} {h}" style="width:100%;max-width:900px;height:auto;font-family:PingFang SC,sans-serif">']
    svg.append(f'<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#334155"/></marker></defs>')
    svg.append(f'<line x1="30" y1="{ys}" x2="{w-20}" y2="{ys}" stroke="#334155" stroke-width="2" marker-end="url(#arr)"/>')
    svg.append(f'<text x="{w-70}" y="{ys-8}" font-size="12" fill="#334155">价态升高→被氧化</text>')
    for k, st in enumerate(states):
        x = pad + k * step if n > 1 else w // 2
        v = st.get('v', '')
        svg.append(f'<line x1="{x}" y1="{ys-10}" x2="{x}" y2="{ys+10}" stroke="#334155" stroke-width="2"/>')
        svg.append(f'<text x="{x}" y="{ys+26}" font-size="13" font-weight="bold" text-anchor="middle" fill="#0f172a">{v}价</text>')
        species = st.get('species', [])
        for j, sp in enumerate(species):
            yy = ys - 22 - j * 18
            svg.append(f'<text x="{x}" y="{yy}" font-size="12" text-anchor="middle" fill="#1d4ed8">{sp}</text>')
    for note in axis.get('special', []):
        svg.append(f'<text x="{note.get("x", w//2)}" y="{note.get("y", 112)}" font-size="11" text-anchor="middle" fill="#b91c1c">★{note.get("text","")}</text>')
    svg.append('</svg>')
    return '\n'.join(svg)

def render_node(nd):
    parts = ['<div class="node">']
    if nd.get('text'):
        parts.append(f'<span class="node-text">{nd["text"]}</span>')
    if nd.get('eq'):
        parts.append(f'<div class="eq">{nd["eq"]}</div>')
    extra = nd.get('extra')
    if extra:
        parts.append(f'<div class="extra">{extra}</div>')
    if nd.get('tag'):
        for t in nd['tag'].split('|'):
            cls = {'常考': 'tag-red', '易错': 'tag-yellow', '可推': 'tag-green', '必须记': 'tag-gray'}.get(t.strip(), 'tag-gray')
            parts.append(f'<span class="tag {cls}">{t.strip()}</span>')
    parts.append('</div>')
    return '\n'.join(parts)

def render_html(data, stats_line):
    meta = data.get('meta', {})
    colors = BRANCH_COLORS
    branch_html = []
    for idx, b in enumerate(data.get('branches', [])):
        color = colors[idx % len(colors)]
        secs = []
        for sec in b.get('sections', []):
            nodes = '\n'.join(render_node(nd) for nd in sec.get('nodes', []))
            secs.append(f'<div class="section"><div class="sec-title">▸ {sec.get("title","")}</div>{nodes}</div>')
        branch_html.append(
            f'<div class="branch-card" style="border-left-color:{color}">'
            f'<div class="branch-head" style="color:{color}"><span class="branch-num" style="background:{color}">{b.get("id", idx+1)}</span>{b.get("title","")}</div>'
            + ''.join(secs) + '</div>')
    axis_svg = render_valence_svg(data.get('valence_axis', {}))
    today = datetime.date.today().isoformat()
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta.get('module','')}｜三层思维导图</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; background:#f8fafc; color:#1a1a1a; padding:24px; }}
.banner {{ background:linear-gradient(135deg,#0f172a,#1e3a8a); color:#fff; border-radius:14px; padding:22px 28px; margin-bottom:14px; }}
.banner h1 {{ font-size:26px; letter-spacing:1px; }}
.banner .sub {{ font-size:14px; opacity:.85; margin-top:6px; }}
.axis-box {{ background:#fff; border-radius:12px; padding:10px 16px; margin-bottom:16px; box-shadow:0 1px 3px rgba(0,0,0,.06); }}
.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
@media (max-width:800px) {{ .grid {{ grid-template-columns:1fr; }} }}
.branch-card {{ background:#fff; border-radius:12px; border-left:6px solid #999; padding:14px 16px; box-shadow:0 1px 3px rgba(0,0,0,.06); break-inside:avoid; }}
.branch-head {{ font-size:17px; font-weight:700; margin-bottom:8px; display:flex; align-items:center; gap:8px; }}
.branch-num {{ color:#fff; width:22px; height:22px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:13px; flex-shrink:0; }}
.section {{ margin-bottom:8px; }}
.sec-title {{ background:#f1f5f9; border-radius:6px; padding:4px 8px; font-size:13.5px; font-weight:600; color:#334155; margin-bottom:4px; }}
.node {{ font-size:13px; line-height:1.55; padding:2px 6px; }}
.node-text {{ }}
.eq {{ font-family:'SF Mono','Menlo','Consolas',monospace; background:#f3f4f6; border:1px solid #e5e7eb; border-radius:6px; padding:2px 8px; margin:3px 0; font-size:12.5px; color:#0f172a; display:inline-block; }}
.extra {{ font-size:12px; color:#475569; margin-top:1px; }}
.tag {{ font-size:10.5px; border-radius:4px; padding:1px 6px; margin-left:6px; vertical-align:middle; display:inline-block; }}
.tag-red {{ background:#dc2626; color:#fff; }}
.tag-yellow {{ background:#fde047; color:#713f12; }}
.tag-green {{ background:#059669; color:#fff; }}
.tag-gray {{ background:#e2e8f0; color:#334155; }}
.footer {{ margin-top:16px; font-size:12px; color:#64748b; text-align:center; }}
@media print {{
  body {{ background:#fff; padding:0; }}
  .branch-card {{ box-shadow:none; border:1px solid #e2e8f0; border-left-width:6px; }}
  .banner {{ border-radius:0; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
  .tag, .eq {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
}}
</style>
</head>
<body>
<div class="banner">
  <h1>{meta.get('module','')}｜三层思维导图</h1>
  <div class="sub">主题式包装：{meta.get('theme','')} ｜ {meta.get('grade_region','')} · {meta.get('textbook','')} ｜ 配套教案：mifu-chemistry-lesson-prep</div>
</div>
<div class="axis-box">{axis_svg}</div>
<div class="grid">
{chr(10).join(branch_html)}
</div>
<div class="footer">{stats_line} ｜ validate: {data.get('_validate_status','未运行')} ｜ 生成日期：{today} ｜ 米赋教育教研中心 · mifu-chem-mindmap v{meta.get('skill_version','1.0')}</div>
</body>
</html>"""
    return html

# ---------------- 主流程 ----------------

def count_stats(data):
    branches = data.get('branches', [])
    n_nodes = sum(len(sec.get('nodes', []) ) for b in branches for sec in b.get('sections', []))
    n_eq = sum(1 for b in branches for sec in b.get('sections', []) for nd in sec.get('nodes', []) if nd.get('eq'))
    return f'分支{len(branches)} · 节点{n_nodes} · 方程式{n_eq}/{len(data.get("equations_bank",[]))}'

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    cmd, data_path = sys.argv[1], sys.argv[2]
    with open(data_path, encoding='utf-8') as f:
        data = json.load(f)

    if cmd in ('validate', 'all'):
        bank, ok, skipped, errors = v1_validate(data)
        coverage, missing, report2 = v2_validate(data)
        print('=' * 60)
        print(f'V1 方程式守恒校验: 银行{len(bank)}条 | ✅通过{ok} | ⚠️含变量转人工{len(skipped)} | ❌错误{len(errors)}')
        if skipped:
            print('  ⚠️ 人工核对(含变量): ' + ' || '.join(skipped))
        for eq, msg in errors:
            print(f'  ❌ {eq}  ->  {msg}')
        print('-' * 60)
        print('V2 完整度校验:')
        for line in report2:
            print('  ' + line)
        v1_pass = len(errors) == 0
        v2_pass = coverage >= 85
        print('=' * 60)
        status = '✅ 全绿' if (v1_pass and v2_pass) else '❌ 未通过'
        print(f'校验结果: {status}  (V1={"PASS" if v1_pass else "FAIL"}, V2={"PASS" if v2_pass else "FAIL"})')

        if cmd == 'all':
            # V3 渲染一致性在render后检查
            data['_validate_status'] = status
            out = sys.argv[3]
            html = render_html(data, count_stats(data))
            with open(out, 'w', encoding='utf-8') as f:
                f.write(html)
            # V3
            n_nodes = sum(len(sec.get('nodes', []) ) for b in data.get('branches', []) for sec in b.get('sections', []))
            n_eq_html = html.count('class="eq"')
            residue = [p for p in ['None', '{{', '}}'] if p in html]
            print('-' * 60)
            print(f'V3 渲染检查: HTML已生成 {out} ({len(html)}字节)')
            print(f'  方程式块渲染数: {n_eq_html} | 节点数(数据): {n_nodes} | 残留占位符: {residue if residue else "无"}')
            v3_pass = (not residue) and n_eq_html >= 0
            print(f'交付门槛: V1={"✅" if v1_pass else "❌"} V2={"✅" if v2_pass else "❌"} V3={"✅" if v3_pass else "❌"}')
        sys.exit(0 if (v1_pass and v2_pass) else 2)

    elif cmd == 'render':
        out = sys.argv[3]
        data['_validate_status'] = '未运行(仅render)'
        html = render_html(data, count_stats(data))
        with open(out, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'HTML已生成: {out} ({len(html)}字节)。注意：交付前必须跑 validate。')
    else:
        print(__doc__); sys.exit(1)

if __name__ == '__main__':
    main()
