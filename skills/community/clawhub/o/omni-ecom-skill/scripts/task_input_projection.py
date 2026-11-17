"""Deterministic role views; full original inputs stay available and immutable."""
import copy

IDENTITY = ('schema_version','artifact_type','contract_name','contract_version',
            'created_by_team_version','legacy_compatibility','run_id','client_scope','team_version')
REPORT_KEYS = ('report_id','file_name','file_path','relative_path','source_file','source_sha256','sha256',
               'sheet_name','sheet','platform','domain','report_type','report_type_label',
               'time_scope','granularity','verdict','verdict_reason','status','reason','identification','confidence','identified_by')
CHAPTER_KEYS = ('chapter_id','title','owner_agent','source_report_ids','cluster_ids',
                'caliber','metric_contract','required_metrics','metrics','cross_checks','status')

def report_index(report):
    out = {k: copy.deepcopy(report[k]) for k in REPORT_KEYS if k in report}
    # Classification evidence can be large; keep the result, original reference
    # and unresolved status. Actual headers/rows remain in the original inventory.
    if isinstance(out.get('identification'), dict):
        out['identification'] = {k:v for k,v in out['identification'].items()
                                 if k in ('status','model_review_pending','confidence','method')}
    return out

def project(kind, content, role):
    if kind == 'baseline':
        # All shared definitions, conflicts and scope remain available to each role.
        return copy.deepcopy(content)
    out = {k:copy.deepcopy(content[k]) for k in IDENTITY if k in content}
    if kind == 'inventory':
        reports = content.get('reports', [])
        out.update(report_count=content.get('report_count',len(reports)),
                   reports=[report_index(r) for r in reports])
    elif kind == 'chapter_plan':
        rows = content.get('chapters', [])
        out['chapters'] = [{k:copy.deepcopy(r[k]) for k in CHAPTER_KEYS if k in r}
                           for r in rows if r.get('owner_agent') == role]
        out['all_chapter_index'] = [{k:r[k] for k in ('chapter_id','title','owner_agent','source_report_ids') if k in r}
                                    for r in rows]
    else:
        raise ValueError('task_projection_kind_invalid')
    return out

def role_packet(packet, role):
    return {kind:{'path':item['path'],'sha256':item['sha256'],
                  'projection':{'version':'1','kind':kind,'role':role,
                      'origin_note':'content 是任务卡紧凑视图，不是原 JSON 原样内容；视图索引字段不能归因到原文件。原字段或状态声明必须检查 path 指向的原件。'},
                  'content':project(kind,item['content'],role)} for kind,item in packet.items()}

