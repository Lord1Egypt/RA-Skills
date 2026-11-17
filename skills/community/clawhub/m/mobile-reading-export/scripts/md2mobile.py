# -*- coding: utf-8 -*-
"""命理档案 Markdown -> 手机优先响应式 HTML 转换器。

设计要点
- 单文件、零外部依赖（仅系统字体栈），离线可读。
- 表格在窄屏全部转卡片：四柱表 -> 4 张竖排卡；键值表 -> 小标签 + 正文两行式；
  多列表 -> 标题卡（col1 作标题、col2 作副标题、其余作字段）。
- 亮/暗色自适应；打印时强制亮色并套手机比例分页（@page）。
用法：python md2mobile.py <in.md> <out.html> [notice]
"""
import re
import sys
import json

PAGE_W_MM = 104      # 393 CSS px，等于 iPhone 视口宽度
PAGE_H_MM = 225      # 850 CSS px，等于 iPhone 视口高度
PAGE_PAD_MM = 5      # 5mm x 2 + 正文 355px ≈ 手机正文宽 357px

CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#f6f3fb;--paper:#fdfcff;--surface:#fbf9fe;--surface2:#f0edf8;--border:#ded7eb;
  --text:#3d315b;--text2:#6f6880;--text3:#a39ab1;
  --accent:#3b2d70;--accent-soft:#f1ecfb;--accent-line:#d5c8e8;
  --gold:#b77b2e;--gold-soft:#fff7e8;--gold-line:#e7c98e;
  --warn-bg:#fff6e7;--warn-tx:#966321;--warn-bd:#eed29f;
  --ok-bg:#edf7f0;--ok-tx:#3c7655;--ok-bd:#c7e6d0;
  --no-bg:#fbedef;--no-tx:#9a4c58;--no-bd:#edc9d0;
  --info-bg:#eef5fb;--info-tx:#4b7195;--info-bd:#cbddea;
  --gray-bg:#f3f0f6;--gray-tx:#776f83;--gray-bd:#ded8e6;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#1e1730;--paper:#28203d;--surface:#30264a;--surface2:#3b3155;--border:#51466a;
    --text:#f8f1ff;--text2:#d4c9e0;--text3:#a79bb8;
    --accent:#d9c2ff;--accent-soft:#3b2d55;--accent-line:#715b8a;
    --gold:#e9bb71;--gold-soft:#4a3823;--gold-line:#8c6a36;
    --warn-bg:#4a3823;--warn-tx:#f1c875;--warn-bd:#82652f;
    --ok-bg:#294536;--ok-tx:#a5d8b8;--ok-bd:#507b60;
    --no-bg:#4b2934;--no-tx:#f0acba;--no-bd:#815362;
    --info-bg:#2b4256;--info-tx:#b4d5ee;--info-bd:#55758e;
    --gray-bg:#382f43;--gray-tx:#d0c2d9;--gray-bd:#5a4c67;
  }
}
html,body{margin:0;padding:0;background:var(--bg)}
body{
  color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Helvetica Neue",sans-serif;
  font-size:17px;line-height:1.78;
  -webkit-text-size-adjust:100%;
  text-rendering:optimizeLegibility;
}
.wrap{max-width:720px;margin:0 auto;padding:38px 24px 64px;background:var(--paper)}
h1{font-family:"Noto Serif CJK SC","Source Han Serif SC","Songti SC","STSong","SimSun",serif;
   font-size:31px;line-height:1.18;font-weight:600;margin:0 0 14px;letter-spacing:-.6px;color:var(--accent)}
h1::first-letter{font-size:1.06em}
h2{display:block;font-size:21px;font-weight:600;margin:46px 0 15px;padding:0 0 15px;
   border-top:1px solid var(--border);border-bottom:1px solid var(--border);line-height:1.35;
   letter-spacing:.1px;color:var(--accent)}
