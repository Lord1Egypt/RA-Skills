# Accounts query reference

Use shared headers pattern from `find-leads.md`:

```bash
CURL_HEADERS=(-H "Authorization: $MARKETUP_API_KEY" -H "Referer: MarketUP-Skills")
```

## 1) Account detail

`GET /api/uc/v1/account/accountDetail/{accountId}`

```bash
ACCOUNT_ID=12345
curl -sS --get "https://uc.marketup.cn/api/uc/v1/account/accountDetail/${ACCOUNT_ID}" \
  "${CURL_HEADERS[@]}"
```

## 2) Account list

`GET /api/uc-open/v1/account/list`

Use flat query params (no `rpo.` prefix):

- `page`, `size`
- `searchValue`
- `stageId`
- `accountId`
- `companyUserId`
- `sort`, `sortType`
- `multipleGroupAdvancedQueryFilter`

```bash
curl -sS --get "https://uc.marketup.cn/api/uc-open/v1/account/list" \
  "${CURL_HEADERS[@]}" \
  --data-urlencode "page=1" \
  --data-urlencode "size=10" \
  --data-urlencode "searchValue=${SEARCH_VALUE}" \
  --data-urlencode "companyUserId=${COMPANY_USER_ID}"
```

## 3) Advanced filter account list

```bash
ADVANCED_FILTER='{"relation":"AND","groups":[]}'
curl -sS --get "https://uc.marketup.cn/api/uc-open/v1/account/list" \
  "${CURL_HEADERS[@]}" \
  --data-urlencode "page=1" \
  --data-urlencode "size=10" \
  --data-urlencode "multipleGroupAdvancedQueryFilter=${ADVANCED_FILTER}"
```

## 4) jq helpers

```bash
jq '{
  code,
  message,
  total: (.data.totalElements // .total // 0),
  accounts: ((.data.content // []) | map({
    accountId,
    accountName,
    ownerName,
    cellPhone,
    email,
    tagNames,
    contactNames,
    notFollowedUpDay,
    createTime
  }))
}'
```
