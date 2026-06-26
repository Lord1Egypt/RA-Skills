#!/usr/bin/env bash
# name: exchange-rate
# description: 查询实时/历史汇率，支持货币换算（数据来源欧洲央行 ECB，每交易日更新）
# tags: 汇率,货币,换算,外汇

set -euo pipefail

BASE_URL="https://api.frankfurter.app"

FROM="" TO="" AMOUNT="" DATE="" START_DATE="" END_DATE="" FORMAT="json"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --from) FROM="$2"; shift 2;;
    --to) TO="$2"; shift 2;;
    --amount) AMOUNT="$2"; shift 2;;
    --date) DATE="$2"; shift 2;;
    --startDate) START_DATE="$2"; shift 2;;
    --endDate) END_DATE="${2:-}"; shift 2;;
    --format) FORMAT="$2"; shift 2;;
    *) shift;;
  esac
done

# 构造 URL 路径
if [[ -n "$START_DATE" ]]; then
  URL="${BASE_URL}/${START_DATE}..${END_DATE}"
elif [[ -n "$DATE" ]]; then
  URL="${BASE_URL}/${DATE}"
else
  URL="${BASE_URL}/latest"
fi

# 构造查询参数
PARAMS=""
[[ -n "$FROM" ]] && PARAMS="${PARAMS}&from=${FROM}"
[[ -n "$TO" ]] && PARAMS="${PARAMS}&to=${TO}"
[[ -n "$AMOUNT" ]] && PARAMS="${PARAMS}&amount=${AMOUNT}"
[[ -n "$PARAMS" ]] && URL="${URL}?${PARAMS:1}"

RESP=$(curl -sf "$URL")

if [[ "$FORMAT" == "table" ]]; then
  echo "$RESP" | python3 -c "
import json, sys
data = json.load(sys.stdin)
base = data.get('base', '')
amount = data.get('amount', 1)
date = data.get('date', '')
rates = data.get('rates', {})

if isinstance(next(iter(rates.values()), None), dict):
    # 时间序列
    print(f'基准货币: {base}  金额: {amount}')
    dates = sorted(rates.keys())
    currencies = sorted(rates[dates[0]].keys())
    header = f'{\"日期\":<12} ' + ' '.join(f'{c:>10}' for c in currencies)
    print(header)
    print('─' * len(header))
    for d in dates:
        vals = ' '.join(f'{rates[d].get(c, 0):>10.4f}' for c in currencies)
        print(f'{d:<12} {vals}')
else:
    # 单日汇率
    print(f'基准货币: {base}  金额: {amount}  日期: {date}')
    print(f'{\"货币\":<6} {\"汇率\":>12}')
    print('─' * 20)
    for k, v in rates.items():
        print(f'{k:<6} {v:>12.4f}')
"
else
  echo "$RESP" | python3 -m json.tool
fi
