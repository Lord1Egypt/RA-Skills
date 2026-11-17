"""Report-type views and navigation over approved content, without new claims."""
FOCUS = {
    'weekly_report': ('本周变化与异常','上次行动回验与下周安排'),
    'monthly_report': ('月度目标与结构变化','利润质量与下月资源'),
    'quarterly_report': ('季度目标与策略复盘','下季度优先级'),
    'annual_report': ('年度趋势与增长来源','次年经营方向'),
    'campaign_review': ('活动阶段与基准对比','得失与可复用动作'),
    'store_diagnosis': ('经营现状与关键短板','优先改善路径'),
    'data_quality_audit': ('数据口径与阻断项','可用范围与补数清单'),
    'single_topic': ('专题事实与限制','验证方案与停止条件'),
}

def action_order(items):
    rank={'P0':0,'P1':1,'P2':2,'high':0,'medium':1,'low':2}
    return sorted((r for r in items if isinstance(r,dict)),key=lambda r:rank.get(str(r.get('priority')),3))

def view(package):
    task=package.get('task_type','store_diagnosis')
    focus=FOCUS.get(task,FOCUS['store_diagnosis'])
    # Finding ids can repeat across authors and some legacy items have no id.
    # Presentation ownership must use the actual list occurrence, not the id.
    items=[dict(item,kind=kind,presentation_key=kind+':'+str(index))
           for kind in ('facts','judgments','hypotheses')
           for index,item in enumerate(package.get(kind,[])) if isinstance(item,dict)]
    chapters=[]
    assigned=set()
    for chapter in package.get('chapter_plan',{}).get('chapters',[]):
        cid=chapter.get('chapter_id')
        related=[r for r in items if cid in (r.get('chapter_ids') or [r.get('chapter_id')])]
        assigned.update(r['presentation_key'] for r in related)
        chapters.append({'chapter_id':cid,'title':chapter.get('title'),
            'owner_agent':chapter.get('owner_agent'),'source_report_ids':chapter.get('source_report_ids',[]),
            'items':related,'binding_status':'bound' if related else 'no_explicit_finding_binding'})
    unassigned=[r for r in items if r['presentation_key'] not in assigned]
    return {'status':'presentation_prepared_not_reviewed','task_type':task,'focus':list(focus),
        'comparison_expectation':package.get('task_profile',{}).get('comparison_expectation'),
        'chapters':chapters,'unassigned_findings':unassigned,
        'summary_item_ids':[r.get('id') for r in (package.get('judgments') or package.get('facts') or [])[:3]],
        'action_ids':[r.get('action_id') for r in action_order(package.get('actions',[]))],
        'all_findings_retained':True,'all_actions_retained':True}

def review_index(package):
    return {'status':'navigation_only','review_decision':None,
        'run_id':package.get('run_id'),'report_revision':package.get('report_revision'),
        'task_type':package.get('task_type'),
        'findings':[{'kind':kind,'id':r.get('id'),'chapter_ids':r.get('chapter_ids',[]),
            'evidence_ids':r.get('evidence_ids',[]),'claim_ids':r.get('claim_ids',[])}
            for kind in ('facts','judgments','hypotheses') for r in package.get(kind,[]) if isinstance(r,dict)],
        'numbers':[{'claim_id':r.get('claim_id'),'metric':r.get('metric'),'source_ref':r.get('source_ref'),
                   'inputs':r.get('inputs',[])} for r in package.get('claim_ledger',{}).get('claims',[])],
        'actions':[{'action_id':r.get('action_id'),'owner':r.get('owner'),'acceptance':r.get('acceptance'),
                    'stop_condition':r.get('stop_condition')} for r in action_order(package.get('actions',[]))]}

