---
name: juya-ai-daily
description: "Fetch the latest AI daily brief from imjuya/juya-ai-daily (GitHub) and return the Overview (summary) section."
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🗞️",
        "requires": { "bins": ["curl"] },
      },
  }
---

# Juya AI Daily (AI 日报)

Fetch the latest daily AI news brief from the public repo `imjuya/juya-ai-daily` and return the **summary / overview** section.

## When to use (trigger phrases)

- “AI 日报 / AI 早报 / 今日 AI 新闻”
- “拉取今天最新的 AI 新闻总结”
- “juya ai daily”

## What you should return

- The latest available date (from the repo)
- The `## 概览` section only (this is the repo’s “summary view”)
- A short note: “Reply with #n if you want the detailed explanation for item n”

## Fetch latest summary (bash)

This repo stores daily posts under `BACKUP/*.md` (public, no auth required).
If you run this frequently and hit GitHub rate limits, set `GITHUB_TOKEN` (or `GH_TOKEN`) to increase limits.

```bash
set -euo pipefail

API="https://api.github.com/repos/imjuya/juya-ai-daily/contents/BACKUP?ref=master"

latest_url="$(
  auth=()
  if [ -n "${GITHUB_TOKEN:-}" ]; then
    auth=(-H "Authorization: Bearer $GITHUB_TOKEN")
  elif [ -n "${GH_TOKEN:-}" ]; then
    auth=(-H "Authorization: Bearer $GH_TOKEN")
  fi
  curl -fsSL "${auth[@]}" -H "Accept: application/vnd.github+json" "$API" | node -e '
    const fs = require("node:fs");
    const items = JSON.parse(fs.readFileSync(0, "utf8"));
    const candidates = items
      .filter((it) => it && typeof it.name === "string" && typeof it.download_url === "string")
      .map((it) => {
        const m = it.name.match(/(?:^|_)(\d{4}-\d{2}-\d{2})\.md$/);
        return m ? { ...it, date: m[1] } : null;
      })
      .filter(Boolean);
    if (candidates.length === 0) {
      throw new Error("No BACKUP markdown files found.");
    }
    candidates.sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0));
    console.log(candidates[candidates.length - 1].download_url);
  '
)"

latest_date="$(basename "$latest_url" .md | sed -E 's/^[0-9]+_//')"

echo "Latest: $latest_date" >&2

curl -fsSL "$latest_url" | awk '
  done { next }
  /^## 概览/ { in_section=1 }
  in_section && /^---$/ { in_section=0; done=1 }
  in_section && /^\\* \\* \\*$/ { in_section=0; done=1 }
  in_section { print }
'
```

## Optional: fetch detailed explanation for a specific item `#n`

If the user asks for details for item `#3`, fetch the same latest file and extract that block:

```bash
set -euo pipefail

n="3"

API="https://api.github.com/repos/imjuya/juya-ai-daily/contents/BACKUP?ref=master"
latest_url="$(
  auth=()
  if [ -n "${GITHUB_TOKEN:-}" ]; then
    auth=(-H "Authorization: Bearer $GITHUB_TOKEN")
  elif [ -n "${GH_TOKEN:-}" ]; then
    auth=(-H "Authorization: Bearer $GH_TOKEN")
  fi
  curl -fsSL "${auth[@]}" -H "Accept: application/vnd.github+json" "$API" | node -e '
    const fs = require("node:fs");
    const items = JSON.parse(fs.readFileSync(0, "utf8"));
    const candidates = items
      .filter((it) => it && typeof it.name === "string" && typeof it.download_url === "string")
      .map((it) => {
        const m = it.name.match(/(?:^|_)(\d{4}-\d{2}-\d{2})\.md$/);
        return m ? { ...it, date: m[1] } : null;
      })
      .filter(Boolean);
    candidates.sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0));
    console.log(candidates[candidates.length - 1].download_url);
  '
)"

curl -fsSL "$latest_url" | awk -v n="$n" '
  done { next }
  $0 ~ /^## \\[/ {
    if (in_section && $0 !~ ("`#" n "`")) {
      in_section=0
      done=1
    }
    if (!in_section && $0 ~ ("`#" n "`")) {
      in_section=1
    }
  }
  in_section && /^\\* \\* \\*$/ { in_section=0; done=1 }
  in_section { print }
'
```
