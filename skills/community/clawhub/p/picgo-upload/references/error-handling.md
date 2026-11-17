# Upload error triage

**One rule:** separate failures a retry can fix (network / 5xx) from failures it can't (login, quota, file type, path, config). Retry the former **at most once**; for the latter, guide the user to do one specific thing and do **not** loop.

## Triage table

| Failure | Typical signal | Handling |
|---|---|---|
| **Not logged in / session invalid** | `picgo cloud auth status` returns `logged_out` (exit 1) or `invalid` (exit 2); CLI upload error mentions login required / re-login required | Guide PicGo Cloud login (`picgo login <token>`, or ask the user to run `picgo login` in their own terminal). **Don't retry the upload blindly.** |
| **File type not allowed** | server message like `File extension is not allowed: .dmg` | Tell the user PicGo Cloud doesn't accept that type. Don't retry. Optionally suggest a different host. |
| **Quota exceeded / paid plan needed** | `Storage quota exceeded for plan free`, `plan_required` | Tell the user the free tier is used up and **guide them to upgrade at cloud.picgo.app**. Don't retry. |
| **Network / 5xx** | TLS error, timeout, connection reset, HTTP 500 | Transient — **retry at most once**, then report the failure. |
| **Config error (custom image hosting)** | auth/config error from a non-cloud image hosting (e.g. github token wrong) | Guide the user to check their image hosting config: `picgo set uploader <type>`. Don't retry. |
| **File not found** | `... does not exist`, gui-upload.mjs exit 1 | Re-check the path with the user. Don't retry. |
| **GUI server unreachable** | gui-upload.mjs exit 2 | Not an error to surface — fall back to the `picgo` CLI route. |
| **GUI auth required** | gui-upload.mjs exit 3 | Provide `--secret`, or fall back to the CLI route. |

## Important nuances

- `picgo cloud auth status` exit **3 (`error`)** means the login probe itself failed (usually network) — it is **not** the same as "logged out". Don't push the user to re-login on an `error`; treat it as transient (retry once).
- A token that's `invalid` gets cleared from local config the first time the server returns 401, so a second `auth status` may report `logged_out` instead of `invalid`. Both lead to the same action (guide login).
- On partial multi-file failures, report exactly which files failed and why — never silently drop results.
