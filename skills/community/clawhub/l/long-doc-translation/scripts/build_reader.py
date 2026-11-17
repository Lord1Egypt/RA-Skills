# -*- coding: utf-8 -*-
"""
build_reader.py — 生成「增强阅读版 HTML」（依赖 merge_build.py，务必与本文件同目录）

特性：
  1. 脚注正文↔注文双向跳转（按片段隔离编号，仅链接可配对项）
  2. 全文搜索（高亮 + 命中计数 + 上/下一处 + 键盘 n/p）
  3. 原书页码跳转（输入 537 → 定位到〔S. 537〕）
  4. 目录当前位置高亮 + 自动滚动 + 层级折叠
  5. 阅读设置：字号 / 主题（日间·护眼·夜间）/ 大字（老年友好）/ 行宽，localStorage 记忆
  6. 页边码锚点化；原注·译注·新术语块可折叠
  7. 卷首「阅读说明」卡片；单文件自包含（CSS/JS 全内联，可离线、可直接发送）

依赖: pip install markdown pypinyin
用法: python build_reader.py
输出: output/译著阅读版.html
"""
import os, re, glob, sys

# ==================== CONFIG：按项目改这里 ====================
BASE = os.environ.get("LB_BASE", os.getcwd())
CHUNKS = os.path.join(BASE, "output", "chunks")
OUT_HTML = os.path.join(BASE, "output", "译著阅读版.html")
TITLE_L1 = "译著主稿"                 # 书名（第一级标题）
TITLE_L2 = "作为哲学与神学的体系"     # 副标题（第二级）
AUTHOR = "原著者（Wilhelm Dilthey）著 · 编者（Martin Redeker）编"
# =============================================================

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import merge_build as MB   # 复用切片读取、标题折叠、术语汇总、页边码换算
try:
    from _common import die, warn, ensure_chunks, check_python_deps
except ImportError:
    print("[出错] 找不到 _common.py —— 请确保它与本脚本在同一目录（scripts/）。",
          file=sys.stderr)
    sys.exit(1)

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
SUP_RE = "[⁰¹²³⁴⁵⁶⁷⁸⁹]+"
# PAGE_RE / page_val / sort_terms / collect_doubts / SECTIONS 等一律复用 MB.*，避免两份实现漂移。


def sup2int(s):
    return int("".join(str(SUP.index(c)) for c in s))


# ---------------------------------------------------------------- 片段组装
def global_dedup(parts):
    """与 merge_build 主稿一致的全局同级标题折叠（跨片段连续处理）。"""
    last, out = {}, []
    for name, text in parts:
        keep = []
        for ln in text.split("\n"):
            s = ln.strip()
            m = re.match(r"^(#{1,3})\s", s)
            if m:
                L = len(m.group(1))
                n = MB._norm_heading(s)
                if last.get(L) == n:
                    continue
                last[L] = n
                for k in [k for k in last if k > L]:
                    del last[k]
            keep.append(ln)
        out.append((name, "\n".join(keep)))
    return out


def build_parts():
    """返回 [(chunk_name_or_None, markdown_text), ...]，保持全书顺序。"""
    parts = []
    parts.append((None, "# %s\n" % TITLE_L1))
    if TITLE_L2:
        parts.append((None, "## %s\n" % TITLE_L2))
    if AUTHOR:
        parts.append((None, "**%s**\n" % AUTHOR))
    for prefix, zh, de in MB.SECTIONS:
        files = MB.chunk_files(prefix)
        if not files:
            continue
        texts = MB.dedup_heading([MB.read_text(f) for f in files])
        parts.append((None, "\n\n## %s\n\n*%s*\n" % (zh, de)))
        for f, t in zip(files, texts):
            parts.append((os.path.basename(f)[:-3], t))
    terms = MB.sort_terms(MB.collect_new_terms())
    app = "\n\n## 附录 · 全书新术语总表\n\n" + "\n".join(terms) + "\n"
    parts.append(("appendix", app))
    doubts = MB.collect_doubts()
    if doubts:
        parts.append(("doubts", "\n\n## 附录 · 存疑与待核清单\n\n"
                      + "以下 %d 条为译者在译注中标明存疑、待核或依 OCR 讹字推定之处，"
                        "引用或研究时建议回查原版对应页。\n\n" % len(doubts)
                      + "\n".join(doubts) + "\n"))
    return global_dedup(parts)


