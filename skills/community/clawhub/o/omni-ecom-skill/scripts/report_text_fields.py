"""Full semantic fields for presentation; never shorten acceptance conditions."""
import json

def text(value):
    if isinstance(value,(dict,list)):
        return json.dumps(value,ensure_ascii=False)
    return str(value if value is not None else '')

def gap_lines(value):
    if not isinstance(value,dict):
        return [text(value)]
    labels={'item':'待补项','name':'名称','field':'字段','description':'说明',
            'purpose':'用途','reason':'原因','impact':'影响','priority':'优先级',
            'required_source':'补数来源','required_input':'所需输入及授权',
            'required_data':'所需资料及条件','missing_fields':'缺失字段',
            'needed_data':'需要补充','blocker':'阻断原因','authorization':'授权条件'}
    # Unknown fields are preserved too: future expert inputs must not disappear.
    return [labels.get(key,key)+'：'+text(item) for key,item in value.items()
            if item is not None and item!='' and item!=[]]
