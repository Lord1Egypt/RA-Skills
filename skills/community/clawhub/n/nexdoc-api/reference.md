# NexDoc Design API — endpoint reference

Base URL `https://api.nexdoc.design` · header `Authorization: Bearer $NXD_API_KEY` · errors are `{"detail": "..."}`.

API keys are created at `https://app.nexdoc.design/keys` and use the `nxd_live_` prefix. Default key scopes: `files:rw`, `jobs:rw`, `runs:rw`.

## Auth

| Method | Path | Returns |
|--------|------|---------|
| `GET` | `/v1/auth/me` | `user_id`, `org_id`, `email`, `name`, `scopes` |
| `GET` | `/v1/auth/keys` | `{data:[{key_id, name, secret_prefix, created_at}]}` |
| `POST` | `/v1/auth/keys` `{name}` | `{key_id, secret_key}` — secret shown once |
| `DELETE` | `/v1/auth/keys/{key_id}` | `{key_id, revoked:true}` |

Do not create or revoke keys unless the user asks.

## Jobs

| Method | Path | Body | Returns |
|--------|------|------|---------|
| `POST` | `/v1/jobs` | `{name}` | **201** `{job_id, name, current_commit, created_at}` |
| `GET` | `/v1/jobs` | — | `{data:[{job_id, name, total_runs, viewer_url, created_at, …}]}` newest first, max 100 |
| `GET` | `/v1/jobs/{job_id}` | — | + `published_url`, `published_run_id`, `published_at`, `viewer_expires_at` |
| `DELETE` | `/v1/jobs/{job_id}` | — | `{job_id, deleted:true, runs_deleted_count}` (soft delete) |

## Runs

### `POST /v1/jobs/{job_id}/runs` → **202**

JSON body:

| Field | Type | Notes |
|-------|------|-------|
| `format` | string | Format slug. Always send it. |
| `instructions` | string | Design brief (create) or edit diff (update) |
| `content` | string | Source copy, markdown. `""` on updates that keep copy |
| `files` | string[] | `file_…` ids to place in the workspace |
| `assets` | `[{name, file_id}]` | Map a filename under `assets/` to a file id |
| `webhook_url` | string | Accepted and stored; completion delivery is not guaranteed — prefer `notify_email` or poll |
| `notify_email` | bool | Email the account owner when the run finishes (`completed` / `failed` / `cancelled`) |

Multipart fields: `format`, `instructions`, `content` (text **or** file part), repeated `files` (png/jpg/gif/pdf, stored immediately), optional `file_ids` (JSON array text), `assets` (JSON array text), `webhook_url`, `notify_email`.

Response `{job_id, run_id, status:"queued", notify_email, created_at}`.
`402` cannot start (no balance / past due) · `404` job or file · `503` enqueue failed.

Markdown image references whose basename matches an uploaded filename are rewritten to `assets/<filename>`.

### `GET /v1/jobs/{job_id}/runs/{run_id}`

`status`, `charge_usd`, `commit_hash`, `summary_diff`, `created_at`, `completed_at`, `notify_email`; on `completed`: `viewer_url`, `viewer_expires_at`; on `failed`: `error`, `log_tail`.

Status values: `queued`, `preparing`, `running`, `validating`, `uploading_outputs`, `completed`, `failed`, `cancelled`, `cancelling`.

### Other run endpoints

| Method | Path | Returns |
|--------|------|---------|
| `GET` | `/v1/jobs/{job_id}/runs` | `{job_id, data:[{run_id, status, commit_hash, charge_usd, created_at, completed_at}]}` (oldest first) |
| `POST` | `/v1/jobs/{job_id}/runs/{run_id}/notify-email` | `{notify_email:true}` while in progress; if already terminal, **sends now** (`sent:true`) unless already mailed |
| `POST` | `/v1/jobs/{job_id}/runs/{run_id}/cancel` | `{status:"cancelling"}`; `409` if already terminal |
| `DELETE` | `/v1/jobs/{job_id}/runs/{run_id}` | `{job_id, run_id, deleted:true}` |

## Files

Allowed `content_type`: `image/png`, `image/jpeg`, `image/gif`, `image/webp`, `image/heic`, `image/heif`, `image/svg+xml`, `application/pdf`, `text/markdown`, `text/plain`, `text/csv`, `application/json`. Anything else is `400`. The worker normalizes uploads per run (exotic images → PNG, PDF → page PNGs + text, CSV/JSON/MD/TXT → `content.md`). Office formats are not accepted yet.

