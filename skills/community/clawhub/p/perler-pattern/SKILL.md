---
name: perler-pattern
description: Convert any image into a perler/hama/fuse bead pattern with automatic background removal. 把任意图片转换成精美的拼豆图纸，内置自动去背景。Use when the user wants to generate a bead pattern from a photo, image, or URL. Automatically removes background using GrabCut (fully offline, no API), places subject on dark background, then generates: interactive HTML viewer, print-ready SVG with color codes, 3D bead preview PNG, and bead count list. Supports Hama, Artkal, Perler, and universal palettes. Zero API cost — pure Python + OpenCV.
version: 1.2.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🧩"
    requires:
      bins:
        - python3
---

# Perler Bead Pattern Generator · 拼豆图纸生成器

把任意图片自动去背景，生成精美拼豆图纸。
内置 GrabCut 离线去背景，无需任何外部 API，零费用。

Palette reference → `references/palettes.md`
Style guide → `references/styles.md`

## Trigger / 触发时机

- "Turn this photo into a perler bead pattern"
- "帮我把这张图片做成拼豆图纸"
- "Make a hama bead pattern from my pet photo"
- "把我家宠物的照片转成拼豆图纸"
- "Generate a 40×40 Artkal bead pattern"
- "用欧小色板生成拼豆图纸，深色背景"

---

## Step 0: Dependency Check / 环境检查

```bash
# Check and install required packages
python3 -c "import cv2" 2>/dev/null || pip3 install opencv-python-headless --quiet
python3 -c "from PIL import Image" 2>/dev/null || pip3 install Pillow --quiet
python3 -c "import numpy" 2>/dev/null || pip3 install numpy --quiet
echo "✅ Ready"
```

---

## Step 1: Extract Parameters / 提取参数

```
Image / 图片来源:
  Local path 本地路径  or  URL 网络链接

Grid size / 网格尺寸 (default 40×40):
  "small"  → 29×29   (one board / 一块板)
  "medium" → 40×40   (default / 默认)
  "large"  → 48×48
  "xlarge" → 64×64

Palette / 色板 (default: hama):
  hama / artkal / perler / universal

Background color / 背景色 (default: dark_navy):
  dark_navy  → (15, 15, 40)   深海军蓝，最常见
  black      → (5, 5, 5)      纯黑
  white      → (255,255,255)  白色（适合浅色主体）
  custom     → 用户指定 RGB

Max colors / 颜色数 (default: 25):
  "simple"   → 15
  "standard" → 25
  "detailed" → 32
```

---

## Step 2: Run / 执行脚本

