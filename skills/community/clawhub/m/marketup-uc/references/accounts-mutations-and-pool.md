# Accounts mutation + pool reference

Use shared headers pattern from `find-leads.md`:

```bash
CURL_HEADERS=(-H "Authorization: $MARKETUP_API_KEY" -H "Referer: MarketUP-Skills")
```

## 1) Create account

`POST /api/uc/v1/account/saveV2`

Body shape:

- `accountInfo`: object keyed by ACCOUNT `formFieldId` numeric strings
- `contacts`: array of CONTACT-field objects
- `accountType`: optional (`DEFAULT_TYPE` / `ABM_TYPE`)

```bash
curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/account/saveV2" \
  "${CURL_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d @create-account.json
```

Example `create-account.json`:

```json
{
  "accountInfo": {
    "200001": "上海某某科技有限公司",
    "200002": "021-12345678"
  },
  "contacts": [
    {
      "300001": "张三",
      "300002": "13800000000"
    }
  ],
  "accountType": "DEFAULT_TYPE"
}
```

## 2) Modify one account field

`POST /api/uc/v1/account/modify/profileData?accountId=<id>`

Body:

```json
{ "formFieldId": 200001, "value": "new value" }
```

```bash
curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/account/modify/profileData?accountId=${ACCOUNT_ID}" \
  "${CURL_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{"formFieldId":200001,"value":"new value"}'
```

## 3) Account pool config

`GET /api/uc/v1/account/accountPool/-1`

```bash
curl -sS --get "https://uc.marketup.cn/api/uc/v1/account/accountPool/-1" \
  "${CURL_HEADERS[@]}"
```

Useful fields:

- `visibleRule` (`ALL_ACCOUNT` / `NONE_ACCOUNT`)
- `receiveLimit`
- `autoRecycle`
- `executeTime`
- `accountMinCreateTime`
- `recycleRules[].rules[].{stage,day,hour,state}`
