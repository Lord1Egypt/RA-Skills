# -*- coding: utf-8 -*-
"""把 HTML 打成 PDF（手机比例），并回读每页 MediaBox 做核验。

页面尺寸由 HTML 内的 @page 规则决定；这里只负责调用与校验，
不传 --window-size（打印布局由 @page 决定，与窗口无关）。
"""
import os
import re
import subprocess
import sys

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'


def to_pdf(src, out):
    import tempfile
    if os.path.abspath(out) == os.path.abspath(src):
        return None, 'refusing to overwrite the source file'
    if os.path.exists(out) and '--overwrite' not in sys.argv:
        return None, ('output already exists: %s — pass --overwrite after confirming the '
                      'replacement; the original is kept until a valid PDF is verified' % out)
    fd, staged = tempfile.mkstemp(suffix='.pdf', prefix='.', dir=os.path.dirname(os.path.abspath(out)))
    os.close(fd)
    url = 'file:///' + os.path.abspath(src).replace('\\', '/')
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
                        '--no-pdf-header-footer', '--virtual-time-budget=6000',
                        f'--print-to-pdf={staged}', url],
                       capture_output=True)
    if not os.path.exists(staged) or os.path.getsize(staged) == 0:
        return None, r.stderr.decode('utf-8', 'replace')
    raw = open(staged, 'rb').read()
    boxes = re.findall(rb'/MediaBox\s*\[([^\]]*)\]', raw)
    pages = len(re.findall(rb'/Type\s*/Page[^s]', raw))
    dims = []
    for b in boxes:
        v = [float(x) for x in b.split()]
        dims.append((round(v[2], 1), round(v[3], 1)))
    uniq = sorted(set(dims))
    os.replace(staged, out)
    return {'bytes': len(raw), 'pages': pages, 'media': uniq}, ''


if __name__ == '__main__':
    src = sys.argv[1]
    out = sys.argv[2]
    info, err = to_pdf(src, out)
    if not info:
        print('FAILED', err[:500])
        sys.exit(1)
    pt2mm = 25.4 / 72.0
    print('source :', src)
    print('output :', out)
    print('bytes  :', info['bytes'], ' pages:', info['pages'])
    for w, h in info['media']:
        print('  MediaBox %s x %s pt  =  %.1f x %.1f mm' % (w, h, w * pt2mm, h * pt2mm))
