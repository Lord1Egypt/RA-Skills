# -*- coding: utf-8 -*-
"""个股公开数据速读 · 出报告（V2 米白 · 公众号 8 贴图初稿）。
读 analyze.py 产出的 analysis.json，生成 01..08-*.html（图表+数字已对）。
中立复盘文案是模板初稿，交付前请按 references/report-structure.md 人工/LLM 润色，再 screenshot.js 截图。
用法：python3 build_report.py <out目录> [公司简称]
⚠️ 合规：不荐股/不预测，自动套风险提示条（references/compliance.md）。
"""
import os
import sys
import json
from html import escape

# 默认不注入作者品牌；需要署名时用 --brand/--handle 或环境变量。
BRAND = os.environ.get("STOCK_REPORT_BRAND", "")
HANDLE = os.environ.get("STOCK_REPORT_HANDLE", "")

# 字体取自兄弟 skill hekouwang-content-factory（两者同在 ~/.claude/skills/ 下）。
# 动态推算 skills 目录 → 拼兄弟 skill，换机/改用户名都不断；可用环境变量覆盖；对外发布改相对内嵌。
_SKILLS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS = os.environ.get("HEKOUWANG_FONTS_DIR") or os.path.join(
    _SKILLS_DIR, "hekouwang-content-factory", "assets", "fonts")

