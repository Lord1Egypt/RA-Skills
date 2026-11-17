#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 扫描文件夹下所有照片/视频的 EXIF：拍摄时间 + GPS + 文件大小 → JSON
# 用法: python exif_scan.py <root_folder> [out_json]
# 依赖: exiftool (PATH 或 /opt/homebrew/bin/exiftool)
import os, sys, json, subprocess
from collections import defaultdict

EXIFS = {'.jpg','.jpeg','.heic','.png','.livp','.mp4','.mov','.avi','.mkv','.m4v','.3gp','.wmv','.flv','.webm'}
EXIFT = '/opt/homebrew/bin/exiftool' if os.path.exists('/opt/homebrew/bin/exiftool') else 'exiftool'
B = 400

def collect(root):
    out = []
    for dp, _, fns in os.walk(root):
        for n in fns:
            if n == '.DS_Store': continue
            if os.path.splitext(n)[1].lower() in EXIFS:
                out.append(os.path.join(dp, n))
    return out

def main():
    root = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.getcwd(), '_exif.json')
    files = collect(root)
    print(f"扫描到 {len(files)} 个媒体文件", flush=True)
    data = {}
    if os.path.exists(out):
        try: data = json.load(open(out, encoding='utf-8'))
        except Exception: data = {}
    todo = [p for p in files if p not in data]
    print(f"已缓存 {len(data)}, 待扫 {len(todo)}", flush=True)
    for i in range(0, len(todo), B):
        batch = todo[i:i+B]
        # -CreateDate 兼容视频/照片; -DateTimeOriginal 照片; -GPSLatitude/-GPSLongitude
        res = subprocess.run([EXIFT,'-T','-n','-CreateDate','-DateTimeOriginal',
                              '-GPSLatitude','-GPSLongitude','-FileSize'] + batch,
                             capture_output=True, text=True)
        for p, line in zip(batch, (res.stdout or '').strip().split('\n')):
            parts = line.split('\t')
            if len(parts) < 5:
                data[p] = {'date': None, 'gps': None, 'size': None}; continue
            cd, dto, lat, lon, sz = parts[0], parts[1], parts[2], parts[3], parts[4]
            t = (dto or cd)
            date = t[:10].replace(':', '-') if t and len(t) >= 10 else None
            try: g = (float(lat), float(lon)) if lat not in ('','0','0.0') else None
            except Exception: g = None
            try: sz = float(sz)
            except Exception: sz = None
            data[p] = {'date': date, 'gps': g, 'size': sz}
        json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
        print(f"  扫完 {min(i+B, len(todo))}/{len(todo)}", flush=True)
    print(f"完成,共 {len(data)} 条 → {out}")

if __name__ == '__main__':
    main()