# ---------------------------------------------------------------- 标题与目录
def slugify(text, used):
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "", text)[:28]
    if not s:
        s = "sec"
    base = s
    i = 2
    while s in used:
        s = f"{base}-{i}"
        i += 1
    used.add(s)
    return s


def plan_headings(master_text):
    used = set()
    plan = []
    for ln in master_text.split("\n"):
        m = re.match(r"^(#{1,3})\s+(.*?)\s*$", ln)
        if m:
            plan.append((len(m.group(1)), m.group(2), slugify(m.group(2), used)))
    return plan


def build_toc(plan, chunk_of_h):
    items = [(l, t, i) for l, t, i in plan if l >= 2]
    root = []
    stack = [(-1, root)]
    for lvl, title, hid in items:
        while stack and stack[-1][0] >= lvl:
            stack.pop()
        node = {"t": title, "id": hid, "kids": []}
        stack[-1][1].append(node)
        stack.append((lvl, node["kids"]))

    def render(nodes):
        out = ["<ul>"]
        for n in nodes:
            ck = chunk_of_h.get(n["id"], "")
            if n["kids"]:
                out.append('<li class="has-kids"><span class="caret">▸</span>'
                           '<a href="#%s" data-chunk="%s">%s</a>' % (n["id"], ck, esc(n["t"])))
                out.append(render(n["kids"]))
                out.append("</li>")
            else:
                out.append('<li><a href="#%s" data-chunk="%s">%s</a></li>'
                           % (n["id"], ck, esc(n["t"])))
        out.append("</ul>")
        return "".join(out)
    return render(root)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- 片段渲染
MD = None


def get_md():
    global MD
    if MD is None:
        try:
            import markdown
        except ImportError:
            # 与其他脚本一致：缺依赖给「可执行的下一步」，而不是抛 traceback
            die("缺少依赖：markdown（build_reader 需要它把主稿 .md 渲染成 HTML）。",
                "安装：pip install markdown",
                "说明：merge_build.py 缺它时仍会生成主稿 .md、只跳过 HTML；"
                "但 build_reader.py 的产物就是 HTML，无法跳过这一步。")
        MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    return MD


def render_chunk(name, md_text, page_ids):
    """渲染单个片段：脚注链接化 + 页边码锚点 + 注释块折叠。"""
    md = get_md()
    md.reset()
    html = md.convert(md_text)

    anchors = set()
    m = re.search(r"####\s*原注\s*\n(.*?)(?=\n####|\Z)", md_text, re.S)
    if m:
        for ln in m.group(1).split("\n"):
            mm = re.match(r"^(%s)\s" % SUP_RE, ln.strip())
            if mm:
                anchors.add(sup2int(mm.group(1)))

    note_m = re.search(r"<h4>原注</h4>", html)
    head = html[: note_m.start()] if note_m else html
    tail = html[note_m.start():] if note_m else ""

    seen = {}

    def ref_sub(mo):
        n = sup2int(mo.group(0))
        if n not in anchors:
            return mo.group(0)
        k = seen.get(n, 0) + 1
        seen[n] = k
        return ('<a class="fnref" id="r-%s-%d-%d" href="#n-%s-%d">%s</a>'
                % (name, n, k, name, n, mo.group(0)))
    head = re.sub(SUP_RE, ref_sub, head)

    a_seen = {}

    def anchor_sub(mo):
        n = sup2int(mo.group(2))
        if n not in anchors:
            return mo.group(0)
        k = a_seen.get(n, 0) + 1
        a_seen[n] = k
        aid = "n-%s-%d" % (name, n) if k == 1 else "n-%s-%d-%d" % (name, n, k)
        if n not in seen:
            return '%s<span class="fnnum" id="%s">%s</span>' % (mo.group(1), aid, mo.group(2))
        return ('%s<span class="fnnum" id="%s"><a href="#r-%s-%d-1" '
                'title="返回正文">%s</a></span>'
                % (mo.group(1), aid, name, n, mo.group(2)))
    tail = re.sub(r"(?m)(<p>\s*|<br\s*/?>\s*|^)(%s)" % SUP_RE, anchor_sub, tail)
    html = head + tail

    def page_sub(mo):
        p = mo.group(1)
        pid = "P" + p
        if pid in page_ids:
            pid = "%s-%d" % (pid, page_ids[pid] + 1)
        page_ids[pid.split("-")[0]] = page_ids.get(pid.split("-")[0], 0) + 1
        return '<span class="pagemark" id="%s">%s</span>' % (pid, mo.group(0))
    html = MB.PAGE_RE.sub(page_sub, html)

    html = html.replace("<h4>原注</h4>", '<h4 class="notebox">原注</h4>')
    html = html.replace("<h4>译注</h4>", '<h4 class="notebox">译注</h4>')
    html = html.replace("<h4>新术语</h4>", '<h4 class="notebox">新术语</h4>')
    return html


