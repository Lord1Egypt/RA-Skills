#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_build.py — 长篇翻译合并与交付构建（增强版，供 build_reader.py 复用）

对外暴露的 API（build_reader.py 依赖这些）：
  SECTIONS, chunk_files(), read_text(), dedup_heading(), _norm_heading(),
  PAGE_RE, page_val(), TERM_RE, sort_terms(), collect_new_terms(),
  collect_doubts(), append_glossary(), build_master()

同时保留通用合并能力（merge() / build_html()），不依赖 SECTIONS 也可独立使用。

依赖: pip install markdown pypinyin
"""
import re
import os
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from _common import die, warn, opt, ensure_chunks, safe_read, check_python_deps
except ImportError:
    print("[出错] 找不到 _common.py —— 请确保它与本脚本在同一目录（scripts/）。",
          file=sys.stderr)
    sys.exit(1)

# ==================== CONFIG：按项目改这里 ====================
# 工作根目录（输出写在此目录下 output/）。可用环境变量 LB_BASE 覆盖。
BASE = os.environ.get("LB_BASE", os.getcwd())
CHUNKS = os.path.join(BASE, "output", "chunks")

# 部类结构：(prefix, 中文标题, 德/英标题)。按原书结构分章； prefix 用于 glob 片段文件。
# 单卷无分部的项目可只放一个 ("", "正文", "") 或直接让 SECTIONS=[] 走通用 merge()。
SECTIONS = [
    ("00_front", "前处理 · 编者导言", "Vorbemerkung / Einleitung des Herausgebers"),
    ("01_phil",  "第一部 · 哲学（Philosophie）", "Erster Teil · Philosophie"),
    ("02_theol", "第二部 · 神学（Theologie）", "Zweiter Teil · Theologie"),
    ("03_herm",  "第三部 · 解释学（Hermeneutik）", "Dritter Teil · Hermeneutik"),
    ("04_index", "索引（Register）", "Personenregister und Sachregister"),
]

# 通用合并配置
TOC_DEPTH = "2-3"                       # 目录收录层级
GLOSSARY_APPENDIX = "附录 · 全书新术语总表"
DOUBT_APPENDIX = "附录 · 存疑与待核清单"
TERM_HEADING = "#### 新术语"
DOUBT_HEADING = "#### 译注"
KEEP_REPEAT = ("#### 原注", "#### 译注", "#### 新术语")
EXCLUDE_DIRS = ("_redundant", "_backup")
# =============================================================


def _norm_heading(h):
    """去掉末尾的（续）/〔续〕等续标，用于比较同一标题的不同续写形态。"""
    if not h:
        return ""
    return re.sub(r"[（(]?续[）)]?$", "", h.replace("〔续〕", "")).strip()


def _level(line):
    m = re.match(r"^(#{1,6})\s", line.strip())
    return len(m.group(1)) if m else None


# ---------------------------------------------------------------- 章节结构组装
def chunk_files(prefix):
    files = glob.glob(os.path.join(CHUNKS, f"{prefix}_*.md")) if prefix else \
            glob.glob(os.path.join(CHUNKS, "*.md"))
    def key(p):
        m = re.search(r"_(\d+)\.md$", p)
        return int(m.group(1)) if m else 0
    return sorted(files, key=key)


def read_text(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def dedup_heading(chunks_texts):
    """折叠跨片段重复标题：本片首标题 == 上片首标题 或 == 上片末标题时删首标题行。"""
    out = []
    prev_open = prev_last = None
    for txt in chunks_texts:
        lines = txt.split("\n")
        opening = opening_idx = None
        for i, ln in enumerate(lines):
            s = ln.strip()
            if s == "":
                continue
            if re.match(r"^#{1,4}\s", s):
                opening, opening_idx = s, i
            break
        last = None
        for ln in lines:
            s = ln.strip()
            if re.match(r"^#{1,4}\s", s):
                last = s
        drop = bool(opening) and (_norm_heading(opening) == _norm_heading(prev_open)
                                  or _norm_heading(opening) == _norm_heading(prev_last))
        if drop and opening_idx is not None:
            lines = lines[:opening_idx] + lines[opening_idx + 1:]
            txt = "\n".join(lines).strip()
        else:
            txt = txt.strip()
        out.append("\n\n" + txt)
        prev_open, prev_last = opening, last
    return out


# ---------------------------------------------------------------- 页边码取值
# 阿拉伯数字（正文）与罗马数字（前处理/目次）都需锚点化；容许 OCR 变体「… 续/末/ff」
PAGE_RE = re.compile(r"〔S\.\s*(\d{1,3}|[IVXLCDM]{1,8})(?:\s*(?:续|末|f{1,2}))?\s*〕")


def page_val(s):
    """页码取值：阿拉伯数字直接转，罗马数字换算。"""
    s = s.strip().upper()
    if s.isdigit():
        return int(s)
    tbl = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    v = prev = 0
    for ch in reversed(s):
        c = tbl.get(ch, 0)
        v += -c if c < prev else c
        prev = c
    return v


# ---------------------------------------------------------------- 附录：术语表
TERM_RE = re.compile(r"^- \*\*(.+?)\*\*(.+)$")

try:
    from pypinyin import lazy_pinyin
    def _py(s):
        return "".join(lazy_pinyin(s))
except Exception:
    def _py(s):
        return s


def _head(t):
    m = TERM_RE.match(t)
    return (m.group(1) if m else t[2:]).strip()


def sort_terms(terms):
    """中文条目按拼音排序，西文条目按拉丁字母排序并置于末尾（pypinyin）。"""
    cn, latin, other = [], [], []
    for t in terms:
        first = (_head(t) or " ")[0]
        if re.match(r"[A-Za-zÄÖÜäöüß]", first):
            latin.append(t)
        elif re.search(r"[\u4e00-\u9fff]", first):
            cn.append(t)
        else:
            other.append(t)
    cn.sort(key=lambda s: _py(_head(s)).lower())
    other.sort(key=lambda s: _py(_head(s)).lower())
    # 西文只取开头连续拉丁字母比较，避免全角括号（Unicode 码点极大）打乱次序
    latin.sort(key=lambda s: re.split(r"[^A-Za-zÄÖÜäöüß]", _head(s))[0].lower())
    return cn + other + latin


# ---------------------------------------------------------------- 附录：存疑清单
DOUBT_RE = re.compile(r"存疑|待核|待考|俟考|未能判定|无法确定|不确定")


def collect_doubts(chunks_dir=None):
    """抽取各片 #### 译注 中含存疑/待核表述的条目，附片段与原书页码定位。"""
    d = chunks_dir or CHUNKS
    rows = []
    for f in sorted(glob.glob(os.path.join(d, "*.md"))):
        name = os.path.basename(f)[:-3]
        t = read_text(f)
        m = re.search(r"####\s*译注\s*\n(.*?)(?=\n####|\Z)", t, re.S)
        if not m:
            continue
        pages = [page_val(x) for x in PAGE_RE.findall(t)]
        loc = "S.%d–%d" % (min(pages), max(pages)) if pages else "（无页边码）"
        for ln in m.group(1).split("\n"):
            s = ln.strip()
            if len(s) < 15 or not DOUBT_RE.search(s):
                continue
            s = re.sub(r"^[-*]\s*", "", s)
            s = re.sub(r"^\d+\.\s*", "", s)
            rows.append("- **%s**（%s）：%s" % (name, loc, s))
    return rows


