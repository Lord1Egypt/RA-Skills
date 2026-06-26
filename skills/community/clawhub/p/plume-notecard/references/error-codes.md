# Error Codes Reference

## API Response Codes

| code | Type | Description | Suggested Handling |
|------|------|-------------|-------------------|
| `SUCCESS` | Success | Operation successful | - |
| `CREATED` | Success | Resource created successfully | - |
| `VALIDATION_ERROR` | Client Error | Parameter validation failed | Check required parameters |
| `UNAUTHORIZED` | Auth Error | API Key invalid or missing | Check PLUME_API_KEY |
| `FORBIDDEN` | Permission Error | API Key disabled | Contact admin to enable Key |
| `NOT_FOUND` | Client Error | Resource not found | Check if task_id is correct |
| `INSUFFICIENT_CREDITS` | Business Error | Insufficient credits | Prompt user to top up |
| `CREDITS_ACCOUNT_NOT_FOUND` | Business Error | Credits account not found | Contact admin to create account |
| `CONCURRENT_MODIFICATION` | Concurrent Conflict | Optimistic lock conflict | Auto retry |
| `UPLOAD_FAILED` | Server Error | R2 upload failed | Retry |
| `INTERNAL_ERROR` | Server Error | Internal error | Retry or contact admin |

## Task Status Codes

| status | Name | Description | Is Terminal |
|--------|------|-------------|-------------|
| 1 | Initialized | Task created, waiting to be processed | No |
| 2 | Processing | Executor pulled,正在处理 | No |
| 3 | Success | Task completed, result field contains result | Yes |
| 4 | Failed | Task execution failed | Yes |
| 5 | Timeout | Task processing timeout (default 1 hour) | Yes |
| 6 | Cancelled | Task was cancelled | Yes |

## Polling Recommendations

- Polling interval: 3 seconds
- Max polling count: 60 times (total 3 minutes)
- Terminal state判断: `status >= 3` means task has ended
- Success判断: `status == 3`, result in `data.result`
- Failure判断: `status >= 4`, can explain reason to user

## Common Error Scenarios

### 1. API Key Not Configured
```
Error: PLUME_API_KEY environment variable not set
Handling: Remind user to configure PLUME_API_KEY in OpenClaw config or environment variable
```

### 2. Insufficient Credits
```json
{ "success": false, "code": "INSUFFICIENT_CREDITS" }
Handling: Inform user of insufficient credits, suggest topping up via Portal
```

### 3. Image Upload Failed
```json
{ "success": false, "code": "VALIDATION_ERROR", "error": { "details": { "file": "..." } } }
Possible causes: File too large (>20MB), unsupported format, corrupted file
```

### 4. Task Timeout
```
Still not completed after polling for 3 minutes
Handling: Inform user task processing time is long, suggest checking again later
```
