#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 生成可交互对比 HTML：每组成员缩略图，点击切换保留/移除，导出决定CSV到剪贴板
# 用法: python interactive_review_html.py <groups_json> <root_folder> [out_html]
# groups_json = similarity_cluster.py 的 out_json。照片缩略图直接用原图; 视频抽中间帧(大文件前段)
# 依赖: opencv-python, pillow, pillow-heif
import os, sys, json, html
import cv2
from PIL import Image

LARGE = 500 * 1024 * 1024
try:
    import pillow_heif; pillow_heif.register_heif_opener(); HEIC_OK = True
except Exception:
    HEIC_OK = False
VIDEO_EXTS = {'.mp4','.mov','.avi','.mkv','.m4v'}

def thumb(video_or_img, tp, w=320):
    if os.path.exists(tp): return True
    try:
        if video_or_img.lower().endswith(VIDEO_EXTS) or os.path.splitext(video_or_img)[1].lower() in VIDEO_EXTS:
            cap = cv2.VideoCapture(video_or_img)
            if not cap.isOpened(): return False
            fps = cap.get(cv2.CAP_PROP_FPS) or 0
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
            is_large = os.path.getsize(video_or_img) >= LARGE
            if is_large: total = min(total if total>0 else 400, int(13*(fps or 30)), 400)
            elif total <= 0 or total > 800: total = min(800, max(1, int(3*(fps or 30))))
            mid = total // 2; fi = 0; ok = False
            while fi <= mid + 20:
                ok, frame = cap.read()
                if not ok: break
                if fi >= mid: break
                fi += 1
            cap.release()
            if not ok or frame is None: return False
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            img = Image.open(video_or_img).convert('RGB')
        img.thumbnail((w, w)); img.save(tp, 'JPEG', quality=80); return True
    except Exception:
        return False

def main():
    groups = json.load(open(sys.argv[1], encoding='utf-8'))
    root = sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.getcwd(), '相似组_可交互.html')
    tdir = os.path.join(os.path.dirname(out), '_review_thumbs')
    os.makedirs(tdir, exist_ok=True)
    groups.sort(key=lambda g: len(g['keep'])+len(g['move']), reverse=True)
    sections = []
    for g in groups:
        cards = []
        for p in g['keep']: cards.append((p, 'keep'))
        for p in g['move']: cards.append((p, 'move'))
        ch = ''
        for idx, (p, dec) in enumerate(cards):
            name = os.path.basename(p); tp = os.path.join(tdir, f"{g['gid']}_{idx}.jpg")
            thumb(p, tp)
            rel = os.path.relpath(tp, os.path.dirname(out))
            ch += f'<div class="card {dec}" data-file="{html.escape(name)}" onclick="toggle(this)"><img src="{html.escape(rel)}"><div class="fn">{html.escape(name)}</div><div class="badge">{"保留" if dec=="keep" else "移除"}</div></div>'
        sections.append(f'<div class="grp"><div class="gh">组 {g["gid"]} | 日期 {g.get("date","")} | 成员 {len(cards)} | sim {g.get("sim_max",0):.3f}</div><div class="gc">{ch}</div></div>')
    doc = '''<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><title>相似组核对</title>
<style>body{font-family:-apple-system,sans-serif;margin:0;background:#f0f0f0;}
.bar{position:sticky;top:0;background:#263238;color:#fff;padding:10px 14px;z-index:100;display:flex;gap:14px;align-items:center;}
.bar button{background:#ffb74d;color:#000;border:0;padding:8px 14px;border-radius:4px;font-weight:bold;cursor:pointer;}
.grp{border:1px solid #bbb;margin:10px;padding:8px;background:#fff;border-radius:4px;}
.gh{font-weight:bold;color:#1565c0;margin-bottom:6px;}
.gc{display:flex;flex-wrap:wrap;}
.card{display:inline-block;margin:4px;width:170px;padding:4px;border-radius:4px;cursor:pointer;border:3px solid transparent;text-align:center;}
.card.keep{background:#e8f5e9;border-color:#2e7d32;} .card.move{background:#ffebee;border-color:#c62828;}
.card img{width:160px;height:110px;object-fit:cover;border:1px solid #888;}
.card .fn{font-size:10px;color:#333;word-break:break-all;height:26px;overflow:hidden;}
.card .badge{font-size:11px;color:#fff;background:#2e7d32;border-radius:3px;} .card.move .badge{background:#c62828;}
</style></head><body><div class="bar"><b>相似组调整</b><span>候选移除: <b id="mc">0</b></span><button onclick="exp()">导出决定(复制剪贴板)</button></div>
''' + ''.join(sections) + '''
<script>function recalc(){document.getElementById('mc').textContent=document.querySelectorAll('.card.move').length;}
function toggle(c){if(c.classList.contains('keep')){c.classList.remove('keep');c.classList.add('move');c.querySelector('.badge').textContent='移除';}else{c.classList.remove('move');c.classList.add('keep');c.querySelector('.badge').textContent='保留';}recalc();}
function exp(){var L=['gid,decision,filename'];document.querySelectorAll('.grp').forEach(function(gp){var m=gp.querySelector('.gh').textContent.match(/组 (\\d+)/);var gid=m?m[1]:'';gp.querySelectorAll('.card').forEach(function(c){L.push(gid+','+(c.classList.contains('keep')?'keep':'move')+','+c.dataset.file);});});var t=L.join('\\n');navigator.clipboard.writeText(t).then(function(){alert('已复制 '+L.length+' 行,粘贴给助手执行移动');},function(){var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);alert('已复制 '+L.length+' 行');});}
recalc();</script></body></html>'''
    open(out, 'w', encoding='utf-8').write(doc)
    print(f"HTML: {out}")

if __name__ == '__main__':
    main()
