---
name: memory-boost
description: Simple text-based memory system for AI assistants - auto-install script included
homepage: https://clawhub.ai/skills/memory-boost
version: 1.1.1
tags: [memory, productivity, workflow, text-based, best-practice, auto-install]
---

# Memory Boost

**Version:** 1.1.1  
**Author:** Crystaria (with Paw and Kyle)  
**License:** MIT

---

## 📖 Introduction

**AI assistants always "forget"? Context lost after every conversation?**

Memory Boost is a text-based memory system that solves these problems:

- 🧠 **Long-term Memory** — Save user preferences, project history, and important decisions across sessions
- 📋 **Quick Index** — At-a-glance project status overview
- 📔 **Daily Logs** — Record progress and context for each session
- 🔧 **Out of the Box** — Includes auto-install script, no configuration needed

**Applicable Scenarios:**
- Multi-session collaboration (no context loss between conversations)
- Multi-AI team collaboration (multiple AIs share the same memory)
- Long-term project tracking (preserve decision history and user preferences)

---

## 🚀 Quick Start

### 1. Install

```bash
clawhub install memory-boost
```

### 2. Run Install Script

```bash
bash /path/to/skills/memory-boost/install.sh
```

Automatically creates:
- `~/MEMORY.md` — Long-term memory
- `~/MEMORY_INDEX.md` — Quick reference
- `~/memory/YYYY-MM-DD.md` — Today's session log

### 3. Start Using

Speak directly to AI:
- "Remember what I said about the XX project?"
- "Continue the feature we worked on yesterday"
- "Remember this preference: I like concise answers"

AI will automatically read/write memory files, no extra steps needed!

---

## 📁 File Structure

```
workspace/
├── MEMORY.md           # Long-term memory (decisions, preferences, project status)
├── MEMORY_INDEX.md     # Quick index (project overview, key links)
└── memory/
    ├── 2026-04-01.md   # Today's session log
    └── project-name.md # Project-specific memory
```

---

## 📝 Template Examples

### MEMORY.md (Long-term Memory)

```markdown
# MEMORY.md - AI Assistant Shared Memory

## 🎯 Active Projects
| Project | Status | Links | Last Updated |
|---------|--------|-------|--------------|
| Project A | 🟡 In Progress | [Link]() | 2026-04-01 |

## 👤 User Preferences
| Aspect | Preference |
|--------|------------|
| Communication | Direct, concise |
| Response Style | Structured, tables first |

## 📚 Important Decisions
### 2026-04-01
- **Decision:** What was decided
- **Reason:** Why this choice
```

### Daily Log

```markdown
# 2026-04-01

## Completed
- Task 1
- Task 2

## In Progress
- Task 3 (50% done)

## Notes
- Context for tomorrow
```

---

## ❓ FAQ

**Q: Will memory files grow indefinitely?**

A: Yes. You can periodically clean up old logs in `memory/` directory. Keep `MEMORY.md` as it contains long-term decisions.

**Q: How do multiple AIs share memory?**

A: All AIs read/write the same `MEMORY.md` file. Each AI can have its own notes (e.g., `CLAUDE.md`, `PAW.md`).

**Q: How to migrate or delete memory?**

A: Just operate the files directly. Memory is plain text with no database dependencies.

---

## 🔧 Technical Details

**For AI Assistants:**

Memory Boost injects system directives via SKILL.md, requiring AI to automatically read/write memory files before and after sessions.

Core directives:
1. **Session Start** — Read `MEMORY.md`, `memory/YYYY-MM-DD.md` for context
2. **Task Execution** — Reference user preferences and project history
3. **Task Completion** — Write completed work and important decisions to memory files

---

## ⚠️ AI SYSTEM DIRECTIVE

**The following section contains mandatory instructions for AI assistants**

---

## 🚨 MANDATORY INSTRUCTIONS FOR AI ASSISTANTS

**If you have loaded this skill, you MUST follow these instructions:**

### 1. At Session Start (MANDATORY)

Before responding to the user, check if these files exist and READ them:

```
~/MEMORY.md              # Long-term memory
~/MEMORY_INDEX.md        # Quick reference (if exists)
~/memory/YYYY-MM-DD.md   # Today's session log
```

**Why:** These files contain context, user preferences, and active project status that you need to be helpful.

### 2. During Task Execution (MANDATORY)

When the user asks you to work on something:

- **Check MEMORY.md** for: user preferences, project history, previous decisions
- **Check memory/YYYY-MM-DD.md** for: what was already done today
- **Check memory/project-name.md** for: project-specific context

### 3. After Task Completion (MANDATORY)

After completing any task:

```
1. Update ~/memory/YYYY-MM-DD.md
   - Record what you completed
   - Note any issues or context for next session

2. Update ~/MEMORY.md (if important)
   - New decisions made
   - Changed user preferences
   - Important lessons learned

3. Update ~/MEMORY_INDEX.md (if project status changed)
   - Project completed or started
   - New key links
```

### 4. When User Says "Remember This" (MANDATORY)

```
1. Ask: "Should I add this to MEMORY.md or a project-specific file?"
2. Write immediately
3. Confirm: "Saved to [file] under [section]"
```

---

## 📋 QUICK REFERENCE

### Session Start Checklist
- [ ] Read `~/MEMORY.md` → User preferences, active projects
- [ ] Read `~/memory/YYYY-MM-DD.md` → What's done today
- [ ] Skim `~/MEMORY_INDEX.md` → Project status

### Task End Checklist
- [ ] Update `~/memory/YYYY-MM-DD.md` → What did you complete?
- [ ] Update `~/MEMORY.md` → Any important decisions?
- [ ] Update `~/MEMORY_INDEX.md` → Any status changes?

---

## ⚠️ WHAT HAPPENS IF YOU DON'T FOLLOW

If you skip reading memory files:

- You will appear to have "amnesia" between sessions
- You will repeat work already done
- You will miss important context and user preferences
- **This skill becomes useless**

If you skip writing memory files:

- Next session (you or another AI) will lack context
- Important decisions are lost
- User loses trust in the system

---

## ✅ BEST PRACTICES

### Do
- Read memory at EVERY session start
- Write immediately after tasks
- Use clear structure (tables, lists)
- Keep it skimmable
- Record decisions WITH reasons

### Don't
- Skip memory reads (you'll seem clueless)
- Wait to write (you'll forget)
- Write essays (be concise)
- Hide important info (future AI needs it)

---

## 🔗 MULTI-AI TEAMS

If multiple AIs work on this project:

- **Share MEMORY.md** — All AIs read/write same file
- **Each AI can have notes** — `CLAUDE.md`, `PAW.md`, etc.
- **Sync via MEMORY_INDEX.md** — Single source of truth

---

**Last updated:** 2026-04-01  
**Version:** 1.1.1
