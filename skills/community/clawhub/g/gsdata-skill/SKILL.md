---
name: gsdata
version: 1.0.0
author: yangyuwen-bri
license: MIT
description: |
  Use GSData open platform via local adapter script for account/content/rank/pubsent/nlp queries.
  Use when user asks for 舆情检索、热点事件、平台榜单、账号数据、小红书/微博/抖音等数据查询。
  Triggers: "gsdata", "清博", "舆情", "热点", "榜单", "关键词检索".
env:
  - GSDATA_APP_KEY
  - GSDATA_APP_SECRET
---

# GSData Skill

This skill allows you to query the GSData open platform for public sentiment (舆情), rankings (榜单), and account data. 

**Prerequisites:**
This skill requires the `requests` library. If a module cannot be found, you may need to run `pip install requests` once.

**Credentials:**
Authentication is handled via the `GSDATA_APP_KEY` and `GSDATA_APP_SECRET` environment variables. Do not attempt to use hardcoded test keys. 

## Adapter Usage
Use the bundled python script to interact with the API:

`python3 ./gsdata_adapter.py`

*Note: The script and its mapping `gsdata_tool_mapping_v1.json` are bundled in this skill's directory. Always run the script via relative path (`./gsdata_adapter.py`) from this directory.*

## Rules
1. For a new request, run `--dry-run` first to verify route/action mapping.
2. Default to read-only actions.
3. **CRITICAL FOR CONVERSATIONS**: If you are answering a user in a chat interface (like Telegram), you MUST append `--param size=5` (or a similarly small number) to prevent dumping enormous JSON payloads into the chat context.
4. Never run write-like actions unless user explicitly confirms.
5. For write-like actions, require `--allow-write`.
6. Return a concise summary first; included route + key fields used.
7. **PAGINATION LIMIT**: The API strictly enforces a maximum of 20 items per page (e.g., passing `size=100` defaults to 20). To fetch large datasets, use a loop with `--param page=1`, `--param page=2`, etc. Do NOT attempt to fetch more than 20 items in a single call.
8. **TOTAL COUNT ESTIMATION**: Before scraping multiple pages for `gsdata_pubsent_search`, ALWAYS probe the total volume first by running a test search with `--param limit=1` and checking the `numFound` field in the response JSON. Calculate total pages as `ceil(numFound / 20)`. (Note: The dedicated `num_found` action has a bug with date parameters and should NOT be used for this purpose).

## Quick Commands

**1. Discover endpoint capabilities:**
```bash
python3 ./gsdata_adapter.py list-tools
```

**2. Keyword search (with size limit):**
```bash
python3 ./gsdata_adapter.py invoke \
  --tool gsdata_pubsent_search \
  --action search \
  --param keywords_include=人工智能 \
  --param size=5 
```

**3. Probe data volume estimation (returns `numFound`):**
```bash
python3 ./gsdata_adapter.py invoke \
  --tool gsdata_pubsent_search \
  --action search \
  --param keywords_include=人工智能 \
  --param date_start=2026-03-01 \
  --param date_end=2026-03-04 \
  --param media_type=weibo \
  --param limit=1
```

**4. Hot events:**
```bash
python3 ./gsdata_adapter.py invoke \
  --tool gsdata_pubsent_hot \
  --action event_list \
  --params '{"type":"1"}'
```

**5. Xiaohongshu account search:**
```bash
python3 ./gsdata_adapter.py invoke \
  --tool gsdata_account \
  --action search \
  --platform xiaohongshu \
  --param xiaohongshu_name=AI \
  --param size=2
```



## Write Actions (Explicit Confirmation Required)

Examples:
- `gsdata_pubsent_warning create_rule/update_rule/open_rule/close_rule`
- `gsdata_myrank_group group_add/group_del`
- `gsdata_myrank_account acct_add/acct_del/acct_add_by_url`

When approved, append `--allow-write`:

```bash
python3 ./gsdata_adapter.py invoke \
  --tool gsdata_pubsent_warning \
  --action create_rule \
  --params '{"name":"demo"}' \
  --allow-write
```
