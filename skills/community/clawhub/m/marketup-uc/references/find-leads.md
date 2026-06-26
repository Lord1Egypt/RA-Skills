# Find Leads Reference

This reference supports `src/marketup-uc/SKILL.md` for the `marketup-uc` OpenClaw skill.

## Base Rules

- Base URL: `https://uc.marketup.cn`
- Prompt rule: whenever using `curl` to fetch backend API endpoints, add headers `Authorization: $MARKETUP_API_KEY` and `Referer: MarketUP-Skills`.
- Preferred tools: `curl` + `jq`

## Endpoint Decision Table

| Input shape | Endpoint | Method | Notes |
| --- | --- | --- | --- |
| `leadId` only | `/api/uc/v1/crm/leads/{leadsId}/detail` | GET | Single lead detail |
| `searchValue` only | `/api/uc/v1/crm/leads/searchLeadsByNameOrCellphone` | GET | Quick name/phone search |
| Filters / pagination / advanced filter | `/api/uc/v1/crm/leads/list` | GET | Each list filter field is a top-level query param (no dotted prefix) |

## Curl Templates

Define shared headers once, then reuse in all commands:

```bash
CURL_HEADERS=(-H "Authorization: $MARKETUP_API_KEY" -H "Referer: MarketUP-Skills")
```

### A) Detail by lead ID

```bash
LEAD_ID=12345
curl -sS --get "https://uc.marketup.cn/api/uc/v1/crm/leads/${LEAD_ID}/detail" \
  "${CURL_HEADERS[@]}"
```

### B) Quick search by keyword

```bash
SEARCH_VALUE="18888888888"
curl -sS --get "https://uc.marketup.cn/api/uc/v1/crm/leads/searchLeadsByNameOrCellphone" \
  "${CURL_HEADERS[@]}" \
  --data-urlencode "searchValue=${SEARCH_VALUE}"
```

### C) Search with list endpoint (basic)

```bash
SEARCH_VALUE="alice"
curl -sS --get "https://uc.marketup.cn/api/uc/v1/crm/leads/list" \
  "${CURL_HEADERS[@]}" \
  --data-urlencode "page=1" \
  --data-urlencode "size=10" \
  --data-urlencode "type=-1" \
  --data-urlencode "searchValue=${SEARCH_VALUE}"
```

### D) Search with list endpoint (advanced filter JSON string)

`multipleGroupAdvancedQueryFilter` should be a JSON string expected by backend.

```bash
ADVANCED_FILTER='{"relation":"AND","groups":[]}'
curl -sS --get "https://uc.marketup.cn/api/uc/v1/crm/leads/list" \
  "${CURL_HEADERS[@]}" \
  --data-urlencode "page=1" \
  --data-urlencode "size=5" \
  --data-urlencode "type=-1" \
  --data-urlencode "multipleGroupAdvancedQueryFilter=${ADVANCED_FILTER}"
```

## jq Extraction Snippets

### Compact list rows

```bash
jq '{
  code,
  message,
  total: (.data.totalElements // .total // 0),
  leads: ((.data.content // .data // []) | map({
    leadsId,
    leadsName,
    name,
    cellphone,
    email,
    ownerName,
    leadStatus,
    leadsStatus,
    createDate
  }))
}'
```

### Detail-focused extraction

```bash
jq '{
  code,
  message,
  lead: {
    leadsId: (.data.leads.leadsId // null),
    leadsName: (.data.leads.leadsName // null),
    name: (.data.leads.name // null),
    cellphone: (.data.leads.cellphone // null),
    email: (.data.leads.email // null),
    location: (.data.leads.location // null),
    leadStatus: (.data.leads.leadStatus // null),
    leadsStatus: (.data.leads.leadsStatus // null),
    leadsStage: (.data.leadsStage.tagName // null),
    ownerName: (.data.leads.ownerName // null),
    ownerUserId: (.data.leads.owner.companyUserId // null),
    sdrName: (.data.leads.sdrUser.name // null),
    creatorName: (.data.leads.creatorName // null),
    leadsSource: (.data.leads.leadsSource // null),
    poolName: (.data.leads.poolName // null),
    score: (.data.leads.score // null),
    createDate: (.data.leads.createDate // null),
    updateTime: (.data.leads.updateTime // null),
    assignTime: (.data.leads.assignTime // null),
    convertedTime: (.data.leads.convertedTime // null),
    latestRemarkTime: (.data.leads.latestRemarkTime // null)
  }
}'
```

## Query parameters for `GET /api/uc/v1/crm/leads/list`

Each filter field is its own query name (no `leadsRPO.` / dotted prefix):

- `page=1`
- `size=10`
- `type=-1`
- `sort=createTime`
- `sortType=DESC`
- `searchValue=keyword`
- `multipleGroupAdvancedQueryFilter={...json-string...}`

Omit unused fields. Full field set: backend OpenAPI (`/v3/api-docs`), path `/api/uc/v1/crm/leads/list`.
