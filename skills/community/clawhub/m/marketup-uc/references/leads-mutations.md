# Leads write APIs (curl)

Use the same `CURL_HEADERS` pattern as [find-leads.md](./find-leads.md). JSON bodies: prefer `-d @payload.json` for real shells.

## Create lead

`POST /api/uc/v1/crm/leads/saveLeads`  
`Content-Type: application/json`

Minimal shape (extend with assign fields as in `SKILL.md` §3):

```json
{
  "type": 1,
  "leads": { "17263687": "张三", "29028938": "13800138000" },
  "coverInfo": false,
  "genCompanyAccount": false,
  "notAssign": false,
  "assignType": null,
  "autoAssign": false,
  "ownerCompanyUserId": null,
  "sourceChannelId": null,
  "remark": null,
  "fileUrl": null,
  "formFieldMappers": null,
  "companyAccountId": null,
  "grade": null,
  "tagIds": null,
  "leadsSaveParams": null,
  "tagNames": null,
  "ownerAccount": null,
  "companyAccount": null,
  "operator": null,
  "validateValue": null
}
```

```bash
curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/crm/leads/saveLeads" \
  "${CURL_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d @create-lead.json
```

## Modify one profile field

`POST /api/uc/v1/crm/leads/modify/profileData?leadsId=<id>`  
Body: `{ "formFieldId": <number>, "value": "<string>" }`

```bash
curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/crm/leads/modify/profileData?leadsId=${LEADS_ID}" \
  "${CURL_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{"formFieldId":12345,"value":"new value"}'
```

## Add follow-up (remark)

`POST /api/uc/v1/crm/leads/addOrUpdate/remark`

```bash
curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/crm/leads/addOrUpdate/remark" \
  "${CURL_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d "{\"leadsId\":${LEADS_ID},\"historyId\":null,\"remark\":\"跟进内容\",\"attachments\":null,\"type_id\":null}"
```

## Assign or unassign owner

`POST /api/uc/v1/crm/leads/assign?leadsId=<id>`  
Query: add `companyUserId=<id>` to assign; omit it to unassign.  
Body: `{ "reason": "...", "type": null }`

```bash
# assign
curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/crm/leads/assign?leadsId=${LEADS_ID}&companyUserId=${USER_ID}" \
  "${CURL_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{"reason":null,"type":null}'

# unassign
curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/crm/leads/assign?leadsId=${LEADS_ID}" \
  "${CURL_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{"reason":null,"type":null}'
```

## Add / remove tag (query params)

```bash
curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/crm/leads/addTag?leadsId=${LEADS_ID}&tagId=${TAG_ID}" \
  "${CURL_HEADERS[@]}"

curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/crm/leads/deleteTag?leadsId=${LEADS_ID}&tagId=${TAG_ID}" \
  "${CURL_HEADERS[@]}"
```

## Receive from pool

`POST /api/uc/v1/crm/leads/receive?leadsId=<id>`

```bash
curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/crm/leads/receive?leadsId=${LEADS_ID}" \
  "${CURL_HEADERS[@]}"
```

## Return to pool (discard)

`POST /api/uc/v1/crm/leads/discard`

```bash
curl -sS -X POST "https://uc.marketup.cn/api/uc/v1/crm/leads/discard" \
  "${CURL_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d "{\"leadsId\":${LEADS_ID},\"returnLead\":true,\"reason\":null,\"giveUpReasonId\":null,\"tagId\":null,\"attachments\":null}"
```