Replace all `__PARAM__` placeholders before running.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Perler Bead Pattern Generator v1.2 — Auto background removal via GrabCut"""

import os, sys, json, math
import cv2
import numpy as np
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

# ── Parameters (filled by OpenClaw) ──────────────────────
IMAGE_PATH   = "__IMAGE_PATH__"
GRID_W       = 40
GRID_H       = 40
MAX_COLORS   = 25
PALETTE_NAME = "hama"           # hama / artkal / perler / universal
BG_COLOR     = (15, 15, 40)     # deep navy blue
OUTPUT_DIR   = "__OUTPUT_DIR__"

# ── Guard ────────────────────────────────────────────────
if "__IMAGE_PATH__" in IMAGE_PATH or not IMAGE_PATH:
    print("❌ IMAGE_PATH not set."); sys.exit(1)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Palettes ─────────────────────────────────────────────
PALETTES = {
    "hama": {
        "H01":("White/白",        (255,255,255)), "H02":("Cream/奶油",     (255,253,208)),
        "H03":("Lt Yellow/淡黄",  (255,239, 96)), "H04":("Yellow/黄",      (255,216,  0)),
        "H05":("Orange/橙",       (255,140,  0)), "H06":("Red-Orange/橙红",(230, 75,  0)),
        "H07":("Red/红",          (210, 20, 20)), "H08":("Dark Red/暗红",  (155,  0,  0)),
        "H09":("Lt Pink/浅粉",    (255,190,210)), "H10":("Pink/粉",        (255,130,170)),
        "H11":("Rose/玫红",       (220, 45,120)), "H12":("Purple/紫",      (128, 28,156)),
        "H13":("Violet/紫罗兰",   ( 88, 18,196)), "H14":("Lavender/薰衣草",(200,168,255)),
        "H15":("Lt Blue/天蓝",    (130,198,255)), "H16":("Blue/蓝",        (  0, 96,200)),
        "H17":("Dark Blue/深蓝",  (  0, 28,138)), "H18":("Turquoise/青",   (  0,178,178)),
        "H19":("Dark Green/深绿", (  0, 88,  0)), "H20":("Green/绿",       ( 28,158, 28)),
        "H21":("Lime/黄绿",       (146,218,  0)), "H22":("Mint/薄荷",      (168,255,210)),
        "H23":("Dark Brown/深棕", ( 78, 38,  0)), "H24":("Brown/棕",       (138, 68, 18)),
        "H25":("Tan/浅棕",        (198,152, 88)), "H26":("Skin/肤色",      (255,208,168)),
        "H27":("Peach/桃",        (255,178,140)), "H28":("Coral/珊瑚",     (255,108,100)),
        "H29":("Lt Grey/浅灰",    (210,210,210)), "H30":("Grey/灰",        (148,148,148)),
        "H31":("Dark Grey/深灰",  ( 78, 78, 78)), "H32":("Black/黑",       ( 10, 10, 10)),
        "H33":("Gold/金",         (218,178,  0)), "H34":("Silver/银",      (188,188,188)),
        "H35":("Neon Yellow/荧光黄",(226,255,0)),"H36":("Neon Pink/荧光粉",(255,18,144)),
        "H37":("Neon Green/荧光绿",(  0,252, 78)),"H38":("Neon Orange/荧光橙",(255,100,0)),
    },
    "artkal": {
        "C01":("White/白",(255,255,255)),"C02":("Cream/奶油",(255,248,208)),
        "C03":("Lt Yellow/淡黄",(255,232,88)),"C04":("Yellow/黄",(255,212,0)),
        "C05":("Orange/橙",(255,138,0)),"C06":("Red-Orange/橙红",(228,68,0)),
        "C07":("Red/红",(208,14,14)),"C08":("Dark Red/深红",(138,0,0)),
        "C09":("Lt Pink/浅粉",(255,172,192)),"C10":("Rose/玫红",(222,38,118)),
        "C11":("Purple/紫",(118,24,152)),"C12":("Dark Purple/深紫",(78,0,118)),
        "C13":("Sky Blue/天蓝",(128,192,255)),"C14":("Blue/蓝",(0,88,192)),
        "C15":("Navy/深蓝",(0,18,128)),"C16":("Cyan/青",(0,172,172)),
        "C17":("Green/绿",(24,152,24)),"C18":("Dark Green/深绿",(0,78,0)),
        "C19":("Yellow-Green/黄绿",(138,212,0)),"C20":("Brown/棕",(132,62,14)),
        "C21":("Dark Brown/深棕",(72,32,0)),"C22":("Tan/浅棕",(192,148,82)),
        "C23":("Skin/肤色",(248,202,162)),"C24":("Coral/珊瑚",(248,122,102)),
        "C25":("Lt Grey/浅灰",(208,208,208)),"C26":("Grey/灰",(142,142,142)),
        "C27":("Dark Grey/深灰",(72,72,72)),"C28":("Black/黑",(4,4,4)),
        "C29":("Gold/金",(212,172,0)),"C30":("Lavender/薰衣草",(202,172,248)),
    },
    "perler": {
        "P01":("White/白",(255,255,255)),"P02":("Cream/奶油",(255,246,218)),
        "P03":("Yellow/黄",(255,222,0)),"P04":("Orange/橙",(255,118,0)),
        "P05":("Red/红",(212,0,14)),"P06":("Lt Pink/浅粉",(255,168,188)),
        "P07":("Pink/粉",(255,108,158)),"P08":("Rose/玫红",(218,42,118)),
        "P09":("Purple/紫",(122,28,152)),"P10":("Lt Blue/天蓝",(122,188,255)),
        "P11":("Blue/蓝",(0,82,188)),"P12":("Dark Blue/深蓝",(0,22,128)),
        "P13":("Teal/青",(0,162,162)),"P14":("Green/绿",(18,148,18)),
        "P15":("Dark Green/深绿",(0,72,0)),"P16":("Kiwi/黄绿",(142,208,0)),
        "P17":("Brown/棕",(128,58,8)),"P18":("Peach/桃",(255,198,158)),
        "P19":("Lt Grey/浅灰",(208,208,208)),"P20":("Grey/灰",(138,138,138)),
        "P21":("Black/黑",(0,0,0)),"P22":("Gold/金",(208,168,0)),
        "P23":("Silver/银",(182,182,182)),"P24":("Clear/透明",(238,238,238)),
    },
    "universal": {
        "U01":("White/白",(255,255,255)),"U02":("Ivory/米白",(255,248,210)),
        "U03":("Lt Yellow/浅黄",(255,238,82)),"U04":("Yellow/黄",(255,212,0)),
        "U05":("Amber/琥珀",(222,178,0)),"U06":("Lt Orange/浅橙",(255,168,58)),
        "U07":("Orange/橙",(255,110,0)),"U08":("Dk Orange/深橙",(218,68,0)),
        "U09":("Salmon/鲑鱼",(255,120,100)),"U10":("Red/红",(210,0,0)),
        "U11":("Dark Red/深红",(138,0,0)),"U12":("Lt Pink/浅粉",(255,198,212)),
        "U13":("Pink/粉",(255,148,178)),"U14":("Hot Pink/玫红",(218,38,118)),
        "U15":("Magenta/品红",(198,0,148)),"U16":("Lavender/薰衣草",(208,178,255)),
        "U17":("Purple/紫",(128,28,158)),"U18":("Dk Purple/深紫",(78,0,118)),
        "U19":("Baby Blue/婴儿蓝",(178,222,255)),"U20":("Sky Blue/天蓝",(98,178,255)),
        "U21":("Blue/蓝",(0,88,198)),"U22":("Dark Blue/深蓝",(0,22,138)),
        "U23":("Cyan/青",(0,178,178)),"U24":("Dark Cyan/深青",(0,118,118)),
        "U25":("Lt Green/浅绿",(148,228,148)),"U26":("Green/绿",(28,158,28)),
        "U27":("Dark Green/深绿",(0,88,0)),"U28":("Yellow Green/黄绿",(152,222,0)),
        "U29":("Lt Brown/浅棕",(208,168,108)),"U30":("Brown/棕",(148,78,22)),
        "U31":("Dark Brown/深棕",(88,42,0)),"U32":("Skin/肤色",(255,208,168)),
        "U33":("Peach/桃",(255,178,138)),"U34":("Lt Grey/浅灰",(208,208,208)),
        "U35":("Grey/灰",(148,148,148)),"U36":("Dark Grey/深灰",(78,78,78)),
        "U37":("Black/黑",(4,4,4)),"U38":("Gold/金",(218,178,0)),
        "U39":("Silver/银",(190,190,190)),"U40":("Neon Yellow/荧光黄",(228,255,0)),
        "U41":("Neon Pink/荧光粉",(255,18,144)),"U42":("Neon Green/荧光绿",(0,252,78)),
    }
}

# ── Color math: Lab color space ───────────────────────────
def rgb_to_lab(rgb):
    r,g,b = [c/255.0 for c in rgb]
    def lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
    r,g,b = lin(r),lin(g),lin(b)
    X=r*0.4124564+g*0.3575761+b*0.1804375
    Y=r*0.2126729+g*0.7151522+b*0.0721750
    Z=r*0.0193339+g*0.1191920+b*0.9503041
    X/=0.95047; Z/=1.08883
    def f(t): return t**(1/3) if t>0.008856 else 7.787*t+16/116
    fx,fy,fz=f(X),f(Y),f(Z)
    return 116*fy-16, 500*(fx-fy), 200*(fy-fz)

def lab_dist(a,b): return sum((x-y)**2 for x,y in zip(a,b))**0.5

def build_lab_pal(palette):
    return {code:(info[0],info[1],rgb_to_lab(info[1])) for code,info in palette.items()}

def nearest_color(rgb, lab_pal):
    lab=rgb_to_lab(rgb)
    best,dist=None,float('inf')
    for code,(_,pal_rgb,pal_lab) in lab_pal.items():
        d=lab_dist(lab,pal_lab)
        if d<dist: dist,best=d,code
    _,pal_rgb,_=lab_pal[best]
    return best,pal_rgb

# ── Load image ────────────────────────────────────────────
def load_image(path):
    if path.startswith(("http://","https://")):
        import urllib.request,tempfile
        ext=".jpg" if "jpg" in path.lower() else ".png"
        tmp=tempfile.mktemp(suffix=ext)
        urllib.request.urlretrieve(path,tmp)
        path=tmp
    return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)

# ── Auto background removal (GrabCut, fully offline) ─────
def remove_background(img_rgb, bg_color=(15,15,40)):
    h,w=img_rgb.shape[:2]
    # Init rect: 10% margins, avoids edge artifacts
    mx,my=int(w*0.10),int(h*0.08)
    rect=(mx,my,w-2*mx,h-2*my)
    mask=np.zeros((h,w),np.uint8)
    bgd=np.zeros((1,65),np.float64)
    fgd=np.zeros((1,65),np.float64)
    cv2.grabCut(img_rgb,mask,rect,bgd,fgd,7,cv2.GC_INIT_WITH_RECT)
    fg=np.where((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD),255,0).astype(np.uint8)
    # Smooth edges
    fg=cv2.GaussianBlur(fg,(3,3),0)
    _,fg=cv2.threshold(fg,128,255,cv2.THRESH_BINARY)
    # Fill holes, remove specks
    fg=cv2.morphologyEx(fg,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    fg=cv2.morphologyEx(fg,cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    result=img_rgb.copy()
    result[fg==0]=bg_color
    return result

# ── Resize center-crop ────────────────────────────────────
def resize_crop(img_rgb,w,h):
    ih,iw=img_rgb.shape[:2]
    scale=max(w/iw,h/ih)
    nw,nh=math.ceil(iw*scale),math.ceil(ih*scale)
    img_pil=Image.fromarray(img_rgb).resize((nw,nh),Image.LANCZOS)
    left=(nw-w)//2; top=(nh-h)//2
    return np.array(img_pil.crop((left,top,left+w,top+h)))

# ── Lab-based brightness equalization ────────────────────
def lab_equalize(arr):
    def r2l(a):
        rgb=a.astype(np.float32)/255.0
        m=rgb>0.04045
        rgb=np.where(m,((rgb+0.055)/1.055)**2.4,rgb/12.92)
        M=np.array([[0.4124564,0.3575761,0.1804375],[0.2126729,0.7151522,0.0721750],[0.0193339,0.1191920,0.9503041]])
        xyz=rgb@M.T/[0.95047,1,1.08883]
        m2=xyz>0.008856
        xyz=np.where(m2,xyz**(1/3),7.787*xyz+16/116)
        return np.stack([116*xyz[:,:,1]-16,500*(xyz[:,:,0]-xyz[:,:,1]),200*(xyz[:,:,1]-xyz[:,:,2])],2)
    def l2r(lab):
        L,a,b=lab[:,:,0],lab[:,:,1],lab[:,:,2]
        fy=(L+16)/116;fx=a/500+fy;fz=fy-b/200
        xyz=np.stack([fx,fy,fz],2)
        m=xyz>0.2068966
        xyz=np.where(m,xyz**3,(xyz-16/116)/7.787)*[0.95047,1,1.08883]
        Mi=np.array([[3.2404542,-1.5371385,-0.4985314],[-0.9692660,1.8760108,0.0415560],[0.0556434,-0.2040259,1.0572252]])
        rgb=np.clip(xyz@Mi.T,0,1)
        m2=rgb>0.0031308
        return np.clip(np.where(m2,1.055*rgb**(1/2.4)-0.055,12.92*rgb)*255,0,255).astype(np.uint8)
    lab=r2l(arr)
    L=lab[:,:,0]
    p2,p98=np.percentile(L,2),np.percentile(L,98)
    if p98-p2>5:
        lab[:,:,0]=np.clip((L-p2)/(p98-p2)*100,0,100)
    return l2r(lab)

# ── Map pixels to palette ─────────────────────────────────
def map_to_palette(arr,lab_pal,max_colors):
    h,w=arr.shape[:2]
    cache={}
    grid=[[None]*w for _ in range(h)]
    usage={}
    for y in range(h):
        for x in range(w):
            rgb=tuple(arr[y,x])
            if rgb not in cache:
                code,pal_rgb=nearest_color(rgb,lab_pal)
                name=lab_pal[code][0]
                cache[rgb]=(code,name,pal_rgb)
            code,name,pal_rgb=cache[rgb]
            grid[y][x]=code
            if code not in usage:
                usage[code]={"name":name,"rgb":pal_rgb,"count":0}
            usage[code]["count"]+=1
    # Enforce max_colors: merge least-used into nearest
    while len(usage)>max_colors:
        least=min(usage,key=lambda c:usage[c]["count"])
        ll=rgb_to_lab(usage[least]["rgb"])
        best_alt,bd=None,float('inf')
        for c in usage:
            if c==least: continue
            d=lab_dist(ll,rgb_to_lab(usage[c]["rgb"]))
            if d<bd: bd,best_alt=d,c
        for y in range(h):
            for x in range(w):
                if grid[y][x]==least: grid[y][x]=best_alt
        usage[best_alt]["count"]+=usage[least]["count"]
        del usage[least]
    grid_rgb=np.zeros((h,w,3),dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            grid_rgb[y,x]=usage[grid[y][x]]["rgb"]
    return grid,grid_rgb,usage

# ── SVG output ────────────────────────────────────────────
def gen_svg(grid,usage,cell=16):
    rows,cols=len(grid),len(grid[0])
    W,H=cols*cell,rows*cell
    fs=max(5,cell//3)
    L=['<?xml version="1.0" encoding="UTF-8"?>',
       f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       f'<style>text{{font-family:Arial;font-size:{fs}px;}}</style>']
    for y,row in enumerate(grid):
        for x,code in enumerate(row):
            r,g,b=usage[code]["rgb"]
            fill=f"#{r:02x}{g:02x}{b:02x}"
            lum=0.299*r+0.587*g+0.114*b
            tc="#fff" if lum<128 else "#000"
            px,py=x*cell,y*cell
            L.append(f'<rect x="{px}" y="{py}" width="{cell}" height="{cell}" fill="{fill}" stroke="#ccc" stroke-width="0.4"/>')
            if cell>=10:
                num=''.join(c for c in code if c.isdigit())
                L.append(f'<text x="{px+cell//2}" y="{py+cell//2}" fill="{tc}" text-anchor="middle" dominant-baseline="central">{num}</text>')
    for i in range(0,cols+1,10): L.append(f'<line x1="{i*cell}" y1="0" x2="{i*cell}" y2="{H}" stroke="#888" stroke-width="0.8"/>')
    for i in range(0,rows+1,10): L.append(f'<line x1="0" y1="{i*cell}" x2="{W}" y2="{i*cell}" stroke="#888" stroke-width="0.8"/>')
    L.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#222" stroke-width="1.5"/>')
    L.append('</svg>')
    return '\n'.join(L)

# ── 3D Bead preview PNG ───────────────────────────────────
def gen_bead_preview(arr_q,bg_color,cell=20):
    rows,cols=arr_q.shape[:2]
    canvas=Image.new("RGB",(cols*cell,rows*cell),bg_color)
    draw=ImageDraw.Draw(canvas)
    for y in range(rows):
        for x in range(cols):
            r,g,b=int(arr_q[y,x,0]),int(arr_q[y,x,1]),int(arr_q[y,x,2])
            cx,cy=x*cell+cell//2,y*cell+cell//2
            pad=1
            # Main bead body
            draw.ellipse([cx-cell//2+pad,cy-cell//2+pad,cx+cell//2-pad,cy+cell//2-pad],fill=(r,g,b))
            # Bottom-right shadow (same hue, darker)
            dark=(max(0,r-55),max(0,g-55),max(0,b-55))
            draw.arc([cx-cell//2+pad+1,cy-cell//2+pad+1,cx+cell//2-pad-1,cy+cell//2-pad-1],
                     start=30,end=210,fill=dark,width=2)
            # Top-left highlight (lighter)
            hs=cell//5
            hi=(min(255,r+90),min(255,g+90),min(255,b+90))
            draw.ellipse([cx-hs,cy-hs,cx,cy],fill=hi)
    return canvas

# ── Interactive HTML viewer ───────────────────────────────
def gen_html(grid,usage,palette_name,bg_color):
    rows,cols=len(grid),len(grid[0])
    total=sum(v["count"] for v in usage.values())
    bg_hex="#{:02x}{:02x}{:02x}".format(*bg_color)
    cells_js=json.dumps([[grid[y][x] for x in range(cols)] for y in range(rows)])
    colors_js=json.dumps([
        {"code":c,"name":v["name"],"hex":"#{:02x}{:02x}{:02x}".format(*v["rgb"]),"count":v["count"]}
        for c,v in sorted(usage.items(),key=lambda x:-x[1]["count"])
    ])
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Perler Pattern · 拼豆图纸 {cols}×{rows}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'PingFang SC','Segoe UI',Arial,sans-serif;background:#f0f0f0}}
header{{background:linear-gradient(135deg,#6c63ff,#3ec6e0);color:#fff;padding:18px 24px}}
header h1{{font-size:20px;margin-bottom:3px}}
header p{{font-size:12px;opacity:.85}}
.wrap{{max-width:1280px;margin:0 auto;padding:16px}}
.bar{{background:#fff;border-radius:10px;padding:12px 16px;margin-bottom:12px;
      box-shadow:0 2px 8px rgba(0,0,0,.07);display:flex;gap:14px;align-items:center;flex-wrap:wrap}}
.bar label{{font-size:13px;color:#555;display:flex;align-items:center;gap:6px}}
input[type=range]{{width:100px}}
.btn{{padding:7px 14px;border-radius:7px;border:none;cursor:pointer;font-size:13px;font-weight:600}}
.btn-p{{background:#6c63ff;color:#fff}}.btn-s{{background:#e8e8e8;color:#333}}
.btn:hover{{opacity:.85}}
.layout{{display:grid;grid-template-columns:1fr 290px;gap:12px}}
@media(max-width:780px){{.layout{{grid-template-columns:1fr}}}}
.cbox{{background:#fff;border-radius:10px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.07);overflow:auto}}
canvas{{cursor:crosshair;display:block}}
.side{{display:flex;flex-direction:column;gap:12px}}
.card{{background:#fff;border-radius:10px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.07)}}
.card h3{{font-size:13px;font-weight:700;color:#333;margin-bottom:10px}}
.stats{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.stat{{background:#f7f7f7;border-radius:8px;padding:10px;text-align:center}}
.stat-n{{font-size:18px;font-weight:700;color:#6c63ff}}
.stat-l{{font-size:10px;color:#888;margin-top:2px}}
.clist{{max-height:420px;overflow-y:auto}}
.ci{{display:flex;align-items:center;gap:8px;padding:5px 4px;border-bottom:1px solid #f0f0f0;cursor:pointer;border-radius:5px}}
.ci:hover{{background:#f5f5ff}}.ci.active{{background:#eeeeff;outline:2px solid #6c63ff}}
.sw{{width:22px;height:22px;border-radius:4px;border:1px solid #ddd;flex-shrink:0}}
.cc{{font-size:10px;font-weight:700;color:#6c63ff;width:38px}}
.cn{{font-size:11px;color:#555;flex:1;line-height:1.3}}
.cnt{{font-size:10px;color:#999;white-space:nowrap}}
.tip{{position:fixed;background:rgba(30,30,30,.88);color:#fff;padding:6px 10px;border-radius:6px;
      font-size:11px;pointer-events:none;display:none;z-index:999;line-height:1.5}}
@media print{{header,.bar,.side{{display:none!important}}
  .wrap{{padding:0;max-width:100%}}.cbox{{box-shadow:none;padding:0;border-radius:0}}}}
</style></head><body>
<header>
  <h1>🧩 Perler Bead Pattern · 拼豆图纸</h1>
  <p>{cols}×{rows} · {palette_name.upper()} · {len(usage)} colors · {total:,} beads</p>
</header>
<div class="wrap">
<div class="bar">
  <label>Cell 格子 <input type="range" id="sz" min="6" max="32" value="14"><span id="szv">14px</span></label>
  <label><input type="checkbox" id="nums" checked> Numbers 编号</label>
  <label><input type="checkbox" id="grid" checked> Grid 网格</label>
  <button class="btn btn-p" onclick="dlSVG()">⬇ SVG</button>
  <button class="btn btn-p" onclick="dlPNG()">⬇ PNG</button>
  <button class="btn btn-s" onclick="window.print()">🖨 Print</button>
  <button class="btn btn-s" onclick="hl=null;draw()">✖ Clear</button>
</div>
<div class="layout">
<div class="cbox"><canvas id="c"></canvas></div>
<div class="side">
  <div class="card">
    <h3>📊 Stats · 统计</h3>
    <div class="stats">
      <div class="stat"><div class="stat-n">{cols}×{rows}</div><div class="stat-l">Grid 网格</div></div>
      <div class="stat"><div class="stat-n">{total:,}</div><div class="stat-l">Beads 豆数</div></div>
      <div class="stat"><div class="stat-n">{len(usage)}</div><div class="stat-l">Colors 颜色</div></div>
      <div class="stat"><div class="stat-n" style="font-size:13px">{palette_name.upper()}</div><div class="stat-l">Palette 色板</div></div>
    </div>
  </div>
  <div class="card">
    <h3>🎨 Bead List · 用豆清单</h3>
    <div class="clist" id="cl"></div>
  </div>
</div></div></div>
<div class="tip" id="tip"></div>
<script>
const CELLS={cells_js},COLORS={colors_js};
const ROWS={rows},COLS={cols},BG="{bg_hex}";
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d');
const tip=document.getElementById('tip');
let cell=14,showN=true,showG=true,hl=null;
function draw(){{
  canvas.width=COLS*cell;canvas.height=ROWS*cell;
  ctx.fillStyle=BG;ctx.fillRect(0,0,canvas.width,canvas.height);
  for(let y=0;y<ROWS;y++)for(let x=0;x<COLS;x++){{
    const code=CELLS[y][x],ci=COLORS.find(c=>c.code===code);
    ctx.fillStyle=(hl&&code!==hl)?'rgba(128,128,128,0.3)':ci.hex;
    ctx.fillRect(x*cell,y*cell,cell,cell);
    if(showG){{ctx.strokeStyle='rgba(0,0,0,0.15)';ctx.lineWidth=.4;ctx.strokeRect(x*cell,y*cell,cell,cell);}}
    if(showN&&cell>=10){{
      const lum=parseInt(ci.hex.slice(1,3),16)*.299+parseInt(ci.hex.slice(3,5),16)*.587+parseInt(ci.hex.slice(5,7),16)*.114;
      ctx.fillStyle=lum<128?'#fff':'#000';
      ctx.font=`${{Math.max(5,Math.floor(cell/3))}}px Arial`;
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(code.replace(/\\D/g,''),x*cell+cell/2,y*cell+cell/2);
    }}
  }}
  ctx.strokeStyle='#888';ctx.lineWidth=.9;
  for(let i=0;i<=COLS;i+=10){{ctx.beginPath();ctx.moveTo(i*cell,0);ctx.lineTo(i*cell,ROWS*cell);ctx.stroke();}}
  for(let i=0;i<=ROWS;i+=10){{ctx.beginPath();ctx.moveTo(0,i*cell);ctx.lineTo(COLS*cell,i*cell);ctx.stroke();}}
  ctx.strokeStyle='#333';ctx.lineWidth=1.8;ctx.strokeRect(0,0,COLS*cell,ROWS*cell);
}}
function buildList(){{
  document.getElementById('cl').innerHTML=COLORS.map(c=>`
    <div class="ci" id="ci_${{c.code}}" onclick="toggleHL('${{c.code}}')">
      <div class="sw" style="background:${{c.hex}}"></div>
      <div class="cc">${{c.code}}</div><div class="cn">${{c.name}}</div>
      <div class="cnt">${{c.count.toLocaleString()}}</div>
    </div>`).join('');
}}
function toggleHL(code){{
  hl=(hl===code)?null:code;
  document.querySelectorAll('.ci').forEach(e=>e.classList.remove('active'));
  if(hl)document.getElementById('ci_'+code)?.classList.add('active');
  draw();
}}
canvas.addEventListener('mousemove',e=>{{
  const r=canvas.getBoundingClientRect(),x=Math.floor((e.clientX-r.left)/cell),y=Math.floor((e.clientY-r.top)/cell);
  if(x>=0&&x<COLS&&y>=0&&y<ROWS){{
    const code=CELLS[y][x],ci=COLORS.find(c=>c.code===code);
    tip.style.display='block';tip.style.left=(e.clientX+14)+'px';tip.style.top=(e.clientY-10)+'px';
    tip.innerHTML=`<b>${{code}}</b> ${{ci.name}}<br>(${{x+1}},${{y+1}}) · ${{ci.count}} beads`;
  }}
}});
canvas.addEventListener('mouseleave',()=>tip.style.display='none');
document.getElementById('sz').addEventListener('input',e=>{{cell=+e.target.value;document.getElementById('szv').textContent=cell+'px';draw();}});
document.getElementById('nums').addEventListener('change',e=>{{showN=e.target.checked;draw();}});
document.getElementById('grid').addEventListener('change',e=>{{showG=e.target.checked;draw();}});
function dlSVG(){{
  const fs=Math.max(5,Math.floor(cell/3));
  let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${{COLS*cell}}" height="${{ROWS*cell}}" viewBox="0 0 ${{COLS*cell}} ${{ROWS*cell}}">`;
  s+=`<style>text{{font-family:Arial;font-size:${{fs}}px;}}</style>`;
  s+=`<rect width="${{COLS*cell}}" height="${{ROWS*cell}}" fill="{bg_hex}"/>`;
  for(let y=0;y<ROWS;y++)for(let x=0;x<COLS;x++){{
    const code=CELLS[y][x],ci=COLORS.find(c=>c.code===code);
    const lum=parseInt(ci.hex.slice(1,3),16)*.299+parseInt(ci.hex.slice(3,5),16)*.587+parseInt(ci.hex.slice(5,7),16)*.114;
    const tc=lum<128?'#fff':'#000',px=x*cell,py=y*cell;
    s+=`<rect x="${{px}}" y="${{py}}" width="${{cell}}" height="${{cell}}" fill="${{ci.hex}}" stroke="rgba(0,0,0,0.15)" stroke-width="0.4"/>`;
    if(cell>=10){{const num=code.replace(/\\D/g,'');s+=`<text x="${{px+cell/2}}" y="${{py+cell/2}}" fill="${{tc}}" text-anchor="middle" dominant-baseline="central">${{num}}</text>`;}}
  }}
  for(let i=0;i<=COLS;i+=10)s+=`<line x1="${{i*cell}}" y1="0" x2="${{i*cell}}" y2="${{ROWS*cell}}" stroke="#888" stroke-width="0.8"/>`;
  for(let i=0;i<=ROWS;i+=10)s+=`<line x1="0" y1="${{i*cell}}" x2="${{COLS*cell}}" y2="${{i*cell}}" stroke="#888" stroke-width="0.8"/>`;
  s+=`<rect x="0" y="0" width="${{COLS*cell}}" height="${{ROWS*cell}}" fill="none" stroke="#333" stroke-width="1.8"/>`;
  s+='</svg>';
  const a=document.createElement('a');a.href='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(s);a.download='perler.svg';a.click();
}}
function dlPNG(){{const a=document.createElement('a');a.href=canvas.toDataURL('image/png');a.download='perler.png';a.click();}}
draw();buildList();
</script></body></html>"""

