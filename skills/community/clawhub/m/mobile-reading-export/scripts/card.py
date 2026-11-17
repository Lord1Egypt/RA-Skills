# -*- coding: utf-8 -*-
"""生成速览卡（PNG 用）HTML。一页五块：四柱 / 格局 / 强弱 / 调候 / 大运主线。"""
import json
import os
import sys

CSS = """
*,*::before,*::after{box-sizing:border-box}
html,body{margin:0;padding:0;background:#ffffff}
body{width:393px;color:#16161a;
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  -webkit-font-smoothing:antialiased}
.card{padding:26px 22px 20px}
.kicker{font-size:12.5px;color:#96969e;letter-spacing:1.2px;margin:0 0 6px}
h1{font-size:25px;font-weight:600;margin:0 0 8px;letter-spacing:-.3px}
.sub{font-size:13px;color:#6a6a72;line-height:1.6;margin:0}
.rule{height:1px;background:#e3e3e6;margin:20px 0}
.pillars{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0 0 20px}
.p{border:1px solid #e3e3e6;border-radius:11px;padding:11px 0 12px;text-align:center;background:#f6f6f7}
.p .n{font-size:11.5px;color:#96969e;display:block;margin:0 0 5px}
.p .g{font-size:22px;font-weight:600;color:#1a6b58;letter-spacing:1.5px}
.p.cur{border-color:#bfe0d6;background:#eaf5f1}
.p.cur .g{color:#13503f}
.blk{margin:0 0 15px}
.blk .lb{font-size:12px;color:#96969e;letter-spacing:.6px;margin:0 0 5px}
.blk .vl{font-size:16.5px;font-weight:600;line-height:1.5;margin:0}
.blk .vl .lite{font-weight:400;color:#6a6a72;font-size:14.5px}
.blk .note{font-size:13.5px;color:#6a6a72;line-height:1.6;margin:4px 0 0}
.chips{display:flex;gap:7px;flex-wrap:wrap;margin:6px 0 0}
.chip{font-size:12.5px;font-weight:600;padding:3px 10px;border-radius:999px;border:1px solid}
.c-ok{background:#eaf5ee;color:#1d6b3f;border-color:#c3e2cf}
.c-no{background:#fdeceb;color:#a1322d;border-color:#f2c9c6}
.c-warn{background:#fdf3e3;color:#8a5a08;border-color:#f0d9ae}
.c-gray{background:#f0f0f2;color:#63636b;border-color:#dcdce0}
.yun{border-top:1px solid #e3e3e6;padding-top:14px;margin-top:20px}
.yrow{display:flex;gap:11px;padding:7px 0;border-bottom:1px solid #f0f0f2;font-size:14px;align-items:baseline}
.yrow:last-child{border-bottom:0}
.yg{flex:0 0 46px;font-weight:600;color:#1a6b58;letter-spacing:.5px}
.ya{flex:0 0 62px;color:#96969e;font-size:12.5px}
.yt{flex:1;color:#33333a;line-height:1.5}
.yrow.on .yg{color:#13503f}
.yrow.on .yt{font-weight:600}
.foot{margin-top:18px;font-size:11.5px;color:#96969e;text-align:center;letter-spacing:.5px}
"""


def render(d):
    ps = []
    for i, (n, g) in enumerate(zip(['年柱', '月柱', '日柱', '时柱'], d['pillars'])):
        cls = 'p cur' if i == d.get('cur_idx', 2) else 'p'
        ps.append(f'<div class="{cls}"><span class="n">{n}</span>'
                  f'<span class="g">{g}</span></div>')
    yun = []
    for y in d['yun']:
        cls = 'yrow on' if y.get('on') else 'yrow'
        yun.append(f'<div class="{cls}"><span class="yg">{y["g"]}</span>'
                   f'<span class="ya">{y["a"]}</span>'
                   f'<span class="yt">{y["t"]}</span></div>')
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="card">
<p class="kicker">{d['kicker']}</p>
<h1>{d['title']}</h1>
<p class="sub">{d['sub']}</p>
<div class="rule"></div>
<div class="pillars">{''.join(ps)}</div>
<div class="blk"><p class="lb">格局</p>
  <p class="vl">{d['geju']}</p>
  <div class="chips">{''.join(f'<span class="chip {c}">{t}</span>' for t, c in d['geju_chips'])}</div></div>
<div class="blk"><p class="lb">日主强弱</p>
  <p class="vl">{d['qiangruo']} <span class="lite">{d['qiangruo_x']}</span></p></div>
<div class="blk"><p class="lb">调候用神</p>
  <p class="vl">{d['tiaohou']} <span class="lite">{d['tiaohou_x']}</span></p>
  <div class="chips">{''.join(f'<span class="chip {c}">{t}</span>' for t, c in d.get('tiaohou_chips', []))}</div></div>
<div class="blk"><p class="lb">喜用 / 忌讳</p>
  <p class="vl">{d['xiyong']} <span class="lite">{d['jihui']}</span></p></div>
<div class="yun">{''.join(yun)}</div>
<p class="foot">{d['foot']}</p>
</div></body></html>
"""


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f:
        data = json.load(f)
    for key, d in data.items():
        out = sys.argv[2].replace('*', key)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(render(d))
        print('WROTE', out, os.path.getsize(out))
