#!/usr/bin/env python3
"""Lock staged outputs, package only verified files, and verify release ZIP integrity."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from PIL import Image
from workflow_contracts import (
    digest, load_object, validate_approval_state,
    validate_current_sources_and_captions, write_object,
)
from review_checklist import validate as validate_checklist
from review_gate import verify_receipt_scope, verify_sample
from renderer_receipt import load as load_renderer_receipt, validate as validate_renderer_receipt

IMAGE_RE=re.compile(r'^(\d+)\.(png|webp|jpg|jpeg)$',re.I)
XMP_INFO_KEYS={"xmp","xml:com.adobe.xmp","raw profile type xmp"}


def forbidden_metadata(image: Image.Image) -> list[str]:
    issues=[]
    try:
        if len(image.getexif()):
            issues.append('EXIF/GPS')
    except Exception:
        # An undecodable EXIF block is still metadata and must not pass silently.
        if image.info.get('exif'):
            issues.append('EXIF/GPS')
    if image.info.get('exif') and 'EXIF/GPS' not in issues:
        issues.append('EXIF/GPS')
    if any(str(key).lower() in XMP_INFO_KEYS or 'xmp' in str(key).lower() for key in image.info):
        issues.append('XMP')
    if any('gps' in str(key).lower() for key in image.info):
        issues.append('GPS')
    return issues


def inspect_release_image(path: Path) -> tuple[int,int]:
    with Image.open(path) as image:
        size=image.size
        issues=forbidden_metadata(image)
        if issues:
            raise ValueError(f"forbidden image metadata in {path.name}: {', '.join(sorted(set(issues)))}")
    # Reopen so lazy metadata reads cannot invalidate Pillow's verify() stream position.
    with Image.open(path) as image:
        image.verify()
    return size


def stage(args)->int:
    candidates=[p for p in args.input.iterdir() if IMAGE_RE.match(p.name)]
    if any(p.is_symlink() for p in candidates):raise ValueError('staging directory contains a symlinked image')
    files=sorted(p for p in candidates if p.is_file())
    if not files:raise ValueError('staging directory has no numbered image files')
    entries=[]
    for p in files:
        w,h=inspect_release_image(p)
        entries.append({'page':int(IMAGE_RE.match(p.name).group(1)),'filename':p.name,'sha256':digest(p),'bytes':p.stat().st_size,'width':w,'height':h})
    pages=[x['page'] for x in entries]
    if pages!=list(range(1,len(pages)+1)):raise ValueError(f'numbered pages must be contiguous from 1: {pages}')
    write_object(args.output,{'schema_version':'1.1.0','staging_directory':str(args.input.resolve()),
        'metadata_policy':{'exif_gps_xmp':'forbidden','verified':True},'files':entries})
    print(f'Locked {len(entries)} staged images in {args.output}');return 0

def verify_stage(directory:Path,manifest:dict)->list[Path]:
    paths=[];expected={x['filename'] for x in manifest.get('files',[])}
    actual={p.name for p in directory.iterdir() if p.is_file() and IMAGE_RE.match(p.name)}
    if actual!=expected:raise ValueError(f'staged files differ from manifest: expected {sorted(expected)}, got {sorted(actual)}')
    for entry in manifest['files']:
        p=directory/entry['filename']
        if p.is_symlink():raise ValueError(f'staged file became a symlink: {p.name}')
        if digest(p)!=entry['sha256']:raise ValueError(f'staged file changed: {p.name}')
        if p.stat().st_size!=entry.get('bytes'):raise ValueError(f'byte size changed: {p.name}')
        size=inspect_release_image(p)
        if list(size)!=[entry['width'],entry['height']]:raise ValueError(f'dimensions changed: {p.name}')
        paths.append(p)
    return paths

def validate_composition_manifest(path: Path, state: dict, plan: dict, staged: list[Path]) -> dict:
    composition=load_object(path,'composition manifest')
    if composition.get('schema_version')!='1.1.0' or composition.get('deterministic') is not True:
        raise ValueError('composition manifest schema/deterministic contract is invalid')
    if composition.get('render_plan_sha256')!=state.get('render_plan_sha256'):
        raise ValueError('composition manifest does not match the approved render plan')
    config_lock=plan.get('resolved_config_lock',{})
    if composition.get('config_sha256')!=config_lock.get('sha256'):
        raise ValueError('composition manifest does not match the approved resolved config')
    if composition.get('metadata_policy')!={'exif_gps_xmp':'forbidden','verified':True}:
        raise ValueError('composition manifest metadata policy is missing or invalid')
    font=composition.get('font')
    modules=plan.get('modules',{})
    typography_required=any(isinstance(modules.get(name),dict) and modules[name].get('enabled')
        for name in ('caption','watermark'))
    if typography_required and not isinstance(font,dict):
        raise ValueError('composition manifest font evidence is required by enabled typography')
    if isinstance(font,dict):
        font_path=Path(str(font.get('path','')))
        if not font_path.is_file() or digest(font_path)!=font.get('sha256'):
            raise ValueError('composition font changed or is missing')
    renderer=composition.get('renderer_receipt')
    if not isinstance(renderer,dict):
        raise ValueError('composition manifest renderer receipt is missing')
    renderer_path=Path(str(renderer.get('path','')))
    if not renderer_path.is_file() or digest(renderer_path)!=renderer.get('sha256'):
        raise ValueError('composition renderer receipt changed or is missing')
    receipt=load_renderer_receipt(renderer_path)
    receipt_errors=validate_renderer_receipt(receipt,check_files=True,require_rendered_output=True)
    if receipt_errors:
        raise ValueError('composition renderer receipt is invalid: '+'; '.join(receipt_errors))
    receipt_outputs={(str(Path(str(entry.get('path',''))).resolve()),entry.get('sha256'))
        for entry in receipt.get('rendered_outputs',[]) if isinstance(entry,dict)}
    receipt_sources={(str(Path(str(entry.get('path',''))).resolve()),entry.get('sha256'))
        for entry in receipt.get('sources',[]) if isinstance(entry,dict)}
    expected_sources={(str(Path(str(page.get('source_path',''))).resolve()),page.get('source_sha256'))
        for page in plan.get('pages',[]) if isinstance(page,dict)}
    if receipt_sources!=expected_sources:
        raise ValueError('composition renderer receipt sources do not exactly match the approved page sources')
    receipt_references={(str(Path(str(entry.get('path',''))).resolve()),entry.get('sha256'))
        for entry in receipt.get('references',[]) if isinstance(entry,dict)}
    expected_references={(str(Path(str(entry.get('image_path',''))).resolve()),entry.get('image_sha256'))
        for entry in plan.get('style_reference_locks',[]) if isinstance(entry,dict)}
    if receipt_references!=expected_references:
        raise ValueError('composition renderer receipt references do not exactly match the approved style references')
    plates=composition.get('plates')
    if not isinstance(plates,list) or not plates:
        raise ValueError('composition manifest has no plate evidence')
    plate_pages=[]
    expected_plate_outputs=set()
    for entry in plates:
        if not isinstance(entry,dict):
            raise ValueError('composition plate evidence entry is invalid')
        plate=Path(str(entry.get('path','')))
        evidence=(str(plate.resolve()),entry.get('sha256'))
        if not plate.is_file() or digest(plate)!=entry.get('sha256'):
            raise ValueError(f"composition plate {entry.get('page')} changed or is missing")
        expected_plate_outputs.add(evidence)
        plate_pages.append(entry.get('page'))
    if receipt_outputs != expected_plate_outputs:
        raise ValueError('composition renderer receipt outputs do not exactly match the normalized plate set')
    outputs=composition.get('outputs')
    if not isinstance(outputs,list):
        raise ValueError('composition manifest outputs are missing')
    composed={(entry.get('page'),Path(str(entry.get('path',''))).name,entry.get('sha256'))
        for entry in outputs if isinstance(entry,dict)}
    staged_set={(int(IMAGE_RE.match(item.name).group(1)),item.name,digest(item)) for item in staged}
    if composed!=staged_set:
        raise ValueError('composition outputs do not exactly match staged page bytes')
    if sorted(plate_pages)!=sorted(page for page,_,_ in staged_set):
        raise ValueError('composition plate pages do not match staged page set')
    return composition


def package(args)->int:
    stage_manifest=load_object(args.staging_manifest,'staging manifest')
    if stage_manifest.get('schema_version')!='1.1.0' or stage_manifest.get('metadata_policy')!={'exif_gps_xmp':'forbidden','verified':True}:
        raise ValueError('staging manifest lacks the required metadata-free verification policy')
    if Path(str(stage_manifest.get('staging_directory',''))).resolve()!=args.input.resolve():
        raise ValueError('staging manifest belongs to a different staging directory')
    paths=verify_stage(args.input,stage_manifest)
    checklist=load_object(args.review_checklist,'review checklist')
    checklist_errors = validate_checklist(checklist)
    if checklist_errors:
        raise ValueError('review checklist is incomplete: ' + '; '.join(checklist_errors))
    if checklist.get('page_level_compliance',{}).get('status')!='pass':raise ValueError('page-level compliance is not complete/pass')
    if checklist.get('set_level_cohesion',{}).get('status')!='pass':raise ValueError('set-level cohesion is not complete/pass')
    qpath=Path(str(checklist.get('qa_report_path','')))
    if not qpath.is_file() or digest(qpath)!=checklist.get('qa_report_sha256'):raise ValueError('QA report is missing or changed')
    qa_report=load_object(qpath,'QA report')
    stage_files=[(e.get('filename'),e.get('sha256')) for e in stage_manifest.get('files',[])]
    reviewed_pages=checklist.get('page_level_compliance',{}).get('pages',[])
    reviewed_files=[(e.get('filename'),e.get('sha256')) for e in reviewed_pages if isinstance(e,dict)]
    qa_files=[(e.get('filename'),e.get('sha256')) for e in qa_report.get('images',[]) if isinstance(e,dict)]
    if reviewed_files!=stage_files or qa_files!=stage_files:
        raise ValueError('QA-reviewed final page hashes do not match the exact staging manifest')
    evidence=[]
    for page in reviewed_pages:
        for key in ('full_size_evidence','phone_scale_evidence'):
            path=Path(str(page.get(key,'')));expected=page.get(f'{key}_sha256')
            if not path.is_file() or not isinstance(expected,str) or digest(path)!=expected:
                raise ValueError(f"review evidence changed or is missing for {page.get('filename')}: {key}")
            evidence.append({'page':page.get('page'),'kind':key,'filename':path.name,'sha256':expected})
    state=load_object(args.state,'approval state')
    state_errors=validate_approval_state(state)
    if state_errors:
        raise ValueError('approval state schema is incomplete: '+'; '.join(state_errors))
    for stem in ('render_plan','production_plan','sample','sample_plate'):
        path_value, expected = state.get(f'{stem}_path'), state.get(f'{stem}_sha256')
        path = Path(str(path_value))
        if not path.is_file() or digest(path) != expected:
            raise ValueError(f'locked {stem} changed or is missing')
    renderer=state['renderer_record']
    renderer_path=Path(str(renderer.get('path','')))
    if not renderer_path.is_file() or digest(renderer_path)!=renderer.get('sha256'):
        raise ValueError('locked renderer record changed or is missing')
    renderer_receipt=load_renderer_receipt(renderer_path)
    receipt_errors=validate_renderer_receipt(renderer_receipt,check_files=True,require_rendered_output=True)
    if receipt_errors:
        raise ValueError('locked renderer record is invalid: '+'; '.join(receipt_errors))
    sample_plate=Path(state['sample_plate_path']).resolve()
    sample_plate_evidence=(str(sample_plate),state['sample_plate_sha256'])
    receipt_outputs={(str(Path(str(entry.get('path',''))).resolve()),entry.get('sha256'))
        for entry in renderer_receipt.get('rendered_outputs',[]) if isinstance(entry,dict)}
    if sample_plate_evidence not in receipt_outputs:
        raise ValueError('renderer receipt does not hash-lock the approved sample plate')
    verify_sample(state)
    if state.get('render_plan_path'):
        locked_plan = load_object(Path(state['render_plan_path']), 'locked render plan')
        verify_receipt_scope(renderer_receipt,locked_plan,state.get('sample_page'))
        plan_input_errors=validate_current_sources_and_captions(locked_plan)
        if plan_input_errors:
            raise ValueError('locked render plan inputs are stale or unconfirmed: '+'; '.join(plan_input_errors))
        contract=locked_plan.get('sample_style_contract')
        contract_hash=hashlib.sha256(json.dumps(contract,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        if contract_hash!=state.get('sample_style_contract_sha256'):
            raise ValueError('approval state sample style contract lock does not match the render plan')
        config_lock = locked_plan.get('resolved_config_lock')
        if not isinstance(config_lock, dict):
            raise ValueError('locked render plan has no resolved config lock')
        path = Path(str(config_lock.get('path', '')))
        if not path.is_file() or digest(path) != config_lock.get('sha256'):
            raise ValueError('locked resolved config changed or is missing')
        locked_config=load_object(path,'locked resolved config')
        for reference in locked_plan.get('style_reference_locks', []):
            for stem in ('image', 'source_metadata'):
                path = Path(str(reference.get(f'{stem}_path', '')))
                if not path.is_file() or digest(path) != reference.get(f'{stem}_sha256'):
                    raise ValueError(f"locked style reference {reference.get('id')} {stem} changed or is missing")
    planned_pages=[page.get('page') for page in locked_plan.get('pages',[]) if isinstance(page,dict)]
    if not planned_pages or state.get('sample_page')!=planned_pages[0]:
        raise ValueError('approval state sample page does not match the first approved plan page')
    if state.get('permitted_render_pages')!=planned_pages[1:] or state.get('blocked_render_pages')!=[]:
        raise ValueError('approval state authorization scope does not cover the approved batch pages')
    staged_pages=[entry.get('page') for entry in stage_manifest.get('files',[]) if isinstance(entry,dict)]
    if staged_pages!=planned_pages:
        raise ValueError(f'staged page set/order does not match approved plan: {staged_pages} != {planned_pages}')
    approved_sample=next((entry for entry in stage_manifest.get('files',[]) if entry.get('page')==state.get('sample_page')),None)
    if not isinstance(approved_sample,dict) or approved_sample.get('sha256')!=state.get('sample_sha256'):
        raise ValueError('staged sample page bytes do not match the explicitly approved sample')
    canvas=locked_config.get('profiles',{}).get('composition',{}).get('canvas',{})
    expected_dimensions=(canvas.get('width'),canvas.get('height'))
    if not all((entry.get('width'),entry.get('height'))==expected_dimensions for entry in stage_manifest.get('files',[])):
        raise ValueError(f'staged page dimensions do not match approved config: {expected_dimensions}')
    if qa_report.get('render_plan_sha256')!=state.get('render_plan_sha256'):
        raise ValueError('QA report was not generated from the approved render plan')
    if qa_report.get('resolved_config_sha256')!=locked_plan.get('resolved_config_lock',{}).get('sha256'):
        raise ValueError('QA report was not generated from the approved resolved config')
    if Path(str(qa_report.get('image_directory',''))).resolve()!=args.input.resolve():
        raise ValueError('QA report belongs to a different final-image directory')
    composition=validate_composition_manifest(args.composition_manifest,state,locked_plan,paths)
    revision=state.get('active_revision')
    if isinstance(revision,dict):
        baseline=revision.get('baseline_stage',{});stale=set(revision.get('stale_pages',[]))
        current={e['page']:e['sha256'] for e in stage_manifest['files']}
        for page,old_hash in baseline.items():
            page=int(page)
            if page not in stale and current.get(page)!=old_hash:raise ValueError(f'unchanged approved page {page} was modified')
            if page in stale and current.get(page)==old_hash:raise ValueError(f'stale revision page {page} was not replaced')
    release={'schema_version':'1.1.0','files':[{k:e[k] for k in ('page','filename','sha256','bytes','width','height')} for e in stage_manifest['files']],
        'verification':{'page_level_compliance':'pass','set_level_cohesion':'pass','objective_gate':'pass',
            'metadata_policy':'EXIF/GPS/XMP forbidden',
            'staging_manifest_sha256':digest(args.staging_manifest),
            'review_checklist_sha256':digest(args.review_checklist),
            'qa_report_sha256':checklist['qa_report_sha256'],
            'approval_state_sha256':digest(args.state),
            'composition_manifest_sha256':digest(args.composition_manifest),
            'composition_renderer_receipt_sha256':composition['renderer_receipt']['sha256'],
            'review_evidence':evidence}}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    manifest_bytes=(json.dumps(release,indent=2,ensure_ascii=False)+'\n').encode()
    with zipfile.ZipFile(args.output,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in paths:z.write(p,p.name)
        z.writestr('release-manifest.json',manifest_bytes)
    write_object(args.manifest_output,release)
    with zipfile.ZipFile(args.output) as z:
        bad=z.testzip()
        if bad:raise ValueError(f'ZIP integrity failed at {bad}')
    if state.get('status') == 'revision_in_progress':
        state['status'] = 'revision_completed'
        state['last_verified_package'] = {'path': str(args.output.resolve()), 'sha256': digest(args.output)}
        state.pop('active_revision', None)
        write_object(args.state, state)
    print(f'Packaged verified staged files to {args.output}');return 0

def verify(args)->int:
    with zipfile.ZipFile(args.zip) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):raise ValueError('ZIP contains duplicate members')
        for info in z.infolist():
            name = info.filename
            p=Path(name)
            if p.is_absolute() or '..' in p.parts:raise ValueError(f'unsafe ZIP member: {name}')
            if ((info.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError(f'symlink ZIP member is forbidden: {name}')
        if 'release-manifest.json' not in names:raise ValueError('release-manifest.json missing')
        embedded_manifest=z.read('release-manifest.json')
        if embedded_manifest!=args.manifest.read_bytes():
            raise ValueError('embedded release manifest does not match the trusted sidecar manifest')
        manifest=json.loads(embedded_manifest)
        if manifest.get('schema_version')!='1.1.0':raise ValueError('release manifest schema is invalid')
        verification=manifest.get('verification')
        if not isinstance(verification,dict):raise ValueError('release manifest verification record is missing')
        for key in ('staging_manifest_sha256','review_checklist_sha256','qa_report_sha256','approval_state_sha256','composition_manifest_sha256','composition_renderer_receipt_sha256'):
            value=verification.get(key)
            if not isinstance(value,str) or len(value)!=64 or any(c not in '0123456789abcdef' for c in value):
                raise ValueError(f'release manifest {key} is invalid')
        expected_order=[e['filename'] for e in manifest.get('files',[])]+['release-manifest.json']
        if names!=expected_order:raise ValueError(f'ZIP members/order mismatch: {names}')
        import hashlib
        for e in manifest['files']:
            raw=z.read(e['filename'])
            if hashlib.sha256(raw).hexdigest()!=e['sha256']:raise ValueError(f"checksum mismatch: {e['filename']}")
            try:
                with Image.open(io.BytesIO(raw)) as image:
                    issues=forbidden_metadata(image)
                    if issues:
                        raise ValueError(f"forbidden image metadata in {e['filename']}: {', '.join(sorted(set(issues)))}")
                    if list(image.size) != [e['width'], e['height']]:
                        raise ValueError(f"dimension mismatch: {e['filename']}")
                    image.verify()
            except ValueError:
                raise
            except Exception as exc:
                raise ValueError(f"undecodable image: {e['filename']}: {exc}") from exc
        bad=z.testzip()
        if bad:raise ValueError(f'ZIP integrity failed at {bad}')
    print('ZIP verification passed');return 0

def main()->int:
    p=argparse.ArgumentParser(description='Stage and package only hash-locked, QA-approved carousel outputs')
    sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('stage');s.add_argument('--input',required=True,type=Path);s.add_argument('--output',required=True,type=Path);s.set_defaults(handler=stage)
    b=sub.add_parser('package');b.add_argument('--input',required=True,type=Path);b.add_argument('--staging-manifest',required=True,type=Path);b.add_argument('--review-checklist',required=True,type=Path);b.add_argument('--state',required=True,type=Path);b.add_argument('--composition-manifest',required=True,type=Path);b.add_argument('--output',required=True,type=Path);b.add_argument('--manifest-output',required=True,type=Path);b.set_defaults(handler=package)
    v=sub.add_parser('verify');v.add_argument('--zip',required=True,type=Path);v.add_argument('--manifest',required=True,type=Path,help='Trusted release-manifest sidecar written by package');v.set_defaults(handler=verify)
    args=p.parse_args()
    try:return args.handler(args)
    except (ValueError,OSError,json.JSONDecodeError,zipfile.BadZipFile) as exc:print(f'Packaging blocked: {exc}',file=sys.stderr);return 4
if __name__=='__main__':raise SystemExit(main())
