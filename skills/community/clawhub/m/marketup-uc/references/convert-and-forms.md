# Form fields + lead → account (curl)

Use `CURL_HEADERS` from [find-leads.md](./find-leads.md).

## Query form fields

`GET /api/uc-open/formField/queryCurrentFields?marketEntityType=<n>`

| Intent | `marketEntityType` |
| --- | ---: |
| 线索 | `0` |
| 客户 | `2` |
| 联系人 | `3` |

```bash
curl -sS --get "https://uc.marketup.cn/api/uc-open/formField/queryCurrentFields" \
  "${CURL_HEADERS[@]}" \
  --data-urlencode "marketEntityType=0"
```

## Convert lead to account

`POST /api/uc/v1/crm/leads/leadsConvertAccount`  
`Content-Type: application/json`

Body keys: `leadsId`, `accountInfo` (object, keys are **numeric formFieldId strings**), `contacts` (array of such objects), `companyUserId`.

```bash
curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/crm/leads/leadsConvertAccount" \
  "${CURL_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d @convert-lead.json
```

Example `convert-lead.json` (replace ids with real formFieldIds from the two `queryCurrentFields` calls):

```json
{
  "leadsId": 12345,
  "accountInfo": { "200001": "公司名", "200002": "13800000000" },
  "contacts": [{ "300001": "张三", "300002": "13800000000" }],
  "companyUserId": 999
}
```
