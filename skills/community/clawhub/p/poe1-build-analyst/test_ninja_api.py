from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path('/home/ubuntu/skills/poe1-build-analyst/testdata')
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'https://poe.ninja/api/data/builds'
QUERIES = [
    {'overview': 'allflame', 'type': 'exp'},
    {'overview': 'Allflame', 'type': 'exp'},
    {'overview': 'CurseOfTheAllflame', 'type': 'exp'},
    {'overview': 'Curse of the Allflame', 'type': 'exp'},
]

for index, query in enumerate(QUERIES, 1):
    url = BASE + '?' + urllib.parse.urlencode(query)
    request = urllib.request.Request(
        url,
        headers={'User-Agent': 'poe1-build-analyst/1.0', 'Accept': 'application/json'},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read()
            print(index, response.status, response.headers.get('content-type'), len(payload), url)
            if response.status == 200 and payload.lstrip().startswith((b'{', b'[')):
                path = OUT / f'ninja_query_{index}.json'
                path.write_bytes(payload)
                parsed = json.loads(payload)
                if isinstance(parsed, dict):
                    print('keys=', list(parsed)[:20])
                else:
                    print('payload_type=', type(parsed).__name__)
    except Exception as exc:
        print(index, type(exc).__name__, str(exc), url)
