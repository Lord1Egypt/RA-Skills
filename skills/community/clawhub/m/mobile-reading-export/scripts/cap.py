# -*- coding: utf-8 -*-
"""手机视口截图与排版诊断。

背景：Windows 上 Chrome 的 --window-size 存在最小宽度（约 552 CSS px），
--force-device-scale-factor 又不会缩小 CSS 视口，因此无法直接用窗口参数
得到 393px 的手机视口。这里的做法是：把正文列在页面里锁死为 393px，
用足够大的窗口渲染，再把截图裁到该列。

输出：
  <prefix>.png        首屏（393 x 850 CSS px 区域）
  <prefix>_full.png   整页
并打印实测的 scrollWidth / scrollHeight / 溢出元素清单。
"""
import os
import re
import subprocess
import sys
from PIL import Image

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
CSS_W = 393
WIN_H = 900

FORCE_STYLE = """
<style id="__cap_force">
  html{background:#ffffff !important;color-scheme:light}
  body{width:393px !important;margin:0 !important;padding:0 !important;background:#ffffff !important}
</style>
"""

PROBE = """
<script>
window.addEventListener('load', function () {
  var de = document.documentElement;
  var vw = de.clientWidth;
  var out = ['SW=' + de.scrollWidth, 'CW=' + vw,
             'BH=' + document.body.scrollHeight,
             'DH=' + de.scrollHeight,
             'BW=' + Math.round(document.body.getBoundingClientRect().width)];
  var all = document.querySelectorAll('*');
  var bad = [];
  for (var i = 0; i < all.length; i++) {
    var el = all[i], r = el.getBoundingClientRect();
    if (r.width > vw + 1 || r.right > vw + 1) {
      var id = el.tagName.toLowerCase();
      if (el.className && typeof el.className === 'string') {
        id += '.' + el.className.trim().split(/\\s+/).join('.');
      }
      bad.push(id + '|w=' + Math.round(r.width) + '|r=' + Math.round(r.right)
               + '|txt=' + (el.textContent || '').trim().slice(0, 22));
    }
  }
  out.push('BAD=' + bad.length);
  var secs = document.querySelectorAll('h2, h3');
  var map = [];
  for (var j = 0; j < secs.length; j++) {
    var t = secs[j];
    map.push(Math.round(t.getBoundingClientRect().top + window.scrollY)
             + '@' + t.tagName.toLowerCase() + '@' + (t.textContent || '').trim().slice(0, 14));
  }
  out.push('SEC=' + map.join(' ~ '));
  document.title = out.concat(bad.slice(0, 18)).join(' ;; ');
});
</script>
"""


def chrome(args):
    r = subprocess.run([CHROME] + args, capture_output=True)
    return r.stdout.decode('utf-8', 'replace'), r.stderr.decode('utf-8', 'replace'), r.returncode


def url_of(p):
    return 'file:///' + os.path.abspath(p).replace('\\', '/')


def build_variant(src, dst, extra_head='', extra_body=''):
    with open(src, encoding='utf-8') as f:
        h = f.read()
    if extra_head:
        h = h.replace('</head>', extra_head + '</head>')
    if extra_body:
        h = h.replace('</body>', extra_body + '</body>')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(h)


def png_size(p):
    b = open(p, 'rb').read(33)
    w = b[16] * 16777216 + b[17] * 65536 + b[18] * 256 + b[19]
    h = b[20] * 16777216 + b[21] * 65536 + b[22] * 256 + b[23]
    return w, h


def capture(src, prefix, scale=2, find_h=9000):
    tmp_dir = os.path.dirname(os.path.abspath(prefix))
    base = os.path.basename(prefix)

    # 1) 诊断：拿到整页高度与溢出清单
    probe_path = os.path.join(tmp_dir, f'_m_{base}.html')
    build_variant(src, probe_path, extra_head=FORCE_STYLE, extra_body=PROBE)
    out, err, rc = chrome(['--headless=new', '--disable-gpu', '--no-sandbox',
                           '--hide-scrollbars', '--virtual-time-budget=4000',
                           f'--window-size={CSS_W + 307},{find_h}',
                           '--dump-dom', url_of(probe_path)])
    m = re.search(r'<title>(.*?)</title>', out, re.S)
    info = m.group(1) if m else '(no title)'
    meta = {}
    secs = []
    for kv in info.split(' ;; '):
        if kv.startswith('SEC='):
            for it in kv[4:].split(' ~ '):
                parts = it.split('@')
                if len(parts) == 3:
                    secs.append((int(parts[0]), parts[1], parts[2]))
            continue
        if '=' in kv and '|' not in kv:
            k, v = kv.split('=', 1)
            meta[k] = v
    bad = [x for x in info.split(' ;; ') if '|' in x]
    full_h = max(int(meta.get('BH', WIN_H) or WIN_H), int(meta.get('DH', WIN_H) or WIN_H))

    # 2) 渲染：锁宽渲染整页
    render_path = os.path.join(tmp_dir, f'_r_{base}.html')
    build_variant(src, render_path, extra_head=FORCE_STYLE)
    raw = os.path.join(tmp_dir, f'_raw_{base}.png')
    if os.path.exists(raw):
        os.remove(raw)
    win_h = max(full_h + 240, WIN_H)
    chrome(['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
            '--virtual-time-budget=4000', f'--force-device-scale-factor={scale}',
            f'--window-size={CSS_W + 307},{win_h}',
            f'--screenshot={raw}', url_of(render_path)])
    if not os.path.exists(raw):
        return None

    # 3) 裁到正文列；底边按像素内容判定，避免高度测量偏差造成截断
    im = Image.open(raw).convert('RGB')
    cw = min(CSS_W * scale, im.size[0])
    px = im.load()
    bottom = 0
    for y in range(im.size[1] - 1, -1, -1):
        hit = False
        for x in range(0, cw, 3):
            r, g, b = px[x, y]
            if r < 250 or g < 250 or b < 250:
                hit = True
                break
        if hit:
            bottom = y + 1
            break
    if bottom == 0:
        bottom = min(full_h * scale, im.size[1])
    bottom = min(bottom + 26 * scale, im.size[1])
    body = im.crop((0, 0, cw, bottom))
    full_out = prefix + '_full.png'
    body.save(full_out, optimize=True)
    first = body.crop((0, 0, cw, min(850 * scale, body.size[1])))
    first_out = prefix + '.png'
    first.save(first_out, optimize=True)

    for p in (probe_path, render_path, raw):
        try:
            os.remove(p)
        except OSError:
            pass

    return {'meta': meta, 'bad': bad, 'full': png_size(full_out),
            'first': png_size(first_out), 'full_h_css': full_h, 'secs': secs}


if __name__ == '__main__':
    src = sys.argv[1]
    prefix = sys.argv[2]
    scale = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    r = capture(src, prefix, scale)
    if not r:
        print('FAILED')
        sys.exit(1)
    print('source   :', src)
    print('viewport : CW=%s  SW=%s  BW=%s' % (r['meta'].get('CW'), r['meta'].get('SW'),
                                              r['meta'].get('BW')))
    print('page     : %s css px  ->  %sx%s px @%dx' % (r['full_h_css'], r['full'][0],
                                                       r['full'][1], scale))
    print('first    : %sx%s' % r['first'])
    print('overflow : BAD=%s' % r['meta'].get('BAD'))
    for b in r['bad']:
        print('   ', b)
    print('sections (css px):')
    for y, tag, txt in r['secs']:
        print('   %6d  %-3s %s' % (y, tag, txt))
