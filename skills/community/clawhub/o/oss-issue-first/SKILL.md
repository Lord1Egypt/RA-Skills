---
name: oss-issue-first
description: |
  Open source problem-solving workflow: ALWAYS search the project's GitHub/GitLab issue tracker and check the latest version BEFORE attempting custom workarounds.
  Use this skill whenever encountering bugs, errors, or unexpected behavior in any open-source project (RAGFlow, SpringAI, RuoYi, Vue, Element Plus, etc.), including 401/403/404 errors, SecurityErrors, CORS issues, missing features, or unexpected API behavior. Trigger this skill even if you think you can fix it with configuration — checking the issue tracker first saves hours of wasted effort.
---

# Open Source Issue-First Workflow

## Why This Skill Exists

When encountering a bug in an open-source project, the instinct is often to immediately start debugging — tweaking configs, writing proxy rules, adding workarounds. But the project maintainers may have already fixed the issue weeks ago. Spending hours on workarounds that a simple version update would resolve is wasted effort.

**Real example**: Spent 2+ hours configuring Nginx sub_filter, proxy headers, and referer-based routing to work around a RAGFlow image 401 error — only to discover the fix had been merged two weeks earlier (https://github.com/infiniflow/ragflow/pull/16525).

## The Workflow

When you encounter a bug, error, or unexpected behavior in an open-source project:

### Step 1: Identify the Project and Version

- Determine which open-source project is causing the issue (RAGFlow, SpringAI, RuoYi, Vue, etc.)
- If possible, determine the current version being used

### Step 2: Search the Issue Tracker

Go to the project's GitHub/GitLab repository and search for the error:

1. Search issues: `https://github.com/{org}/{repo}/issues?q={error+keywords}`
2. Search PRs: `https://github.com/{org}/{repo}/pulls?q={error+keywords}`
3. Check if the issue is marked as "fixed" or "merged"
4. Note the version/commit where the fix was applied

Use `web-search` or `Bash` with `curl` to search GitHub:
```bash
# Search GitHub issues via API
curl -s "https://api.github.com/search/issues?q=repo:{org}/{repo}+{keywords}+state:all&sort=updated&order=desc" | head -100
```

Or use web search:
```
site:github.com/{org}/{repo} {error keywords}
```

### Step 3: Check Latest Version

- Compare the user's version with the latest release
- If the fix is in a newer version, recommend upgrading

### Step 4: Only Then Attempt Workarounds

If and only if:
- The issue has NOT been reported, OR
- The issue has been reported but NOT fixed, OR
- Upgrading is not possible (locked version, breaking changes)

...then proceed with custom debugging and workarounds.

### Step 5: If You Find a Relevant Issue

Report to the user:
- The issue/PR URL
- Whether it's been fixed
- Which version contains the fix
- Whether upgrading is feasible

## Common Signs This Skill Should Apply

- HTTP 401/403/404 errors from a third-party service
- CORS / SecurityError in browser console
- "Unexpected" API behavior in a library
- Missing features that "should" exist
- Errors after upgrading a dependency
- Any `Uncaught` errors from third-party JS

## Quick Reference: Common Project Repos

| Project | Repo |
|---------|------|
| RAGFlow | https://github.com/infiniflow/ragflow |
| SpringAI | https://github.com/spring-projects/spring-ai |
| RuoYi | https://gitee.com/y_project/RuoYi-Vue |
| Vue | https://github.com/vuejs/vue (v2) / https://github.com/vuejs/core (v3) |
| Element Plus | https://github.com/element-plus/element-plus |
| Element Plus X | https://github.com/element-plus-x/Element-Plus-X |
| MyBatis | https://github.com/mybatis/mybatis-3 |

When the project is not in this list, identify the repo from `package.json`, `pom.xml`, or the error message itself.