h1+h2,h1+p+h2{margin-top:28px}
h3{font-family:"Noto Serif CJK SC","Source Han Serif SC","Songti SC","STSong","SimSun",serif;
   font-size:18px;font-weight:600;margin:30px 0 11px;color:var(--accent)}
p{margin:0 0 14px}
hr{border:0;border-top:1px solid var(--border);margin:30px 0}
strong{font-weight:600;color:var(--accent)}
em{font-style:normal;color:var(--text2)}
.hero{position:relative;padding:0 0 24px;margin-bottom:20px;border-bottom:1px solid var(--border)}
.hero::before{content:"PERSONAL READING · STRUCTURED NOTE";display:block;margin:0 0 15px;font-size:10px;line-height:1.3;letter-spacing:2px;color:var(--gold);font-weight:700}
.hero::after{content:"";display:block;width:52px;height:2px;margin-top:18px;background:var(--gold)}
.hero + p{font-size:13px;line-height:1.75;color:var(--text2);margin-bottom:13px}
.hero + p strong{color:var(--gold)}
.hero + p + p{font-family:"Noto Serif CJK SC","Source Han Serif SC","Songti SC","STSong","SimSun",serif;font-size:16px;line-height:1.7;color:var(--text2);max-width:620px}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
     font-size:.88em;background:var(--surface2);padding:1px 5px;border-radius:4px;
     color:var(--accent);word-break:break-all}
ul,ol{margin:0 0 14px;padding-left:22px}
li{margin:0 0 9px}
li::marker{color:var(--text3)}

.meta{list-style:none;margin:0 0 20px;padding:0;font-size:14px;color:var(--text2);line-height:1.65}
.meta li{margin:0 0 4px}
.lead{font-size:15px;color:var(--text2);line-height:1.72;margin:0 0 17px;
      padding:14px 16px;background:var(--surface);border:1px solid var(--border);border-radius:14px}
.lead b{color:var(--text);font-weight:700}

.notice{display:inline-block;font-size:12px;color:var(--accent);
        border:1px solid var(--accent-line);border-radius:999px;background:var(--accent-soft);
        padding:3px 11px;margin:0 0 18px}

.note{background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--gold);
      border-radius:0;padding:15px 17px;margin:0 0 20px;font-size:15px}
.note p:last-child{margin-bottom:0}
.note .note-title{font-weight:600;color:var(--accent);margin:0 0 8px;font-size:15px}

.kv{margin:0 0 20px}
.kvrow{padding:11px 0;border-bottom:1px solid var(--border)}
.kvrow:first-child{border-top:1px solid var(--border)}
.kv dt{font-size:12.5px;color:var(--text3);margin:0 0 2px;letter-spacing:.2px}
.kv dd{margin:0;font-size:16.5px;line-height:1.62}

.section-kicker{margin:34px 0 7px;color:var(--gold);font-size:10px;line-height:1.3;
               letter-spacing:2px;font-weight:700;text-transform:uppercase}
.section-kicker + h2{margin-top:0}
.pillars{display:grid;grid-template-columns:1fr;gap:0;margin:0 0 24px}
.pillar{border:0;border-top:1px solid var(--border);border-radius:0;padding:16px 0;background:transparent}
.pillar:last-child{border-bottom:1px solid var(--border)}
.pname{font-family:"Noto Serif CJK SC","Source Han Serif SC","Songti SC","STSong","SimSun",serif;
       font-size:16px;color:var(--accent);font-weight:600;letter-spacing:.3px;margin:0 0 9px}
.prow{display:flex;gap:10px;padding:6px 0;border-top:1px solid var(--border);font-size:15px}
.prow:first-of-type{border-top:0}
.pl{flex:0 0 80px;color:var(--text3);font-size:12.5px;line-height:1.9}
.pv{flex:1;min-width:0;line-height:1.6;word-break:break-word}
.prow.hero .pv{font-size:20px;font-weight:700;letter-spacing:1px;color:var(--accent)}
.prow.hero .pl{line-height:2.1}

