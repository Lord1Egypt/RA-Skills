# Live Run Notes

Validated with real user tokens and real workflow executions.

## End-to-end validated sequence

The following sequence is now confirmed working in production:

1. Upload inbound/local files with `POST https://maibei.maybe.ai/api/trpc/imageGetUploadUrl`
2. PUT raw file bytes to returned `uploadUrl`
3. Run copy workflow
4. Run analyze workflow
5. Run audit workflow
6. Run font-audit workflow

## Upload step

Observed working request shape:

```json
{ "key": "superapp/uploads/<timestamp>-<filename>" }
```

Observed working response fields:

```json
{
  "result": {
    "data": {
      "uploadUrl": "https://maybe-static-...cos...",
      "url": "https://statics.maybe.ai/superapp/uploads/..."
    }
  }
}
```

Observed result:

- `PUT uploadUrl` returned `200`
- returned `url` worked as the public file URL for later workflows

## Copy workflow

Request succeeded with:

- artifact_id: `69ca226377efb8a1de743d34`
- workflow_id: `69ca238877efb8a1de743e3b`

Observed outputs:

- `copy_excel_flow` returned a scalar new sheet URL
- `copy_excel_url` returned `dataframe:copy_excel_url_data`

Recent observed result:

- new copied sheet: `https://www.maybe.ai/docs/spreadsheets/d/69ce1c80d30c7504d2e4d3ad`

## Analyze workflow

Request succeeded with:

- artifact_id: `69c245bca5e657510a37a6a2`
- workflow_id: `69ca2ce467a09db8deb16dc5`
- uploaded file rows shaped as `{ url, file_type, file_name }`
- copied sheet url in `variable:scalar:copy_excel_url`

Observed behavior:

- classified file types
- OCR/extracted text from images
- wrote results into worksheet `审核文件信息`
- appended new rows when `file_url` values were new

Recent observed success payload:

```json
{
  "success": true,
  "spreadsheet_url": "https://www.maybe.ai/docs/spreadsheets/d/69ce1c80d30c7504d2e4d3ad?gid=0",
  "spreadsheet_id": "69ce1c80d30c7504d2e4d3ad",
  "worksheet": "审核文件信息",
  "message": "Updated 0 cells in 0 rows (matched 0 lookup keys, 2 unmatched), 2 new rows appended. Lookup columns: [file_url]"
}
```

## Audit workflow

Request succeeded with:

- artifact_id: `69c6582612aa26396bd2ace7`
- workflow_id: `69ca2e1d45c46dbe33ffcd49`
- variables:
  - `variable:scalar:copy_excel_url`
  - `variable:scalar:excel_url`
  - `variable:dataframe:copy_excel_url_data`

Observed behavior:

- extracted `copy_excel_url`
- ran image/context/audio/video/internal/industry audit branches
- returned `no result data` for audio/video when no matching data existed
- surfaced high-risk findings in internal and industry rules

Recent observed findings:

- screenshot/login-style content flagged as context mismatch / possible sensitive information leakage
- image with no OCR text flagged as unable to audit / missing mandatory information
- internal and industry rules both returned `BLOCK` on problematic rows

## Font-audit workflow

Request succeeded with:

- artifact_id: `69ccb9d584cf626fe68ff7ea`
- workflow detail returned workflow_id: `69ce02be964d081c20ea6c94`
- variable:
  - `variable:scalar:copy_excel_url`

Observed behavior:

- read data from the working Excel file
- processed image rows with extracted text
- skipped actual font auditing for rows with no text
- wrote results into worksheet `第三方字体鉴权`

Recent observed success payload:

```json
{
  "success": true,
  "spreadsheet_url": "https://www.maybe.ai/docs/spreadsheets/d/69ce1c80d30c7504d2e4d3ad?gid=2",
  "spreadsheet_id": "69ce1c80d30c7504d2e4d3ad",
  "worksheet": "第三方字体鉴权",
  "message": "Updated 0 cells in 0 rows (matched 0 lookup keys, 7 unmatched), 7 new rows appended. Lookup columns: [file_url]"
}
```

Observed font results on a live screenshot:

- `San Francisco (SF Pro Text Semi-Bold)`
- `San Francisco (SF Pro Text Regular)`
- `auth_tag`: `商用或系统字体`
- `audit_result`: `PASS`
- `has_non_free_fonts`: `true`
- `non_free_fonts`: `San Francisco (Apple System Font)`

## Practical conclusion

The full API-first pipeline is now validated end-to-end, including upload, copy, analyze, audit, and font-audit.
If future runs fail, first check:

- expired token or wrong `user-id`
- changed upload API response shape
- changed workflow artifact ids
- changed workflow detail ids returned by `workflow/detail/public`