def collect_new_terms():
    """汇总全部片段的 #### 新术语 条目，去重后排序，供附录使用。"""
    terms, seen = [], set()
    for f in sorted(glob.glob(os.path.join(CHUNKS, "*.md"))):
        txt = read_text(f)
        m = re.search(r"####\s*新术语\s*\n(.*?)(?:\n####|\Z)", txt, re.S)
        if not m:
            continue
        for ln in m.group(1).split("\n"):
            s = ln.strip()
            if s.startswith("- "):
                k = re.sub(r"\s+", "", s)
                if k not in seen:
                    seen.add(k)
                    terms.append(s)
    return sorted(terms)


def append_glossary(master):
    """在 master 末尾追加术语总表 + 存疑清单附录（均经 sort_terms 排序）。"""
    terms = sort_terms(collect_new_terms())
    app = "\n\n## %s\n\n" % GLOSSARY_APPENDIX + "\n".join(terms) + "\n"
    doubts = collect_doubts()
    if doubts:
        app += ("\n\n## %s\n\n" % DOUBT_APPENDIX +
                "以下 %d 条为译者在译注中标明存疑、待核或依 OCR 讹字推定之处，"
                "引用或研究时建议回查原版对应页。\n\n" % len(doubts) +
                "\n".join(doubts) + "\n")
    return master.rstrip() + "\n" + app


