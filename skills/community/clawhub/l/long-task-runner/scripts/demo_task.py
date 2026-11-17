"""Cheap deterministic workload and fault fixtures; never uses a model or network."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import wave

p = argparse.ArgumentParser()
p.add_argument('--mode', choices=['ok','fail','badjson','empty','noise','flaky','tree','wav','badwav','noop'], default='ok')
p.add_argument('--seconds', type=float, default=1)
p.add_argument('--output', default='result.json')
p.add_argument('--counter')
a = p.parse_args()
if a.counter:
    cp = Path(a.counter)
    count = int(cp.read_text())+1 if cp.exists() else 1
    cp.write_text(str(count))
else:
    count = 1
if a.mode == 'tree':
    child = subprocess.Popen([sys.executable,'-c',"import time; from pathlib import Path; time.sleep(4); Path('escaped-child.txt').write_text('escaped'); time.sleep(40)"])
    Path('descendant-pid.txt').write_text(str(child.pid))
if a.mode == 'noise':
    for _ in range(256):
        os.write(1, b'x'*8192)
time.sleep(a.seconds)
out = Path(a.output)
if a.mode == 'fail' or a.mode == 'flaky' and count == 1:
    print('deliberate transient failure' if a.mode == 'flaky' else 'deliberate failure',file=sys.stderr)
    raise SystemExit(7)
if a.mode == 'badjson':
    out.write_text('{broken',encoding='utf-8')
elif a.mode == 'empty':
    out.write_bytes(b'')
elif a.mode in {'wav','badwav'}:
    with wave.open(str(out),'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(8000)
        w.writeframes(b'\x00\x00'*8000)
    if a.mode == 'badwav':
        out.write_bytes(out.read_bytes()[:100])
elif a.mode != 'noop':
    out.write_text(json.dumps({'ok':True,'mode':a.mode}),encoding='utf-8')