| Method | Path | Body | Returns |
|--------|------|------|---------|
| `POST` | `/v1/files/request-upload` | `{filename, content_type, size_bytes}` | `{file_id, upload_url, uri, expires_at}` |
| `GET` | `/v1/files/{file_id}` | — | `status` (`pending_upload` → `ready`), `filename`, `content_type`, `size_bytes` |
| `DELETE` | `/v1/files/{file_id}` | — | `{file_id, deleted:true}` |

Presigned flow (use when bytes live on a server, when reusing one asset across many runs, or when the multipart body would be large):

```bash
UP=$(curl -sS -X POST "$API/v1/files/request-upload" -H "$AUTH" -H "Content-Type: application/json" \
  -d "{\"filename\":\"logo.png\",\"content_type\":\"image/png\",\"size_bytes\":$(wc -c < logo.png | tr -d ' ')}")
FILE_ID=$(echo "$UP" | jq -r .file_id)
curl -sS -X PUT "$(echo "$UP" | jq -r .upload_url)" -H "Content-Type: image/png" --data-binary @logo.png
# then in the JSON run body:
#   "files": ["$FILE_ID"], "assets": [{"name": "logo.png", "file_id": "$FILE_ID"}]
```

Otherwise multipart `files=@…` on `POST …/runs` is simpler.

## Export, publish, preview

| Method | Path | Body | Returns |
|--------|------|------|---------|
| `POST` | `/v1/jobs/{job_id}/export` | `{format:"pdf"\|"html"\|"png", run_id?}` | `{job_id, format, run_id, commit_hash, download_url, expires_at}` (~1 hour). `html` is a ZIP of the site; `png` is a ZIP of PNG pages/slides/artboards |
| `POST` | `/v1/jobs/{job_id}/publish` | `{run_id?}` | `{public_url, run_id, commit_hash}` — only on explicit user request |
| `POST` | `/v1/jobs/{job_id}/unpublish` | — | `{job_id, unpublished:true}` |
| `GET` | `/v1/jobs/{job_id}/viewer/session` | — | `{viewer_url, expires_at}` — 24 hours, remint anytime |
| `GET` | `/v1/jobs/{job_id}/viewer/resume` | — | Signed-in visitors receive a fresh preview token (expired-token recovery) |
| `PATCH` | `/v1/jobs/{job_id}/nodes` | `{node_id, content}` | Hot-edit one text node |

`run_id` omitted = latest completed run.

## Credits

| Method | Path | Notes |
|--------|------|-------|
| `GET` | `/v1/credits` | `balance_usd`, `free_balance_usd`, `paid_balance_usd`, `subscription_balance_usd`, `plan`, `concurrent_run_limit`, `past_due`, `outstanding_usd`, `auto_topup_enabled`, `threshold_usd`, `topup_usd`, `monthly_max_usd`, `has_payment_method`, `spent_usd`, `job_count`, `run_count`, `storage_bytes`, `daily_storage_cost_usd`, `monthly_storage_cost_usd`, `storage_spent_usd` |
| `GET` | `/v1/credits/ledger` | `{data:[...], storage?:{kind,amount_usd,note}, meta:{page, per_page, total_count}}`. Query `page` (default 1), `per_page` (default 50, max 100). `storage` is a lifetime sum, not a per-day row. |
| `POST` | `/v1/credits/checkout` `{amount_usd}` | Stripe Checkout URL; whole dollars, minimum $10 |
| `POST` | `/v1/billing/subscribe` | Stripe Checkout for Pro ($20/mo). Human-driven. |
| `GET` | `/v1/billing/portal` | Stripe customer portal `{url}` |

Billing is human-driven. Surface `balance_usd` and `https://app.nexdoc.design`; do not start checkout on the user's behalf unless asked.

## Formats

Web `landing-page` `link-in-bio` `portfolio` `lookbook` · Slides `slide-deck` `presentation` `pitch-deck` · Print `invoice` `receipt` `resume` `cv` `cover-letter` `proposal` `case-study` `report` `contract` `nda` `certificate` `whitepaper` `brochure` `menu` `poster` · Fixed canvas `social-card` `og-image` `banner` `business-card` `ticket` `boarding-pass` `coupon` `voucher` `invitation` · Other `email-newsletter` `infographic` `timeline` `roadmap` `org-chart` `dashboard`
