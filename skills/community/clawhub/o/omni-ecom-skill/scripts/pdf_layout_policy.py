"""One page allowance for generation and downstream review of full content."""
def page_limit(package):
    counts=len(package.get('report_inventory',{}).get('reports',[]))+sum(
        len(package.get(k,[])) for k in ('facts','judgments','hypotheses','actions'))
    base={'annual_report':24,'quarterly_report':20,'store_diagnosis':20,'campaign_review':20}.get(package.get('task_type'),12)
    # A long single finding/condition can occupy several pages; counting only
    # list items penalizes preserving full text and encourages truncation.
    import json
    semantic={key:package.get(key,[]) for key in
              ('facts','judgments','hypotheses','actions','missing_data','risks','previous_action_review')}
    chars=len(json.dumps(semantic,ensure_ascii=False))
    return min(120,max(17,base+(counts+5)//6+(chars//4500)))

