---
name: "pmtools"
description: "Operate Feishu OKR via Feishu OpenAPI (periods, OKR list, progress records, images, reviews). Invoke when you need to query or update OKR progress."
user-invocable: true
metadata:
  openclaw:
    emoji: "🎯"
    category: "productivity"
    requires:
      anyBins: ["python3", "python"]
      env: ["FEISHU_ACCESS_TOKEN"]
---

# pmtools

## Safety

- Never print or persist access tokens.
- Confirm before deleting a progress record or changing a period status.

## Setup

- Set `FEISHU_ACCESS_TOKEN` (either `tenant_access_token` or `user_access_token`) for most endpoints.
- For `/reviews/query`, set `FEISHU_TENANT_ACCESS_TOKEN` because the doc requires `tenant_access_token`.

## Auto-update

Auto-update is executed automatically before every command (with a 7-day local whitelist cache). To force-run and see the update result, run:

```bash
python3 scripts/pm_tools.py self-update
```

This checks for updates at most once per 7 days (local whitelist cache). If a newer version is detected, it updates first, then proceeds.

## Commands

All commands print JSON to stdout.

### Periods

```bash
python3 scripts/pm_tools.py periods-create --period_rule_id <id> --start_month <YYYY-MM>
python3 scripts/pm_tools.py periods-update-status --period_id <id> --status <1|2|3>
python3 scripts/pm_tools.py periods-list [--page_token <token>] [--page_size <n>]
python3 scripts/pm_tools.py period-rules-list
```

### OKRs

```bash
python3 scripts/pm_tools.py user-okrs-list --user_id <id> --offset <n> --limit <n> [--user_id_type open_id|union_id|user_id|people_admin_id] [--lang zh_cn|en_us] [--period_id <id> ...]
python3 scripts/pm_tools.py okrs-batch-get --okr_id <id> ... [--user_id_type open_id|union_id|user_id|people_admin_id] [--lang zh_cn|en_us]
```

### Progress records

```bash
python3 scripts/pm_tools.py progress-create --source_title <title> --source_url <url> --target_id <id> --target_type <2|3> (--text <plain-text> | --content_json <json> | --content_file <path>) [--percent <float>] [--status <-1|0|1|2>] [--source_url_pc <url>] [--source_url_mobile <url>]
python3 scripts/pm_tools.py progress-update --progress_id <id> (--text <plain-text> | --content_json <json> | --content_file <path>)
python3 scripts/pm_tools.py progress-delete --progress_id <id>
python3 scripts/pm_tools.py progress-get --progress_id <id>
```

### Images

```bash
python3 scripts/pm_tools.py image-upload --file <path> --target_id <id> --target_type <2|3>
```

### Reviews

```bash
python3 scripts/pm_tools.py reviews-query --user_id <id> ... --period_id <id> ... [--user_id_type open_id|union_id|user_id|people_admin_id]
```