# ---------------------------------------------------------------- 主流程
def build():
    parts = build_parts()
    master = "\n".join(t for _, t in parts)
    plan = plan_headings(master)

    page_ids = {}
    sections = []
    h_idx = 0
    chunk_of_h = {}

    for idx, (name, text) in enumerate(parts):
        cname = name if name else "p%03d" % idx
        html = render_chunk(cname, text, page_ids)

        def inject(mo):
            nonlocal h_idx
            lvl = mo.group(1)
            if h_idx < len(plan):
                hid = plan[h_idx][2]
                chunk_of_h[hid] = cname
                h_idx += 1
                return '<h%s id="%s">' % (lvl, hid)
            return mo.group(0)
        html = re.sub(r"<h([123])>", inject, html)

        pages = [MB.page_val(x) for x in MB.PAGE_RE.findall(text)]
        rng = ("原书 S.%d–%d" % (min(pages), max(pages))) if pages else ""
        if name is None:
            sections.append('<section class="chunk plain">%s</section>' % html)
        else:
            label = {"appendix": "附录 · 术语总表",
                     "doubts": "附录 · 存疑清单"}.get(name, name)
            sections.append(
                '<section class="chunk" data-chunk="%s" data-range="%s">'
                '<div class="chunkmark">%s<span class="cr">%s</span></div>%s</section>'
                % (name, esc(rng), esc(label), esc(rng), html)
            )

    body = "\n".join(sections)
    toc = build_toc(plan, chunk_of_h)

    md = get_md()
    md.reset()
    gm = re.search(r"## 附录 · 全书新术语总表\n(.*?)(?=\n## 附录 · 存疑|\Z)", master, re.S)
    n_terms = len(re.findall(r"^- \*\*", gm.group(1), re.M)) if gm else 0
    dm2 = re.search(r"## 附录 · 存疑与待核清单\n(?:.*?\n)?(.*?)\Z", master, re.S)
    n_doubts = len(re.findall(r"^- \*\*", dm2.group(1), re.M)) if dm2 else 0
    intro = md.convert(INTRO_MD.replace("{{TERM_COUNT}}", str(n_terms)))

    html = (TEMPLATE
            .replace("<!--TOC-->", toc)
            .replace("<!--INTRO-->", intro)
            .replace("<!--BODY-->", body)
            .replace("<!--STATS-->",
                     "%d 片段 · %d 条脚注链接 · %d 处原书页码 · %d 条术语 · %d 条存疑"
                     % (len(sections),
                        body.count('class="fnref"'),
                        body.count('class="pagemark"'),
                        n_terms, n_doubts)))
    open(OUT_HTML, "w", encoding="utf-8").write(html)
    print("reader html:", OUT_HTML, len(html), "chars")
    print("  脚注链接 %d / 页边码锚点 %d" % (body.count('class="fnref"'),
                                            body.count('class="pagemark"')))


