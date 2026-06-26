#!/usr/bin/env bash
# name: courier-track
# description: 查询快递物流轨迹，支持国内快递（顺丰、圆通、京东等）
# tags: 快递,物流,查询

set -euo pipefail

TRACKING_NUMBER="" CARRIER_CODE="" FORMAT="json"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --trackingNumber) TRACKING_NUMBER="$2"; shift 2;;
    --carrierCode) CARRIER_CODE="$2"; shift 2;;
    --format) FORMAT="$2"; shift 2;;
    *) shift;;
  esac
done

if [[ -z "$TRACKING_NUMBER" ]]; then
  echo '{"status":"error","error_type":"missing_parameter","missing":"trackingNumber","suggestion":"请提供快递单号，例如 --trackingNumber SF1234567890"}' >&2
  exit 1
fi

# 双通道路由：有自有凭证 → 直连快递100；无凭证 → 免费代理
KEY="${KUAIDI100_KEY:-}"
CUSTOMER="${KUAIDI100_CUSTOMER:-}"

if [[ -n "$KEY" && -n "$CUSTOMER" ]]; then
  # ── 通道 A：直连快递100（用户凭证不经过任何第三方） ──
  PARAM=$(python3 -c "
import json, sys
print(json.dumps({'com': sys.argv[1], 'num': sys.argv[2]}, separators=(',',':')))
" "${CARRIER_CODE:-}" "$TRACKING_NUMBER")

  SIGN=$(printf '%s' "${PARAM}${KEY}${CUSTOMER}" | md5sum | awk '{print toupper($1)}' 2>/dev/null \
      || printf '%s' "${PARAM}${KEY}${CUSTOMER}" | md5 -q | tr '[:lower:]' '[:upper:]')

  RESP=$(curl -sf --max-time 15 -X POST \
    -d "customer=${CUSTOMER}&sign=${SIGN}&param=${PARAM}" \
    "https://poll.kuaidi100.com/poll/query.do" 2>/dev/null) || {
    echo '{"status":"error","error_type":"api_unavailable","service":"kuaidi100.com","suggestion":"快递100 API 请求失败，请检查网络或凭证是否正确。"}' >&2
    exit 1
  }

  # 快递100原始格式 → 统一输出格式
  export _COURIER_JSON="$RESP"
  python3 -c "
import json, os, sys

resp = json.loads(os.environ['_COURIER_JSON'])
fmt = sys.argv[1]

# 快递100返回格式: {com, nu, state, data: [{time, context}]}
if resp.get('status') == '200' or 'data' in resp:
    result = {
        'trackingNumber': resp.get('nu', ''),
        'carrierName': resp.get('com', ''),
        'status': {
            '0': '运输中', '1': '揽收', '2': '疑难', '3': '已签收',
            '4': '退签', '5': '派件中', '6': '退回', '7': '转投',
            '10': '待清关', '11': '清关中', '12': '已清关', '13': '清关异常',
            '14': '收件人拒签'
        }.get(str(resp.get('state', '')), '未知'),
        'dataSource': 'kuaidi100-direct',
        'events': [
            {'time': e.get('time', ''), 'desc': e.get('context', '')}
            for e in resp.get('data', [])
        ]
    }
else:
    result = {
        'status': 'error',
        'error_type': 'query_failed',
        'message': resp.get('message', '查询失败'),
        'suggestion': '请核实单号是否正确，或尝试指定 --carrierCode'
    }

print(json.dumps(result, ensure_ascii=False, indent=2))
" "$FORMAT"

else
  # ── 通道 B：免费代理（仅发送单号，不发送任何凭证） ──
  BODY=$(python3 -c "
import json, sys
d = {'trackingNumber': sys.argv[1]}
if sys.argv[2]:
    d['carrierCode'] = sys.argv[2]
print(json.dumps(d))
" "$TRACKING_NUMBER" "${CARRIER_CODE:-}")

  RESP=$(curl -sf --max-time 15 -X POST \
    -H "Content-Type: application/json" \
    -d "$BODY" \
    "https://api.fenxianglife.com/fenxiang-ai-brain/skill/courier/track" 2>/dev/null) || {
    echo '{"status":"error","error_type":"api_unavailable","service":"fenxianglife.com","suggestion":"快递查询服务暂时不可用，请稍后重试。如有自有快递100凭证，可设置 KUAIDI100_KEY 和 KUAIDI100_CUSTOMER 环境变量直连。"}' >&2
    exit 1
  }

  # 代理返回格式: {code, data: {...}}
  export _COURIER_JSON="$RESP"
  python3 -c "
import json, os, sys

resp = json.loads(os.environ['_COURIER_JSON'])
fmt = sys.argv[1]
data = resp.get('data', resp)

if isinstance(data, dict) and data.get('trackingNumber'):
    data['dataSource'] = 'free-proxy'
    print(json.dumps(data, ensure_ascii=False, indent=2))
elif resp.get('code') and resp.get('code') != 200:
    print(json.dumps({
        'status': 'error',
        'error_type': 'query_failed',
        'message': resp.get('message', resp.get('msg', '查询失败')),
        'suggestion': '请核实单号是否正确，或尝试指定 --carrierCode'
    }, ensure_ascii=False, indent=2))
else:
    print(json.dumps(data if data else resp, ensure_ascii=False, indent=2))
" "$FORMAT"
fi
