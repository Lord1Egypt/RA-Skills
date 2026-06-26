---
name: http-requests
description: Send HTTP requests with Python requests instead of curl when quoting and escaping would be error-prone. Use for GET, POST, PUT, DELETE requests with headers, query params, JSON body, form data, timeout control, and concise response inspection. Triggers on phrases like "调用这个 API", "发 GET 请求", "发 POST 请求", "请求这个接口", "带 header 调接口", "用 requests 代替 curl", "测试 webhook", or "看接口返回了什么".
---

# HTTP Requests

Use this skill when an HTTP API call is needed and `curl` quoting/escaping would be fragile.

## What this skill does

- Sends HTTP requests via Python `requests`
- Supports `GET`, `POST`, `PUT`, `DELETE`
- Supports headers, query params, JSON body, form data, and timeout
- Writes a light daily JSONL log under `logs/`
- Avoids logging sensitive values like authorization tokens and full bodies

## Inputs to collect

Before running the script, gather:

- Method: `GET` / `POST` / `PUT` / `DELETE`
- URL
- Headers if any
- Query params if any
- JSON body or form data if any
- Timeout if the user cares (otherwise use default)

## Script

Primary script:

- `scripts/request_http.py`

Run it with Python and pass method/url plus optional inputs.

## Logging

Logs are stored inside this skill directory:

- `logs/YYYY-MM-DD.jsonl`

Each line contains a light summary only:

- timestamp
- method
- url
- status
- ok
- duration_ms
- response_bytes
- error (if any)

Do **not** log authorization tokens, cookies, or full request/response bodies by default.

## When to read references

Read `references/usage-patterns.md` when:

- the request has multiple headers/params/body fields
- the user wants an example pattern
- you need to choose between JSON body and form data
- you need the expected command-line argument style for the script
