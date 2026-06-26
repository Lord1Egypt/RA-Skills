#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/scripts/pengbo_smm.py"

pass(){ echo "[PASS] $1"; }
fail(){ echo "[FAIL] $1"; exit 1; }

python3 -m py_compile "$PY" || fail "语法检查"
pass "语法检查"

python3 "$PY" --lang zh health >/tmp/pengbo_smoke_health.json || true
grep -q '"action": "health"' /tmp/pengbo_smoke_health.json || fail "health 返回 action"
pass "health 返回"

python3 "$PY" --lang en setup >/tmp/pengbo_smoke_setup_en.json || true
grep -q '"lang": "en"' /tmp/pengbo_smoke_setup_en.json || fail "英文语言输出"
pass "英文语言输出"

rm -f "$ROOT/data/language-state.json"
python3 "$PY" --lang auto --input-text 'hola necesito ayuda con pedido' health >/tmp/pengbo_smoke_es.json || true
grep -q '"lang": "es"' /tmp/pengbo_smoke_es.json || fail "西语自动识别"
pass "西语自动识别"

if [[ -n "${PENGBO_API_KEY:-}" ]]; then
  python3 "$PY" --lang zh --key "$PENGBO_API_KEY" list-orders --limit 1 >/tmp/pengbo_smoke_orders.json || fail "list-orders 调用"
  grep -q '"action": "list_orders"' /tmp/pengbo_smoke_orders.json || fail "list-orders action"
  pass "list-orders 调用"

  python3 "$PY" --lang zh --key "$PENGBO_API_KEY" status --order 36 >/tmp/pengbo_smoke_status.json || true
  grep -q '"display"' /tmp/pengbo_smoke_status.json || fail "status display 映射"
  pass "status display 映射"
fi

echo "全部冒烟测试通过"