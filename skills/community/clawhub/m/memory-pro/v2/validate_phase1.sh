#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
CLIENT="$(cd "$BASE_DIR/../scripts" && pwd)/search_semantic.py"
API_URL="${MEMORY_PRO_API_URL:-http://127.0.0.1:8001}"

pass() { echo "✅ $1"; }
fail() { echo "❌ $1"; exit 1; }

cd "$BASE_DIR"

echo "[1/5] Python syntax compile check"
python3 -m py_compile preprocess.py build_index.py retrieval_hybrid.py main.py "$CLIENT" \
  || fail "py_compile failed"
pass "Syntax compile OK"

echo "[2/5] Build artifacts check (rebuild index)"
python3 build_index.py >/tmp/memory_pro_build.log 2>&1 || {
  tail -n 60 /tmp/memory_pro_build.log || true
  fail "build_index.py failed"
}
for f in memory.index sentences.txt memory_meta.jsonl bm25_corpus.pkl; do
  [[ -f "$f" ]] || fail "Missing artifact: $f"
done
pass "Artifacts generated"

echo "[3/5] Alignment check"
python3 - <<PY || fail "Alignment check failed"
import json, pickle, faiss
from pathlib import Path
base=Path(r"$BASE_DIR")
idx=faiss.read_index(str(base/'memory.index'))
sent=(base/'sentences.txt').read_text(encoding='utf-8').splitlines()
meta=[json.loads(x) for x in (base/'memory_meta.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
bm=pickle.load(open(base/'bm25_corpus.pkl','rb'))
assert idx.ntotal==len(sent)==len(meta)==len(bm.get('tokenized_docs',[])), (idx.ntotal,len(sent),len(meta),len(bm.get('tokenized_docs',[])))
print('aligned', idx.ntotal)
PY
pass "Alignment OK"

echo "[4/5] Service health check (restart + wait)"
systemctl --user restart memory-pro.service || fail "systemctl restart failed"
python3 - <<'PY' || fail "Service health check failed"
import time, requests, sys
u='http://127.0.0.1:8001/health'
for i in range(120):
    try:
        r=requests.get(u,timeout=2)
        if r.status_code==200:
            print(r.text)
            sys.exit(0)
    except Exception:
        pass
    time.sleep(1)
sys.exit(1)
PY
pass "Service health OK"

echo "[5/5] Search smoke tests (vector + hybrid + hybrid debug)"
python3 "$CLIENT" "handover load" --url "$API_URL/search" --mode vector --json >/tmp/memory_pro_vector.json || fail "Vector query failed"
python3 "$CLIENT" "handover load" --url "$API_URL/search" --mode hybrid --json >/tmp/memory_pro_hybrid.json || fail "Hybrid query failed"
python3 - <<'PY' || fail "Hybrid debug query failed"
import requests, sys
r=requests.post('http://127.0.0.1:8001/search',json={
    'query':'handover load',
    'top_k':2,
    'mode':'hybrid',
    'include_debug':True,
},timeout=20)
if r.status_code != 200:
    print(r.status_code, r.text)
    sys.exit(1)
js=r.json()
assert 'results' in js and len(js['results'])>0
assert 'debug' in js['results'][0], js['results'][0]
print('hybrid_debug_ok')
PY
pass "Search smoke tests OK"

echo
echo "🎉 Phase 1 validation PASSED"
echo "- Build log: /tmp/memory_pro_build.log"
echo "- Vector sample: /tmp/memory_pro_vector.json"
echo "- Hybrid sample: /tmp/memory_pro_hybrid.json"
