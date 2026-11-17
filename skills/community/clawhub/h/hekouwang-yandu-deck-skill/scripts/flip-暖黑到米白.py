#!/usr/bin/env python3
"""暖黑 #161514 → 米白 #faf9f5（同为 V2 黏土系统的明暗两极）

映射源 = 两套引擎模板 deck-engine-{暖黑,米白}.html 的 :root 逐 token 对照（不是手编）。
铁律：单遍同时替换 —— 源集与目标集有交集（#f4f2eb 既是源又是目标），
      顺序 sed 会把前一条写出的颜色被后一条再吃一次。
"""
import re, sys, pathlib

# ── 20 个 token 值映射（暖黑 → 米白），抽自引擎模板 :root ──
TOKENS = {
    '#161514': '#faf9f5',  # --bg
    '#221f1d': '#ffffff',  # --surface
    '#1b1917': '#f4f2eb',  # --surface2
    '#2a2623': '#efece3',  # --surfaceHi
    '#f4f2eb': '#1a1a18',  # --text      ← 同时是 --surface2 的目标，故必须单遍
    '#cdc8bd': '#56544e',  # --read
    '#aea99f': '#6b685f',  # --text2
    '#948e84': '#8a877e',  # --text3
    '#5f5a52': '#a8a49a',  # --text4
    '#e08a5f': '#c15f3c',  # --hot   黏土
    '#efb79b': '#a84f30',  # --hot2
    '#f6e1d1': '#9a4a2c',  # --hl0
    '#8fa6bd': '#5c6b7a',  # --cool  石板蓝
    '#aec2d4': '#48555f',  # --cool2
    '#c8896f': '#a07a3c',  # --ochre 赭石
    '#dcab8e': '#8a6a32',  # --ochre2
    '#e0795f': '#c0392b',  # --warn
}
# ── 正文/SVG 里的裸色，映射表未覆盖但需随亮底翻（同族归并）──
EXTRA = {
    '#f4ddcb': '#9a4a2c',  # 图表高亮文字（≈--hl0 家族，暗底浅桃 → 亮底深黏土）
    '#c6c2b7': '#56544e',  # 图表正文文字（≈--read 家族）
}
# ── 线/辉光的 rgba 基色（暖黑用浅色描线，米白用深色）──
RGBA = {
    'rgba(244,242,235,': 'rgba(20,20,19,',
}
# ── 刻意不翻（讲者私窗 #pmode / 终端 .shell 本就该是深底）──
KEEP_DARK = ['#0c0d10', '#ececf2', '#9a9aac', '#6c6c7e', '#7c7c8e', '#b6b6c6', '#1f1d1b']

MAP = {**TOKENS, **EXTRA}


def flip(html: str) -> str:
    # 单遍：一个大 alternation，一次扫过，绝不二次命中
    keys = sorted(MAP, key=len, reverse=True)
    pat = re.compile('|'.join(re.escape(k) for k in keys), re.I)
    out = pat.sub(lambda m: MAP[m.group(0).lower()], html)
    for a, b in RGBA.items():
        out = out.replace(a, b)
    # data-URI 里 URL 编码的 #（%23xxxxxx）
    for a, b in MAP.items():
        out = out.replace('%23' + a[1:], '%23' + b[1:])
    # 主题标记 + 颗粒混合模式（亮底用 multiply，暗底用 screen）
    out = out.replace('class="dark"', 'class="light"')
    out = re.sub(r'(\.grain\{[^}]*?mix-blend-mode:)\s*screen', r'\1multiply', out)
    return out


def scan_uncovered(html: str) -> set:
    """报出映射表没覆盖、也不在「刻意保留」名单里的裸色 —— 交人工判断"""
    m = re.search(r':root\{.*?\n\s*\}', html, re.S)
    body = html[:m.start()] + html[m.end():] if m else html
    found = {c.lower() for c in re.findall(r'#[0-9a-fA-F]{6}\b', body)}
    return found - set(MAP) - {k.lower() for k in KEEP_DARK} - set(MAP.values())


if __name__ == '__main__':
    files = [pathlib.Path(p) for p in sys.argv[1:]]
    if not files:
        sys.exit('用法: flip_black_to_cream.py <html>...')

    # ① 先全量扫「未覆盖色」，有就停下来问人，别闷头转
    problems = {}
    for p in files:
        u = scan_uncovered(p.read_text())
        if u:
            problems[p.name] = u
    if problems:
        print('⚠️ 以下裸色映射表未覆盖，需人工判断后再跑：')
        for n, u in problems.items():
            print(f'   {n}: {", ".join(sorted(u))}')
        sys.exit(2)
    print('✓ 全部裸色均已覆盖或在保留名单内')

    # ② 先读后写（src==dst 时 open(w) 会先截空 —— 踩过，9 期全毁）
    for p in files:
        data = p.read_text()
        out = flip(data)
        p.write_text(out)
        size = p.stat().st_size
        bg = re.search(r'--bg:(#[0-9a-fA-F]{6})', out)
        assert size > 0, f'{p} 写成了空文件！'
        print(f'  ✓ {p.parent.name[:28]:<30} {bg.group(1) if bg else "?"}  {size}字节')
