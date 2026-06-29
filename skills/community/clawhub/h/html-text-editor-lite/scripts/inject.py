#!/usr/bin/env python3
"""
html-text-editor-lite : inject a lightweight inline text editor into any static HTML.

Adds a floating toolbar (bottom-right):
  - 开始编辑 / Edit   : toggle contentEditable on all leaf text blocks
  - 暂存 / Save        : persist edits to localStorage (survives refresh)
  - 导出改动给AI / Diff : download a small JSON of {orig,new} per CHANGED block  <-- recommended round-trip
  - 导出干净版 / Clean : (fallback) download a clean standalone HTML with editor stripped

Why JSON-diff export is the default round-trip:
  - It records only the text blocks the user actually changed, each carrying BOTH the
    original innerHTML and the new innerHTML. The companion apply_edits.py then locates
    each `orig` by CONTENT inside the real source file and replaces it with `new`.
  - This is immune to (a) structure/position drift, (b) browser re-serialization that
    mangles inline styles (e.g. font-family:"X" -> font-family:"" garbage), and
    (c) leaving editor residue in the source. The source file stays the single source
    of truth; the browser never overwrites it wholesale.

Usage:
    python inject.py <input.html> [-o output.html] [--force] [--inplace]
    python inject.py in.html --exclude ".side-nav,.legend"
"""
import argparse
import os
import re
import sys
import hashlib

START_MARK = "<!-- ==== HVE-LITE START (html-text-editor-lite) ==== -->"
END_MARK = "<!-- ==== HVE-LITE END ==== -->"

