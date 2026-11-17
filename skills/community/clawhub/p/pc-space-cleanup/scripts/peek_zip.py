"""List top-level entries of zip files (reads only the central directory). Usage: python -I peek_zip.py <zip> [...]"""
import sys, zipfile

for p in sys.argv[1:]:
    try:
        with zipfile.ZipFile(p) as z:
            names = z.namelist()
            tops = []
            for n in names:
                t = n.split('/')[0] + ('/' if '/' in n.strip('/') or n.endswith('/') else '')
                if t not in tops:
                    tops.append(t)
            print(f"[{p.split(chr(92))[-1]}] {len(names)} 条，顶层: {' | '.join(tops[:10])}")
    except Exception as e:
        print(f"[{p.split(chr(92))[-1]}] 读取失败: {e}")
