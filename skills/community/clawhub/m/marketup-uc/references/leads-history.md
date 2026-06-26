# Lead history APIs (GET + flat query)

Use `CURL_HEADERS` from [find-leads.md](./find-leads.md).

All three endpoints use **flat** query keys (no `rpo.` prefix): `page`, `size`, `sort`, `sortType`, `startTime`, `endTime`, `historyTypeEnum`, `id` (the entity id, e.g. `leadsId`), `appId`, `ocuid`, `cursor`, `behaviorCodes`, `ascending`. Omit unused.

## Follow-up / remark history

`GET /api/uc/v1/crm/historyRecord/remarkHistoryList`

```bash
curl -sS --get "https://uc.marketup.cn/api/uc/v1/crm/historyRecord/remarkHistoryList" \
  "${CURL_HEADERS[@]}" \
  --data-urlencode "page=1" \
  --data-urlencode "size=50" \
  --data-urlencode "historyTypeEnum=LEADS_HISTORY" \
  --data-urlencode "id=${LEADS_ID}" \
  --data-urlencode "startTime=2020-01-01 00:00"
```

## Field change history

`GET /api/uc/v1/crm/historyRecord/entityChangeHistoryList`

```bash
curl -sS --get "https://uc.marketup.cn/api/uc/v1/crm/historyRecord/entityChangeHistoryList" \
  "${CURL_HEADERS[@]}" \
  --data-urlencode "page=1" \
  --data-urlencode "size=50" \
  --data-urlencode "historyTypeEnum=LEADS_HISTORY" \
  --data-urlencode "id=${LEADS_ID}"
```

## Behavior records

`GET /api/uc/v1/crm/historyRecord/behaviorRecordList`

```bash
curl -sS --get "https://uc.marketup.cn/api/uc/v1/crm/historyRecord/behaviorRecordList" \
  "${CURL_HEADERS[@]}" \
  --data-urlencode "page=1" \
  --data-urlencode "size=50" \
  --data-urlencode "historyTypeEnum=LEADS_HISTORY" \
  --data-urlencode "id=${LEADS_ID}"
```

## jq: total + first page slice

```bash
jq '{ code, message, total: (.data.totalElements // 0), sample: (.data.content // [])[:5] }'
```