def build_master(title_l1="译著主稿", title_l2="", author=""):
    """按 SECTIONS 组装增强主稿（含术语/存疑附录）。SECTIONS=[] 时退化为通用合并。"""
    parts = []
    if title_l1:
        parts.append("# %s\n" % title_l1)
    if title_l2:
        parts.append("## %s\n" % title_l2)
    if author:
        parts.append("**%s**\n" % author)
    if SECTIONS:
        for prefix, zh, de in SECTIONS:
            files = chunk_files(prefix)
            if not files:
                continue
            texts = dedup_heading([read_text(f) for f in files])
            parts.append("\n\n## %s\n\n*%s*\n" % (zh, de))
            parts.append("\n".join(texts))
    else:
        files = chunk_files("")
        parts.append("\n".join(dedup_heading([read_text(f) for f in files])))
    master = "\n".join(parts).rstrip() + "\n"
    master = append_glossary(master)
    # 全局再清理：折叠同一层级上与「上一个同级标题」完全相同的标题（消除（续）重标）
    lines = master.split("\n")
    out, last_same_level = [], {}
    for ln in lines:
        s = ln.strip()
        m = re.match(r"^(#{1,4})\s", s)
        if m and len(m.group(1)) <= 3:
            L, n = len(m.group(1)), _norm_heading(s)
            if last_same_level.get(L) == n:
                continue
            last_same_level[L] = n
            for k in list(last_same_level):
                if k > L:
                    del last_same_level[k]
        out.append(ln)
    return "\n".join(out).rstrip() + "\n"


# ---------------------------------------------------------------- 通用合并（无 SECTIONS 也可用）
def merge(chunks_dir=None):
    files = sorted(glob.glob(os.path.join(chunks_dir or CHUNKS, "*.md")))
    files = [f for f in files if not any(d in f for d in EXCLUDE_DIRS)]
    parts = []
    for f in files:
        txt = open(f, encoding="utf-8", errors="ignore").read().strip()
        parts.append("\n\n" + txt + "\n")
    master = "\n".join(parts)
    lines, out, last_by_level = master.split("\n"), [], {}
    for ln in lines:
        s = ln.strip()
        if s in KEEP_REPEAT:
            out.append(ln)
            continue
        lv = _level(s)
        if lv is not None:
            n = _norm_heading(s)
            if n and last_by_level.get(lv) == n:
                continue
            last_by_level[lv] = n
            for k in list(last_by_level):
                if k > lv:
                    del last_by_level[k]
        out.append(ln)
    master = "\n".join(out).rstrip() + "\n"
    terms, seen = [], set()
    for f in files:
        text = open(f, encoding="utf-8", errors="ignore").read()
        m = re.search(re.escape(TERM_HEADING) + r"(.*?)(?=\n#### |\n### |\n## |\Z)", text, re.S)
        if not m:
            continue
        for line in m.group(1).split("\n"):
            t = line.strip()
            if t.startswith("- ") and t not in seen:
                seen.add(t)
                terms.append(t)
    if terms:
        master += "\n\n## %s\n\n" % GLOSSARY_APPENDIX + "\n".join(terms) + "\n"
    return master, len(files), len(terms)


