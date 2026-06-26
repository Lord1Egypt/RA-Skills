---
name: nicebox-site-manager
description: Manage AI-built websites via NiceBox OpenClaw API. Supports article publishing, viewing messages, and checking site status.
metadata: {"clawdbot":{"emoji":"🛠️","requires":{"bins":["python3"],"env":["AIBOX_API_KEY"]},"primaryEnv":"AIBOX_API_KEY"}}
---

# NiceBox Site Manager

Manage AI-built websites through the NiceBox OpenClaw API.

Base URL:

```bash
https://ai.nicebox.cn/api/openclaw
```

Authentication:

```bash
Authorization: $AIBOX_API_KEY
```

This skill provides 3 main capabilities:

* Publish article
* View messages
* Check site status

## Publish article

Publish an article to your site.

```bash
python3 {baseDir}/scripts/publish_article.py \
  --title "Hello World" \
  --content "<p>This is article content</p>" \
  --summary "Optional summary" \
  --author "NiceBox AI" \
  --cover "https://example.com/cover.jpg" \
  --status publish
```

Options:

* `--title`: Article title (required)
* `--content`: Article content, usually HTML (required)
* `--summary`: Article summary (optional)
* `--author`: Author name (optional)
* `--cover`: Cover image URL (optional)
* `--status`: `draft` or `publish` (default: `publish`)

## View messages

List messages, inquiries, or leads from your site.

```bash
python3 {baseDir}/scripts/list_messages.py
python3 {baseDir}/scripts/list_messages.py --page 1 --page-size 20
python3 {baseDir}/scripts/list_messages.py --is-read 0
```

Options:

* `--page`: Page number (default: `1`)
* `--page-size`: Number of items per page (default: `20`)
* `--is-read`: Filter by read status, `0` unread / `1` read (optional)

## Check site status

Check the current status of your site.

```bash
python3 {baseDir}/scripts/site_status.py
```

No additional options required.

## Environment

Set your API key before using this skill:

```bash
export AIBOX_API_KEY="your_api_key"
```

Optional override for base URL:

```bash
export AIBOX_BASE_URL="https://ai.nicebox.cn/api/openclaw"
```

## Default endpoint assumptions

This skill assumes the following API paths:

* `POST /article/publish`
* `GET /message/getlist`
* `GET /site/status`

If your actual backend uses different paths, update the `ENDPOINT_*` constants in the Python scripts.

## Notes

* All requests use the HTTP `Authorization` header.
* The API key is sent as plain header value:

  * `Authorization: YOUR_KEY`
* Output is printed as formatted JSON for easier debugging and agent use.
* If your API field names differ, update the payload fields in the scripts.
