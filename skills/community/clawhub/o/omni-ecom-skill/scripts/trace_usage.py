"""Aggregate reported per-request usage, without estimating fees or missing data."""
def summarize_usage(rows):
    providers=[]
    def walk(value):
        if isinstance(value,dict):
            provider=value.get('providerData')
            if isinstance(provider,dict) and isinstance(provider.get('rawUsage'),dict):
                providers.append(provider)
            for key,item in value.items():
                if key!='providerData':walk(item)
        elif isinstance(value,list):
            for item in value:walk(item)
    for row in rows:walk(row)
    seen=set(); totals={'input_tokens':0,'output_tokens':0,'cache_hit_tokens':0,'cache_miss_tokens':0}
    missing_cache=False; measured=0
    for provider in providers:
        mid=provider.get('messageId')
        raw=provider['rawUsage']
        input_count=raw.get('prompt_tokens',raw.get('input_tokens'))
        output_count=raw.get('completion_tokens',raw.get('output_tokens'))
        if not mid or mid in seen or not isinstance(input_count,(int,float)) or not isinstance(output_count,(int,float)):
            continue
        seen.add(mid); measured+=1
        totals['input_tokens']+=input_count;totals['output_tokens']+=output_count
        hit=raw.get('prompt_cache_hit_tokens');miss=raw.get('prompt_cache_miss_tokens')
        if isinstance(hit,(int,float)) and isinstance(miss,(int,float)):
            totals['cache_hit_tokens']+=hit;totals['cache_miss_tokens']+=miss
        else:missing_cache=True
    if not measured:return {'status':'not_reported','usage_records':0,'cost':None}
    if missing_cache:totals['cache_hit_tokens']=totals['cache_miss_tokens']=None
    return dict(status='reported_per_request_sum',usage_records=measured,**totals,cost=None,
        note='按真实 messageId 去重；累计输入包含重复上下文和缓存，不能视为单次上下文或付费额度。未核实价格和套餐，不计算费用。')

