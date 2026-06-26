# Stale Data Verification

How to verify dynamic data before reporting it as fact in session warmups or plan reviews.

## The Problem

Static snapshot files (`docs/STATE-SNAPSHOT.md`, dated entity counts in plans, etc.) go stale within days. Reporting stale counts as current state causes incorrect assessments and wrong prioritization.

## The Pattern

1. **Identify the data point** — is it a live count or a static note?
2. **If live, prefer existing APIs or git log over direct DB queries** — commit messages and application API endpoints are safer than raw database access
3. **If static, note the date** — include the snapshot date when presenting counts
4. **Prefer git log over memory** — commit messages tell you what actually shipped

## ⚠️ Data Source Safety

**Direct database queries (via CLI, Prisma, curl, etc.) require explicit user approval in the current turn.** Never run queries against production databases without confirmation. Prefer:

- **git log** — commit messages tell you what shipped
- **Application API endpoints** — use existing routes (e.g., `/api/admin/stats`)
- **File timestamps** — check mtime on snapshot files
- **User-provided context** — let the user confirm before reaching for a connection string

If a DB query is necessary and approved:
- Use read-only credentials
- Prefer staging over production
- Limit to the minimum data needed
- Never output connection strings or credentials

## Examples (conceptual — not executable)

```bash
# SAFER: Use git log to check what shipped
git log --oneline --since="7 days ago"

# REQUIRE APPROVAL: Any direct database access
# (Never run without user confirmation in the current turn)
```
