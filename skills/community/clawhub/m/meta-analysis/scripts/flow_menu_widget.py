#!/usr/bin/env python3
"""flow_menu_widget.py — CCM 交互选单渲染器（HTML 片段，紧凑版）。

单一真源：复用 flow_menu.build_menu() 的确定性菜单模型，仅新增 HTML 渲染，
不复制任何状态机/校验逻辑。产物可直接作为 Visualizer show_widget 的 widget_code，
实现「选单式」上下文菜单（替代默认 plaintext）。

用法:
  python flow_menu_widget.py [--session P] [--lang zh|en] [--out FILE]

stdout = 可内联 HTML 片段；--out 另存一份。
点击只在本地高亮 + 提示下一步，不回传；决策仍走
  python scripts/flow_menu.py decide --option N --apply
"""
import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import flow_menu  # noqa: E402
import form_schema  # noqa: E402

_STYLE = (
    "<style>"
    ".ccm{background:var(--color-background-primary);border:0.5px solid var(--color-border-tertiary);"
    "border-radius:var(--border-radius-lg);padding:1rem 1.25rem;max-width:680px;"
    "font-family:var(--font-sans);color:var(--color-text-primary)}"
    ".ccm .hd{font-size:12px;color:var(--color-text-tertiary);margin-bottom:10px}"
    ".ccm .nav{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px}"
    ".ccm .pill{font-size:11px;padding:3px 8px;border-radius:var(--border-radius-md);"
    "border:0.5px solid var(--color-border-tertiary);color:var(--color-text-tertiary)}"
    ".ccm .pill.done{background:var(--color-background-secondary);color:var(--color-text-secondary)}"
    ".ccm .pill.cur{border-color:var(--color-border-info);background:var(--color-background-info);"
    "color:var(--color-text-info)}"
    ".ccm .ttl{font-weight:500;font-size:15px}"
    ".ccm .chip{font-size:12px;font-weight:400;padding:2px 8px;border-radius:var(--border-radius-md);"
    "margin-left:8px;background:var(--color-background-info);color:var(--color-text-info);"
    "border:0.5px solid var(--color-border-info)}"
    ".ccm .chip.red{background:var(--color-background-danger);color:var(--color-text-danger);"
    "border-color:var(--color-border-danger)}"
    ".ccm .hint{font-size:13px;color:var(--color-text-info);background:var(--color-background-info);"
    "border-left:2px solid var(--color-border-info);padding:8px 10px;"
    "border-radius:var(--border-radius-md);margin:6px 0}"
    ".ccm .ln{font-size:13px;line-height:1.7}"
    ".ccm .warn{font-size:12px;color:var(--color-text-danger);"
    "border-left:2px solid var(--color-border-danger);padding-left:8px;margin:4px 0}"
    ".ccm .opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:16px}"
    ".ccm button{width:100%;padding:10px 12px;text-align:left;font-size:13px;"
    "border-radius:var(--border-radius-md);border:0.5px solid var(--color-border-secondary);"
    "background:transparent;color:var(--color-text-primary);cursor:pointer}"
    ".ccm button.on{border-color:var(--color-border-info);background:var(--color-background-info)}"
    ".ccm .sel{margin-top:14px;font-size:13px;color:var(--color-text-tertiary);min-height:20px}"
    "</style>"
)

_SCRIPT = (
    "<script>"
    "function pick(b,n,l){var o=document.querySelectorAll('.ccm button');"
    "for(var i=0;i<o.length;i++){o[i].className='';}"
    "b.className='on';"
    "document.getElementById('sel').innerHTML='已选 <b style=\"font-weight:500\">['+n+'] '+l+"
    "'</b><br><span style=\"color:var(--color-text-tertiary);font-size:12px\">把选项号告诉我，"
    "我执行 decide --option '+n+' --apply</span>';}"
    "</script>"
)

