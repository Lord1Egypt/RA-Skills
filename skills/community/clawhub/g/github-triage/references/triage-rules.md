# GitHub Triage Rules

## Priority Levels

### 🔴 P0 — Immediate Forward

Forward to main email immediately. Prepend `[紧急]` to subject. Main email is resolved via `mail-cli clawemail master-user`.

**Matching patterns** (case-insensitive, check subject + body):
- CI/CD failures: `failed`, `broken`, `build error`, `workflow run failed`, `check suite failed`
- Security: `dependabot`, `security alert`, `vulnerability`, `CVE-`
- Direct mentions requiring action: body contains `@<your-username>` AND words like `please`, `need`, `urgent`, `ASAP`, `decision`, `approve`, `block`
- Deploy failures: `deploy failed`, `rollback`

**Forward format:**
```
Subject: [紧急] <original-subject>
Body: <original-body>
```

### 🟡 P1 — Buffer for Daily Summary

Do NOT forward immediately. Store metadata for daily summary.

**Matching patterns:**
- PR review requests: `requested your review`, `review requested`
- PR merged: `merged`, `pull request merged`
- PR approved: `approved your pull request`
- Issue assigned: `assigned to you`, `you were assigned`

**Store format (one line per item):**
```
<repo>|<type>|<title>|<url>|<timestamp>
```

### 🟢 P2 — Silent Archive

No forward. No reply. Mark as read.

**Everything else**, including:
- Star/watch notifications
- Comment threads you're CC'd on
- Subscription digests
- Bot auto-comments (codecov, dependabot auto-merge, etc.)

## Daily Summary Format

Send at configured time (default 18:00) to main email (resolved via `mail-cli clawemail master-user`).

```
Subject: [GitHub 日报] <date> — <n> 条待处理通知

# GitHub 通知日报 — <date>

## 🔍 待你 Review 的 PR（<count>）

### <repo-name>
- [ ] #<number> <title>  — <author>, <time-ago>

### <repo-name>
- [ ] #<number> <title>  — <author>, <time-ago>

## ✅ 今日 Merged PR（<count>）
- <repo>#<number> <title>

## 🔒 今日 Closed Issue（<count>）
- <repo>#<number> <title>

---
此邮件由 GitHub Triage Skill 自动生成
```

If no buffered items exist, skip sending the summary (don't send empty reports).
