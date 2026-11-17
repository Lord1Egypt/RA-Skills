#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 字节级完全相同检测（Tier A）：头尾2MB MD5 指纹 + 指纹相同组全量 MD5 校验
# 用法: python exact_dup.py <root_folder> [out_csv] [out_json]
# 只读，不修改文件。可断点续传（指纹缓存 _fp_cache.json）。
import os, sys, csv, hashlib, json

EXTS = {'.jpg','.jpeg','.heic','.png','.livp','.mp4','.mov','.avi','.mkv','.m4v'}
HEAD = 2 * 1024 * 1024
TAIL = 2 * 1024 * 1024

def collect(root):
    out = []
    for dp, _, fns in os.walk(root):
        for n in fns:
            if n != '.DS_Store' and os.path.splitext(n)[1].lower() in EXTS:
                out.append(os.path.join(dp, n))
    return out

def fp_of(path):
    size = os.path.getsize(path)
    h = hashlib.md5(); t = hashlib.md5()
    with open(path, 'rb') as f:
        h.update(f.read(HEAD))
        if size > HEAD + TAIL:
            f.seek(-TAIL, os.SEEK_END)
            t.update(f.read())
        else:
            t.update(f.read())
    return size, h.hexdigest(), t.hexdigest()

def full_md5(path):
    m = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4*1024*1024), b''):
            m.update(chunk)
    return m.hexdigest()

def main():
    root = sys.argv[1]
    base = os.path.join(os.getcwd(), '_exact')
    report = sys.argv[2] if len(sys.argv) > 2 else base + '_report.csv'
    outj = sys.argv[3] if len(sys.argv) > 3 else base + '_groups.json'
    fpc = base + '_fpcache.json'
    files = collect(root)
    print(f"文件数: {len(files)}", flush=True)
    fp = {}
    if os.path.exists(fpc):
        try: fp = json.load(open(fpc, encoding='utf-8'))
        except Exception: fp = {}
    for i, p in enumerate(files, 1):
        if p in fp and fp[p].get('mt') == os.path.getmtime(p):
            continue
        try:
            size, h, t = fp_of(p)
            fp[p] = {'size': size, 'h': h, 't': t, 'mt': os.path.getmtime(p)}
        except OSError as e:
            print(f"  跳过: {p} {e}", flush=True)
        if i % 200 == 0:
            json.dump(fp, open(fpc, 'w', encoding='utf-8'), ensure_ascii=False)
            print(f"  指纹 {i}/{len(files)}", flush=True)
    json.dump(fp, open(fpc, 'w', encoding='utf-8'), ensure_ascii=False)
    by_fp = {}
    for p, v in fp.items():
        by_fp.setdefault((v['size'], v['h'], v['t']), []).append(p)
    cand = {k: v for k, v in by_fp.items() if len(v) > 1}
    print(f"指纹相同候选组: {len(cand)}", flush=True)
    groups = []
    for k, members in cand.items():
        verified = []
        for p in members:
            try: verified.append((p, full_md5(p)))
            except OSError: pass
        by_md5 = {}
        for p, md5 in verified:
            by_md5.setdefault(md5, []).append(p)
        for md5, grp in by_md5.items():
            if len(grp) < 2: continue
            grp_sorted = sorted(grp)
            # 留优: 优先非微信命名, 否则路径排序第一个
            keep = next((x for x in grp_sorted if 'weixin' not in os.path.basename(x).lower()), grp_sorted[0])
            groups.append({'size': k[0], 'md5': md5, 'keep': keep, 'move': [x for x in grp if x != keep]})
    with open(report, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(['MD5','大小MB','保留','候选移除数','候选移除文件'])
        for g in groups:
            w.writerow([g['md5'], round(g['size']/1024/1024,1), g['keep'], len(g['move']), ' | '.join(g['move'])])
    json.dump(groups, open(outj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"完全相同组: {len(groups)}, 候选移除: {sum(len(g['move']) for g in groups)} → {report}")

if __name__ == '__main__':
    main()
