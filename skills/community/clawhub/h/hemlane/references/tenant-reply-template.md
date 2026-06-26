Confirmed tenant reply mutation from HAR:
- `ODProspectiveTenantGroupMessageCreate`
- mutation field alias: `tenantGroupMessageAdd: tenantGroupMessageAdd2(input: $input)`
- input type: `TenantGroupMessageAdd2Input!`

Observed HAR-derived payload shape:
```json
{
  "input": {
    "tenantGroupId": "53cf1ff2-56d7-41e5-a0bd-9d3cc2a99aab",
    "body": "Good morning Tiffany, as discussed, it seems your $890 December payment bounced and was reversed by Hemlane. You may see a new request for it to be reprocessed in your Financials tab. Thanks!",
    "notifyImmediately": true,
    "isOwnerPrivate": false,
    "attachmentUrl": null
  }
}
```
Use `scripts/send_hemlane_tenant_reply.py` as the live sender wrapper for this workflow.