.rows{margin:0 0 22px}
.row{border:0;border-bottom:1px solid var(--border);border-radius:0;padding:15px 0;
     margin:0; background:transparent;break-inside:avoid}
.row:first-child{border-top:1px solid var(--border)}
.row.cur{border:1px solid var(--accent-line);border-radius:0;padding:15px 16px;margin:5px 0;background:var(--accent-soft)}
.rhead{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin:0 0 9px}
.rtitle{font-family:"Noto Serif CJK SC","Source Han Serif SC","Songti SC","STSong","SimSun",serif;
        font-size:17px;font-weight:700;margin:0;color:var(--text)}
.row.cur .rtitle{color:var(--accent)}
.rsub{font-size:14px;color:var(--text2)}
.rfield{display:flex;gap:10px;padding:5px 0;border-top:1px solid var(--border);font-size:14.5px}
.rfield:first-of-type{border-top:1px solid var(--border)}
.rl{flex:0 0 80px;color:var(--text3);font-size:12.5px;line-height:1.85}
.rv{flex:1;min-width:0;line-height:1.62;word-break:break-word}
.rv.long{font-size:14px;color:var(--text2)}

.chip{display:inline-block;font-size:12.5px;font-weight:600;line-height:1.5;
      padding:2px 9px;border-radius:999px;border:1px solid transparent;white-space:nowrap}
.chip-ok{background:var(--ok-bg);color:var(--ok-tx);border-color:var(--ok-bd)}
.chip-no{background:var(--no-bg);color:var(--no-tx);border-color:var(--no-bd)}
.chip-warn{background:var(--warn-bg);color:var(--warn-tx);border-color:var(--warn-bd)}
.chip-info{background:var(--info-bg);color:var(--info-tx);border-color:var(--info-bd)}
.chip-gray{background:var(--gray-bg);color:var(--gray-tx);border-color:var(--gray-bd)}

.disclaimer{font-size:13px;color:var(--text3);line-height:1.75;
            border-top:1px solid var(--border);padding-top:17px;margin-top:34px}

/* 参考截图的“信息层级”做法：彩色标签只标状态，不把每行都做成卡片 */
.rfield .chip{vertical-align:middle}
.kvrow dd code,.rfield code{background:var(--surface2);color:var(--accent)}
.stamp{font-size:9px;letter-spacing:.8px;color:var(--text3)}

@media (min-width:900px){
  .wrap{max-width:760px;padding-left:34px;padding-right:34px}
  .pillars{grid-template-columns:repeat(2,1fr);column-gap:34px}
  .pillar:last-child{border-bottom:1px solid var(--border)}
  .kvrow,.rfield{align-items:baseline}
  .pl{flex-basis:88px}
  .rl{flex-basis:96px}
}

