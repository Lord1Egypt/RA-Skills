#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import os
ROOT=Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX=ROOT/'memory'/'index'

def load(path): return json.loads(path.read_text(encoding='utf-8'))
def search(items, query, key):
    q=query.lower(); return [x for x in items if q in (x.get(key) or '').lower()]

def recover(query:str)->dict:
    hot=load(INDEX/'retrieval-view-hot.json').get('items',[])
    packed=load(INDEX/'retrieval-view-packed.json').get('items',[])
    thin=load(INDEX/'thin-index.json')
    hot_hits=search(hot, query, 't')
    if hot_hits: return {'route':'hot-first','stage':'hot','hits':len(hot_hits)}
    packed_hits=search(packed, query, 't')
    if packed_hits: return {'route':'fallback','stage':'packed','hits':len(packed_hits)}
    thin_hits=search(thin, query, 'title')
    if thin_hits: return {'route':'recovery','stage':'thin','hits':len(thin_hits)}
    return {'route':'miss','stage':'none','hits':0}

def main():
    import sys
    query=' '.join(sys.argv[1:]) if len(sys.argv)>1 else '不存在的查詢測試'
    print(json.dumps(recover(query), ensure_ascii=False, indent=2))
if __name__=='__main__':
    main()
