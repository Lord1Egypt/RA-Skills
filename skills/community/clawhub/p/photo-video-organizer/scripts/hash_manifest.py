#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 哈希校验清单：对文件夹下所有媒体算 MD5+SHA1 → CSV（断点续传，边算边落盘）
# 用法: python hash_manifest.py <root_folder> [out_csv]
# 列: relative_path,filename,ext,size_bytes,md5,sha1,mtime_iso
import os, sys, csv, json, hashlib, datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

EXTS = {'.jpg','.jpeg','.heic','.png','.livp','.mp4','.mov','.avi','.mkv','.m4v'}

def collect(root):
    out = []
    for dp, _, fns in os.walk(root):
        for n in fns:
            if n != '.DS_Store' and os.path.splitext(n)[1].lower() in EXTS:
                out.append(os.path.join(dp, n))
    return out

def hashes(p):
    m = hashlib.md5(); s = hashlib.sha1()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(4*1024*1024), b''):
            m.update(chunk); s.update(chunk)
    return m.hexdigest(), s.hexdigest()

def main():
    root = sys.argv[1]
    out_csv = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.getcwd(), '哈希校验清单.csv')
    cache = out_csv + '.cache.json'
    done = {}
    if os.path.exists(cache):
        try: done = json.load(open(cache, encoding='utf-8'))
        except Exception: done = {}
    files = collect(root)
    # 写表头(若新文件)
    if not os.path.exists(out_csv):
        with open(out_csv, 'w', encoding='utf-8-sig', newline='') as f:
            csv.writer(f).writerow(['relative_path','filename','ext','size_bytes','md5','sha1','mtime_iso'])
    todo = [p for p in files if p not in done]
    print(f"总 {len(files)}, 已算 {len(done)}, 待算 {len(todo)}", flush=True)
    with open(out_csv, 'a', encoding='utf-8-sig', newline='') as fout:
        w = csv.writer(fout)
        with ProcessPoolExecutor(max_workers=8) as ex:
            futs = {ex.submit(hashes, p): p for p in todo}
            n = 0
            for fut in as_completed(futs):
                p = futs[fut]
                try:
                    md5, sha1 = fut.result()
                except Exception as e:
                    print(f"  失败: {p} {e}", flush=True); continue
                st = os.stat(p)
                rel = os.path.relpath(p, root)
                w.writerow([rel, os.path.basename(p), os.path.splitext(p)[1], st.st_size, md5, sha1,
                            datetime.datetime.fromtimestamp(st.st_mtime).isoformat()])
                done[p] = md5
                n += 1
                if n % 50 == 0:
                    fout.flush()
                    json.dump(done, open(cache, 'w', encoding='utf-8'), ensure_ascii=False)
                    print(f"  {n}/{len(todo)}", flush=True)
    json.dump(done, open(cache, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"完成,共 {len(done)} → {out_csv}")

if __name__ == '__main__':
    main()
