# -*- coding: utf-8 -*-
"""批量PDF处理脚本 v2 - 从index.md自动读取CDN URL"""
import sys, os, subprocess, re

def read_index_urls(index_path):
    if not os.path.exists(index_path):
        return []
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    urls = re.findall(r'https://linlan\.net/cdn/zhishi/yanghu/[^)\s]+\.pdf', content)
    result = []
    for url in urls:
        if url not in result:
            result.append(url)
    return result

def url_to_seq(url):
    m = re.match(r'.*/(\d+)_', url)
    return m.group(1).zfill(2) if m else "00"

def url_to_sid(url):
    fname = url.split('/')[-1]
    for pat in [
        r'DG-?TJ\d+-\d+-\d+',
        r'DG-?TJ\d+-\d+',
        r'CJJ[ -]?\d+[ -]\d+',
        r'CJJ[ -]?\d+',
        r'GB/?T?\d+[-\d]*',
        r'SHA\d+[-\d]*',
        r'DB31/?T?\d+[-\d]*',
        r'GA/?T?\d+[-\d]*',
    ]:
        m = re.search(pat, fname, re.I)
        if m:
            sid = re.sub(r'\s+', '', m.group(0))
            sid = re.sub(r'DG/?TJ', 'DG-TJ', sid, flags=re.I)
            return sid.upper()
    m2 = re.match(r'.*/(\d+)_', url)
    return m2.group(1).zfill(2) if m2 else "Unknown"

def download_and_convert(url, output_dir, script_dir):
    seq = url_to_seq(url)
    sid = url_to_sid(url)
    out = os.path.join(output_dir, "%s_%s.md" % (seq, sid))
    if os.path.exists(out) and os.path.getsize(out) > 1024:
        sz = os.path.getsize(out) // 1024
        print("  [SKIP] %s_%s.md (%dKB)" % (seq, sid, sz))
        return "skip", out
    script = os.path.join(script_dir, "pdf2md.py")
    if not os.path.exists(script):
        print("  [ERROR] pdf2md.py not found")
        return "error", None
    cmd = [sys.executable, script, url, out]
    fname = url.split('/')[-1]
    print("  Converting: %s ..." % fname[:50])
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=180)
        if r.returncode == 0:
            sz = os.path.getsize(out) // 1024 if os.path.exists(out) else 0
            print("  [OK] %s_%s.md (%dKB)" % (seq, sid, sz))
            return "ok", out
        else:
            err = r.stderr.decode('utf-8', errors='replace')
            print("  [FAIL] %s" % err[:100])
            return "fail", None
    except subprocess.TimeoutExpired:
        print("  [TIMEOUT]")
        return "timeout", None
    except Exception as e:
        print("  [ERROR] %s" % str(e))
        return "error", None

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Batch PDF processing')
    parser.add_argument('-i', '--index', default=None)
    parser.add_argument('-o', '--output', default='output')
    parser.add_argument('-s', '--start', type=int, default=1)
    parser.add_argument('-e', '--end', type=int, default=9999)
    parser.add_argument('-l', '--list', action='store_true')
    args = parser.parse_args()

    candidates = [args.index, '../yanghu/00_index.md',
                 '../../ioc-kms-dataset/yanghu/00_index.md', 'yanghu/00_index.md']
    index_path = None
    for c in candidates:
        if c and os.path.exists(c):
            index_path = os.path.abspath(c)
            break
    if not index_path:
        print("Error: index.md not found.")
        sys.exit(1)

    print("Index: %s" % index_path)
    urls = read_index_urls(index_path)
    print("Found %d CDN URLs\n" % len(urls))

    if args.list:
        for i, url in enumerate(urls, 1):
            fname = url.split('/')[-1]
            seq = url_to_seq(url)
            sid = url_to_sid(url)
            print("  %2d. [%s] %s" % (i, seq, fname[:50]))
        return

    output_dir = os.path.abspath(args.output)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    print("Output: %s" % output_dir)
    print("Items %d-%d of %d\n" % (args.start, args.end, len(urls)))

    stats = {}
    for i, url in enumerate(urls, 1):
        if not (args.start <= i <= args.end):
            continue
        status, path = download_and_convert(url, output_dir, script_dir)
        stats[status] = stats.get(status, 0) + 1

    ok = stats.get("ok", 0)
    skip = stats.get("skip", 0)
    fail = stats.get("fail", 0)
    print("\nSummary: OK=%d Skip=%d Fail=%d" % (ok, skip, fail))
    print("Output: %s" % os.path.abspath(output_dir))

if __name__ == '__main__':
    main()
