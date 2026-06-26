# LDR API Reference

This document describes the Local Deep Research (LDR) API endpoints used by this skill.

## Base URL

Default: `http://127.0.0.1:5000`  
Configurable via `LDR_BASE_URL` environment variable.

## Authentication (session + CSRF)

LDR uses **session-cookie authentication with CSRF protection**; it does **not** use HTTP Basic Auth. A proper login flow is required before calling the research API:

1. **GET** the login page (e.g. `/auth/login`) to obtain the session cookie and CSRF token (e.g. from a hidden form field `csrf_token` or `_csrf`).
2. **POST** the login form with `username`, `password`, and the CSRF token (typically `application/x-www-form-urlencoded`).
3. Use the session cookie for all subsequent requests. For state-changing **POST** requests (e.g. `/research/api/start`), send the CSRF token in a header (e.g. `X-CSRFToken`) if the server expects it.

Credentials are for **local LDR only** and must be provided via environment variables or a local `.env` file (never in committed config). The skill script implements this flow automatically.

| Env var | Purpose |
|--------|---------|
| `LDR_SERVICE_USER` / `LDR_USERNAME` | LDR account username |
| `LDR_SERVICE_PASSWORD` / `LDR_PASSWORD` | LDR account password |
| `LDR_LOGIN_URL` | Login page URL (default: `$LDR_BASE_URL/auth/login`) |

---

## Endpoints

### POST /research/api/start

Start a new research job. Requires an established session (and CSRF token for POST).

**Request Body:**
```json
{
  "query": "string (required)",
  "mode": "quick|detailed (optional, default: detailed)",
  "language": "string (optional)",
  "search_tool": "searxng|auto|local_all (optional, default: auto)",
  "iterations": "number (optional)",
  "questions_per_iteration": "number (optional)",
  "max_results": "number (optional)"
}
```

**`mode`** — Research output type:
- **`quick`** — Quick Summary: fewer cycles, shorter output, faster run.
- **`detailed`** — Detailed Report: full multi-cycle research, full markdown report and citations.

**`language`** — Output language for the report/summary. ISO 639-1 code (e.g. `en`, `es`, `fr`, `de`, `zh`, `ja`). Omit or leave empty for LDR default (often English).

**Response (200 OK):**
```json
{
  "research_id": "uuid-string",
  "mode": "detailed",
  "search_tool": "auto",
  "submitted_at": "2026-03-10T08:00:00Z",
  "status": "queued",
  "estimated_duration_seconds": 300
}
```

**Error Responses:**  
`400` Bad Request, `401` Unauthorized / session required, `500` Internal Server Error.

---

### GET /research/api/status/{research_id}

Check the status of a research job. Send session cookie.

**Path Parameters:** `research_id` — research job UUID.

**Response (200 OK):**
```json
{
  "research_id": "uuid-string",
  "state": "pending|running|completed|failed|timeout",
  "progress": 45,
  "message": "Synthesizing sources from iteration 2...",
  "last_milestone": "...",
  "current_iteration": 2,
  "total_iterations": 3,
  "sources_found": 24,
  "questions_generated": 12,
  "started_at": "...",
  "updated_at": "..."
}
```

**Error Responses:** `401` Unauthorized, `404` Not Found.

---

### GET /research/api/report/{research_id}

Fetch the complete research report. Send session cookie.

**Path Parameters:** `research_id` — research job UUID.

**Response (200 OK):**
```json
{
  "research_id": "uuid-string",
  "query": "original research query",
  "mode": "detailed",
  "summary": "Executive summary...",
  "report_markdown": "# Full Report\n\n...",
  "sources": [{"id": 1, "title": "...", "url": "...", "snippet": "...", "type": "web|local_doc", ...}],
  "iterations": 3,
  "total_questions": 24,
  "total_sources": 48,
  "created_at": "...",
  "completed_at": "...",
  "execution_time_seconds": 900
}
```

**Error Responses:** `400` Not yet completed, `401` Unauthorized, `404` Not Found.

---

## Health Check

**GET /health** — Check if the LDR service is running. No auth required for typical setups.

```json
{"status": "healthy", "version": "1.0.0", "uptime_seconds": 86400, "active_jobs": 3, "queued_jobs": 1}
```

---

## Error Codes

| Code | Meaning | Handling |
|------|---------|----------|
| 400 | Bad Request | Fix request parameters |
| 401 | Unauthorized | Re-establish session (login again) |
| 404 | Not Found | Verify research_id or path |
| 429 | Too Many Requests | Retry after delay |
| 500 | Internal Error | Retry with backoff |

---

## Testing auth (session + CSRF)

Do **not** use `curl -u user:pass` (Basic Auth). Instead:

1. Set `LDR_SERVICE_USER` and `LDR_SERVICE_PASSWORD` (or `LDR_USERNAME`/`LDR_PASSWORD`).
2. Run the skill script: `scripts/ldr-research.sh start_research --query "test"` and look for "Login successful".
3. Or open `LDR_LOGIN_URL` in a browser and sign in to confirm LDR’s login page and credentials.