EDITOR_TEMPLATE = """{START}
<style>
  #hve-bar {{ position:fixed; right:18px; bottom:18px; z-index:99999; display:flex; gap:8px;
    background:#1f2937; padding:8px 10px; border-radius:10px; box-shadow:0 6px 20px rgba(0,0,0,0.25);
    font-family:"PingFang SC","Microsoft YaHei",sans-serif; align-items:center; }}
  #hve-bar button {{ font-size:13px; font-weight:600; border:none; border-radius:7px; padding:7px 13px;
    cursor:pointer; transition:opacity 0.15s; color:#fff; }}
  #hve-bar button:hover {{ opacity:0.85; }}
  #hve-edit {{ background:#2563eb; }}
  #hve-edit.on {{ background:#15803d; }}
  #hve-save {{ background:#374151; }}
  #hve-diff {{ background:#b45309; }}
  #hve-clean {{ background:#4b5563; font-weight:500; }}
  #hve-bar .hve-hint {{ color:#cbd5e1; font-size:11.5px; align-self:center; padding:0 4px;
    max-width:180px; line-height:1.4; }}
  body.hve-editing [data-hve]:hover {{ outline:1.5px dashed #2563eb; outline-offset:2px; cursor:text; }}
  body.hve-editing [contenteditable="true"]:focus {{ outline:2px solid #2563eb; outline-offset:2px;
    background:rgba(37,99,235,0.04); }}
  @media print {{ #hve-bar {{ display:none !important; }} }}
</style>
<div id="hve-bar">
  <span class="hve-hint" id="hve-status">点「开始编辑」后，直接点页面文字即可改</span>
  <button id="hve-edit">&#9998; 开始编辑</button>
  <button id="hve-save">&#128190; 暂存</button>
  <button id="hve-diff">&#11015; 导出改动给AI</button>
  <button id="hve-clean">导出干净版</button>
</div>
<script>
(function(){{
  var KEY = '{STORAGE_KEY}';
  var EXCLUDE = {EXCLUDE_JSON};
  var editing = false;
  var editBtn = document.getElementById('hve-edit');
  var saveBtn = document.getElementById('hve-save');
  var diffBtn = document.getElementById('hve-diff');
  var cleanBtn = document.getElementById('hve-clean');
  var statusEl = document.getElementById('hve-status');

  var INLINE = {{SPAN:1,A:1,B:1,I:1,STRONG:1,EM:1,SMALL:1,LABEL:1,CODE:1,SUP:1,SUB:1,
    MARK:1,U:1,S:1,DEL:1,INS:1,TIME:1,FONT:1,BR:1,IMG:1,SVG:1,ABBR:1,CITE:1,Q:1,KBD:1,
    VAR:1,WBR:1,BDI:1,BDO:1,RUBY:1,SAMP:1}};
  var SKIP_TAGS = {{SCRIPT:1,STYLE:1,NOSCRIPT:1,TEMPLATE:1,SVG:1,CANVAS:1,IFRAME:1,
    INPUT:1,TEXTAREA:1,SELECT:1,OPTION:1,BUTTON:1}};

  function excluded(el){{
    for (var i=0;i<EXCLUDE.length;i++){{ if (EXCLUDE[i] && el.closest(EXCLUDE[i])) return true; }}
    return false;
  }}
  function isInline(el){{ return INLINE[el.tagName] === 1; }}
  function hasBlockChild(el){{
    var c = el.children;
    for (var i=0;i<c.length;i++){{ if (!isInline(c[i])) return true; }}
    return false;
  }}
  function hasText(el){{ return !!el.textContent && !!el.textContent.trim(); }}

  var leaves = [];
  function mark(el){{ el.setAttribute('data-hve','1'); leaves.push(el); }}
  function wrapTextNode(node){{
    var s = document.createElement('span');
    s.className = 'hve-t';
    node.parentNode.insertBefore(s, node);
    s.appendChild(node);
    mark(s);
  }}
  function walk(el){{
    if (!el || el.nodeType !== 1) return;
    if (SKIP_TAGS[el.tagName]) return;
    if (el.id === 'hve-bar' || el.closest('#hve-bar')) return;
    if (excluded(el)) return;
    if (!hasBlockChild(el)) {{ if (hasText(el)) mark(el); return; }}
    var kids = Array.prototype.slice.call(el.childNodes);
    for (var i=0;i<kids.length;i++){{
      var n = kids[i];
      if (n.nodeType === 3) {{ if (n.nodeValue && n.nodeValue.trim()) wrapTextNode(n); }}
      else if (n.nodeType === 1) {{ walk(n); }}
    }}
  }}
  walk(document.body);

  // Snapshot TRUE original innerHTML per block (before any localStorage restore),
  // so the exported diff reflects the total change vs the source file.
  var origs = leaves.map(function(el){{ return el.innerHTML; }});

  try {{
    var saved = JSON.parse(localStorage.getItem(KEY) || '{{}}');
    leaves.forEach(function(el, i){{ if (saved[i] !== undefined) el.innerHTML = saved[i]; }});
    if (Object.keys(saved).length) statusEl.textContent = '\u5df2\u6062\u590d\u4e0a\u6b21\u6682\u5b58\u7684\u4fee\u6539';
  }} catch(e){{}}

  editBtn.addEventListener('click', function(){{
    editing = !editing;
    document.body.classList.toggle('hve-editing', editing);
    leaves.forEach(function(el){{ el.contentEditable = editing ? 'true' : 'false'; }});
    editBtn.classList.toggle('on', editing);
    editBtn.innerHTML = editing ? '\u2713 \u7f16\u8f91\u4e2d\uff08\u518d\u70b9\u5173\u95ed\uff09' : '\u270e \u5f00\u59cb\u7f16\u8f91';
    statusEl.textContent = editing ? '\u76f4\u63a5\u70b9\u6587\u5b57\u4fee\u6539\uff0c\u6539\u5b8c\u70b9\u300c\u5bfc\u51fa\u6539\u52a8\u7ed9AI\u300d' : '\u5df2\u9000\u51fa\u7f16\u8f91';
  }});

  saveBtn.addEventListener('click', function(){{
    var data = {{}};
    leaves.forEach(function(el, i){{ data[i] = el.innerHTML; }});
    localStorage.setItem(KEY, JSON.stringify(data));
    statusEl.textContent = '\u2713 \u5df2\u6682\u5b58\u5230\u672c\u6d4f\u89c8\u5668\uff08' + new Date().toLocaleTimeString() + '\uff09';
  }});

  // PRIMARY: export a small JSON of changed blocks {{orig,new}} for content-based backfill.
  diffBtn.addEventListener('click', function(){{
    var changes = [];
    leaves.forEach(function(el, i){{
      var now = el.innerHTML;
      if (origs[i] != null && origs[i].trim() !== now.trim()) {{
        changes.push({{ orig: origs[i], "new": now }});
      }}
    }});
    if (changes.length === 0) {{
      statusEl.textContent = '\u8fd8\u6ca1\u68c0\u6d4b\u5230\u6539\u52a8\uff5e\u5148\u70b9\u2460\u5f00\u59cb\u7f16\u8f91';
      alert('\u8fd8\u6ca1\u68c0\u6d4b\u5230\u4efb\u4f55\u6587\u5b57\u6539\u52a8\u3002\u5148\u70b9\u300c\u5f00\u59cb\u7f16\u8f91\u300d\uff0c\u6539\u5b8c\u518d\u5bfc\u51fa\u3002');
      return;
    }}
    var payload = JSON.stringify({{_note:'\u628a\u8fd9\u4e2a\u6587\u4ef6\u53d1\u7ed9AI\uff0c\u8bf4\u300c\u5e94\u7528\u8fd9\u4e9b\u6539\u52a8\u300d\u5373\u53ef', changes: changes}}, null, 1);
    var blob = new Blob([payload], {{type:'application/json'}});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = '\u6211\u7684\u6539\u52a8-\u4ea4\u7ed9AI.json';
    a.click();
    statusEl.textContent = '\u2713 \u5df2\u5bfc\u51fa ' + changes.length + ' \u5904\u6539\u52a8\uff0c\u53d1\u7ed9 AI \u5373\u53ef';
  }});

  // FALLBACK: clean standalone HTML (use only when there is no source file to backfill).
  cleanBtn.addEventListener('click', function(){{
    var clone = document.documentElement.cloneNode(true);
    var bar = clone.querySelector('#hve-bar'); if (bar) bar.remove();
    clone.querySelectorAll('[data-hve]').forEach(function(el){{
      el.removeAttribute('data-hve'); el.removeAttribute('contenteditable');
    }});
    clone.querySelectorAll('span.hve-t').forEach(function(el){{
      var p = el.parentNode;
      while (el.firstChild) p.insertBefore(el.firstChild, el);
      p.removeChild(el);
    }});
    var html = clone.outerHTML;
    var re = /<!-- ==== HVE-LITE START[\\s\\S]*?HVE-LITE END ==== -->/;
    html = html.replace(re, '');
    html = '<!DOCTYPE html>\\n' + html;
    var blob = new Blob([html], {{type:'text/html'}});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'clean.html';
    a.click();
    statusEl.textContent = '\u2713 \u5df2\u5bfc\u51fa\u5e72\u51c0\u7248 clean.html\uff08\u4ec5\u65e0\u6e90\u6587\u4ef6\u65f6\u7528\uff09';
  }});
}})();
</script>
{END}"""