def build_html(master, out_html):
    try:
        import markdown
    except ImportError:
        print("⚠ 未安装 markdown，跳过 HTML。安装：pip install markdown")
        return False
    body = markdown.markdown(
        master,
        extensions=["tables", "fenced_code", "attr_list", "toc"],
        extension_configs={"toc": {"toc_depth": TOC_DEPTH, "title": "目录"}},
    )
    css = """
    :root{--bg:#fbfaf7;--fg:#23201c;--muted:#7a7268;--accent:#8a5a2b;--line:#e6e2da;}
    *{box-sizing:border-box}
    body{margin:0;background:var(--bg);color:#23201c;
         font-family:"Source Han Serif SC","Noto Serif CJK SC",Georgia,serif;
         font-size:17px;line-height:1.85;}
    .layout{display:flex;max-width:1400px;margin:0 auto}
    nav.toc{width:300px;flex:0 0 300px;position:sticky;top:0;height:100vh;
            overflow-y:auto;padding:28px 18px;border-right:1px solid var(--line);
            background:#f5f2ec;font-size:14px}
    nav.toc h2{font-size:15px;margin:0 0 12px;color:#8a5a2b;letter-spacing:.06em}
    nav.toc ul{list-style:none;padding-left:0;margin:0}
    nav.toc li{margin:3px 0}
    nav.toc li>ul{padding-left:14px}
    nav.toc a{color:#4a453e;text-decoration:none;display:block;padding:2px 4px;border-radius:4px}
    nav.toc a:hover{background:#e9e4db;color:#8a5a2b}
    main{flex:1;padding:36px 56px 120px;min-width:0}
    main h1{font-size:30px;border-bottom:2px solid #e6e2da;padding-bottom:14px}
    main h2{font-size:23px;margin-top:44px;color:#8a5a2b}
    main h3{font-size:19px;margin-top:32px}
    main h4{font-size:16px;margin-top:24px;color:#6b6259}
    blockquote{margin:14px 0;padding:8px 16px;border-left:3px solid #d8d2c7;color:#6b6259;background:#f7f4ee}
    code{background:#f0ece4;padding:2px 5px;border-radius:3px;font-size:.9em}
    table{border-collapse:collapse;width:100%;margin:16px 0;font-size:15px}
    th,td{border:1px solid #ddd8ce;padding:7px 10px;text-align:left}
    th{background:#f0ece4}
    hr{border:0;border-top:1px solid var(--line);margin:36px 0}
    sup{font-size:.75em;color:#8a5a2b}
    @media(max-width:900px){nav.toc{display:none}main{padding:20px}}
    """
    m = re.search(r'<div class="toc">(.*?)</div>', body, re.S)
    nav = ""
    if m:
        nav = f'<nav class="toc"><h2>目录</h2>{m.group(1)}</nav>'
        body = body.replace(m.group(0), "")
    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_l1}</title><style>{css}</style></head>
<body><div class="layout">{nav}<main>
{body}
</main></div></body></html>"""
    open(out_html, "w", encoding="utf-8").write(html)
    return True


def main():
    chunks_dir = sys.argv[1] if len(sys.argv) > 1 else CHUNKS
    out_prefix = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "output", "译著主稿")

    # 合并前校验：目录为空就别生成空白主稿（空文件会被误当成「合并成功」）
    ensure_chunks(chunks_dir, ".md")
    # 依赖自检：缺失不阻断，但明确告知降级后果
    check_python_deps("pypinyin", "markdown")
    # 输出目录不存在时自动创建，避免写文件时才失败
    out_dir = os.path.dirname(out_prefix)
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)
        print(f"（已自动创建输出目录：{out_dir}）")

    # 优先走增强路径（SECTIONS 非空且存在分章片段）
    if SECTIONS and glob.glob(os.path.join(CHUNKS, "*_*.md")):
        master = build_master()
        n_files = len(glob.glob(os.path.join(CHUNKS, "*.md")))
    else:
        master, n_files, _ = merge(chunks_dir)
    md_path = out_prefix + ".md"
    open(md_path, "w", encoding="utf-8").write(master)
    print(f"✅ 主稿已生成：{md_path}（{len(master)} 字符）")
    html_path = out_prefix + ".html"
    if build_html(master, html_path):
        print(f"✅ 基础阅读版已生成：{html_path}")
        print("   如需搜索/脚注跳转/护眼夜间大字等增强体验，另跑 build_reader.py")
    print(f"   合并片段 {n_files} 个")


if __name__ == "__main__":
    main()
