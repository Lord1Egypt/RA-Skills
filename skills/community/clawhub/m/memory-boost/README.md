# Memory Boost

**Version:** 1.0.4

> AI assistants have no real memory. Each session starts fresh. Important context is lost between conversations.
> 
> **This is not your fault. It's how AI works.**

---

## 🚀 Quick Install

### One-Command Install (Recommended)

```bash
# After installing the skill, run the auto-config script
bash skills/memory-boost/install.sh
```

This automatically creates:
- `MEMORY.md` - Long-term memory
- `MEMORY_INDEX.md` - Quick reference
- `memory/YYYY-MM-DD.md` - Today's log

---

## 📁 File Structure

```
workspace/
├── MEMORY.md           # Long-term memory (decisions, preferences, context)
├── MEMORY_INDEX.md     # Quick reference (project status, key links)
└── memory/             # Logs directory
    ├── 2026-04-01.md   # Daily session log
    └── project.md      # Project-specific notes
```

---

## 💡 How to Use

### Before Session (AI auto-executes)

1. Read `MEMORY.md` — Get long-term context
2. Read `memory/YYYY-MM-DD.md` — Get today's log
3. Read `MEMORY_INDEX.md` — Quick project status

### After Session (AI auto-executes)

1. Update `memory/YYYY-MM-DD.md` — Record completed work
2. Update `MEMORY.md` — Record important decisions
3. Update `MEMORY_INDEX.md` — Update project status

---

## 📝 Templates

### MEMORY.md Template

```markdown
# MEMORY.md - AI Assistant Shared Memory

**Created:** 2026-04-01
**Maintained By:** Your Name

---

## 🎯 Active Projects

| Project | Status | Links | Last Updated |
|---------|--------|-------|--------------|
| Project A | 🟡 In Progress | [Link]() | 2026-04-01 |

---

## 👤 User Preferences

| Aspect | Preference |
|--------|------------|
| Communication | Direct, concise |
| Response Style | Structured, tables first |

---

## 📚 Important Decisions

### 2026-04-01
- **Decision:** What was decided
- **Reason:** Why this choice

---

*Last updated: 2026-04-01*
```

### Daily Log Template

```markdown
# 2026-04-01

## Completed
- [ ] Task 1
- [ ] Task 2

## In Progress
- Task 3 (50% done)

## Notes
- Something learned today

## Links
- https://...
```

---

## 🎯 Common Scenarios

### Scenario 1: Starting a New Project

```
1. Create memory/project-name.md
2. Add project to MEMORY.md (Active Projects table)
3. Add to MEMORY_INDEX.md (if using)
4. Start logging work in memory/project-name.md
```

### Scenario 2: Making an Important Decision

```
1. Complete the task
2. Update memory/today.md with what happened
3. Add decision to MEMORY.md (Important Decisions section)
4. Update project status in MEMORY_INDEX.md
```

### Scenario 3: User Says "Remember This"

```
1. Write immediately
2. Confirm: "Added to [file] under [section]"
```

### Scenario 4: Returning After a Break

```
1. Read MEMORY.md (refresh long-term context)
2. Read memory/ files from last session
3. Check MEMORY_INDEX.md for status overview
4. Ask user: "Ready to continue [project]?"
```

---

## ✅ Best Practices

### Do ✅

- **Read memory at session start** — Never skip this
- **Write immediately after tasks** — Don't wait
- **Use clear structure** — Tables, lists, headers
- **Keep it simple** — Bullet points over paragraphs
- **Update on status changes** — When projects move forward

### Don't ❌

- **Don't rely on "mental notes"** — If it matters, write it
- **Don't wait until "later"** — Later never comes
- **Don't write essays** — Be concise
- **Don't over-organize** — Simple is sustainable
- **Don't skip updates** — Stale memory is worse than no memory

---

## 🔧 Advanced Usage

### Multi-AI Teams

If you work with multiple AI assistants:

- **Share MEMORY.md** — All AIs read/write the same file
- **Each AI can have its own notes** — e.g., `CLAUDE.md`, `PAW.md`
- **Sync via MEMORY_INDEX.md** — Single source of truth

### Automation

If you're technical:

- Use cron jobs to create daily memory files
- Auto-archive old memory files monthly
- Create scripts to search across memory files

---

## 📄 License

MIT License — Feel free to use, modify, and share.

---

*Version 1.0.4 | Last updated: 2026-04-01*
