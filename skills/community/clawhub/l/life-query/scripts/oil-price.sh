#!/usr/bin/env bash
# name: oil-price
# description: 查询全国各省油价（92号、95号、柴油等），数据来源东方财富/国家发改委
# tags: 油价,加油,汽油,柴油

set -euo pipefail

API_URL="https://datacenter-web.eastmoney.com/api/data/v1/get"

CITY="" PAGE_SIZE="31" PAGE_NUMBER="1" FORMAT="json"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --city) CITY="$2"; shift 2;;
    --pageSize) PAGE_SIZE="$2"; shift 2;;
    --pageNumber) PAGE_NUMBER="$2"; shift 2;;
    --format) FORMAT="$2"; shift 2;;
    *) shift;;
  esac
done

# 构造请求参数
if [[ -n "$CITY" ]]; then
  COLUMNS="CITYNAME,DIM_DATE,V0,V89,V92,V95,ZDE92,ZDE95,QE92,QE95"
else
  COLUMNS="CITYNAME,DIM_DATE,V0,V89,V92,V95,ZDE92,ZDE95"
fi

CURL_ARGS=(
  -s -G "$API_URL"
  --data-urlencode "reportName=RPTA_WEB_YJ_JH"
  --data-urlencode "columns=${COLUMNS}"
  --data-urlencode "sortColumns=DIM_DATE,CITYNAME"
  --data-urlencode "sortTypes=-1,1"
  --data-urlencode "pageSize=${PAGE_SIZE}"
  --data-urlencode "pageNumber=${PAGE_NUMBER}"
  --data-urlencode "source=WEB"
  -H "Referer: https://data.eastmoney.com/cjsj/oil_default.html"
  -H "User-Agent: Mozilla/5.0"
)

if [[ -n "$CITY" ]]; then
  CURL_ARGS+=(--data-urlencode "filter=(CITYNAME=\"${CITY}\")")
fi

RESP=$(curl "${CURL_ARGS[@]}")

# 检查返回
SUCCESS=$(echo "$RESP" | python3 -c "import json,sys;print(json.load(sys.stdin).get('success',False))")
if [[ "$SUCCESS" != "True" ]]; then
  echo "查询失败:" >&2
  echo "$RESP" | python3 -m json.tool >&2
  exit 1
fi

if [[ "$FORMAT" == "table" ]]; then
  echo "$RESP" | python3 -c "
import json, sys
resp = json.load(sys.stdin)
items = resp.get('result', {}).get('data', [])
if not items:
    print('无数据')
    sys.exit(0)

date = items[0].get('DIM_DATE', '')[:10]
print(f'调价日期: {date}')
print()

has_change = 'QE92' in items[0]

if has_change:
    header = f'{\"省份\":<6} {\"92号\":>7} {\"95号\":>7} {\"柴油\":>7} {\"92涨跌\":>7} {\"95涨跌\":>7}'
else:
    header = f'{\"省份\":<6} {\"89号\":>7} {\"92号\":>7} {\"95号\":>7} {\"柴油\":>7}'

print(header)
print('─' * len(header.encode('gbk', errors='replace')))

for item in items:
    city = item.get('CITYNAME', '')
    if has_change:
        v92 = item.get('V92', 0) or 0
        v95 = item.get('V95', 0) or 0
        v0  = item.get('V0', 0) or 0
        z92 = item.get('ZDE92', 0) or 0
        z95 = item.get('ZDE95', 0) or 0
        z92s = f'+{z92:.2f}' if z92 > 0 else f'{z92:.2f}'
        z95s = f'+{z95:.2f}' if z95 > 0 else f'{z95:.2f}'
        print(f'{city:<6} {v92:>7.2f} {v95:>7.2f} {v0:>7.2f} {z92s:>7} {z95s:>7}')
    else:
        v89 = item.get('V89', 0) or 0
        v92 = item.get('V92', 0) or 0
        v95 = item.get('V95', 0) or 0
        v0  = item.get('V0', 0) or 0
        print(f'{city:<6} {v89:>7.2f} {v92:>7.2f} {v95:>7.2f} {v0:>7.2f}')
"
else
  echo "$RESP" | python3 -c "
import json, sys
resp = json.load(sys.stdin)
data = resp.get('result', {}).get('data', [])
print(json.dumps(data, ensure_ascii=False, indent=2))
"
fi
