#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import os
ROOT=Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX=ROOT/'memory'/'index'

def classify_query(query:str)->dict:
    q=query.lower()
    if any(x in q for x in ['偏好','preference','專案狀態','project-state','entity','實體']):
        return {'class':'structured-hot','route':'hot-first','confidence':0.9}
    if any(x in q for x in ['bootstrap','daily memory','addendum']):
        return {'class':'known-topic','route':'hot-first','confidence':0.85}
    if any(x in q for x in ['2026-03','歷史','history','ssl','測試']):
        return {'class':'historical-broad','route':'packed-first','confidence':0.8}
    return {'class':'unknown','route':'hot-first','confidence':0.5}

def main():
    import sys
    query=' '.join(sys.argv[1:]) if len(sys.argv)>1 else 'Session bootstrap'
    print(json.dumps(classify_query(query), ensure_ascii=False, indent=2))
if __name__=='__main__':
    main()
