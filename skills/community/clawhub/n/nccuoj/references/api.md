# NCCUOJ API Reference

Base URL: `https://nccuoj.ebg.tw/api`

All responses follow the format: `{ "error": null, "data": ... }` on success, or `{ "error": "message", "data": null }` on error.

## CSRF Token

**All requests require a CSRF token.** Obtain it by making any GET request first (e.g. `GET /profile`).

The response will include a `Set-Cookie: csrftoken=...` header. Extract the token value and include it in **every subsequent request**:

- **Cookie header**: `Cookie: csrftoken={token}; sessionid={session}` (sessionid only after login)
- **CSRF header**: `X-CSRFToken: {token}` (required for POST/PUT/DELETE)

Example flow:
```
1. GET  /api/profile           → extract csrftoken from Set-Cookie
2. POST /api/login              → send csrftoken cookie + X-CSRFToken header
3. POST /api/submission          → send csrftoken + sessionid cookies + X-CSRFToken header
```

## Public Endpoints (No Auth Required)

### Get Problem

`GET /problem?problem_id={display_id}`

Returns problem details including `title`, `description`, `input_description`, `output_description`, `samples`, `time_limit`, `memory_limit`, `hint`, `languages`, `tags`, `difficulty`, `_id` (display ID), `id` (internal ID).

### List Problems

`GET /problem?limit={n}&offset={o}`

Optional query params: `tag`, `keyword`, `difficulty` (`Low`, `Mid`, `High`).

Returns paginated list: `{ "results": [...], "total": n }`.

### Get Problem Tags

`GET /problem/tags`

Optional: `keyword` for filtering.

### Pick Random Problem

`GET /pickone`

Returns a random problem display ID.

## Authenticated Endpoints

### Login

`POST /login`

```json
{ "username": "...", "password": "..." }
```

Headers: `X-CSRFToken: {csrftoken}`, Cookie: `csrftoken={csrftoken}`

Sets `sessionid` cookie on success. Optionally include `tfa_code` for 2FA.

### Get Profile

`GET /profile`

Useful as the initial request to obtain the CSRF token. Also returns user info if authenticated.

---

## Public Problem Endpoints

### Submit Code (Public)

`POST /submission`

```json
{
  "problem_id": 1,
  "language": "C++",
  "code": "..."
}
```

Headers: `X-CSRFToken: {csrftoken}`, Cookie: `csrftoken={csrftoken}; sessionid={sessionid}`

`problem_id` is the **internal ID** (numeric), not the display ID. Use the `id` field from the problem detail response.

Returns `{ "submission_id": "..." }` on success.

### Get Submission

`GET /submission?id={submission_id}`

Returns full submission info including `result`, `statistic_info` (time/memory usage), `code`, `info` (detailed test case results).

### List Submissions (Public)

`GET /submissions?limit={n}&offset={o}`

Optional: `problem_id` (display ID), `myself=1`, `result`, `username`.

### Check Submission Exists

`GET /submission_exists?problem_id={id}`

Returns boolean — whether current user has submitted for this problem.

---

## Contest Endpoints

All contest endpoints mirror the public ones but require `contest_id`.

### Get Contest Problem

`GET /contest/problem?contest_id={id}` — list all problems in a contest

`GET /contest/problem?contest_id={id}&problem_id={display_id}` — specific contest problem

Response format is the same as public problem endpoints.

### Submit Code (Contest)

`POST /submission`

```json
{
  "problem_id": 1,
  "language": "C++",
  "code": "...",
  "contest_id": 123
}
```

Headers: `X-CSRFToken: {csrftoken}`, Cookie: `csrftoken={csrftoken}; sessionid={sessionid}`

Returns `{ "submission_id": "..." }` on success. Contest must be ongoing.

### List Contest Submissions

`GET /contest_submissions?contest_id={id}&limit={n}&offset={o}`

Optional: `problem_id` (display ID), `myself=1`, `result`, `username`.

Note: During ACM contests without real-time rank, only your own submissions are visible.

## Result Codes

| Code | Meaning                |
|------|------------------------|
| -2   | Compile Error          |
| -1   | Wrong Answer           |
| 0    | Accepted               |
| 1    | Time Limit Exceeded    |
| 2    | Memory Limit Exceeded  |
| 3    | Runtime Error          |
| 4    | System Error           |
| 6    | Pending                |
| 7    | Judging                |
| 8    | Partial Accepted       |

## Language Names

Use these exact strings for the `language` field:

- `C` — GCC 13, C17
- `C++` — GCC 13, C++20
- `Java` — Temurin 21
- `Python3` — Python 3.12
- `Golang` — Go 1.22
- `JavaScript` — Node.js 20