_LABELED = ("missing", "probe", "scope", "limit", "raw_topic", "query",
            "untranslated", "retracted", "type_dist", "type_confirm",
            "rule_src", "pending_pdf", "type_readonly", "gate_dist")


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _strip_emoji(s):
    out = []
    for ch in str(s):
        o = ord(ch)
        if 0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF or o in (0xFE0F, 0x20E3):
            continue
        out.append(ch)
    return "".join(out).strip()


def _line_html(k, v, lang):
    if isinstance(v, tuple):
        v = v[-1]
    txt = _esc(v)
    if k == "hint":
        return f'<div class="hint">{txt}</div>'
    if k in _LABELED:
        lab = _esc(_strip_emoji(flow_menu.L(k, lang)))
        txt = f'<span style="color:var(--color-text-secondary)">{lab}：</span>{txt}'
    return f'<div class="ln">{txt}</div>'


def render_menu_widget(m, lang="zh"):
    """菜单模型 → 可内联 HTML 片段（紧凑、类驱动）。"""
    sid = m["await"]["stage_id"]
    prog = m["progress"]
    pills = []
    for _blk, s_id, lab in form_schema.STAGE_ORDER:
        label = lab if lang == "zh" else flow_menu._EN_SHORT.get(s_id, lab)
        status = prog.get(s_id, "pending")
        cls = "pill cur" if status == "current" else ("pill done" if status == "done" else "pill")
        pills.append(f'<span class="{cls}">{_esc(s_id.split(".")[0])} {_esc(label)}</span>')
    nav = '<div class="nav">' + "".join(pills) + "</div>"
    hd = f'<div class="hd">全流程 · 当前停靠 {_esc(sid or "—")}</div>'

    head = '<h2 class="sr-only">CCM 上下文菜单（选单式，可点选）</h2>'
    if m["await"]["kind"] == "done":
        body = f'<div class="ttl">{_esc(_strip_emoji(m["tag"]))}</div>'
        return head + _STYLE + f'<div class="ccm">{hd}{nav}{body}</div>'

    chip_cls = "chip red" if m["redline"] else "chip"
    title = _esc(flow_menu._ccm_title(sid, lang)) if sid else _esc(m["title"] or "")
    body = [f'<div class="ttl">{title}<span class="{chip_cls}">'
            f'{_esc(_strip_emoji(m["tag"]))}</span></div>']
    for w in m["warnings"]:
        body.append(f'<div class="warn">{_esc(_strip_emoji(w[-1] if isinstance(w, tuple) else w))}</div>')
    for k, v in m["lines"]:
        body.append(_line_html(k, v, lang))
    if m["options"]:
        btns = []
        for o in m["options"]:
            lab = _esc(o["label"]) + ("（暂不可用）" if o.get("blocked") else "")
            btns.append(f'<button onclick="pick(this,{o["n"]},\'{_esc(o["label"])}\')">'
                        f'[{o["n"]}] {lab}</button>')
        body.append('<div class="opts">' + "".join(btns) + "</div>")
    body.append('<div class="sel" id="sel">点选项查看下一步</div>')
    return head + _STYLE + '<div class="ccm">' + hd + nav + "".join(body) + "</div>" + _SCRIPT


def main(argv=None):
    ap = argparse.ArgumentParser(prog="flow_menu_widget",
                                 description="CCM 选单式菜单 → HTML 片段")
    ap.add_argument("--session", "-s", default=None)
    ap.add_argument("--runs-dir", default=None)
    ap.add_argument("--lang", default=None, choices=["zh", "en"])
    ap.add_argument("--out", default=None, help="另存 HTML 文件")
    a = ap.parse_args(argv)
    lang = flow_menu._lang(a.lang)
    sess, _p = flow_menu.resolve_session(a.session, a.runs_dir)
    html = render_menu_widget(flow_menu.build_menu(sess, lang), lang)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(html)
    sys.stdout.write(html)
    return 0


if __name__ == "__main__":
    sys.exit(main())