# ── Bead list text ────────────────────────────────────────
def gen_bead_list(usage,palette_name,gw,gh):
    total=sum(v["count"] for v in usage.values())
    lines=[f"Perler Bead List · 用豆清单",f"Palette: {palette_name.upper()}  Grid: {gw}×{gh}  Colors: {len(usage)}",
           "="*62,f"{'Code':<8}{'Name':<28}{'Count':>6}   {'Hex'}","-"*62]
    for code,v in sorted(usage.items(),key=lambda x:-x[1]["count"]):
        r,g,b=v["rgb"]
        lines.append(f"{code:<8}{v['name']:<28}{v['count']:>4} pcs  #{r:02x}{g:02x}{b:02x}")
    lines+=["="*62,f"{'Total / 合计':<36}{total:>4} pcs"]
    return '\n'.join(lines)

# ── MAIN ──────────────────────────────────────────────────
print("🧩 Perler Pattern Generator v1.2 starting...")

if not Path(IMAGE_PATH).exists() and not IMAGE_PATH.startswith("http"):
    print(f"❌ Not found: {IMAGE_PATH}"); sys.exit(1)

print("📷 Loading image...")
img_rgb = load_image(IMAGE_PATH)
print(f"   Size: {img_rgb.shape[1]}×{img_rgb.shape[0]}")

