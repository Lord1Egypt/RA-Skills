# -*- coding: utf-8 -*-
"""从 cn_inbox_full.json 生成 cn_inbox.json：每门店取「含 DDL 或近 14 天活跃」的重点线程，上限 6 个。
输出精简字段（subject/progress/todos/fresh 英文原文）供 LLM 翻译归纳。
"""
import json, datetime

full = json.load(open('cn_inbox_full.json', encoding='utf-8'))
TODAY = datetime.date.today()
CUT = (TODAY - datetime.timedelta(days=14)).strftime('%Y-%m-%d')

def datepart(s):
    return (s or '')[:10]

out = {'generated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
       'window': {'today': TODAY.strftime('%Y-%m-%d'), 'active_since': CUT, 'cap_per_store': 6},
       'stores': {}}

for sk in ['Cologne', 'Rome', 'Dusseldorf', 'Zurich']:
    sv = full['stores'].get(sk) or {'label': sk, 'items': []}
    picked = []
    for t in sv['items']:
        has_ddl = bool(t.get('ddl'))
        active = datepart(t.get('last')) >= CUT
        if not (has_ddl or active):
            continue
        picked.append(t)
    # 优先：含 DDL > 最近活跃
    picked.sort(key=lambda t: (0 if t.get('ddl') else 1, -1 * int(datepart(t.get('last')).replace('-', '') or 0)))
    picked = picked[:6]
    out['stores'][sk] = {
        'label': sv.get('label'),
        'count': len(picked),
        'items': [{
            'thread_id': t.get('thread_id'),
            'subject': t.get('subject'),
            'sub': t.get('sub'),
            'last': t.get('last'),
            'count': t.get('count'),
            'responsible': t.get('responsible'),
            'ddl': t.get('ddl'),
            'head_from': t.get('head_from'),
            'to': t.get('to'),
            'progress': t.get('progress'),
            'todos': t.get('todos'),
            'fresh': t.get('fresh'),
        } for t in picked],
    }

json.dump(out, open('cn_inbox.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('cn_inbox.json written')
for sk, v in out['stores'].items():
    print(' ', sk, v['label'], '=>', v['count'])
print('total', sum(v['count'] for v in out['stores'].values()))
