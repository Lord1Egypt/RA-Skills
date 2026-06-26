# Protocol Notes

## Page

Target page:
- `https://maibei.maybe.ai/e-commerce/upload-audit-file`

Embedded source sheet:
- `https://www.maybe.ai/docs/spreadsheets/d/69c2400ea25ba20198828d73?gid=0`

## Front-end extracted config

```json
{
  "copyExcelArtifactId": "69ca226377efb8a1de743d34",
  "analyzeArtifactId": "69c245bca5e657510a37a6a2",
  "auditArtifactId": "69c6582612aa26396bd2ace7",
  "sourceExcelUrl": "https://www.maybe.ai/docs/spreadsheets/d/69c2400ea25ba20198828d73?gid=0",
  "historyStorageKey": "superapp:upload-audit-file:sheet_history:v1"
}
```

## Workflow service

Public workflow detail endpoint:
- `POST https://play-be.omnimcp.ai/api/v1/workflow/detail/public`
- body: `{ "artifact_id": "..." }`

Workflow run endpoint:
- `POST https://play-be.omnimcp.ai/api/v1/workflow/run`
- headers:
  - `Accept: text/event-stream`
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>`
  - `user-id: <user_id>`
- returns streamed events

Important request fields:

```json
{
  "artifact_id": "...",
  "interaction": true,
  "task": "",
  "task_id": "uuid",
  "workflow_id": "...",
  "variables": [],
  "metadata": {
    "case": "upload-audit-file",
    "title": "上传文件并审核"
  }
}
```

## Captured working examples

### 1. Copy source sheet

```json
{
  "artifact_id": "69ca226377efb8a1de743d34",
  "interaction": true,
  "task": "",
  "task_id": "7834c6b3-6f76-4415-b877-fc8945dc7c3d",
  "workflow_id": "69ca238877efb8a1de743e3b",
  "variables": [
    {
      "name": "variable:scalar:source_excel_url",
      "default_value": "https://www.maybe.ai/docs/spreadsheets/d/69c2400ea25ba20198828d73?gid=0"
    }
  ],
  "metadata": {
    "case": "upload-audit-file",
    "title": "上传文件并审核"
  }
}
```

### 2. Analyze uploaded files into the copied sheet

```json
{
  "artifact_id": "69c245bca5e657510a37a6a2",
  "interaction": true,
  "task": "",
  "task_id": "4d3b9ed5-00da-4fac-8cb5-684b6170f890",
  "workflow_id": "69ca2ce467a09db8deb16dc5",
  "variables": [
    {
      "name": "variable:dataframe:product_images",
      "default_value": [
        {
          "url": "https://statics.maybeai.cn/superapp/upload-audit-file/...jpg?imageMogr2/auto-orient/strip/thumbnail/3072x3072>/quality/95",
          "file_type": "image",
          "file_name": "光泽焕白系列_page-0001.jpg"
        }
      ]
    },
    {
      "name": "variable:scalar:copy_excel_url",
      "default_value": "https://www.maybe.ai/docs/spreadsheets/d/69ca5a223d9d52683626b454"
    }
  ],
  "metadata": {
    "case": "upload-audit-file",
    "title": "上传文件并审核"
  }
}
```

### 3. Audit the sheet

```json
{
  "artifact_id": "69c6582612aa26396bd2ace7",
  "interaction": true,
  "task": "",
  "task_id": "b827ed81-0d58-4f91-a5c9-abf875fdd8b9",
  "workflow_id": "69ca2e1d45c46dbe33ffcd49",
  "variables": [
    {
      "name": "variable:scalar:copy_excel_url",
      "default_value": "https://www.maybe.ai/docs/spreadsheets/d/69ca5a223d9d52683626b454"
    }
  ],
  "metadata": {
    "case": "upload-audit-file",
    "title": "上传文件并审核"
  }
}
```

Normalize captured URLs before replaying them:
- remove Slack angle brackets `<...>`
- remove HTML-escaped `&gt;`

## Variables

Analyze workflow writes uploaded media into the sheet using:
- `variable:dataframe:product_images`
- `variable:scalar:copy_excel_url`

Audit workflow accepts:
- `variable:scalar:copy_excel_url`
- `variable:scalar:excel_url`
- `variable:dataframe:copy_excel_url_data`

## Upload notes

The page code shows a tRPC upload mutation. Confirm actual payload encoding from browser requests before relying on automation.

Observed facts:
- `uploadImage` exists as a mutation path
- wrong payload shape returns validation errors for missing `key` and `base64`
- `uploadImages` path is not directly exposed as a tRPC procedure name on this host

## Validation shortcut

Token validity can be checked with:
- `GET https://www.maybe.ai/api/trpc/getVipInfo`
- headers: bearer token + user-id