print("✂️  Removing background (GrabCut, fully offline)...")
img_nobg = remove_background(img_rgb, BG_COLOR)
print("   Done")

print(f"📐 Resizing to {GRID_W}×{GRID_H}...")
img_small = resize_crop(img_nobg, GRID_W, GRID_H)

print("🌈 Equalizing brightness (Lab color space)...")
img_eq = lab_equalize(img_small)

print("🔪 Sharpening edges...")
img_pil = Image.fromarray(img_eq)
img_pil = img_pil.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=2))
img_pil = ImageEnhance.Contrast(img_pil).enhance(1.25)
img_arr = np.array(img_pil)

print(f"🎨 Quantizing → {PALETTE_NAME} palette ({MAX_COLORS} colors)...")
img_q = img_pil.quantize(colors=MAX_COLORS, method=Image.Quantize.MEDIANCUT, dither=0).convert("RGB")
palette = PALETTES.get(PALETTE_NAME, PALETTES["hama"])
lab_pal = build_lab_pal(palette)
grid, grid_rgb, usage = map_to_palette(np.array(img_q), lab_pal, MAX_COLORS)
print(f"   Actual colors used: {len(usage)}")

print("💾 Generating output files...")

svg = gen_svg(grid, usage, cell=16)
p = os.path.join(OUTPUT_DIR, "pattern.svg")
open(p,"w",encoding="utf-8").write(svg); print(f"   ✅ SVG: {p}")

