# Lead pool + user helpers (curl)

Use `CURL_HEADERS` from [find-leads.md](./find-leads.md).

## Lead pool list (same as `search-leads-pool` tool)

`GET /api/uc/v1/crm/leads/list` with pool filters:

- `type=5`
- `leadPoolId=-1`
- `convertedStatus=0`
- plus `page`, `size`, optional `searchValue`, optional `sort` / `sortType`

```bash
curl -sS --get "https://uc.marketup.cn/api/uc/v1/crm/leads/list" \
  "${CURL_HEADERS[@]}" \
  --data-urlencode "page=1" \
  --data-urlencode "size=10" \
  --data-urlencode "type=5" \
  --data-urlencode "leadPoolId=-1" \
  --data-urlencode "convertedStatus=0" \
  --data-urlencode "searchValue=${SEARCH_VALUE:-}"
```

## Lead pool config

`GET /api/uc/v1/leads/leadPool/-1`

```bash
curl -sS --get "https://uc.marketup.cn/api/uc/v1/leads/leadPool/-1" \
  "${CURL_HEADERS[@]}"
```

## Current user

`GET /api/uc-open/v1/user/currentUser`

```bash
curl -sS --get "https://uc.marketup.cn/api/uc-open/v1/user/currentUser" \
  "${CURL_HEADERS[@]}"
```

## Team company users (search)

`GET /api/uc-open/v1/company/user/team/list` — flat query keys (no `companyUserRPO.` prefix), e.g. `page`, `size`, `sort`, `sortType`, `searchValue`, `leadsManageType`.

```bash
curl -sS --get "https://uc.marketup.cn/api/uc-open/v1/company/user/team/list" \
  "${CURL_HEADERS[@]}" \
  --data-urlencode "page=1" \
  --data-urlencode "size=10" \
  --data-urlencode "searchValue=${SEARCH_VALUE}" \
  --data-urlencode "leadsManageType=SALE"
```