def build_editor(storage_key: str, exclude_selectors):
    import json
    exclude_json = json.dumps(exclude_selectors, ensure_ascii=False)
    return EDITOR_TEMPLATE.format(
        START=START_MARK, END=END_MARK,
        STORAGE_KEY=storage_key, EXCLUDE_JSON=exclude_json,
    )


def main():
    ap = argparse.ArgumentParser(description="Inject lightweight inline text editor into HTML.")
    ap.add_argument("input", help="input HTML file")
    ap.add_argument("-o", "--output", help="output HTML file (default: <input>-editable.html)")
    ap.add_argument("--force", action="store_true", help="overwrite output if exists")
    ap.add_argument("--exclude", default=".side-nav,nav",
                    help="comma-separated CSS selectors to exclude from editing (default: .side-nav,nav)")
    ap.add_argument("--inplace", action="store_true",
                    help="write back to the input file instead of a new -editable file")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        html = f.read()

    if "</body>" not in html:
        print("ERROR: no </body> tag found — is this a complete HTML document?", file=sys.stderr)
        sys.exit(1)

    html = re.sub(r"<!-- ==== HVE-LITE START[\s\S]*?HVE-LITE END ==== -->\s*", "", html)

    if args.inplace:
        out_path = args.input
    elif args.output:
        out_path = args.output
    else:
        base, ext = os.path.splitext(args.input)
        out_path = f"{base}-editable{ext or '.html'}"

    if os.path.exists(out_path) and not args.force and out_path != args.input:
        print(f"ERROR: output exists: {out_path} (use --force)", file=sys.stderr)
        sys.exit(1)

    storage_key = "hve_" + hashlib.md5(os.path.basename(out_path).encode("utf-8")).hexdigest()[:10]
    exclude_selectors = [s.strip() for s in args.exclude.split(",") if s.strip()]
    editor = build_editor(storage_key, exclude_selectors)

    new_html = html.replace("</body>", editor + "\n</body>", 1)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"OK  -> {out_path}")
    print(f"    storage key : {storage_key}")
    print(f"    excluded    : {exclude_selectors}")
    print(f"    next: open it, edit text, click 「导出改动给AI」 -> apply with apply_edits.py")


if __name__ == "__main__":
    main()
