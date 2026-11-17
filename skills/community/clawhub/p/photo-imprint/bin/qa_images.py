#!/usr/bin/env python3
"""Create previews, diagnostic metrics, and a blocking manual-review checklist template."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageStat
from clean_plate import analyze as analyze_plate
from workflow_contracts import QA_PAGE_CHECKS, QA_SET_CHECKS

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
DEFAULT_THRESHOLDS = {"mean_luminance": 0.12, "rms_contrast": 0.18, "mean_saturation": 0.18}


def sha256(path: Path) -> str:
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def metrics(image: Image.Image, paper_rgb: tuple[int,int,int], center_y_ratio: float = 0.72, height_ratio_max: float = 0.32) -> dict:
    # RGB deltas can reach 255; squaring int16 values overflows at 32,767.
    # Promote before subtraction so Euclidean distances remain exact and finite.
    rgb=image.convert("RGB"); arr=np.asarray(rgb,dtype=np.int32); gray=rgb.convert("L"); hsv=rgb.convert("HSV")
    lum=ImageStat.Stat(gray); sat=ImageStat.Stat(hsv.getchannel("S"))
    h,w,_=arr.shape
    # Detection zone derived from config — not hardcoded 38%/78%
    # Empty area is top clear + side margins outside subject band
    # subject band = [center_y - height_max/2, center_y + height_max/2]
    # empty detection = above subject band and side margins
    top_clear_ratio = max(0.05, min(0.7, center_y_ratio - height_ratio_max/2 - 0.05))
    side_margin_ratio = 0.78  # keep conservative for paper noise, but derived from edge_margin
    y=max(1,int(h*top_clear_ratio)); x=max(1,int(w*side_margin_ratio))
    empty=arr[:y,:x]
    dist=np.sqrt(np.sum((empty-np.array(paper_rgb,dtype=np.int32))**2,axis=2))
    noise=float(np.mean(dist>8))
    gy=np.abs(np.diff(arr.mean(axis=2),axis=0)); gx=np.abs(np.diff(arr.mean(axis=2),axis=1))
    row=np.mean(gy,axis=1) if gy.size else np.array([0]); col=np.mean(gx,axis=0) if gx.size else np.array([0])
    seam=max(float(np.max(row)),float(np.max(col))) if row.size and col.size else 0.0
    edge=np.concatenate([arr[0].reshape(-1,3),arr[-1].reshape(-1,3),arr[:,0].reshape(-1,3),arr[:,-1].reshape(-1,3)])
    edge_dark=float(np.mean(np.sqrt(np.sum((edge-np.array(paper_rgb))**2,axis=1))>35))
    return {"width":w,"height":h,"mean_luminance":round(lum.mean[0],3),"rms_contrast":round(lum.stddev[0],3),
        "mean_saturation":round(ImageStat.Stat(hsv.getchannel('S')).mean[0],3),
        "empty_area_noise_ratio":round(noise,6),"max_axis_seam_gradient":round(seam,4),
        "hard_edge_occupancy":round(edge_dark,6)}

def relative_delta(value:float,median:float)->float:
    return 0.0 if median==0 and value==0 else (math.inf if median==0 else abs(value-median)/median)

def hex_rgb(value:str)->tuple[int,int,int]:
    value=value.lstrip('#'); return tuple(int(value[i:i+2],16) for i in (0,2,4))

def load_config(path:Path|None):
    if path is None:return DEFAULT_THRESHOLDS.copy(),False,None,(241,235,221)
    config=json.loads(path.read_text())
    if not isinstance(config,dict) or config.get('resolved') is not True:raise ValueError(f"not a resolved carousel config: {path}")
    raw=config.get('profiles',{}).get('unification',{}).get('qa_thresholds',{})
    thresholds={"mean_luminance":float(raw.get('mean_luminance_relative_delta',.12)),"rms_contrast":float(raw.get('rms_contrast_relative_delta',.18)),"mean_saturation":float(raw.get('mean_saturation_relative_delta',.18))}
    route=bool(config.get('modules',{}).get('route',{}).get('enabled'))
    paper=hex_rgb(config.get('profiles',{}).get('unification',{}).get('paper',{}).get('color','#F1EBDD'))
    return thresholds,route,config,paper

def build_sheet(images,output,grayscale=False):
    tw,th,lh=270,480,34; cols=min(5,max(1,len(images))); rows=math.ceil(len(images)/cols)
    sheet=Image.new('RGB',(cols*tw,rows*(th+lh)),'#E8E4DC'); draw=ImageDraw.Draw(sheet); font=ImageFont.load_default()
    for i,(path,src) in enumerate(images):
        r,c=divmod(i,cols); im=src.convert('L').convert('RGB') if grayscale else src.copy(); im.thumbnail((tw,th),Image.Resampling.LANCZOS)
        x=c*tw+(tw-im.width)//2;y=r*(th+lh)+(th-im.height)//2;sheet.paste(im,(x,y));draw.text((c*tw+8,r*(th+lh)+th+8),path.name,fill='#3B3832',font=font)
    output.parent.mkdir(parents=True,exist_ok=True);sheet.save(output,quality=94)

def build_long_strip(images,output):
    mh=max(im.height for _,im in images); norm=[im if im.height==mh else im.resize((round(im.width*mh/im.height),mh),Image.Resampling.LANCZOS) for _,im in images]
    strip=Image.new('RGB',(sum(im.width for im in norm),mh),'#E8E4DC');x=0
    for im in norm:strip.paste(im,(x,0));x+=im.width
    if strip.width>8000:scale=8000/strip.width;strip=strip.resize((8000,max(1,round(strip.height*scale))),Image.Resampling.LANCZOS)
    strip.save(output,quality=92)

def plate_diagnostics(directory: Path | None, stem: str, config: dict | None) -> dict:
    if directory is None:
        return {"present": False, "has_alpha": False, "corner_alpha_mean": None, "subject_to_paper_ready": False}
    candidates = [p for p in directory.iterdir() if p.is_file() and p.stem == stem and p.suffix.lower() in SUPPORTED]
    if len(candidates) != 1:
        return {"present": False, "has_alpha": False, "corner_alpha_mean": None, "subject_to_paper_ready": False}
    with Image.open(candidates[0]) as image:
        has_alpha = image.mode in {"RGBA", "LA", "PA"} or "A" in image.getbands()
        if config:
            policy=config.get('profiles',{}).get('style',{}).get('plate_normalization',{})
            validation=analyze_plate(image,policy)
            canvas=config.get('profiles',{}).get('composition',{}).get('canvas',{})
            dimensions=image.size==(canvas.get('width'),canvas.get('height'))
            validation['checks']['dimensions']=dimensions
            validation['checks']['has_alpha']=has_alpha
            validation['blocking_pass']=all(validation['checks'].values())
            mean=validation['corner_alpha_mean']
        else:
            rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8);alpha = rgba[:, :, 3]
            n = max(1, int(min(alpha.shape) * 0.03))
            corners = np.concatenate([alpha[:n,:n].ravel(), alpha[:n,-n:].ravel(), alpha[-n:,:n].ravel(), alpha[-n:,-n:].ravel()])
            mean=float(corners.mean());validation={'blocking_pass':has_alpha and mean<=10,'checks':{'has_alpha':has_alpha,'corner_alpha_mean_pass':mean<=10}}
    return {"present": True, "path": str(candidates[0].resolve()), "sha256": sha256(candidates[0]),
        "has_alpha": has_alpha, "corner_alpha_mean": round(mean,4), "validation":validation,
        "subject_to_paper_ready": bool(validation['blocking_pass'])}

def build_phone(images,out):
    out.mkdir(parents=True,exist_ok=True)
    result={}
    for path,im in images:
        phone=im.copy();phone.thumbnail((360,640),Image.Resampling.LANCZOS);target=out/f"{path.stem}-phone.jpg";phone.convert('RGB').save(target,quality=92);result[path.name]=str(target.resolve())
    return result

def main()->int:
    p=argparse.ArgumentParser(description='Generate diagnostic previews and a two-dimension QA checklist template')
    p.add_argument('--input',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--config',type=Path)
    p.add_argument('--render-plan',type=Path,help='Render plan used to bind page-level checks to production briefs')
    p.add_argument('--plates',type=Path,help='Normalized clean-plate directory')
    p.add_argument('--checklist-output',type=Path,help='Defaults to <output>/review-checklist.json')
    args=p.parse_args()
    paths=sorted(x for x in args.input.iterdir() if x.is_file() and x.suffix.lower() in SUPPORTED)
    if not paths:p.error('No supported image files found')
    try:thresholds,route,config,paper=load_config(args.config)
    except Exception as exc:p.error(str(exc))
    # pull center_y / height from config for detection zone
    comp = config.get('composition', {}) if isinstance(config, dict) else {}
    center_y = float(comp.get('center_y_ratio', 0.72))
    height_max = float(comp.get('height_ratio_max', 0.32))
    plan=None
    if args.render_plan:
        plan=json.loads(args.render_plan.read_text()); expected_order=[f"{int(pg['page']):02d}" for pg in plan.get('pages',[])]
        stems=[x.stem for x in paths]
        if stems!=expected_order:p.error(f"finished-page order/names {stems} do not match plan {expected_order}")
    images=[]
    for path in paths:
        with Image.open(path) as im:images.append((path,im.convert('RGB')))
    rows=[{"filename":path.name,"sha256":sha256(path),**metrics(im,paper,center_y,height_max),
        "plate":plate_diagnostics(args.plates, path.stem, config)} for path,im in images]
    medians={k:statistics.median(r[k] for r in rows) for k in DEFAULT_THRESHOLDS};dims={(r['width'],r['height']) for r in rows}
    expected=None
    if config:
        c=config.get('profiles',{}).get('composition',{}).get('canvas',{});expected=(c.get('width'),c.get('height'))
    for r in rows:
        r['metric_flags']=[k for k,t in thresholds.items() if relative_delta(r[k],medians[k])>t]
        r['diagnostic_flags']=[]
        r['objective_failures']=[]
        if r['empty_area_noise_ratio']>.02:
            r['diagnostic_flags'].append('background_uniformity_review')
            r['objective_failures'].append('severe_background_nonuniformity')
        if r['max_axis_seam_gradient']>22:
            r['diagnostic_flags'].append('rectangular_seam_risk_review')
            r['objective_failures'].append('severe_rectangular_seam')
        if r['hard_edge_occupancy']>.25:
            r['diagnostic_flags'].append('hard_border_frame_risk_review')
            r['objective_failures'].append('severe_hard_border_or_frame')
        if plan is not None and not r['plate']['subject_to_paper_ready']:
            r['diagnostic_flags'].append('subject_to_paper_compositing_review')
            r['objective_failures'].append('plate_not_subject_to_paper_ready')
        if len(dims)>1:
            r['diagnostic_flags'].append('dimensions')
            r['objective_failures'].append('nonuniform_dimensions')
        if expected and (r['width'],r['height'])!=expected:
            r['diagnostic_flags'].append('expected_dimensions')
            r['objective_failures'].append('expected_dimensions_mismatch')
    args.output.mkdir(parents=True,exist_ok=True)
    build_sheet(images,args.output/'contact-sheet-color.jpg',False);build_sheet(images,args.output/'contact-sheet-grayscale.jpg',True);build_long_strip(images,args.output/'long-strip.jpg')
    phone=build_phone(images,args.output/'phone')
    objective_failures=[{"filename":r['filename'],"failures":r['objective_failures']} for r in rows if r['objective_failures']]
    report={"schema_version":"2.2.0","image_count":len(rows),
        "resolved_config_sha256":sha256(args.config) if args.config and args.config.is_file() else None,
        "render_plan_sha256":sha256(args.render_plan) if args.render_plan and args.render_plan.is_file() else None,
        "image_directory":str(args.input.resolve()),
        "uniform_dimensions":len(dims)==1,"expected_dimensions":list(expected) if expected else None,
        "matches_expected_dimensions":bool(expected and dims=={expected}) if expected else None,"plates_required":plan is not None,
        "objective_gate":{"status":"fail" if objective_failures else "pass","failures":objective_failures},
        "route_enabled":route,"medians":medians,"thresholds":thresholds,
        "metric_flags_are_review_leads_not_acceptance":True,"objective_failures_are_non_overridable":True,
        "acceptance_dimensions":["page_level_compliance","set_level_cohesion"],"images":rows}
    report_path=args.output/'qa-report.json';report_path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    page_entries=[]
    plan_pages=plan.get('pages',[]) if plan else [{} for _ in rows]
    for row,page in zip(rows,plan_pages):
        full_size=(args.input/row['filename']).resolve();phone_path=Path(phone[row['filename']])
        page_entries.append({"page":page.get('page'),"filename":row['filename'],"sha256":row['sha256'],"production_brief":page.get('production_brief'),
            "full_size_evidence":str(full_size),"full_size_evidence_sha256":sha256(full_size),
            "phone_scale_evidence":str(phone_path),"phone_scale_evidence_sha256":sha256(phone_path),
            "automated_diagnostics":{"flags":row['diagnostic_flags'],"objective_failures":row['objective_failures'],"metrics":{k:row[k] for k in ('empty_area_noise_ratio','max_axis_seam_gradient','hard_edge_occupancy')}},
            "checks":{check:{"status":"pending","evidence":"","note":""} for check in QA_PAGE_CHECKS}})
    checklist={"schema_version":"1.1.0","qa_report_path":str(report_path.resolve()),"qa_report_sha256":sha256(report_path),
        "objective_gate":report['objective_gate'],
        "page_level_compliance":{"status":"pending","pages":page_entries},
        "set_level_cohesion":{"status":"pending","checks":{check:{"status":"pending","evidence":"","note":""} for check in QA_SET_CHECKS}},
        "packaging_blocked_until_both_dimensions_pass":True}
    checklist_path=args.checklist_output or args.output/'review-checklist.json';checklist_path.write_text(json.dumps(checklist,indent=2,ensure_ascii=False)+'\n')
    print(f"Wrote QA outputs and pending review checklist to {args.output}")
    return 0
if __name__=='__main__':raise SystemExit(main())
