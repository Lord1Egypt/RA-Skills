---
name: integration-microsoft-365
description: Microsoft Excel + SharePoint nodes. OAuth2 credential setup, drive + item ID quirks.
user-invocable: false
---

# Microsoft 365 (Excel + SharePoint)

## Node types

- `n8n-nodes-base.microsoftExcel` — Excel workbook operations.
- `n8n-nodes-base.microsoftOneDrive` — file CRUD on OneDrive.
- `n8n-nodes-base.microsoftSharepoint` — SharePoint list / file ops.
- `n8n-nodes-base.microsoftOutlook` — email + calendar.

## Credential type

`microsoftOAuth2Api` (or per-app variants like `microsoftExcelOAuth2Api`, `microsoftOutlookOAuth2Api` — check the specific node's docs).

For the actual setup flow, see [`skills/manage-credentials.md`](../../manage-credentials.md). Both Path A (helper POSTs from `.env.<env>`) and Path B (link to a credential created in the n8n UI) work.

## OAuth quirks

- Microsoft OAuth requires admin consent for app-only / delegated permissions on tenant-owned data. Path B is often easier here because the n8n UI walks the user through the consent dance.
- The OAuth token refresh window can be short for personal accounts; production credentials are usually app-registration-based.

## Drive + item IDs

Excel and SharePoint nodes need both a drive ID and a file ID. Store these in your env YAML (NOT in the template):

```yaml
sharepoint:
  driveId: "b!abc..."
  reportFolderId: "01ABCD..."
```

Then in your template:

```json
{
  "type": "n8n-nodes-base.microsoftExcel",
  "parameters": {
    "driveId": "{{@env:sharepoint.driveId}}",
    "fileId": "{{@env:sharepoint.reportFolderId}}"
  }
}
```

Different envs (dev/prod) typically have different IDs; the env layered config keeps templates env-agnostic.

## Regional endpoints

Some Microsoft tenants are in non-default regions. The `Base URL` field on the credential lets you point at the right region (e.g. `https://graph.microsoft.us` for GCC).
