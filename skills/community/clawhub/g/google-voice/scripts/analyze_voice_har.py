#!/usr/bin/env python3
import json, pathlib, urllib.parse, collections, re, sys
p = pathlib.Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else pathlib.Path.home()/'Downloads/har/voice.google.com.har'
h = json.loads(p.read_text(errors='ignore'))
counts = collections.Counter()
samples = {}
for e in h.get('log',{}).get('entries',[]):
    r=e.get('request',{}); u=urllib.parse.urlparse(r.get('url',''))
    if u.netloc == 'clients6.google.com' and '/voice/v1/voiceclient/' in u.path:
        key=(r.get('method'), u.path)
        counts[key]+=1
        if key not in samples:
            text=(r.get('postData') or {}).get('text','')
            text=re.sub(r'\+?\d[\d\-() ]{7,}\d','<NUMBER>',text)
            text=re.sub(r'"![^"]{20,}"', '"<TOKEN>"', text)
            text=re.sub(r'"[^"]{40,}"', '"<TOKEN_OR_LONG_VALUE>"', text)
            text=re.sub(r'"[^"]{20,}"', lambda m: '"<TEXT>"' if any(c.isspace() for c in m.group(0)) else m.group(0), text)
            text=re.sub(r'"[^"\\]*(token|id|text|message|recipient|phone)[^"\\]*"\s*:\s*"[^"\\]+"','"<redacted>":"<redacted>"',text, flags=re.I)
            samples[key]=text[:500]
for (method,path),n in counts.most_common():
    print(f'{n:3} {method} {path}')
    if samples.get((method,path)):
        print('    sample:', samples[(method,path)].replace('\n',' ')[:500])