INTRO_MD = """
> ### 阅读说明
>
> 本卷为中文全译本。
>
> - **〔S. XXX〕** 为原版页码（页边码）。可用左侧「跳至原书页」输入页码直接定位，便于与原版对照。
> - **原注** = 原书脚注；**译注** = 译者注（含 OCR 讹误订正、存疑标注）；**新术语** = 本片新出术语的原文→中文对照。
> - 正文中的上标数字（如 ⁽³⁷⁾）可**点击跳到注文**，注文编号可**点击返回正文**。
> - **粗体**对应原版的舒展字体（Sperrdruck），即作者强调处。
> - 左侧目录随阅读位置自动高亮；顶部搜索框支持全文检索（快捷键 `/` 聚焦，`n`/`p` 切换命中）。
> - 顶部「**日间 / 护眼 / 夜间**」按钮循环切换配色：**护眼**为柔和豆沙绿降低眩光，**夜间**为深色背景；选择自动记忆。
> - 顶部「**大字**」为老年友好模式：放大字号、放宽行距并加宽版面，按钮与输入框同步放大更易点按；亦可用 `A−`/`A＋` 微调字号、`行宽` 切换版心。
>
> 书末「附录 · 全书新术语总表」汇总本卷 {{TERM_COUNT}} 条新出术语，按中文主词排序，西文条目列于末尾。
"""


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>译著阅读版</title>
<style>
:root{
  --bg:#fbfaf7; --side:#1c222b; --side-fg:#c8d0da; --side-hl:#ffd479;
  --text:#24282d; --muted:#6b7280; --rule:#e5dfd6; --accent:#8a5a2b;
  --mark:#ffe08a; --quote:#f4f0e7; --bar:#fffdf8; --fs:18px; --mw:880px; --lh:1.9;
}
/* 护眼模式：柔和豆沙绿，降低屏幕眩光 */
body.eye{
  --bg:#c9e2c4; --side:#2f3b2c; --side-fg:#dfe7d8; --side-hl:#ffe08a;
  --text:#22301f; --muted:#5b6650; --rule:#aebfa3; --accent:#7a5a2a;
  --mark:#f1da8c; --quote:#d8e7d2; --bar:#bcd3b5;
}
body.dark{
  --bg:#15171b; --side:#101216; --side-fg:#b3bbc6; --side-hl:#ffd479;
  --text:#d7dbe1; --muted:#8b93a0; --rule:#2b3038; --accent:#d8a05a;
  --mark:#6d5a1c; --quote:#1e2128; --bar:#1a1d22;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:"Songti SC","Noto Serif CJK SC","Source Han Serif SC",Georgia,serif;
     background:var(--bg); color:var(--text); font-size:var(--fs); line-height:var(--lh);
     transition:background .25s,color .25s}
#topbar{position:sticky; top:0; z-index:50; background:var(--bar);
  border-bottom:1px solid var(--rule); display:flex; gap:6px; align-items:center;
  padding:7px 14px; font-family:system-ui,"PingFang SC","Microsoft YaHei",sans-serif;
  font-size:13px; flex-wrap:wrap}
#topbar button{background:transparent; border:1px solid var(--rule); color:var(--text);
  border-radius:6px; padding:3px 9px; cursor:pointer; font-size:13px}
#topbar button:hover{border-color:var(--accent); color:var(--accent)}
#topbar button.on{border-color:var(--accent); color:var(--accent); font-weight:700; background:var(--mark)}
#topbar input{border:1px solid var(--rule); background:var(--bg); color:var(--text);
  border-radius:6px; padding:3px 8px; font-size:13px}
#q{width:190px} #pg{width:74px}
#hitinfo{color:var(--muted); min-width:74px}
#navToggle{font-weight:600}
body.large #topbar button, body.large #topbar input{font-size:15px; padding:5px 12px}
body.large #q{width:220px} body.large #pg{width:88px}
body.large #nav{font-size:14px}
#layout{display:flex; align-items:flex-start}
nav{width:308px; min-width:308px; background:var(--side); color:var(--side-fg);
    position:sticky; top:44px; height:calc(100vh - 44px); overflow-y:auto;
    padding:16px 12px 70px; font-family:system-ui,"PingFang SC","Microsoft YaHei",sans-serif}
