"""Shared, non-verifying decision presentation for Markdown and PDF."""
import copy
import json
import hashlib
from pathlib import Path

from artifact_contract import validate_analysis_identity

CLAIM_FIELDS=('metric','unit','value','period','previous_value','previous_period','direction','absolute_change',
              'comparability_note','current_days','previous_days','baseline_sha256','caliber_sha256')
ROW_FIELDS=('conflict_id','decision','not_adopted_disposition','residual_risk','challenge_review')
PRESENTATION_FIELDS=('adjudicated_claims','adjudication_summary','adjudicated_downstream','unresolved_conflicts')


def require(ok,reason):
    if not ok: raise ValueError(reason)


def attach(package,payload):
    validate_analysis_identity(payload,'conflict_verdict',package.get('team_version'))
    for key in ('run_id','client_scope','team_version','report_revision'):
        require(payload.get(key)==package.get(key),'decision_display_identity_mismatch')
    claims=payload.get('adjudicated_claims',{})
    rows=payload.get('verdicts',[])
    require(isinstance(claims,dict) and isinstance(rows,list) and all(isinstance(r,dict) for r in rows),
            'decision_display_invalid')
    ids=[r.get('conflict_id') for r in rows]
    require(all(isinstance(i,str) and i for i in ids) and len(ids)==len(set(ids)) and set(claims).issubset(ids),
            'decision_display_conflict_mismatch')
    require(all(isinstance(value,dict) for value in claims.values()),'decision_display_claim_invalid')
    # Do not copy calculation input paths, host exports, or credentials into public reports.
    package['adjudicated_claims']={cid:{k:copy.deepcopy(value[k]) for k in CLAIM_FIELDS if k in value}
                                  for cid,value in claims.items()}
    package['adjudication_summary']=[{k:copy.deepcopy(row[k]) for k in ROW_FIELDS if k in row} for row in rows]
    package['adjudicated_downstream']=copy.deepcopy(payload.get('adjudicated_downstream',{}))
    package['unresolved_conflicts']=copy.deepcopy(payload.get('unresolved_conflicts',[]))
    package['decision_presentation_status']='candidate_requires_quality_and_review'


def auto_attach(package,report_dir,explicit=None):
    """Use this run's configured adjudication; do not guess a file from history."""
    root=Path(report_dir).resolve()
    config_path=root/'quality-inputs.json'
    tracked={}
    def read_bound(path):
        raw=path.read_bytes()
        tracked[path]=hashlib.sha256(raw).hexdigest()
        value=json.loads(raw.decode('utf-8-sig'))
        require(isinstance(value,dict),'decision_display_source_invalid')
        return value
    canonical=None
    if config_path.is_file():
        config=read_bound(config_path)
        require(all(config.get(k)==package.get(k) for k in ('run_id','client_scope','report_revision')),
                'decision_display_quality_identity_mismatch')
        raw=config.get('adjudication')
        if raw:
            require(isinstance(raw,str) and not Path(raw).is_absolute(),'decision_display_path_invalid')
            canonical=(root/raw).resolve()
            require(canonical.is_relative_to(root) and canonical.is_file(),'decision_display_source_outside_or_missing')
        else:
            require(not explicit,'decision_display_source_not_configured')
    selected=canonical or (Path(explicit).resolve() if explicit else None)
    if selected is None:
        return False
    payload=read_bound(selected)
    if canonical and explicit:
        require(read_bound(Path(explicit).resolve())==payload,'decision_display_override_conflicts_with_quality')
    rows=payload.get('verdicts',[])
    require(isinstance(rows,list) and all(isinstance(row,dict) for row in rows),'decision_display_invalid')
    claims=payload.get('adjudicated_claims',{})
    require(isinstance(claims,dict) and all(row.get('conflict_id') in claims for row in rows if
            row.get('method') not in ('scope_degradation','pending_verification')),
            'decision_display_canonical_claims_missing')
    attach(package,payload)
    for path,original in tracked.items():
        require(hashlib.sha256(path.read_bytes()).hexdigest()==original,'decision_display_source_changed')
    package.setdefault('sources',[]).append(dict(type='adjudication',source=selected.name,
        sha256=tracked[selected],status='candidate_requires_quality_and_review'))
    return True


