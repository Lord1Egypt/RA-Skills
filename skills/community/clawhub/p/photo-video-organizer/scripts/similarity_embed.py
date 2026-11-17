#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 语义嵌入（Tier B 用）：照片整张 CLIP / 视频关键帧 CLIP → 512维向量缓存
# 用法: python similarity_embed.py <root_folder> <photo|video|auto> [cache_json] [batch]
# 照片: 整张图 CLIP；视频: 抽 N 帧覆盖头/中/尾(小文件整段, 大文件前13秒/400帧)
# 依赖: opencv-python, pillow, pillow-heif, openai-clip, torch
# 可断点续传（按路径+mtime缓存）。只读。
import os, sys, json
import cv2
import numpy as np
from PIL import Image
import clip, torch

PHOTO_EXTS = {'.jpg','.jpeg','.heic','.png','.livp'}
VIDEO_EXTS = {'.mp4','.mov','.avi','.mkv','.m4v'}
LARGE = 500 * 1024 * 1024
NF = 6          # 视频抽帧数
FLUSH_EVERY = 10

device = 'cpu'
model, preprocess = clip.load('ViT-B/32', device=device)
model.eval()
try:
    import pillow_heif; pillow_heif.register_heif_opener(); HEIC_OK = True
except Exception:
    HEIC_OK = False

def collect(root, mode):
    photos, videos = [], []
    for dp, _, fns in os.walk(root):
        for n in fns:
            if n == '.DS_Store': continue
            e = os.path.splitext(n)[1].lower()
            p = os.path.join(dp, n)
            if e in PHOTO_EXTS: photos.append(p)
            elif e in VIDEO_EXTS: videos.append(p)
    if mode == 'photo': return photos
    if mode == 'video': return videos
    return photos + videos

def load_image(path):
    import io, zipfile
    e = os.path.splitext(path)[1].lower()
    if e == '.livp':
        try:
            with zipfile.ZipFile(path) as z:
                for n in z.namelist():
                    if n.lower().endswith(('.jpg','.jpeg')):
                        return Image.open(io.BytesIO(z.read(n))).convert('RGB')
        except Exception: return None
    if e == '.heic' and not HEIC_OK: return None
    try: return Image.open(path).convert('RGB')
    except Exception: return None

def embed_pil(img):
    t = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad(): f = model.encode_image(t)
    return f.cpu().numpy().flatten().tolist()

def embed_video(p):
    cap = cv2.VideoCapture(p)
    if not cap.isOpened(): return None, 0
    fps = cap.get(cv2.CAP_PROP_FPS) or 0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    dur = (total / fps) if fps > 0 else 0
    is_large = os.path.getsize(p) >= LARGE
    if is_large:  # 大文件只前13秒/400帧
        total = min(total if total > 0 else 400, int(13 * (fps or 30)), 400)
    if total > 80000: total = min(80000, max(1, int((dur or 30)*(fps or 30))))
    N = max(5, min(20, int(round(dur / 8)))) if dur > 0 else 5
    idxs = sorted(set(int(round(i*(total-1)/(N-1))) for i in range(N))) if N > 1 and total > 1 else [0]
    targets = set(idxs); last = max(idxs) if idxs else 0
    vecs, fi = [], 0
    while fi <= last + 20:
        ok, frame = cap.read()
        if not ok: break
        if fi in targets:
            try: vecs.append(embed_pil(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))))
            except Exception: pass
        fi += 1
        if fi > last: break
    cap.release()
    if not vecs: return None, dur
    return (np.mean(np.array(vecs, dtype=np.float32), axis=0).tolist()), dur

def main():
    root = sys.argv[1]; mode = sys.argv[2]
    cache_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.getcwd(), '_clip_cache.json')
    batch = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    files = collect(root, mode)
    print(f"待嵌入({mode}): {len(files)}", flush=True)
    cache = {}
    if os.path.exists(cache_path):
        try: cache = json.load(open(cache_path, encoding='utf-8'))
        except Exception: cache = {}
    new = 0
    for i, p in enumerate(files, 1):
        c = cache.get(p)
        if c and c.get('mt') == os.path.getmtime(p): continue
        try:
            if p.lower().endswith(('.mp4','.mov','.avi','.mkv','.m4v')):
                vec, dur = embed_video(p)
            else:
                img = load_image(p); vec = embed_pil(img) if img else None; dur = 0
        except Exception as e:
            print(f"  跳过(异常): {p} {e}", flush=True); continue
        if vec is None: continue
        cache[p] = {'vec': vec, 'mt': os.path.getmtime(p), 'dur': round(dur, 1)}
        new += 1
        if new % FLUSH_EVERY == 0:
            json.dump(cache, open(cache_path, 'w', encoding='utf-8'), ensure_ascii=False)
            print(f"  {i}/{len(files)} 新算{new} 已缓存{len(cache)}", flush=True)
        if batch and new >= batch:
            json.dump(cache, open(cache_path, 'w', encoding='utf-8'), ensure_ascii=False)
            print(f"  batch上限{batch},暂停", flush=True); return
    json.dump(cache, open(cache_path, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"完成,共 {len(cache)} 向量 → {cache_path}")

if __name__ == '__main__':
    main()