nav.hidden{display:none}
nav .nh{font-size:14px; color:#fff; margin:0 0 2px}
nav .ns{font-size:11.5px; color:#7f8996; margin-bottom:10px}
nav .nstat{font-size:11px; color:#7f8996; margin:0 0 10px; line-height:1.5}
nav ul{list-style:none; padding-left:0; margin:0}
nav li{margin:1px 0; position:relative}
nav li ul{padding-left:13px}
nav a{color:var(--side-fg); text-decoration:none; display:block; padding:2px 6px;
  border-left:2px solid transparent; font-size:13px; line-height:1.5; border-radius:0 3px 3px 0}
nav a:hover{color:var(--side-hl)}
nav > ul > li > a{color:#eef2f6; font-weight:600; font-size:13.5px}
nav a.cur{color:var(--side-hl); border-left-color:var(--side-hl); background:rgba(255,212,121,.09)}
li.has-kids > .caret{position:absolute; left:-11px; top:3px; cursor:pointer;
  color:#7f8996; font-size:10px; user-select:none; transition:transform .15s}
li.collapsed > ul{display:none}
li.has-kids > .caret{transform:rotate(90deg)}
main{flex:1; max-width:var(--mw); margin:0 auto; padding:26px 40px 160px}
main h1{font-size:1.75em; text-align:center; margin:.2em 0}
main h2{font-size:1.4em; margin:2em 0 .7em; padding-bottom:.22em;
  border-bottom:2px solid var(--accent); color:var(--accent)}
main h3{font-size:1.17em; margin:1.6em 0 .5em; color:var(--accent); opacity:.85}
main p{margin:.72em 0; text-align:justify}
blockquote{border-left:3px solid var(--accent); margin:.8em 0; padding:.2em 1em;
  color:var(--muted); font-style:normal}
blockquote p{margin:.35em 0}
strong{color:var(--accent); font-weight:700}
hr{border:none; border-top:1px solid var(--rule); margin:2em 0}
ul,ol{padding-left:1.5em}
table{border-collapse:collapse; width:100%; margin:1em 0; font-size:.92em}
th,td{border:1px solid var(--rule); padding:5px 9px}
th{background:var(--quote)}
code{background:var(--quote); padding:1px 5px; border-radius:3px; font-size:.88em}
a{color:var(--accent)}
.pagemark{display:block; text-align:right; color:var(--muted); font-size:.72em;
  letter-spacing:.5px; font-family:system-ui,sans-serif; margin:.5em 0 -.35em; opacity:.75}
.pagemark.flash{color:var(--accent); opacity:1; font-weight:700}
a.fnref{text-decoration:none; color:var(--accent); font-size:.82em; padding:0 1px}
a.fnref:hover{background:var(--mark); border-radius:3px}
.chunkmark{font-family:system-ui,sans-serif; font-size:10.5px; color:var(--muted);
  opacity:0; text-align:right; height:0; transition:opacity .2s}
section.chunk:hover > .chunkmark{opacity:.4}
.chunkmark .cr{margin-left:8px}
.notebox{margin:.6em 0; border:1px solid var(--rule); border-radius:7px;
  background:var(--quote); overflow:hidden}
.notebox h4{margin:0; padding:5px 11px; font-size:.86em; cursor:pointer;
  color:var(--accent); font-family:system-ui,sans-serif; user-select:none;
  display:flex; justify-content:space-between; align-items:center}
.notebox h4::after{content:"▸"; font-size:10px; transition:transform .15s}
.notebox.open h4::after{transform:rotate(90deg)}
.notebox .notebody{display:none; padding:2px 13px 10px; font-size:.9em; border-top:1px solid var(--rule)}
.notebox.open .notebody{display:block}
body.notes-open .notebox .notebody{display:block}
.notebox .notebody p{margin:.42em 0; text-align:justify}
.fnnum{color:var(--accent); font-weight:700; margin-right:4px}
.fnnum a{text-decoration:none}
mark.hit{background:var(--mark); color:inherit; border-radius:2px}
mark.hit.cur{outline:2px solid var(--accent); background:var(--accent); color:#fff}
#intro{margin-bottom:2em}
#totop{position:fixed; right:22px; bottom:22px; z-index:60; opacity:.35}
#totop:hover{opacity:1}
@media (max-width:900px){ nav{display:none} main{padding:18px 16px 120px} #q{width:120px} }
@media print{
  #topbar,nav,#totop{display:none !important}
  main{max-width:none; margin:0; padding:0}
  body{font-size:11pt; background:#fff; color:#000}
  .notebox .notebody{display:block !important}
  .notebox{break-inside:avoid; border:1px solid #ccc}
  .chunkmark{display:none}
  main h2{break-after:avoid} main h3{break-after:avoid}
  a{color:#000; text-decoration:none}
}
</style>
</head>
<body>
<div id="topbar">
  <button id="navToggle" title="显示/隐藏目录">☰ 目录</button>
  <input id="q" placeholder="全文搜索（/）" autocomplete="off">
  <button id="prevHit" title="上一处">↑</button>
  <button id="nextHit" title="下一处">↓</button>
  <span id="hitinfo"></span>
  <input id="pg" placeholder="原书页 S." autocomplete="off">
  <button id="goPage">跳转</button>
  <button id="fontD" title="缩小字号">A−</button>
  <button id="fontU" title="放大字号">A＋</button>
  <button id="widthBtn" title="切换行宽">行宽</button>
  <button id="largeBtn" title="老年友好 · 大字模式（大字号 + 宽松行距 + 加宽）">大字</button>
  <button id="themeBtn" title="切换 日间 / 护眼 / 夜间">日间 ▸</button>
  <button id="notesBtn" title="展开/折叠全部注释">展开注释</button>
</div>
<div id="layout">
<nav id="nav">
  <div class="nh">译著阅读版</div>
  <div class="ns">中译 · 增强阅读</div>
  <div class="nstat"><!--STATS--></div>
  <!--TOC-->
</nav>
<main id="main">
<!--INTRO-->
<!--BODY-->
</main>
</div>
<button id="totop">↑ 顶部</button>
<script>
(function(){
  var nav=document.getElementById('nav'), main=document.getElementById('main');
  var $=function(s){return document.querySelector(s)};

  /* ---------- 注释块分组与折叠 ---------- */
  document.querySelectorAll('section.chunk').forEach(function(sec){
    var kids=Array.prototype.slice.call(sec.children);
    var groups=[], cur=null;
    kids.forEach(function(el){
      if(el.tagName==='H4' && el.classList.contains('notebox')){ cur={head:el,items:[]}; groups.push(cur); return; }
      if(cur){
        var t=el.tagName;
        if(t==='H1'||t==='H2'||t==='H3'){ cur=null; return; }
        cur.items.push(el);
      }
    });
    groups.forEach(function(g){
      var box=document.createElement('div'); box.className='notebox';
      var head=g.head, body=document.createElement('div');
      body.className='notebody';
      sec.insertBefore(box, head);
      box.appendChild(head); box.appendChild(body);
      g.items.forEach(function(i){ body.appendChild(i); });
      var n=body.querySelectorAll('p,li').length;
      var tag=document.createElement('span');
      tag.style.fontWeight='400'; tag.style.color='var(--muted)';
      tag.textContent=(n?(n+' 条'):'（无）');
      head.appendChild(tag);
      head.addEventListener('click',function(){ box.classList.toggle('open'); });
    });
  });
  $('#notesBtn').addEventListener('click',function(){
    var on=document.body.classList.toggle('notes-open');
    this.textContent=on?'折叠注释':'展开注释';
  });

  /* ---------- 目录折叠 ---------- */
  nav.addEventListener('click',function(e){
    if(e.target.classList.contains('caret')){
      e.target.parentNode.classList.toggle('collapsed');
      e.stopPropagation();
    }
  });

  /* ---------- 阅读设置 ---------- */
  function set(k,v){ try{localStorage.setItem(k,v)}catch(e){} }
  function get(k){ try{return localStorage.getItem(k)}catch(e){return null} }
  var root=document.documentElement;
  var fs=parseFloat(get('rd-fs')||'18');
  if(isNaN(fs)) fs=18;
  if(fs<13) fs=13; if(fs>32) fs=32;
  var wide=get('rd-wide')==='1';
  var large=get('rd-large')==='1';
  var THEMES=['light','eye','dark'];
  var THEME_LABEL={light:'日间',eye:'护眼',dark:'夜间'};
  var theme=get('rd-theme')||'light';
  if(THEMES.indexOf(theme)<0) theme='light';

  function applyRead(){
    var f = large ? Math.max(fs,23) : fs;
    var lh = large ? 2.2 : 1.9;
    var mw = large ? 1180 : (wide ? 1180 : 880);
    root.style.setProperty('--fs', f+'px');
    root.style.setProperty('--lh', lh);
    root.style.setProperty('--mw', mw+'px');
    document.body.classList.toggle('large', large);
    $('#largeBtn').classList.toggle('on', large);
    $('#largeBtn').textContent = large ? '大字 ✓' : '大字';
    $('#widthBtn').classList.toggle('on', wide && !large);
  }
  function applyTheme(){
    document.body.classList.remove('dark','eye');
    if(theme==='dark') document.body.classList.add('dark');
    else if(theme==='eye') document.body.classList.add('eye');
    $('#themeBtn').textContent = THEME_LABEL[theme]+' ▸';
    $('#themeBtn').classList.toggle('on', theme!=='light');
  }
  applyRead();
  applyTheme();

  $('#fontU').onclick=function(){ fs=Math.min(32,fs+1); applyRead(); set('rd-fs',fs); };
  $('#fontD').onclick=function(){ fs=Math.max(13,fs-1); applyRead(); set('rd-fs',fs); };
  $('#widthBtn').onclick=function(){ wide=!wide; applyRead(); set('rd-wide',wide?1:0); };
  $('#largeBtn').onclick=function(){ large=!large; applyRead(); set('rd-large',large?1:0); };
  $('#themeBtn').onclick=function(){
    theme=THEMES[(THEMES.indexOf(theme)+1)%THEMES.length];
    applyTheme(); set('rd-theme',theme);
  };
  $('#navToggle').onclick=function(){ nav.classList.toggle('hidden'); };
  $('#totop').onclick=function(){ window.scrollTo({top:0,behavior:'smooth'}); };

  /* ---------- 目录高亮 ---------- */
  var map={};
  nav.querySelectorAll('a[data-chunk]').forEach(function(a){
    var c=a.getAttribute('data-chunk'); if(!c) return;
    (map[c]=map[c]||[]).push(a);
  });
  var visible=new Set(), lastC='';
  function highlight(c){
    if(c===lastC||!c) return;
    nav.querySelectorAll('a.cur').forEach(function(a){a.classList.remove('cur')});
    (map[c]||[]).forEach(function(a){a.classList.add('cur')});
    var first=(map[c]||[])[0];
    if(first){ nav.scrollTop=Math.max(0, first.offsetTop-nav.clientHeight/2); }
    lastC=c;
  }
  if('IntersectionObserver' in window){
    var obs=new IntersectionObserver(function(es){
      es.forEach(function(e){ e.isIntersecting?visible.add(e.target):visible.delete(e.target); });
      var top=null;
      visible.forEach(function(s){ if(!top||s.offsetTop<top.offsetTop) top=s; });
      if(top) highlight(top.getAttribute('data-chunk'));
    },{rootMargin:'-5% 0px -75% 0px'});
    document.querySelectorAll('section.chunk[data-chunk]').forEach(function(s){obs.observe(s)});
  }

  /* ---------- 原书页码跳转 ---------- */
  var pageIdx=[];
  function pageVal(s){
    if(/^\d+$/.test(s)) return parseInt(s,10);
    var map={I:1,V:5,X:10,L:50,C:100,D:500,M:1000}, t=s.toUpperCase(), v=0, prev=0, i, c;
    for(i=t.length-1;i>=0;i--){ c=map[t.charAt(i)]||0; v+=(c<prev?-c:c); prev=c; }
    return v;
  }
  document.querySelectorAll('.pagemark').forEach(function(e){
    var m=/S\.\s*([0-9IVXLCDM]+)/.exec(e.textContent);
    if(m) pageIdx.push([pageVal(m[1]), e.id]);
  });
  pageIdx.sort(function(a,b){return a[0]-b[0]});
  function gotoPage(v){
    var n=parseInt(v,10); if(isNaN(n)) return;
    var cand=null;
    for(var i=0;i<pageIdx.length;i++){ if(pageIdx[i][0]<=n) cand=pageIdx[i]; else break; }
    if(!cand) cand=pageIdx[0];
    if(!cand) return;
    var el=document.getElementById(cand[1]); if(!el) return;
    el.scrollIntoView({block:'center'});
    document.querySelectorAll('.pagemark.flash').forEach(function(e){e.classList.remove('flash')});
    el.classList.add('flash');
    $('#hitinfo').textContent = (cand[0]===n) ? ('S.'+n) : ('≈S.'+cand[0]+'（无 '+n+'）');
    setTimeout(function(){
      el.classList.remove('flash');
      if($('#hitinfo').textContent.indexOf('≈S.')===0 || $('#hitinfo').textContent==='S.'+n){
        $('#hitinfo').textContent='';
      }
    },4000);
  }
  $('#goPage').onclick=function(){ gotoPage($('#pg').value); };
  $('#pg').addEventListener('keydown',function(e){ if(e.key==='Enter') gotoPage(this.value); });

  /* ---------- 全文搜索 ---------- */
  var hits=[], cur=-1, MAX=4000;
  function clearMarks(){
    var ms=document.querySelectorAll('mark.hit');
    for(var i=0;i<ms.length;i++){
      var m=ms[i], p=m.parentNode;
      p.replaceChild(document.createTextNode(m.textContent), m);
      p.normalize && p.normalize();
    }
    hits=[]; cur=-1;
  }
  function doSearch(q){
    clearMarks();
    if(!q || !q.trim()){ $('#hitinfo').textContent=''; return; }
    var walker=document.createTreeWalker(main, NodeFilter.SHOW_TEXT, null, false);
    var nodes=[], n;
    while(n=walker.nextNode()) nodes.push(n);
    var lq=q.toLowerCase(), total=0;
    for(var i=0;i<nodes.length;i++){
      var node=nodes[i], t=node.nodeValue, lt=t.toLowerCase();
      if(lt.indexOf(lq)===-1) continue;
      var frag=document.createDocumentFragment(), k, from=0;
      while((k=lt.indexOf(lq,from))!==-1){
        if(k>from) frag.appendChild(document.createTextNode(t.slice(from,k)));
        var mk=document.createElement('mark'); mk.className='hit';
        mk.textContent=t.slice(k,k+q.length);
        frag.appendChild(mk); hits.push(mk);
        from=k+q.length; total++;
        if(total>=MAX) break;
      }
      if(from<t.length) frag.appendChild(document.createTextNode(t.slice(from)));
      node.parentNode.replaceChild(frag, node);
      if(total>=MAX) break;
    }
    $('#hitinfo').textContent = total? ('1 / '+hits.length) : '无结果';
    if(hits.length){ cur=0; focusHit(0); }
  }
  function focusHit(i){
    if(!hits.length) return;
    cur=(i+hits.length)%hits.length;
    hits.forEach(function(h){h.classList.remove('cur')});
    var h=hits[cur]; h.classList.add('cur');
    var box=h.closest? h.closest('.notebox'):null;
    if(box && !box.classList.contains('open')) box.classList.add('open');
    h.scrollIntoView({block:'center'});
    $('#hitinfo').textContent=(cur+1)+' / '+hits.length;
  }
  var qt;
  $('#q').addEventListener('input',function(){
    clearTimeout(qt); var v=this.value;
    qt=setTimeout(function(){ doSearch(v); },260);
  });
  $('#q').addEventListener('keydown',function(e){
    if(e.key==='Enter'){ e.preventDefault(); doSearch(this.value); }
  });
  $('#nextHit').onclick=function(){ focusHit(cur+1) };
  $('#prevHit').onclick=function(){ focusHit(cur-1) };
  document.addEventListener('keydown',function(e){
    if(e.key==='/' && document.activeElement!==$('#q') && document.activeElement!==$('#pg')){
      e.preventDefault(); $('#q').focus(); return;
    }
    if(document.activeElement===$('#q')) return;
    if(e.key==='n'){ focusHit(cur+1) }
    if(e.key==='p'){ focusHit(cur-1) }
    if(e.key==='Escape'){ clearMarks(); $('#q').value=''; $('#hitinfo').textContent=''; }
  });
})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    # 生成前校验：没有片段就别产出空壳 HTML（看起来"成功"实则什么都没有）
    ensure_chunks(CHUNKS, ".md")
    check_python_deps("pypinyin", "markdown", hard=("markdown",))
    out_dir = os.path.dirname(OUT_HTML)
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    build()