def validate_presentation(package,verdict,report_text):
    """Do not let a checked JSON verdict disappear from the delivered Markdown."""
    expected=[{k:row[k] for k in ROW_FIELDS if k in row} for row in verdict['verdicts']]
    require(package.get('adjudication_summary')==expected,'quality_decision_display_stale_or_missing')
    # Older records may keep claims in report.json only; recomputation still
    # validates those. New canonical decision packs additionally bind projection.
    if 'adjudicated_claims' in verdict:
        projected={k:package[k] for k in ('run_id','client_scope','team_version','report_revision')}
        attach(projected,verdict)
        require(all(package.get(k,{} if k in ('adjudicated_claims','adjudicated_downstream') else [])==projected[k]
                    for k in PRESENTATION_FIELDS),'quality_decision_projection_changed')
    # Ignore HTML comments and code blocks: including the text only in hidden or
    # example content is not presenting the decision to the reader.
    import re
    visible=re.sub(r'<!--(?:[\s\S]*?-->|[\s\S]*$)', '',report_text)
    lines=[]; fence=None
    for line in visible.splitlines():
        match=re.match(r'^ {0,3}(`{3,}|~{3,})',line)
        if match:
            marker=match.group(1)
            if fence is None: fence=marker
            elif marker[0]==fence[0] and len(marker)>=len(fence) and re.fullmatch(r' {0,3}[`~]+\s*',line): fence=None
            continue
        if fence is None: lines.append(line)
    visible='\n'.join(lines)
    required='\n'.join(markdown(package)).strip()
    require(bool(required) and '\n'+required in '\n'+visible and visible.count('## 专家分歧与总监裁决')==1,
            'quality_decision_markdown_missing_or_stale')


def text(value):
    if value is None: return '未提供'
    if isinstance(value,(list,dict)): return json.dumps(value,ensure_ascii=False)
    return str(value)


def sections(package):
    """Return complete plain text; renderers escape markup without truncation."""
    result=[]
    claims=package.get('adjudicated_claims',{})
    summaries={r['conflict_id']:r for r in package.get('adjudication_summary',[])}
    for cid in sorted(set(claims)|set(summaries)):
        claim=claims.get(cid,{})
        row=summaries.get(cid,{})
        lines=['展示状态：候选裁决，是否通过以质量检查和独立复核凭证为准。']
        if claim:
            lines.append(f"采用值：{text(claim.get('metric'))}；期间：{text(claim.get('period'))}；数值：{text(claim.get('value'))}；单位：{text(claim.get('unit'))}")
            if 'previous_value' in claim:
                direction={'up':'上升','down':'下降','flat':'持平'}.get(claim.get('direction'),'未确认')
                change_unit='百分点' if claim.get('unit')=='%' else text(claim.get('unit'))
                lines.extend([
                    f"对比期：{text(claim.get('previous_period'))}；对比值：{text(claim.get('previous_value'))}；方向：{direction}；绝对变化：{text(claim.get('absolute_change'))} {change_unit}",
                    f"本期/对比期天数：{text(claim.get('current_days'))}/{text(claim.get('previous_days'))}；可比限制：{text(claim.get('comparability_note'))}"])
        lines.extend([f"总监决定：{text(row.get('decision'))}",f"未采纳意见：{text(row.get('not_adopted_disposition'))}",
                      f"剩余风险：{text(row.get('residual_risk'))}"])
        for reply in row.get('challenge_review',[]):
            disposition={'adopted':'采纳','not_adopted':'未采纳','data_gap':'数据不足'}.get(reply.get('disposition'),'未确认')
            lines.append(f"专家回复处理：{text(reply.get('role'))}；{disposition}；理由：{text(reply.get('reason'))}；回传指纹：{text(reply.get('return_event_hash'))}")
        result.append((cid,lines))
    for row in package.get('unresolved_conflicts',[]):
        result.append((text(row.get('conflict_id'))+'（待解决）',[
            '原因：'+text(row.get('reason')),'补充要求：'+text(row.get('remedy'))]))
    if package.get('adjudicated_downstream'):
        result.append(('受影响的下游结果',[str(cid)+'：'+text(value) for cid,value in package['adjudicated_downstream'].items()]))
    return result


def markdown(package):
    import html
    def escape(value):
        value=html.escape(str(value),quote=False)
        for char in ('\\','`','*','_','[',']','|','#'):
            value=value.replace(char,'\\'+char)
        return value.replace('\r',' ').replace('\n',' ')
    blocks=sections(package)
    if not blocks: return []
    lines=['## 专家分歧与总监裁决','']
    for title,body in blocks:
        lines.extend(['### '+escape(title),''])
        lines.extend('- '+escape(line) for line in body)
        lines.append('')
    return lines
