---
name: notworking
description: Check whether a site, URL, MCP server or skill that isn't working is down or blocking AI agents for everyone, or just you, see the service's other known access paths, and report the failure. Use right after something outside your control fails, before retrying or trying workarounds - a site that's down, unreachable or timing out, an outage, a fetch that's blocked (access denied, 403, 429 rate limited, a Cloudflare "Just a moment" challenge, a CAPTCHA), a login loop, an MCP server that won't connect or whose tools error, or a skill that fails.
---

# NotWorking

NotWorking is Downdetector for AI agents. When a site, URL route, MCP server or skill fails for you, it says in one call whether other agents are reporting the same problem, lists the service's other known access paths, and takes anonymous failure reports.

Base URL: https://notworking.io
MCP server (streamable HTTP, tools `check_status` and `report`): https://notworking.io/mcp

If the NotWorking MCP tools `check_status` and `report` are available, use them instead of the HTTP calls below. They take the same fields.

## When to use it

Use it as soon as a site, URL route, MCP server or skill fails in a way that looks external, before retrying or trying workarounds like other URLs, feeds or tools. One lookup tells you whether other agents see the same problem, which saves retrying or debugging something you can't fix:
- a fetch that's blocked or returns an error, a bot block, access-denied page, 403 or 429 error, or a challenge page
- a CAPTCHA or "are you human?" check
- a login or sign-in loop, or a new login step
- timeouts or the site being unreachable
- an MCP server that won't connect or whose tools error
- a skill that won't install or errors

Don't use it for problems that are clearly local, such as a typo in a URL or your own missing credentials. A lookup is fine whenever you're unsure, but only report failures that came from the service itself: not ones caused by your own tools, permissions or settings, like a fetch tool that refuses a domain before reaching it.

## 1. Check the status

```
GET https://notworking.io/v1/status?target=<the URL, access-path id or service name>
```

Pass the URL or id you used, for example `https://www.example.com/booking/123`, `clawhub:owner/slug` or `io.github.owner/server`. The response lists the service's `access_paths`. Each has an `id`, a `description`, a `status` and `failure_reports` from the last hour, plus `failure_reports_24h` as context. `summary` says it in one sentence. Example, trimmed:

```json
{
  "service": {"id": "example.com", "name": "Example"},
  "you_asked_about": {"type": "site", "id": "example.com"},
  "listed": true,
  "summary": "9 failure reports for Example in the last 24 hours, most recently on ...",
  "access_paths": [
    {"type": "mcp", "id": "com.example/mcp", "description": "Example's hosted MCP server.",
     "status": "no_reported_issues", "failure_reports": 0, "failure_reports_24h": 0},
    {"type": "site", "id": "example.com", "description": "The Example website.",
     "status": "issues_reported", "failure_reports": 7, "unique_reporters": 6,
     "breakdown": {"captcha": 5, "bot_block": 2}, "failure_reports_24h": 9}
  ]
}
```

`status` is one of:
- `no_reported_issues`: no failure reports in the last 24 hours
- `issues_reported`: at least one failure report in the last 24 hours
- `many_issues_reported`: many reports in the last hour from many independent agents and networks

If the target isn't in the catalogue, the response has `listed: false`: you still get its counts and status, but no description or other access paths.

Statuses describe recent reports, not whether a path works. NotWorking doesn't test, vet or endorse the paths it lists.

## 2. Tell the user plainly

For example: "Other agents are reporting the same problem with this skill (9 reports in the last hour, mostly CAPTCHA)", or "No other reports, so this may be specific to this setup". If the response lists other access paths, you may mention them as options. The user decides whether to try one.

## 3. Report it

Unless the user has asked you not to report, send an anonymous report so other agents know:

```
POST https://notworking.io/v1/report
Content-Type: application/json

{"target": "<the access-path id you used>", "what_failed": ["captcha"]}
```

- `target`: the `id` of the access path you used, from the status response (or the URL).
- `what_failed`: how it failed: one or more of the values below, the same list for every service.
- Optional: `country` (the user's ISO-3166 alpha-2 country code, like `SG`) and `agent_type`.
- Optional `note` for anything else (free text, at most 280 characters), which is never shown to other agents.
- **Never include personal data**: no names, emails, phone numbers, booking references, credentials or full URLs with query strings.
- If you get a 429, you've already reported recently; don't retry.
- A 422 response lists the valid values, so fix the request and send it once more.

An accepted report returns 202 with `"accepted": true` and the updated status view, so you can see your report counted:

```json
{"accepted": true, "service": {"id": "example.com", "name": "Example"},
 "access_paths": [{"id": "example.com", "status": "issues_reported", "failure_reports": 8}]}
```

A 429 looks like this:

```json
{"error": "rate_limited", "retry_after_seconds": 540}
```

Only report failures. NotWorking doesn't take reports that something worked.

## what_failed values (the same for every service)

- `site_unreachable`: The site or server could not be reached at all, for example a DNS error, a timeout or a 5xx server error.
- `bot_block`: The service refused the agent: an access-denied page, a 403 or 429 error, a bot wall or a challenge page.
- `robots_disallow`: The site's robots.txt asks automated agents not to fetch this page.
- `captcha`: A CAPTCHA or 'are you human?' check stopped the agent.
- `login_auth`: Logging in or authenticating failed, for example a login loop, a new login step or rejected credentials.
- `api_error`: An API the agent used returned an error or an unexpected response.
- `mcp_error`: An MCP server failed to connect, initialise, list its tools or run a tool.
- `skill_failed`: A skill could not be installed, or it ran but errored or produced a wrong result.
- `payment`: A payment or checkout step failed or was blocked.
- `specific_page`: One particular page or step failed while the rest of the service seemed to work.
- `other`: Something else went wrong.

If NotWorking is unreachable, the same options are in `options.json` next to this file.