HEAD_TPL = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<!-- 字体仅用本地 @font-face 与系统字体；截图环境不拉远程字体。 -->
<style>
@font-face{font-family:'Anthropic Sans';src:url('FONTS/anthropicSans.woff2') format('woff2');font-weight:300 800;font-display:swap}
@font-face{font-family:'Anthropic Mono';src:url('FONTS/anthropicMono.woff2') format('woff2');font-weight:300 800;font-display:swap}
@font-face{font-family:'Noto Sans SC';src:local('Noto Sans SC'),local('PingFang SC'),local('Microsoft YaHei');font-weight:400 900;font-display:swap}
:root{--bg:#faf9f5;--surface:#fff;--surface2:#f4f2eb;--line:rgba(20,20,19,.10);--line2:rgba(20,20,19,.17);--line3:rgba(20,20,19,.26);
--text:#1a1a18;--read:#3a3833;--text2:#56544e;--text3:#8a877e;--text4:#b3afa6;
--hot:#c15f3c;--hot2:#d07a52;--cool:#5c6b7a;--cool2:#4a5763;--ochre:#a07a3c;--warn:#c0392b;
--shadow:0 1px 2px rgba(20,20,19,.04),0 8px 24px rgba(20,20,19,.05);
--font:'Anthropic Sans','Noto Sans SC','PingFang SC',system-ui,sans-serif;--mono:'Anthropic Mono','PingFang SC',ui-monospace,monospace;--brand:'Noto Sans SC',system-ui,sans-serif;}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1350px;overflow:hidden}
body{background:var(--bg);color:var(--text);font-family:var(--font);-webkit-font-smoothing:antialiased}
.c{position:relative;width:1080px;height:1350px;display:flex;flex-direction:column;padding:74px 76px 0;overflow:hidden;isolation:isolate;background:radial-gradient(1300px 1050px at 50% -12%,#fffdf8,#faf9f5 46%,#f4f1ea)}
.mesh{position:absolute;inset:0;z-index:0;opacity:.7;background-image:linear-gradient(rgba(20,20,19,.022) 1px,transparent 1px),linear-gradient(90deg,rgba(20,20,19,.022) 1px,transparent 1px);background-size:74px 74px;-webkit-mask:radial-gradient(circle at 50% 24%,#000,transparent 86%)}
.orb{position:absolute;border-radius:50%;filter:blur(120px);z-index:0}.orb.a{width:680px;height:680px;background:radial-gradient(circle,rgba(193,95,60,.10),transparent 70%);top:-220px;right:-160px}.orb.b{width:440px;height:440px;background:radial-gradient(circle,rgba(92,107,122,.09),transparent 70%);bottom:-140px;left:-120px}
.hud{position:absolute;inset:40px;z-index:1;pointer-events:none}.hud i{position:absolute;width:30px;height:30px;border:2px solid var(--hot);opacity:.3}
.hud i:nth-child(1){left:0;top:0;border-right:0;border-bottom:0}.hud i:nth-child(2){right:0;top:0;border-left:0;border-bottom:0}.hud i:nth-child(3){left:0;bottom:0;border-right:0;border-top:0}.hud i:nth-child(4){right:0;bottom:0;border-left:0;border-top:0}
.sysbar{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:center;font-family:var(--mono);font-size:20px;letter-spacing:.16em;text-transform:uppercase;color:var(--text3);border-bottom:1px solid var(--line);padding-bottom:20px}
.sysbar .l{display:flex;align-items:center;gap:12px;color:var(--text2)}.sysbar .dot{width:11px;height:11px;border-radius:50%;background:var(--hot)}.sysbar .r{color:var(--hot)}
.bd{flex:1;position:relative;z-index:2;overflow:hidden;width:100%;min-height:0}.fit{position:absolute;top:0;left:0;transform-origin:top left}
.eyebrow{font-family:var(--mono);font-size:22px;font-weight:500;letter-spacing:.26em;color:var(--cool2);text-transform:uppercase;display:flex;align-items:center;gap:16px;margin-bottom:34px}.eyebrow span{width:54px;height:2px;background:linear-gradient(90deg,var(--cool),transparent)}
h1{font-size:88px;line-height:1.06;font-weight:900;letter-spacing:-.03em;margin-bottom:28px}h1 .hl{color:var(--hot)}
.lead{font-size:32px;line-height:1.62;color:var(--read);max-width:880px;margin-top:6px}.lead b{color:var(--text);font-weight:700}
.kicker{font-family:var(--mono);font-size:23px;letter-spacing:.15em;text-transform:uppercase;color:var(--cool2);margin-bottom:20px;display:flex;align-items:center;gap:14px}.kicker::before{content:'';width:34px;height:2px;background:var(--cool)}
.title{font-size:54px;font-weight:900;line-height:1.16;letter-spacing:-.02em;margin-bottom:28px}.title .u{color:var(--hot)}
.readout{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid var(--line2);border-radius:22px;overflow:hidden;background:#fff;box-shadow:var(--shadow);margin-top:48px}
.gauge{padding:32px 28px;border-right:1px solid var(--line);min-width:0}.gauge:last-child{border-right:0}
.gauge .gl{font-family:var(--mono);font-size:18px;letter-spacing:.06em;text-transform:uppercase;color:var(--text3);margin-bottom:14px;display:flex;align-items:center;gap:9px}.gauge .gl::before{content:'';width:9px;height:9px;border-radius:2px;background:var(--hot);flex:none}.gauge:nth-child(2) .gl::before{background:var(--cool)}.gauge:nth-child(3) .gl::before{background:var(--ochre)}
.gauge .gv{font-family:var(--mono);font-size:48px;font-weight:700;color:var(--hot);line-height:1;white-space:nowrap}.gauge:nth-child(2) .gv{color:var(--cool2)}.gauge:nth-child(3) .gv{color:var(--ochre)}
.gauge .gu{font-size:20px;color:var(--text3);margin-top:12px;line-height:1.4}
.fig{position:relative;background:#fff;border:1px solid var(--line2);border-radius:24px;padding:34px 38px 26px;box-shadow:var(--shadow);overflow:hidden}
.fig .fh{display:flex;justify-content:space-between;align-items:center;font-family:var(--mono);font-size:19px;letter-spacing:.1em;text-transform:uppercase;color:var(--text3);margin-bottom:22px}.fig .fh .id{color:var(--hot)}
.fig svg{width:100%;height:auto;display:block}.fig .cap{text-align:center;font-family:var(--mono);font-size:22px;color:var(--text3);margin-top:20px;line-height:1.5}.fig .cap b{color:var(--cool2);font-weight:600}
.note{font-size:24px;color:var(--text2);line-height:1.55;margin-top:26px}.note b{color:var(--text);font-weight:700}.note .h{color:var(--hot);font-weight:700}.note .w{color:var(--warn);font-weight:700}
.rows{display:flex;flex-direction:column;gap:18px;margin-top:4px}.row{display:flex;gap:24px;background:#fff;border:1px solid var(--line2);border-radius:20px;padding:30px 36px;box-shadow:var(--shadow)}.row .ri{font-size:42px;flex:none;width:56px;text-align:center}.row .rn{font-size:31px;font-weight:800;color:var(--text)}.row .rd{font-size:25px;color:var(--text2);margin-top:8px;line-height:1.5}.row .rd b{color:var(--text);font-weight:700}.row .rd .h{color:var(--hot);font-weight:700}.row .rd .w{color:var(--warn);font-weight:700}
.panel{background:#fff;border:1px solid var(--line2);border-radius:22px;padding:36px 42px;box-shadow:var(--shadow)}.panel .pd{font-size:29px;line-height:1.6;color:var(--read)}.panel .pd b{color:var(--text);font-weight:700}.panel .pd .h{color:var(--hot);font-weight:700}
.pull{position:relative;padding-top:36px}.pull::before{content:'';position:absolute;top:0;left:0;width:80px;height:4px;background:var(--hot)}.pull p{font-family:var(--font);font-size:56px;line-height:1.34;font-weight:800;letter-spacing:-.01em;color:var(--text);max-width:880px}.pull p em{font-style:normal;color:var(--hot)}.pull .by{margin-top:24px;font-family:var(--mono);font-size:23px;letter-spacing:.13em;text-transform:uppercase;color:var(--cool2)}
.disc{margin-top:36px;background:var(--surface2);border:1px solid var(--line2);border-radius:16px;padding:28px 32px;font-size:24px;line-height:1.6;color:var(--text2)}.disc b{color:var(--warn);font-weight:700}
.ghost{position:absolute;top:130px;right:-26px;z-index:1;font-family:var(--mono);font-weight:800;font-size:400px;line-height:.8;color:var(--text);opacity:.05;letter-spacing:-.06em}
.pn{position:absolute;right:76px;bottom:120px;z-index:3;font-family:var(--mono);font-size:22px;color:var(--text3)}
.ft{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:center;height:104px;border-top:1px solid var(--line);margin-top:14px}.brand{font-family:var(--brand);font-size:30px;font-weight:800;color:var(--text)}.handle{font-family:var(--mono);font-size:23px;color:var(--text3)}
</style></head><body>"""

HEAD = HEAD_TPL.replace("FONTS", FONTS)

def head_for(theme="v2"):
    h = HEAD
    if theme == "v3":
        h = (h.replace("--bg:#faf9f5", "--bg:#fbfcfe")
               .replace("--hot:#c15f3c", "--hot:#111111")
               .replace("--hot2:#d07a52", "--hot2:#333333")
               .replace("background:radial-gradient(1300px 1050px at 50% -12%,#fffdf8,#faf9f5 46%,#f4f1ea)",
                        "background:radial-gradient(900px 600px at 20% -5%,rgba(147,197,253,.15),transparent 50%),"
                        "radial-gradient(700px 500px at 85% 10%,rgba(196,181,253,.12),transparent 55%),#fbfcfe"))
    return h

FIT = """<script>(function(){function fit(){var bd=document.querySelector('.bd'),el=document.querySelector('.fit');if(!bd||!el)return;var W=bd.clientWidth,H=bd.clientHeight,k=1;for(var i=0;i<7;i++){el.style.width=(W/k)+'px';var vis=el.scrollHeight*k;var nk=k*(H/vis);nk=Math.max(0.5,Math.min(1.08,nk));if(Math.abs(nk-k)<0.004){k=nk;break;}k=nk;}el.style.width=(W/k)+'px';el.style.transform='scale('+k+')';var fh=el.scrollHeight*k;el.style.top=(fh<H?(H-fh)/2:0)+'px';}if(document.fonts&&document.fonts.ready){document.fonts.ready.then(fit);}fit();setTimeout(fit,300);})();</script></body></html>"""


def card(idx, n, code, right, inner, theme="v2"):
    ft = ""
    if BRAND or HANDLE:
        ft = ('<div class="ft"><div class="brand">' + escape(BRAND)
              + '</div><div class="handle">' + escape(HANDLE) + '</div></div>')
    return (head_for(theme) + '<div class="c"><div class="mesh"></div><div class="orb a"></div><div class="orb b"></div>'
            + '<div class="hud"><i></i><i></i><i></i><i></i></div>'
            + ('<div class="ghost">%02d</div>' % idx)
            + '<div class="sysbar"><div class="l"><span class="dot"></span>财经观察 / 公开数据速读</div><div class="r">' + right + '</div></div>'
            + '<div class="bd"><div class="fit">' + inner + '</div></div>'
            + '<div class="pn">' + code + ' · %02d/%d</div>' % (idx, n)
            + ft + '</div>' + FIT)


def escape_tree(v):
    """analysis.json 里的字符串会拼进 HTML 再被 Chrome 渲染，统一转义。"""
    if isinstance(v, str):
        return escape(v)
    if isinstance(v, list):
        return [escape_tree(x) for x in v]
    if isinstance(v, dict):
        return {k: escape_tree(x) for k, x in v.items()}
    return v


# ───────── SVG（黏土=主角 / 石板蓝=对照 / 砖红=流出·风险）─────────
def svg_coaster(p):
    pts = [(p["start_date"][5:], p["start_px"], p["start_mktcap_yi"]),
           (p["peak_date"][5:], p["peak_px"], p["peak_mktcap_yi"]),
           (p["last_date"][5:], p["last_px"], p["last_mktcap_yi"])]
    xs = [120, 400, 640]; base = 230; top = 60; mx = max(q[1] for q in pts)
    co = [(x, base - (q[1] / mx) * (base - top)) for q, x in zip(pts, xs)]
    s = ['<svg viewBox="0 0 720 300" role="img" aria-label="股价与市值轨迹">']
    s.append('<line x1="80" y1="%d" x2="700" y2="%d" stroke="rgba(20,20,19,.18)"/>' % (base, base))
    s.append('<path d="M %d %.1f L %d %.1f L %d %.1f" fill="none" stroke="#c15f3c" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>' % (co[0][0], co[0][1], co[1][0], co[1][1], co[2][0], co[2][1]))
    for (d, px, mv), (x, y) in zip(pts, co):
        s.append('<circle cx="%d" cy="%.1f" r="8" fill="#fff" stroke="#c15f3c" stroke-width="3"/>' % (x, y))
        s.append('<text x="%d" y="%.1f" text-anchor="middle" fill="#1a1a18" font-family="\'Anthropic Mono\',monospace" font-size="24" font-weight="700">%.2f</text>' % (x, y - 22, px))
        s.append('<text x="%d" y="%.1f" text-anchor="middle" fill="#8a877e" font-family="\'Anthropic Mono\',monospace" font-size="15">市值%d亿</text>' % (x, y - 46, mv))
        s.append('<text x="%d" y="%d" text-anchor="middle" fill="#56544e" font-family="\'Anthropic Mono\',monospace" font-size="17">%s</text>' % (x, base + 28, d))
    s.append('<text x="640" y="%.1f" text-anchor="middle" fill="#56544e" font-family="\'Noto Sans SC\',sans-serif" font-size="14" font-weight="700">较峰值 %s%%</text>' % (co[2][1] + 30, ("-%.0f" % p["drawdown_pct"]) if p["drawdown_pct"] > 0 else ("+%.0f" % -p["drawdown_pct"])))
    s.append('<text x="80" y="288" fill="#8a877e" font-family="\'Anthropic Mono\',monospace" font-size="13">股价（元）· 数据：akshare</text></svg>')
    return "".join(s)


def svg_flow(ff):
    rows = ff["key_days"]; S = 14.0; ZERO = 410; y0 = 64; step = 38; bh = 22
    mxv = max((abs(r["net_yi"]) for r in rows), default=1)
    if mxv * S > 240:
        S = 240.0 / mxv
    s = ['<svg viewBox="0 0 720 312" role="img" aria-label="主力资金净额关键交易日">']
    s.append('<text x="24" y="34" fill="#56544e" font-family="\'Noto Sans SC\',sans-serif" font-size="15" font-weight="700">主力资金净额（亿元）· 4月以来合计 %s 亿</text>' % ff["net_4mo_yi"])
    s.append('<line x1="%d" y1="50" x2="%d" y2="284" stroke="rgba(20,20,19,.18)"/>' % (ZERO, ZERO))
    for i, r in enumerate(rows[:6]):
        y = y0 + i * step; v = r["net_yi"]
        if v >= 0:
            w = v * S; x = ZERO; col = "#5c6b7a"; lab = "+%.2f" % v
        else:
            w = -v * S; x = ZERO - w; col = "#c0392b"; lab = "%.2f" % v
        s.append('<text x="24" y="%d" fill="#56544e" font-family="\'Anthropic Mono\',monospace" font-size="16">%s</text>' % (y + bh - 4, r["date"]))
        s.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="3" fill="%s"/>' % (x, y, w, bh, col))
        s.append('<text x="700" y="%d" text-anchor="end" fill="%s" font-family="\'Anthropic Mono\',monospace" font-size="18" font-weight="700">%s</text>' % (y + bh - 4, col, lab))
    s.append('<text x="24" y="306" fill="#8a877e" font-family="\'Anthropic Mono\',monospace" font-size="13">红=主力净流出　蓝=主力净流入　·　东方财富口径</text></svg>')
    return "".join(s)


def svg_quality(q):
    q = q[:2]; base = 248
    mx = max((max(x["net_yi"], x["cfo_yi"]) for x in q), default=1); S = 180.0 / mx if mx else 1
    cxs = [180, 470]; bw = 88
    s = ['<svg viewBox="0 0 720 312" role="img" aria-label="净利润与经营现金流对比">']
    s.append('<line x1="60" y1="%d" x2="700" y2="%d" stroke="rgba(20,20,19,.18)"/>' % (base, base))
    s.append('<text x="60" y="34" fill="#56544e" font-family="\'Noto Sans SC\',sans-serif" font-size="15" font-weight="700">归母净利 vs 经营现金流净额（亿元）</text>')
    for x, item in zip(cxs, q):
        hn = item["net_yi"] * S; hc = item["cfo_yi"] * S; xn = x - bw - 8; xc = x + 8
        s.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" rx="4" fill="#5c6b7a"/>' % (xn, base - hn, bw, hn))
        s.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" rx="4" fill="#c15f3c"/>' % (xc, base - hc, bw, hc))
        s.append('<text x="%d" y="%.1f" text-anchor="middle" fill="#4a5763" font-family="\'Anthropic Mono\',monospace" font-size="22" font-weight="700">%.2f</text>' % (xn + bw // 2, base - hn - 14, item["net_yi"]))
        s.append('<text x="%d" y="%.1f" text-anchor="middle" fill="#c15f3c" font-family="\'Anthropic Mono\',monospace" font-size="22" font-weight="700">%.2f</text>' % (xc + bw // 2, base - hc - 14, item["cfo_yi"]))
        s.append('<text x="%d" y="%d" text-anchor="middle" fill="#56544e" font-family="\'Noto Sans SC\',sans-serif" font-size="17" font-weight="700">%s</text>' % (x, base + 30, item["period"]))
    s.append('<rect x="60" y="284" width="15" height="15" rx="2" fill="#5c6b7a"/><text x="82" y="296" fill="#4a5763" font-family="\'Noto Sans SC\',sans-serif" font-size="15" font-weight="700">归母净利</text>')
    s.append('<rect x="240" y="284" width="15" height="15" rx="2" fill="#c15f3c"/><text x="262" y="296" fill="#c15f3c" font-family="\'Noto Sans SC\',sans-serif" font-size="15" font-weight="700">经营现金流</text></svg>')
    return "".join(s)


def svg_struct(st):
    segs = sorted(st["segments"], key=lambda x: -(x.get("rev_pct") or 0))
    X = 60; W = 600; pal = ["#5c6b7a", "#c15f3c", "#b3afa6", "#a07a3c"]
    s = ['<svg viewBox="0 0 720 268" role="img" aria-label="营收结构与毛利结构">']

    def bar(y, label, key):
        out = ['<text x="%d" y="%d" fill="#56544e" font-family="\'Noto Sans SC\',sans-serif" font-size="16" font-weight="700">%s</text>' % (X, y - 12, label)]
        x = X
        order = sorted(segs, key=lambda s2: -(s2.get(key) or 0))
        for i, seg in enumerate(order):
            pct = (seg.get(key) or 0) / 100.0
            w = W * pct; out.append('<rect x="%.1f" y="%d" width="%.1f" height="56" fill="%s"/>' % (x, y, w, pal[i % 4]))
            if w > 92:
                out.append('<text x="%.1f" y="%d" text-anchor="middle" fill="#fff" font-family="\'Anthropic Mono\',monospace" font-size="18" font-weight="800">%s %d%%</text>' % (x + w / 2, y + 35, seg["name"][:4], round(pct * 100)))
            x += w
        out.append('<rect x="%d" y="%d" width="%d" height="56" fill="none" stroke="rgba(20,20,19,.14)"/>' % (X, y, W))
        return "".join(out)
    s.append(bar(48, "营收结构 %s" % st["period"], "rev_pct"))
    s.append(bar(160, "毛利结构 %s" % st["period"], "gross_share_pct"))
    s.append('</svg>')
    return "".join(s)


def main(outdir, name=None, theme="v2"):
    with open(os.path.join(outdir, "analysis.json"), encoding="utf-8") as f:
        A = escape_tree(json.load(f))
    code = A.get("code", "")
    nm = escape(name) if name else code
    p = A.get("price"); ff = A.get("fundflow"); q = A.get("profit_quality"); st = A.get("structure")
    lhb = A.get("lhb"); bal = A.get("balance")
    DISC = '<div class="disc"><b>风险提示：</b>本文为基于公开数据的事后复盘与行业科普，不构成任何投资建议，不预测股价涨跌。市场有风险，决策需独立判断。数据来源：akshare、公司年报季报。</div>'
    cards = []

    # 01 封面（取三个反差数）
    g = []
    if ff: g.append(("主力·4月以来", "%s亿" % ff["net_4mo_yi"], "资金净额合计"))
    if p: g.append(("峰值 PE(TTM)", "%s倍" % p["peak_pe"], "现约 %s 倍" % p["last_pe"]))
    if st:
        top = max(st["segments"], key=lambda x: (x.get("gross_margin_pct") or 0))
        g.append(("%s毛利率" % top["name"][:4], "%.1f%%" % (top["gross_margin_pct"] or 0), "分部最高"))
    gh = "".join('<div class="gauge"><div class="gl">%s</div><div class="gv">%s</div><div class="gu">%s</div></div>' % x for x in g[:3])
    cards.append(("封面",
        '<div class="eyebrow"><span></span>%s %s · 公开数据速读</div>'
        '<h1>用数据，<br>看清<span class="hl">一只票</span></h1>'
        '<p class="lead">不预测后市，只把<b>资金怎么流的、公司什么成色</b>用公开数据摆清楚。</p>'
        '<div class="readout">%s</div>' % (nm, code, gh)))

    # 02 价格轨迹
    if p:
        cards.append(("价格轨迹",
            '<div class="kicker">一图看懂这一程</div><div class="title">价格与<span class="u">市值轨迹</span></div>'
            '<div class="fig"><div class="fh"><span class="id">FIG.01</span><span>股价 / 市值</span></div>' + svg_coaster(p) +
            '<div class="cap">年初 %.2f → 峰值 %.2f → 现 %.2f</div></div>'
            '<p class="note">市值 <b>%d 亿 → 峰值 %d 亿 → 现 %d 亿</b>，较峰值回撤约 <b>%s%%</b>。</p>'
            % (p["start_px"], p["peak_px"], p["last_px"], p["start_mktcap_yi"], p["peak_mktcap_yi"], p["last_mktcap_yi"], p["drawdown_pct"])))

    # 03 资金面
    if ff:
        cards.append(("资金面",
            '<div class="kicker">谁在进、谁在出</div><div class="title">主力资金<span class="u">进出</span></div>'
            '<div class="fig"><div class="fh"><span class="id">FIG.02</span><span>主力资金净额 · 关键交易日</span></div>' + svg_flow(ff) +
            '<div class="cap">4 月以来主力净额合计 <b>%s 亿</b></div></div>'
            '<p class="note">数据来自东方财富主力资金口径（大单+超大单）。<b>留意上涨日仍净流出的"拉高派发"信号。</b></p>' % ff["net_4mo_yi"]))

    # 04 龙虎榜
    if lhb:
        inst = "有机构专用席位" if lhb["n_institution_rows"] > 0 else "几乎无机构专用席位"
        cards.append(("龙虎榜",
            '<div class="kicker">这是一轮什么资金</div><div class="title">龙虎榜<span class="u">席位结构</span></div>'
            '<div class="rows">'
            '<div class="row"><div class="ri">🏛</div><div><div class="rn">上榜 %d 行</div><div class="rd">其中沪深股通通道 <b>%d</b> 行，机构专用 <b>%d</b> 行。</div></div></div>'
            '<div class="row"><div class="ri">🔍</div><div><div class="rn">%s</div><div class="rd">机构专用席位少 → 偏<b>资金博弈盘</b>；多 → 有长线资金参与。请按实际席位名单判断。</div></div></div>'
            '</div>' % (lhb["rows"], lhb["n_northbound_rows"], lhb["n_institution_rows"], inst)))

    # 05 利润质量
    if q:
        cards.append(("利润质量",
            '<div class="kicker">利润是不是真的</div><div class="title">净利 vs <span class="u">经营现金流</span></div>'
            '<div class="fig"><div class="fh"><span class="id">FIG.03</span><span>净利 vs 经营现金流</span></div>' + svg_quality(q) +
            '<div class="cap">现金流高于净利 = 利润含金量高</div></div>'
            '<p class="note">经营现金流持续高于净利，说明利润是<b>真收到现金</b>的；反之则需警惕应收/存货等"纸面利润"。</p>'))

    # 06 利润结构
    if st:
        hi = max(st["segments"], key=lambda x: (x.get("gross_share_pct") or 0))
        cards.append(("利润结构",
            '<div class="kicker">钱主要从哪来</div><div class="title">收入与<span class="u">毛利结构</span></div>'
            '<div class="fig"><div class="fh"><span class="id">FIG.04</span><span>营收结构 vs 毛利结构</span></div>' + svg_struct(st) +
            '<div class="cap">看哪块业务"用小收入扛大毛利"</div></div>'
            '<p class="note"><b>%s</b> 贡献约 <span class="h">%s%%</span> 毛利（毛利率 %s%%），是利润的主引擎。</p>'
            % (hi["name"][:6], hi.get("gross_share_pct"), hi.get("gross_margin_pct"))))

    # 07 风险线索
    risk_rows = ['<div class="row"><div class="ri">📈</div><div><div class="rn">估值水位</div><div class="rd">PE(TTM) 峰值 <span class="w">%s 倍</span>，现约 %s 倍；PB 现约 %s。</div></div></div>' % (p["peak_pe"], p["last_pe"], p["last_pb"]) if p else ""]
    if bal and bal.get("debt_ratio_pct"):
        risk_rows.append('<div class="row"><div class="ri">🧱</div><div><div class="rn">资产负债率 %s%%</div><div class="rd">货币资金约 %s 亿、合同负债约 %s 亿（预收）。</div></div></div>' % (bal["debt_ratio_pct"], bal.get("cash", "—"), bal.get("contract_liab", "—")))
    risk_rows.append('<div class="row"><div class="ri">📝</div><div><div class="rn">公司自述风险 / 股东动作</div><div class="rd">补：客户集中度、产能/订单、减持等（查公告，逐条客观罗列，不下结论）。</div></div></div>')
    cards.append(("风险线索",
        '<div class="kicker">客观罗列，不下结论</div><div class="title">需要盯的<span class="u">风险线索</span></div>'
        '<div class="rows">' + "".join(risk_rows) + '</div>'))

    # 08 结语 + 风险提示
    cards.append(("结语",
        '<div class="pull"><p>用<em>数据</em>看清一只票，<br>而不是只看涨跌。</p><div class="by">%s · 公开数据速读</div></div>' % nm + DISC))

    n = len(cards)
    SLUG = {"封面": "cover", "价格轨迹": "price", "资金面": "fundflow", "龙虎榜": "lhb",
            "利润质量": "quality", "利润结构": "structure", "风险线索": "risk", "结语": "closing"}
    for i, (right, inner) in enumerate(cards, 1):
        fn = "%02d-%s.html" % (i, SLUG.get(right, "card"))
        with open(os.path.join(outdir, fn), "w", encoding="utf-8") as fobj:
            fobj.write(card(i, n, code, right, inner, theme))
        print("✓", fn, "(%s)" % theme)
    print("done:", n, "cards →", outdir, "（数字已对；中立文案请按 report-structure.md 润色后截图）")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="个股报告贴图初稿")
    ap.add_argument("outdir", help="analyze.py 输出目录")
    ap.add_argument("name", nargs="?", default=None, help="公司简称")
    ap.add_argument("--theme", choices=("v2", "v3"), default=os.environ.get("STOCK_REPORT_THEME", "v2"),
                    help="v2=米白(默认) v3=Readdy财经白")
    ap.add_argument("--brand", default=None, help="页脚署名（默认取 STOCK_REPORT_BRAND）")
    ap.add_argument("--handle", default=None, help="页脚账号（默认取 STOCK_REPORT_HANDLE）")
    args = ap.parse_args()
    if args.brand is not None:
        BRAND = args.brand
    if args.handle is not None:
        HANDLE = args.handle
    main(args.outdir, args.name, args.theme)
