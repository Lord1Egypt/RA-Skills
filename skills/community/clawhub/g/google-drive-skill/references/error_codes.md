# Google Drive Errors Reference

## HTTP Status Codes

| Code | Reason | Common Cause | Fix |
|------|--------|--------------|-----|
| 400 | Bad Request | Invalid field name, wrong MIME type, malformed query | Check `q` syntax, field names, and MIME strings |
| 401 | Unauthorized | Expired or missing credentials | Refresh token / regenerate service account key |
| 403 | Forbidden | Insufficient permissions on the file or Drive | Check sharing settings; ensure service account has access |
| 404 | Not Found | Wrong `fileId`, file deleted, `supportsAllDrives` missing | Verify ID from URL; add `supportsAllDrives=True` |
| 409 | Conflict | Duplicate file name conflict (rare) | Rename or check for existing file first |
| 429 | Too Many Requests | API quota exceeded | Exponential back-off and retry |
| 500 | Internal Server Error | Transient Google-side error | Retry with back-off |
| 503 | Service Unavailable | Drive temporarily unavailable | Retry with back-off |

## Drive API Error Reasons (inside 403 responses)

| Reason | Meaning |
|--------|---------|
| `appNotAuthorizedToFile` | App is not authorized to access this file |
| `domainPolicy` | File sharing blocked by org policy |
| `forbidden` | Authenticated user lacks permissions |
| `insufficientFilePermissions` | Read-only access on a write operation |
| `rateLimitExceeded` | Per-user or per-project rate limit hit |
| `sharingNotSupported` | Drive doesn't support sharing (e.g., shared drive restrictions) |
| `storageQuotaExceeded` | Drive or user storage quota full |

## Handling in Python

```python
from googleapiclient.errors import HttpError
import time

def with_retry(fn, max_attempts: int = 5):
    """Simple exponential back-off wrapper for Drive API calls."""
    for attempt in range(max_attempts):
        try:
            return fn()
        except HttpError as e:
            if e.resp.status in (429, 500, 503):
                wait = 2 ** attempt
                print(f"Rate-limited or server error, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Max retry attempts exceeded")
```

## Common Query (`q`) Syntax Errors

```
# Wrong — missing quotes around folder ID
q="FOLDER_ID in parents"

# Correct
q="'FOLDER_ID' in parents and trashed=false"

# Wrong — spaces in MIME type value
q="mimeType = 'application/vnd.google-apps.folder '"

# Correct
q="mimeType='application/vnd.google-apps.folder'"
```

## `supportsAllDrives` Requirement

Always pass `supportsAllDrives=True` and `includeItemsFromAllDrives=True` when files may reside in a **Shared Drive** (formerly Team Drive). Without these, the API returns 404 for Shared Drive files.
