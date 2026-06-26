# Trusted Sources — MaxClaw Helper

This file lists the **fully trusted** documentation sources to consult when answering questions or diagnosing issues.
Query in priority order; use the first source that has a clear, matching record.

---

## 1. OpenClaw Official Docs (Highest Priority)

**URL:** https://docs.openclaw.ai/

**Coverage:**
- CLI usage (`openclaw` subcommands)
- Gateway configuration and behavior
- Plugin / Channel setup
- Cron scheduling system
- Skills development specification
- Known issues and FAQ

**How to query:**
```
extract_content_from_websites([{
  "url": "https://docs.openclaw.ai/",
  "prompt": "Find information about [error keyword / feature name / operation]"
}])
```

Common sub-pages (query as needed):
- https://docs.openclaw.ai/cli — CLI command reference
- https://docs.openclaw.ai/gateway — Gateway configuration
- https://docs.openclaw.ai/channels — Channel configuration
- https://docs.openclaw.ai/skills — Skills development
- https://docs.openclaw.ai/cron — Cron scheduling

---

## 2. MiniMax Official Feishu Documentation

**URL:** https://vrfi1sk8a0.feishu.cn/wiki/YwEZwj3iuixCK9koFeacwvC6n9d

**Coverage:**
- MaxClaw-specific configuration
- MiniMax model integration and parameters
- Feishu channel configuration
- Features exclusive to MaxClaw users

Important: Content in this document **applies to MaxClaw users only** and does not apply to general OpenClaw deployments.

**How to read:** This is a Feishu Wiki link — use the `feishu-wiki` and `feishu-doc` skills, not `extract_content_from_websites`.

1. Get the node to resolve `obj_token`:
   ```json
   { "action": "get", "token": "YwEZwj3iuixCK9koFeacwvC6n9d" }
   ```
2. Read the document content using the returned `obj_token`:
   ```json
   { "action": "read", "doc_token": "<obj_token from step 1>" }
   ```
3. If the response `hint` indicates structured content (tables, etc.), follow up with `action: "list_blocks"`

---

## 3. Community & Supplementary Sources (Reference Only — Not Authoritative)

The following may be consulted for reference, but **must not be the sole basis for executing high-risk operations**:

| Source | URL | Notes |
|--------|-----|-------|
| OpenClaw Discord | https://discord.com/invite/clawd | Official community; good for questions |
| ClawhHub | https://clawhub.com | Skills marketplace; reference implementations |

---

## Update Log

| Date | Change |
|------|--------|
| 2026-03-08 | Initial version
| 2026-03-08 | MiniMax Feishu Wiki URL added |
