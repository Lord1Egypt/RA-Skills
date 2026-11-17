#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ppshu — 代码/文本对比审查报告生成器（diff 报告页）。

把两份文件（旧版/新版）生成一张「可验证的 diff 报告」单文件 HTML：
  - 双栏等宽 + 行号对齐（左旧右新），新增行浅绿、删除行浅红；
  - 自适应占满预览窗口，窗口拉宽时左右代码栏同步展开；
  - 差异块导航胶囊（点击跳转）+ 「只看改动」开关；
  - 页脚三栏「我们做的 / 自动化验证 / 不变底稿」留白，供汇报时填写；
  - 两个文件的 SHA-256 内嵌标注，随时可复算核对，结论不是作者编的。

用法
----
    python diff_report.py -a old.mjs -b new.mjs -o report.html
    # 然后交给 save_html.py 存入画册：
    python diff_report.py -a a.py -b b.py -o report.html
    python save_html.py "xx 代码 diff 报告" --file report.html

参数
----
    -a, --old   <路径>  旧版文件（必填）
    -b, --new   <路径>  新版文件（必填）
    -o, --output <路径> 输出 HTML（默认 stdout）
    --name-a / --name-b 显示名（默认取文件名）
    -c, --context <n>   差异块上下文行数（默认 3）
"""
import argparse
import hashlib
import html as _html
import json
import sys
from difflib import unified_diff


def read_lines(path: str) -> list:
    """按行读取，返回剥离行尾换行符的列表（不保留 \r，统一按行语义处理）。"""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    return text.splitlines()


def sha256_of_file(path: str) -> str:
    """对「LF 归一化后的内容」计算 SHA-256。

    约定：先把 CRLF 统一为 LF 再哈希，这样无论原始文件是哪种换行符，
    任何人在任何平台按同一步骤复算都能得到一致结果（页面会注明该约定）。
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    norm = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def build_diff_json(old_lines: list, new_lines: list, ctx: int) -> list:
    """把 unified diff 解析成逐行配对数据，供前端渲染。

    每条：[op, old_line_no, new_line_no, old_text, new_text]
      op: '=' 相同 ｜ '-' 仅旧 ｜ '+' 仅新 ｜ '!' 修改（旧→新）
    """
    diff = list(
        unified_diff(
            old_lines,
            new_lines,
            fromfile="old",
            tofile="new",
            lineterm="",
            n=ctx,
        )
    )
    rows = []
    # 跳过 unified diff 的 --- / +++ 两行文件头
    start = 0
    for i, line in enumerate(diff):
        if line.startswith("--- ") or line.startswith("+++ "):
            continue
        start = i
        break

    on_old = on_new = 0  # 下一行的预期行号（从 1 起）
    buf_old, buf_new = [], []  # 修改块缓冲：连续 - 行、+ 行
    block_old_start = block_new_start = 0  # 当前修改块起始行号
    i = start

    def flush():
        """把缓冲的修改块写成 -/+ 配对（或 '!' 修改行）。"""
        nonlocal buf_old, buf_new, block_old_start, block_new_start
        if not buf_old and not buf_new:
            return
        if not buf_old:
            for j, t in enumerate(buf_new):
                rows.append(["+", None, block_new_start + j, None, t])
        elif not buf_new:
            for j, t in enumerate(buf_old):
                rows.append(["-", block_old_start + j, None, t, None])
        else:
            m = max(len(buf_old), len(buf_new))
            for j in range(m):
                o = buf_old[j] if j < len(buf_old) else None
                n = buf_new[j] if j < len(buf_new) else None
                rows.append(["!", block_old_start + j, block_new_start + j, o, n])
        buf_old, buf_new = [], []
        block_old_start = block_new_start = 0

    while i < len(diff):
        line = diff[i]
        if line.startswith("@@"):
            flush()
            parts = line.split(" ")
            try:
                o_start = int(parts[1].split(",")[0][1:])
                n_start = int(parts[2].split(",")[0][1:])
            except (IndexError, ValueError):
                o_start = n_start = 1
            on_old, on_new = o_start, n_start
        elif line.startswith("-"):
            if not buf_old and not buf_new:
                block_old_start = on_old
                block_new_start = on_new
            buf_old.append(line[1:])
            on_old += 1
        elif line.startswith("+"):
            if not buf_old and not buf_new:
                block_old_start = on_old
                block_new_start = on_new
            buf_new.append(line[1:])
            on_new += 1
        else:
            flush()
            rows.append(["=", on_old, on_new, line[1:], line[1:]])
            on_old += 1
            on_new += 1
        i += 1
    flush()
    return rows


