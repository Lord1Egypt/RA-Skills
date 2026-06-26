---
name: github-pr-writer
description: Write clear, structured GitHub pull request descriptions using a standardized template. Use when creating a PR, updating a PR description, or when asked to document what a branch changes. Automatically fills in summary, type of change, description of changes, impact, and testing notes based on the diff or context provided. Triggers on phrases like "create a PR", "write the PR description", "open a pull request", "update the PR body", "document this PR", or when a branch is ready to merge.
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["gh","git"]},"os":["linux","darwin","win32"]}}
---

# GitHub PR Writer

Generates structured, thorough PR descriptions using a consistent template.

## Template

See `assets/pull_request_template.md` for the full template to copy into your repo's `.github/pull_request_template.md`.

## How to Fill It

When writing a PR description, gather context first:

```bash
# See what changed vs base branch
git diff main --stat

# See commit messages
git log --oneline main..HEAD

# See full diff (for smaller PRs)
git diff main
```

Then fill in each section:

### Summary
One or two sentences. What does this PR do and why? Link the issue if there is one.
```text
Closes #123
Adds user authentication via Devise with email confirmation.
```

### Type of Change
Check exactly one (or two if truly applicable). Be honest — don't check "safe" if there are breaking changes.

### Implements / Fixes
Link issues or describe the specific feature/bug this addresses. Be specific enough that a reviewer knows what to look for.

### Description of Changes
Bullet points — what actually changed in the code:
- New files created
- Existing files modified and why
- Anything removed
- Config changes
- Database migrations

Group related changes together. Lead with the most important change.

### Impact
Honest assessment. If you changed a shared concern, a base class, or anything that touches many parts of the app — flag it.

### Testing Notes
Tell the reviewer how to verify the changes work:
- What specs were added/changed
- Manual QA steps if needed
- Edge cases that were considered
- Anything that was intentionally NOT tested and why

## Rules

- **Fill every section** — empty sections signal an incomplete review
- **Check appropriate checkboxes** — don't leave all unchecked
- **Be specific in Description** — "Updated stuff" is not useful
- **Be honest about Impact** — reviewers need to know what to watch for
- **Never merge** — PRs are for review; the author or maintainer merges

## Example (filled)

```markdown
# 📦 Pull Request

## Summary
Closes #44
Adds the driver availability system for ride booking. When a patron requests a ride,
the system checks which approved drivers are available based on schedule windows,
existing ride conflicts, and drive-time buffers.

---

## ✅ Checklist Before Merging
### Code
- [x] Code runs locally without errors
- [x] My code has no unused or commented-out sections
- [x] I have reviewed my code
- [x] I have added comments to any complex logic

### Testing
- [x] All tests are passing
- [x] I have added or updated tests as needed

---

## 🧪 Type of Change
- [x] 🚀 New feature

---

## 🛠️ Implements / Fixes
Implements driver availability checking for Phase 1 ride scheduling.

---

## 📋 Description of Changes
- Added `role` column to `user_rides` (driver/patron, default: patron)
- Created `driver_schedules` table for recurring and one-off availability windows
- Added `DriverSchedule` model with `covers_time?` method
- Added `GeoapifyDriveTimeService` for real drive time via Geoapify Route Matrix API
- Added `DriverAvailabilityService` — 4-step availability check
- Updated seeds and factories to include `role`

---

## 💣 Impact
- [x] This PR is safe (does not break existing functionality)

---

## 🧪 Testing Notes
- [x] All/most tests changed

75 new tests across 3 spec files. Final suite: 729 examples, 0 failures.
```