@page{size:""" + f"{PAGE_W_MM}mm {PAGE_H_MM}mm" + """;margin:""" + f"{PAGE_PAD_MM}mm" + """}
@media print{
  :root{
    --bg:#ffffff;--paper:#fdfcff;--surface:#fbf9fe;--surface2:#f0edf8;--border:#ded7eb;
    --text:#3d315b;--text2:#6f6880;--text3:#9389a3;
    --accent:#3b2d70;--accent-soft:#f1ecfb;--accent-line:#d5c8e8;
    --gold:#a97029;--gold-soft:#fff7e8;--gold-line:#e1c38b;
    --warn-bg:#fff6e7;--warn-tx:#966321;--warn-bd:#eed29f;
    --ok-bg:#edf7f0;--ok-tx:#3c7655;--ok-bd:#c7e6d0;
    --no-bg:#fbedef;--no-tx:#9a4c58;--no-bd:#edc9d0;
    --info-bg:#eef5fb;--info-tx:#4b7195;--info-bd:#cbddea;
    --gray-bg:#f3f0f6;--gray-tx:#776f83;--gray-bd:#ded8e6;
  }
  html,body{background:#fff !important}
  body{font-size:15px;line-height:1.7}
  .wrap{max-width:none;margin:0;padding:0 0 18px;background:#fdfcff;border:0;border-radius:0;box-shadow:none}
  h1{font-size:23px}
  h2{font-size:17px;margin:22px 0 10px;padding:0 0 9px;break-after:avoid}
  h3{font-size:15px;margin:15px 0 8px;break-after:avoid}
  p{margin:0 0 9px}
  hr{margin:15px 0}
  .hero{padding:0 0 13px;margin-bottom:14px}
  .hero::before{font-size:9px;margin-bottom:6px;letter-spacing:1.5px}
  .hero::after{margin-top:10px;height:2px}
  .hero + p{font-size:11.5px}
  .hero + p + p{font-size:13.5px}
  .section-kicker{margin:20px 0 5px;font-size:9px;letter-spacing:1.5px}
  .section-kicker + h2{margin-top:0}
  .pillars{gap:0}
  .pillar{padding:10px 0;border-radius:0}
  .pname{font-size:13px}
  .prow{font-size:13.5px}
  .prow.hero .pv{font-size:17px}
  .row{padding:10px 0;margin:0}
  .row.cur{padding:10px 12px;margin:4px 0;border-radius:0}
  .kvrow{padding:8px 0}
  .kv dd{font-size:14.5px}
  .rfield{font-size:13px}
  .rv.long{font-size:12.5px}
  .note{padding:11px 13px;font-size:13.5px}
  .disclaimer{font-size:11.5px}
  .notice{font-size:11px}
  .lead{font-size:13px;padding:10px 12px}
  p,li{orphans:2;widows:2}
  h1,h2,h3{break-inside:avoid}
  .pillar,.kvrow,.note,.row{break-inside:avoid}
  /* 打印环境里 Chrome 会按窗口宽度而非页面宽度评估 min-width，
     这里显式钉死窄屏版式，避免桌面分栏规则漏进 PDF */
  .pillars{grid-template-columns:1fr !important}
  .pl{flex-basis:80px !important}
  .rl{flex-basis:80px !important}
  .stamp{position:fixed;bottom:1.5mm;left:0;right:0;text-align:center;
         font-size:9px;color:#9a9aa2;letter-spacing:.6px}
}
.stamp{display:none}
@media print{.stamp{display:block}}
"""


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def inline(s):
    s = esc(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', s)
    return s


def plain(s):
    return re.sub(r'[*`]', '', s).strip()


def split_row(line):
    r = line.strip()
    if r.startswith('|'):
        r = r[1:]
    if r.endswith('|'):
        r = r[:-1]
    return [c.strip() for c in r.split('|')]


def is_sep(cells):
    return all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c != '') and any(c for c in cells)


VERDICT_HEADERS = ('吉平慎', '标注', '评级', '可用性')

# 窄屏标签列只有约 76px（4 个汉字），过长的列名会折成两行，这里统一压缩
LABEL_MAP = {
    '地支藏干·十神': '藏干十神',
    '地支藏干十神': '藏干十神',
    '地支十神（藏干）': '地支十神',
    '关键刑冲合会': '刑冲合会',
    '五行／十神占比': '占比',
    '流年神煞': '流年神煞',
}


def short_label(s):
    s = plain(s)
    if s in LABEL_MAP:
        return LABEL_MAP[s]
    # 通用规则：标签列仅容 4 个汉字，带括注的列名先剥括注
    t = re.sub(r'[（(][^）)]*[）)]', '', s).strip()
    return t if len(t) >= 2 else s

CHIP_WORDS = {
    'chip-ok': ('吉', '宜', '可采信', '是', '顺'),
    'chip-no': ('慎', '避', '不采信', '否', '凶'),
    'chip-info': ('动',),
    'chip-warn': ('平中带吉', '吉中带耗', '吉中带波', '动中有吉', '平'),
}


def chip_class(text):
    t = plain(text)
    if t in ('是',):
        return 'chip-ok'
    if t.startswith('否') or t.startswith('不采信'):
        return 'chip-no'
    if '慎' in t and '吉' in t:
        return 'chip-warn'
    if t.startswith('慎'):
        return 'chip-no'
    if t.startswith('吉中') or t.startswith('动中有') or t.startswith('平中'):
        return 'chip-warn'
    if t.startswith('吉'):
        return 'chip-ok'
    if t.startswith('动'):
        return 'chip-info'
    if t.startswith('平'):
        return 'chip-gray'
    if t.startswith('可采信'):
        return 'chip-ok'
    if t.startswith('可直接采信'):
        return 'chip-ok'
    if t.startswith('口径依赖'):
        return 'chip-warn'
    return 'chip-gray'


def render_pillars(header, body):
    names = [plain(c) for c in header[1:]]
    cols = [[] for _ in names]
    for row in body:
        label = short_label(row[0]) if row else ''
        for i in range(len(names)):
            val = row[i + 1] if i + 1 < len(row) else ''
            if val:
                cols[i].append((label, val))
    out = ['<div class="pillars">']
    for i, nm in enumerate(names):
        out.append('<div class="pillar">')
        out.append(f'<div class="pname">{esc(nm)}</div>')
        for label, val in cols[i]:
            cls = 'prow hero' if label in ('干支',) else 'prow'
            out.append(f'<div class="{cls}"><span class="pl">{esc(label)}</span>'
                       f'<span class="pv">{inline(val)}</span></div>')
        out.append('</div>')
    out.append('</div>')
    return '\n'.join(out)


def render_kv(header, body):
    out = ['<dl class="kv">']
    for row in body:
        k = row[0] if row else ''
        v = row[1] if len(row) > 1 else ''
        out.append(f'<div class="kvrow"><dt>{esc(plain(k))}</dt>'
                   f'<dd>{inline(v)}</dd></div>')
    out.append('</dl>')
    return '\n'.join(out)


def render_rows(header, body):
    heads = [plain(h) for h in header]
    out = ['<div class="rows">']
    for row in body:
        title = plain(row[0]) if row else ''
        sub = plain(row[1]) if len(row) > 1 else ''
        cur = ' cur' if ('现行' in ' '.join(row) or '现年' in ' '.join(row)) else ''
        out.append(f'<article class="row{cur}">')
        out.append('<div class="rhead">')
        out.append(f'<h4 class="rtitle">{inline(title)}</h4>')
        if sub:
            if any(h in heads[1] for h in VERDICT_HEADERS):
                out.append(f'<span class="chip {chip_class(sub)}">{esc(sub)}</span>')
            else:
                out.append(f'<span class="rsub">{inline(sub)}</span>')
        out.append('</div>')
        for j in range(2, len(row)):
            if not row[j]:
                continue
            lab = short_label(heads[j]) if j < len(heads) else ''
            val = row[j]
            if any(h in lab for h in VERDICT_HEADERS) or lab == '吉平慎':
                out.append(f'<div class="rfield"><span class="rl">{esc(lab)}</span>'
                           f'<span class="rv"><span class="chip {chip_class(val)}">'
                           f'{esc(plain(val))}</span></span></div>')
            else:
                cls = 'rv long' if len(plain(val)) > 34 else 'rv'
                out.append(f'<div class="rfield"><span class="rl">{esc(lab)}</span>'
                           f'<span class="{cls}">{inline(val)}</span></div>')
        out.append('</article>')
    out.append('</div>')
    return '\n'.join(out)


def render_table(rows):
    cells = [split_row(r) for r in rows]
    cells = [c for c in cells if not is_sep(c)]
    if not cells:
        return ''
    header, body = cells[0], cells[1:]
    n = max(len(c) for c in cells)
    header = header + [''] * (n - len(header))
    body = [c + [''] * (n - len(c)) for c in body]
    if n == 1:
        return ''
    tail = [plain(h) for h in header[1:5]]
    if tail == ['年柱', '月柱', '日柱', '时柱']:
        return render_pillars(header, body)
    if n == 2:
        return render_kv(header, body)
    return render_rows(header, body)


def render_blocks(lines):
    out = []
    i = 0
    section_no = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        s = line.strip()
        if not s:
            i += 1
            continue
        if s == '---':
            # 紧接标题的分隔线与标题自身的上边框会叠成双线，此时略去分隔线
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip().startswith('#'):
                i += 1
                continue
            out.append('<hr>')
            i += 1
            continue
        if s.startswith('#'):
            lvl = len(s) - len(s.lstrip('#'))
            txt = s[lvl:].strip()
            if lvl == 1:
                out.append(f'<header class="hero"><h1>{inline(txt)}</h1></header>')
            elif lvl == 2:
                section_no += 1
                out.append(f'<div class="section-kicker">SECTION {section_no:02d}</div>')
                out.append(f'<h2>{inline(txt)}</h2>')
            else:
                out.append(f'<h{min(lvl,4)}>{inline(txt)}</h{min(lvl,4)}>')
            i += 1
            continue
        if s.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                t = lines[i].strip()
                t = t[1:]
                if t.startswith(' '):
                    t = t[1:]
                buf.append(t)
                i += 1
            inner = render_blocks(buf)
            if inner.startswith('<p>'):
                body = inner
            else:
                body = inner
            out.append(f'<aside class="note">{body}</aside>')
            continue
        if s.startswith('|'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                buf.append(lines[i])
                i += 1
            out.append(render_table(buf))
            continue
        m = re.match(r'^[-*]\s+(.*)$', s)
        if m:
            items = []
            while i < len(lines):
                mm = re.match(r'^[-*]\s+(.*)$', lines[i].strip())
                if not mm:
                    break
                items.append(mm.group(1))
                i += 1
            out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>')
            continue
        m = re.match(r'^\d+[.)]\s+(.*)$', s)
        if m:
            items = []
            while i < len(lines):
                mm = re.match(r'^\d+[.)]\s+(.*)$', lines[i].strip())
                if not mm:
                    break
                items.append(mm.group(1))
                i += 1
            out.append('<ol>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ol>')
            continue
        buf = []
        while i < len(lines):
            t = lines[i].strip()
            if not t or t == '---' or t.startswith('#') or t.startswith('|') \
               or t.startswith('>') or re.match(r'^[-*]\s+', t) or re.match(r'^\d+[.)]\s+', t):
                break
            buf.append(t)
            i += 1
        txt = ' '.join(buf)
        if txt.startswith('*') and txt.endswith('*') and not txt.startswith('**'):
            out.append(f'<p class="disclaimer">{inline(txt.strip("*"))}</p>')
        else:
            out.append(f'<p>{inline(txt)}</p>')
    return '\n'.join(x for x in out if x)


def convert(md_path, out_path, notice=''):
    with open(md_path, encoding='utf-8') as f:
        src = f.read()
    lines = src.split('\n')
    body = render_blocks(lines)

    title = ''
    m = re.search(r'^#\s+(.+)$', src, re.M)
    if m:
        title = plain(m.group(1))

    notice_html = f'<div class="notice">{esc(notice)}</div>' if notice else ''
    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="format-detection" content="telephone=no">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
{notice_html}
{body}
</div>
<div class="stamp">{esc(notice) if notice else '个人命理资料 · 仅供本人参考'}</div>
</body>
</html>
"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html_doc)
    return len(html_doc)


if __name__ == '__main__':
    a = sys.argv
    notice = a[3] if len(a) > 3 else ''
    n = convert(a[1], a[2], notice)
    print('WROTE', a[2], n, 'bytes')
