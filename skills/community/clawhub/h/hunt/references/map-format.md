# Map Format Reference

The map.md file lives at `~/.openclaw/workspace/map.md`. It tracks hackathons the user has committed to joining.

## Full Template

```markdown
# 🗺 Hunt Map

## Active

### 1. Hackathon Name
- **Host:** Organization Name
- **Dates:** May 8-14, 2026
- **Theme:** GenAI / FinTech / Open
- **Prize:** Cash / Non-cash / None
- **Link:** https://event.url
- **Starts:** May 8 @ 09:00 UTC
- **Reminder:** ✅ Set for May 7
- **Status:** Registered / Upcoming
- **Notes:** Briefing notes or prep needed

### 2. Next Hackathon Name
...
```

## Rules

- Entries are numbered sequentially starting from 1
- After any add or remove, **renumber** all entries
- Keep `# Active` as the only section header
- When listing more than 10 entries, add an `## Archived` section at the bottom
- Move old/completed entries to `## Archived` (don't delete unless user asks)

## Renumbering Example

Before:
```
### 1. Alpha
### 2. Beta
### 5. Gamma
```

After removing #2:
```
### 1. Alpha
### 2. Gamma
```
