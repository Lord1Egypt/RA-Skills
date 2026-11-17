#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

def digits_only(text: str) -> str:
    return ''.join(re.findall(r'\d', text or ''))

def parse_bbox(raw: str):
    vals=[float(x) for x in raw.split(',')]
    if len(vals)!=4 or any(v<0 or v>1 for v in vals): raise ValueError('bbox must be x1,y1,x2,y2 in 0..1')
    x1,y1,x2,y2=vals
    if x2<=x1 or y2<=y1: raise ValueError('invalid bbox')
    return vals

def _tesseract(img: Image.Image, psm: int) -> str:
    with tempfile.NamedTemporaryFile(suffix='.png') as f:
        img.save(f.name)
        cp=subprocess.run(['tesseract',f.name,'stdout','--psm',str(psm),'-l','eng','-c','tessedit_char_whitelist=0123456789'],
                          text=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=20,check=False)
    return digits_only(cp.stdout)

def _variants(crop: Image.Image):
    gray=ImageOps.autocontrast(crop.convert('L')).resize((crop.width*5,crop.height*5),Image.Resampling.LANCZOS)
    yield gray
    yield ImageEnhance.Contrast(gray).enhance(2.2)
    for threshold in (105,130,155,180,205):
        yield gray.point(lambda p,t=threshold: 255 if p>t else 0)

def ocr_display(image_path: str|Path, bbox, expected_digits: int|None=None) -> dict:
    with Image.open(image_path) as src:
        img=ImageOps.exif_transpose(src).convert('RGB')
    x1,y1,x2,y2=bbox; w,h=img.size
    crop=img.crop((int(x1*w),int(y1*h),int(x2*w),int(y2*h)))
    candidates=[]
    for variant in _variants(crop):
        for psm in (7,6,13):
            value=_tesseract(variant,psm)
            if value and value not in candidates: candidates.append(value)
    if expected_digits:
        for variant in _variants(crop):
            cell_w=variant.width/expected_digits; chars=[]; ok=True
            for i in range(expected_digits):
                a=max(0,int((i+0.05)*cell_w)); b=min(variant.width,int((i+0.95)*cell_w))
                cell=variant.crop((a,0,b,variant.height))
                val=_tesseract(cell,10)
                if len(val)!=1: ok=False; break
                chars.append(val)
            if ok:
                value=''.join(chars)
                if value not in candidates: candidates.append(value)
    return {'ok':bool(candidates),'provider_contacted':False,'candidates':candidates,'bbox':bbox}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('image'); ap.add_argument('--bbox',required=True); ap.add_argument('--expected-digits',type=int)
    args=ap.parse_args(); result=ocr_display(args.image,parse_bbox(args.bbox),args.expected_digits)
    print(json.dumps(result,ensure_ascii=False,separators=(',',':')))
if __name__=='__main__': main()
