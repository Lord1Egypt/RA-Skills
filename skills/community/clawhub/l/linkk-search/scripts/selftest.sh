#!/usr/bin/env bash
# selftest.sh — 部署后自检：实例存活 / JSON API 可用 / 引擎有返回
set -uo pipefail
PORT="${SXP_PORT:-8888}"
FAIL=0

echo "== SearXNG 自检 (端口 $PORT) =="

# 1) 存活
CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:$PORT/" || echo 000)
if [ "$CODE" = "200" ]; then echo "[PASS] 实例存活 (HTTP $CODE)"; else echo "[FAIL] 实例无响应 (HTTP $CODE) → TROUBLESHOOT 第 2、3 条"; FAIL=1; fi

# 2) JSON API
JSON=$(curl -s --max-time 15 "http://127.0.0.1:$PORT/search?q=%E6%B5%8B%E8%AF%95&format=json")
if echo "$JSON" | grep -q '"query"'; then
  echo "[PASS] JSON API 可用"
else
  echo "[FAIL] JSON API 异常 → 检查 settings.yml 的 search.formats 是否包含 json（TROUBLESHOOT 第 4 条）"
  FAIL=1
fi

# 3) 有结果
N=$(echo "$JSON" | grep -o '"url"' | wc -l)
if [ "${N:-0}" -ge 3 ]; then echo "[PASS] 实测返回 ${N} 条结果，上游引擎工作正常"; else
  echo "[WARN] 仅返回 ${N:-0} 条 → 可能命中机房IP封锁或引擎被禁（TROUBLESHOOT 第 1、6 条）"; fi

echo
if [ "$FAIL" = "0" ]; then echo "SELFTEST PASS ✅ 把 http://<本机内网IP>:$PORT 填进 OpenClaw 即可"; else echo "SELFTEST FAIL ❌ 按上方提示查 docs/TROUBLESHOOT.md"; exit 1; fi