def render_html(old_name, new_name, old_sha, new_sha, old_lines, new_lines, rows) -> str:
    data = {
        "a": {"name": old_name, "sha": old_sha, "lines": len(old_lines),
              "raw": "\n".join(old_lines)},
        "b": {"name": new_name, "sha": new_sha, "lines": len(new_lines),
              "raw": "\n".join(new_lines)},
        "rows": rows,
    }
    data_json = json.dumps(data, ensure_ascii=False)

    page = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>diff 审查报告 · __TITLE_A__ → __TITLE_B__</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body { margin:0; background:#0f1115; color:#e6e6e6;
         font-family:-apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif; }
  /* 占满预览窗口：拖宽页面时，左右代码栏随可用宽度一起展开。 */
  .wrap { width:100%; max-width:none; margin:0; padding:20px clamp(12px,2vw,32px) 60px; }
  h1 { font-size:20px; font-weight:600; margin:0 0 2px; }
  .sub { color:#8a93a6; font-size:13px; margin-bottom:16px; }
  .files { display:flex; gap:10px; margin-bottom:14px; flex-wrap:wrap; }
  .filechip { background:#1a1d24; border:1px solid #2a2f3a; border-radius:8px;
               padding:8px 12px; font-size:12px; color:#b6c2d2; }
  .filechip b { color:#e6e6e6; font-family:ui-monospace,Consolas,monospace; }
  .filechip .sha { color:#6b7484; font-family:ui-monospace,Consolas,monospace; }
  .toolbar { position:sticky; top:0; z-index:10; background:#14171d; border:1px solid #2a2f3a;
              border-radius:10px; padding:8px 10px; display:flex; gap:8px; align-items:center;
              flex-wrap:wrap; margin-bottom:14px; }
  .btn { background:#1f242d; border:1px solid #333a47; color:#d5dce6; border-radius:7px;
          padding:5px 12px; font-size:13px; cursor:pointer; }
  .btn:hover { background:#2a313d; }
  .btn.on { background:#185fa5; border-color:#378add; color:#fff; }
  .sep { flex:1; }
  .hunks { display:flex; gap:6px; flex-wrap:wrap; }
  .hunkbtn { background:#232836; border:1px solid #38404f; color:#9fb0c8; border-radius:99px;
              padding:3px 11px; font-size:12px; cursor:pointer; }
  .hunkbtn:hover { background:#2e3647; color:#e6e6e6; }
  .view { border:1px solid #2a2f3a; border-radius:10px; overflow:hidden; }
  .colhead { display:grid; grid-template-columns:1fr 1fr; background:#171a21;
              border-bottom:1px solid #2a2f3a; font-size:13px; font-weight:600; }
  .colhead > div { padding:9px 12px; }
  .colhead .newh { color:#7fd0a0; border-left:1px solid #2a2f3a; }
  /* 关键：grid 列必须用 minmax(0, 1fr) 才能真正允许收缩到 1fr 分配。
     子项 .col 设 min-width:0 仍不够——1fr 默认按子项 min-content 撑开列宽。 */
  .dtable { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); }
  .col { font-family:ui-monospace,Consolas,"SF Mono",monospace; font-size:12.5px;
          line-height:1.6; min-width:0; }
  .line { display:flex; }
  .ln { min-width:64px; text-align:right; padding:0 10px 0 4px; color:#5a6474;
         user-select:none; flex-shrink:0; font-family:ui-monospace,Consolas,monospace; }
  .ln .mark { display:inline-block; width:14px; text-align:left; margin-right:4px; font-weight:700; }
  .line.add .ln .mark { color:#4f9a6d; }
  .line.del .ln .mark { color:#b0606f; }
  .tx { flex:1 1 0; min-width:0; white-space:pre-wrap;
        overflow-wrap:anywhere; word-break:break-word; padding-right:8px; }
  /* 不换行模式：一行到底，横向滚动看全（行号列固定）。
     关键：.col 加 max-width:100% 限制 grid 子项被内部长内容撑开（grid 1fr 仍会按
     子项 min-content 扩展），.dtable 兜底 overflow。 */
  body.nowrap .tx { white-space:pre; overflow-wrap:normal; word-break:normal; overflow:visible; }
  body.nowrap .col { overflow-x:auto; max-width:100%; }
  body.nowrap .dtable { overflow-x:auto; }
  body.nowrap .ln { position:sticky; left:0; background:inherit; z-index:1; }
  .line.add { background:#12361f; }
  .line.add .tx { color:#9fe8c0; }
  .line.del { background:#3a1820; }
  .line.del .tx { color:#f0a8b5; }
  .line.same .tx { color:#c2cbd9; }
  .line .tx.dim { color:#7a8494; }
  /* 空位占位：让两侧行高保持一致，内容真正留空 */
  .ln.empty { color:transparent; }
  .tx.empty { visibility:hidden; }
  .gap { display:flex; align-items:center; padding:3px 0; }
  .gap::before { content:"\\22EF"; color:#4a5364; padding-left:10px; font-size:12px; }
  .footer { margin-top:18px; display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; }
  .footbox { border:1px solid #2a2f3a; border-radius:10px; background:#14171d; padding:12px 14px; }
  .footbox h3 { margin:0 0 8px; font-size:14px; }
  .footbox p { margin:0; font-size:13px; color:#8a93a6; min-height:60px; }
  .fb1 h3 { color:#7fd0a0; } .fb2 h3 { color:#7cc4ff; } .fb3 h3 { color:#c9b37a; }
  .note { margin-top:14px; font-size:12px; color:#5f6b7d; }
</style>
</head>
<body>
<div class="wrap">
  <h1>diff 审查报告</h1>
  <div class="sub" id="subtitle"></div>

  <div class="files">
    <div class="filechip">旧版 <b>__NAME_A__</b><br><span class="sha">sha256 <span id="shaA"></span></span></div>
    <div class="filechip">新版 <b>__NAME_B__</b><br><span class="sha">sha256 <span id="shaB"></span></span></div>
  </div>

  <div class="toolbar">
    <button class="btn on" id="onlyBtn">只看改动</button>
    <button class="btn on" id="wrapBtn">换行</button>
    <button class="btn" id="copyA">复制旧版</button>
    <button class="btn" id="copyB">复制新版</button>
    <span class="sep"></span>
    <div class="hunks" id="hunks"></div>
  </div>

  <div class="view">
    <div class="colhead">
      <div>旧版 · <span id="headA"></span></div>
      <div class="newh">新版 · <span id="headB"></span></div>
    </div>
    <div class="dtable" id="table">
      <div class="col old" id="colOld"></div>
      <div class="col new" id="colNew"></div>
    </div>
  </div>

  <div class="footer">
    <div class="footbox fb1"><h3>我们做的</h3><p contenteditable="true">填写本次改动中我们的贡献…</p></div>
    <div class="footbox fb2"><h3>自动化验证</h3><p contenteditable="true">填写验证方式（测试、构建、hash 核对）…</p></div>
    <div class="footbox fb3"><h3>不变底稿</h3><p contenteditable="true">填写沿用的既有方案 / 引用来源…</p></div>
  </div>

  <div class="note">本页由 ppshu 的 diff 报告生成器生成 · 数据内嵌可离线打开 · SHA-256 按 LF 归一化后复算 · 三栏内容可点击编辑后另存。</div>
</div>

<script id="data" type="application/json">__DATA_JSON__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const A = D.a, B = D.b, ROWS = D.rows;
const esc = s => (s ?? '').replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

document.getElementById('subtitle').textContent =
  A.lines + ' 行 → ' + B.lines + ' 行 · ' + ROWS.length + ' 条记录';
document.getElementById('shaA').textContent = A.sha.slice(0, 12) + '…';
document.getElementById('shaB').textContent = B.sha.slice(0, 12) + '…';
document.getElementById('headA').textContent = A.name + ' (' + A.lines + ' 行)';
document.getElementById('headB').textContent = B.name + ' (' + B.lines + ' 行)';

let onlyMode = false;
const colOld = document.getElementById('colOld');
const colNew = document.getElementById('colNew');

function render() {
  colOld.innerHTML = ''; colNew.innerHTML = '';
  const hunkStarts = [];

  for (let i = 0; i < ROWS.length; i++) {
    const [op, ol, nl, ot, nt] = ROWS[i];
    const changed = op !== '=';

    if (changed && (i === 0 || ROWS[i - 1][0] === '=')) hunkStarts.push(i);

    const odiv = document.createElement('div');
    const ndiv = document.createElement('div');
    odiv.dataset.idx = i; ndiv.dataset.idx = i;

    // 符号标记：- 仅旧 / + 仅新 / ! 修改（两侧同标）
    const oldMark = (op === '-' || op === '!') ? '-' : '';
    const newMark = (op === '+' || op === '!') ? '+' : '';

    // 行号：该侧有行则显示行号，无行则显示空占位（保证两侧行高一致、内容真正留空）
    const oldNum = (ol !== null && ol !== undefined) ? ol : '';
    const newNum = (nl !== null && nl !== undefined) ? nl : '';

    odiv.className = 'line ' + (op === '+' ? 'add' : (op === '-' || op === '!') ? 'del' : 'same');
    ndiv.className = 'line ' + (op === '-' ? 'del' : (op === '+' || op === '!') ? 'add' : 'same');

    odiv.innerHTML = '<span class="ln' + (ol == null ? ' empty' : '') + '"><span class="mark">' + oldMark + '</span>' + (ol ?? '') + '</span><span class="tx' + (ot == null ? ' empty' : '') + '">' + esc(ot ?? '') + '</span>';
    ndiv.innerHTML = '<span class="ln' + (nl == null ? ' empty' : '') + '"><span class="mark">' + newMark + '</span>' + (nl ?? '') + '</span><span class="tx' + (nt == null ? ' empty' : '') + '">' + esc(nt ?? '') + '</span>';

    if (onlyMode && op === '=') continue;
    colOld.appendChild(odiv);
    colNew.appendChild(ndiv);
  }

  const hunks = document.getElementById('hunks');
  hunks.innerHTML = '';
  hunkStarts.forEach((start, idx) => {
    const b = document.createElement('button');
    b.className = 'hunkbtn';
    b.textContent = '块 ' + (idx + 1);
    b.onclick = () => {
      const hit = [...colOld.querySelectorAll('.line')].find(el => +el.dataset.idx >= start);
      if (hit) {
        hit.scrollIntoView({ block: 'center', behavior: 'smooth' });
        hit.style.outline = '2px solid #378add';
        setTimeout(() => hit.style.outline = '', 1200);
      }
    };
    hunks.appendChild(b);
  });
}

document.getElementById('onlyBtn').onclick = () => {
  onlyMode = !onlyMode;
  document.getElementById('onlyBtn').classList.toggle('on', onlyMode);
  render();
};
document.getElementById('wrapBtn').onclick = () => {
  document.body.classList.toggle('nowrap');
  document.getElementById('wrapBtn').classList.toggle('on', !document.body.classList.contains('nowrap'));
};
document.getElementById('copyA').onclick = () => navigator.clipboard.writeText(A.raw || '');
document.getElementById('copyB').onclick = () => navigator.clipboard.writeText(B.raw || '');
render();
</script>
</body>
</html>
"""
    return (
        page.replace("__TITLE_A__", _html.escape(old_name))
        .replace("__TITLE_B__", _html.escape(new_name))
        .replace("__NAME_A__", _html.escape(old_name))
        .replace("__NAME_B__", _html.escape(new_name))
        # 关键：JSON 内嵌进 <script> 块，若数据本身含 "</script>" 会提前截断标签。
        # 统一转义成 \u003c/script\u003e，浏览器 JSON.parse 后还原为原始文本。
        .replace("__DATA_JSON__", data_json.replace("</script", "<\\/script"))
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="ppshu diff 报告生成器")
    ap.add_argument("-a", "--old", required=True, help="旧版文件路径")
    ap.add_argument("-b", "--new", required=True, help="新版文件路径")
    ap.add_argument("-o", "--output", help="输出 HTML 路径（默认 stdout）")
    ap.add_argument("--name-a", help="旧版显示名（默认文件名）")
    ap.add_argument("--name-b", help="新版显示名（默认文件名）")
    ap.add_argument("-c", "--context", type=int, default=3, help="上下文行数（默认 3）")
    args = ap.parse_args()

    old_lines = read_lines(args.old)
    new_lines = read_lines(args.new)
    rows = build_diff_json(old_lines, new_lines, args.context)
    name_a = args.name_a or args.old.replace("\\", "/").split("/")[-1]
    name_b = args.name_b or args.new.replace("\\", "/").split("/")[-1]

    html_out = render_html(
        name_a, name_b,
        sha256_of_file(args.old), sha256_of_file(args.new),
        old_lines, new_lines, rows,
    )
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html_out)
        print(args.output)
    else:
        sys.stdout.write(html_out)


if __name__ == "__main__":
    main()
