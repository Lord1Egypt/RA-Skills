# ADP CLI Error Handling Guide for Agent

> This document defines all error types, exit codes, and recommended Agent recovery strategies.

## Error Output Format

Errors are output to **stderr**. In JSON mode (`--json` or non-TTY), the format is:

```json
{
  "type": "ERROR_TYPE",
  "message": "Human-readable error description",
  "fix": "Suggested fix action",
  "retryable": true,
  "details": {"context": "command_name"}
}
```

Key field for Agent: **`retryable`** — if `true`, the Agent should retry with exponential backoff.

---

## Error Types and Agent Recovery Strategies

### AUTH_ERROR (Exit Code: 4)

**Triggers:** Invalid API Key, expired API Key, authentication failed, 401/403 HTTP status.

**Agent strategy:**
1. Run `adp config get` to check if API Key is configured
2. If not configured → prompt user to provide API Key
3. If configured but invalid → prompt user to verify/update API Key
4. Do NOT retry automatically — authentication errors are not transient

### PARAM_ERROR (Exit Code: 2)

**Triggers:** Invalid JSON format, unsupported file type, invalid parameter value, missing required parameter.

**Agent strategy:**
1. Read the `message` field to identify which parameter is wrong
2. Fix the parameter and retry
3. Common fixes:
   - JSON parse error → validate JSON syntax in `--extract-fields` or `--long-doc-config`
   - Unsupported file type → check file extension is one of: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .pdf, .doc, .docx, .xls, .xlsx
   - Invalid enum value → check `--parse-mode` is one of: `advance`, `standard`, `agentic`

### RESOURCE_ERROR (Exit Code: 3)

**Triggers:** app-id not found, file not found, task not found, version not found, 404 HTTP status.

**Agent strategy:**
1. If app-id not found → run `adp app-id list` to refresh, then retry with correct app-id
2. If local file not found → verify file path exists
3. If task not found → the task_id may be incorrect or expired
4. Do NOT retry with same parameters

### NETWORK_ERROR (Exit Code: 1)

**Triggers:** Connection refused, DNS lookup failure, timeout, TLS handshake error.

**Agent strategy:**
1. This is retryable — retry with exponential backoff (2s, 4s, 8s)
2. Max 3 retries
3. If still failing → check network connectivity, verify `--api-base-url` is correct
4. Consider using `--timeout` with a larger value for slow networks

### API_ERROR (Exit Code: 1)

**Triggers:** Rate limiting (429), server error (5xx), generic API failures.

**Agent strategy:**
1. If 429 (rate limited) → wait 30 seconds, then retry
2. If 5xx → retry with exponential backoff, max 3 attempts
3. If persistent → suggest user contact support (global_product@laiye.com)

### CONFLICT_ERROR (Exit Code: 5)

**Triggers:** Resource already exists, duplicate app name.

**Agent strategy:**
1. If creating custom-app with duplicate name → use a different `--app-name`
2. If updating → check current state with `custom-app get-config` first
3. Do NOT retry with same parameters

### SYSTEM_ERROR (Exit Code: 1)

**Triggers:** Unexpected internal errors.

**Agent strategy:**
1. Log the error message for diagnostics
2. Do NOT retry — these are typically programming errors or unexpected states
3. Suggest user report the issue

---

## Exit Codes Quick Reference

| Code | Name | Retryable | Agent Action |
|------|------|-----------|--------------|
| 0 | Success | — | Proceed normally |
| 1 | General Error | Depends on type | Check `retryable` field in error JSON |
| 2 | Parameter Error | No | Fix parameter and retry |
| 3 | Resource Not Found | No | Verify resource ID/path |
| 4 | Permission Denied | No | Prompt user for credentials |
| 5 | Conflict | No | Change conflicting parameter |
| 6 | Partial Failure | — | Check batch summary for per-file status |

---

## Batch Processing Error Handling

Exit code `6` (Partial Failure) means some files succeeded and some failed in a batch.

**Agent strategy:**
1. Parse the stdout summary JSON
2. For files with `"status": "failed"`, read the `error` field
3. Decide per-file: retry failed files individually, or report to user
4. Use `--retry N` flag to enable automatic retry with exponential backoff at CLI level

---

## Credit-Related Errors

When credit balance is insufficient, the API returns a specific error. Agent should:
1. Run `adp credit` to check remaining balance
2. Report the balance to user
3. Provide billing reference:
   - Document parsing: 0.5 credits/page
   - Invoice/receipt extraction: 1.5 credits/page
   - Order extraction: 1.5 credits/page
   - Custom extraction: 1 credit/page

---

## Timeout Handling

Default timeout is 900 seconds (15 minutes). For large documents or slow networks:

**Agent strategy:**
1. If timeout occurs on sync processing → retry with `--async` mode
2. For files >20MB or >200 pages → always use `--async`
3. Increase timeout with `--timeout 1800` if needed