html = gen_html(grid, usage, PALETTE_NAME, BG_COLOR)
p = os.path.join(OUTPUT_DIR, "pattern.html")
open(p,"w",encoding="utf-8").write(html); print(f"   ✅ HTML: {p}")

bead_canvas = gen_bead_preview(grid_rgb, BG_COLOR, cell=20)
p = os.path.join(OUTPUT_DIR, "preview_beads.png")
bead_canvas.save(p); print(f"   ✅ Bead preview: {p}")

flat = Image.fromarray(grid_rgb).resize((GRID_W*16, GRID_H*16), Image.NEAREST)
p = os.path.join(OUTPUT_DIR, "preview_flat.png")
flat.save(p); print(f"   ✅ Flat preview: {p}")

blist = gen_bead_list(usage, PALETTE_NAME, GRID_W, GRID_H)
p = os.path.join(OUTPUT_DIR, "bead_list.txt")
open(p,"w",encoding="utf-8").write(blist); print(f"   ✅ Bead list: {p}")

total=sum(v["count"] for v in usage.values())
print(f"""
╔════════════════════════════════════════╗
║  🧩 Pattern Ready! · 拼豆图纸生成完成  ║
╠════════════════════════════════════════╣
║  Grid  : {GRID_W}×{GRID_H}  Colors: {len(usage)}  Beads: {total:,}
║  Palette: {PALETTE_NAME.upper()}
╠════════════════════════════════════════╣
║  pattern.html      ← 浏览器查看/打印
║  pattern.svg       ← 可打印矢量图纸
║  preview_beads.png ← 3D豆子效果预览
║  preview_flat.png  ← 平铺效果预览
║  bead_list.txt     ← 购买清单
╚════════════════════════════════════════╝
Output: {OUTPUT_DIR}
""")
print(blist)
```

---

## Step 3: Conversation / 多轮对话

```
"background messy / 背景去除不干净" → ask user to pre-crop or use phone app to remove bg first
"more colors / 颜色太少"             → increase MAX_COLORS (+5), re-run
"fewer colors / 颜色太多"            → decrease MAX_COLORS (-5), re-run
"change to black bg / 换黑色背景"    → BG_COLOR=(5,5,5), re-run
"white background / 白色背景"        → BG_COLOR=(255,255,255), re-run
"switch palette / 换色板"            → change PALETTE_NAME, re-run
"how many beads / 需要多少豆"        → show bead_list.txt
```

---

## Tips / 使用建议

**Best images 最佳图片类型:**
- ✅ Pets / animals on simple background · 简单背景的宠物
- ✅ Cartoon / anime characters · 卡通角色
- ✅ Logos, icons · Logo图标
- ✅ Pre-removed background (PNG with transparency) · 已去背景的PNG

**If GrabCut result is poor / 如果去背景效果不好:**
- Use phone app first: iOS "Remove Background" / Android "Background Eraser"
- 先用手机App去背景，效果会更好
- Or crop image to focus on subject only · 先裁剪让主体占满画面

**Color count guide / 颜色数建议:**
- 15: Simple, easy to assemble · 简单，容易拼
- 25: Standard, good detail · 标准，细节好（默认）
- 32: Detailed, complex · 精细，适合大尺寸
