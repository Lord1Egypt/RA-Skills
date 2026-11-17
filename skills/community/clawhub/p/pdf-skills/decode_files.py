# -*- coding: utf-8 -*-
import os, re, sys

d = r'C:\Users\Administrator\.openclaw\workspace\ioc-kms-dataset\yanghu'
files = [x for x in os.listdir(d) if x[:2].isdigit() and x.endswith('.md')]
print('Found %d files' % len(files), file=sys.stderr)
for f in sorted(files):
    fp = os.path.join(d, f)
    with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
        content = fh.read(500)
    m = re.search(r'title:\s*"([^"]+)"', content)
    title = m.group(1) if m else '(no title)'
    m2 = re.search(r'pages_total:\s*(\d+)', content)
    pages = m2.group(1) if m2 else '?'
    m3 = re.search(r'total_chars:\s*(\d+)', content)
    chars = m3.group(1) if m3 else '?'
    print('[%s] %s | P=%s C=%s' % (f[:2], title[:50], pages, chars))
