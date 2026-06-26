# 🔒 Privacy & Data Governance — Nora Persona Framework

> **Last updated:** 2026-06-18
> **Applies to:** v1.4.1+

---

## 1. What This Skill Stores

Nora Persona Framework stores the following data locally:

| Data Category | What | Where | Why |
|---------------|------|-------|-----|
| Persona Files | SOUL.md / IDENTITY.md / AGENTS.md | `{workspace}/` | Define your AI's personality |
| Watchdog Reports | Consistency check results, drift scores | `{workspace}/memory/persona-check-YYYY-MM-DD.md` | Track personality drift over time |
| Backup Files | Previous SOUL.md before overwrite | `{workspace}/SOUL.md.bak` | Safety rollback |

**All data is stored locally on your machine.** Nothing is uploaded to cloud services.

---

## 2. Data Retention

| Data | Default Retention | How to Delete |
|------|-------------------|---------------|
| Persona files | Until you delete | Delete SOUL.md / IDENTITY.md / AGENTS.md manually |
| Watchdog reports | 180 days from creation | Say "清除人格检查记录" or delete `memory/persona-check-*.md` |
| Backup files | Until overwritten by next backup | Delete `SOUL.md.bak` |

**Automatic cleanup:** Watchdog will prompt you to review and optionally purge reports older than 180 days.

---

## 3. Consent Controls

**This skill NEVER modifies your workspace files without asking.**
- Before generating SOUL.md/IDENTITY.md/AGENTS.md: shows a preview and asks for confirmation
- Before saving watchdog reports: asks "保存这次的人格检查报告吗？"
- File overwrites: existing SOUL.md is backed up to `.bak` before modification
- No network calls: this skill does not perform any web searches or external API calls

---

## 4. Your Control Commands

| Command | Effect |
|---------|--------|
| "清除人格检查记录" | Delete all watchdog reports |
| "不保存这次报告" | Skip saving watchdog report for this check |
| "恢复之前的 SOUL.md" | Restore from SOUL.md.bak backup |

---

## 5. What This Skill NEVER Does

- ❌ Send your data to third-party servers
- ❌ Upload persona files or watchdog reports to cloud services
- ❌ Use your data to train external models
- ❌ Modify files without confirmation
- ❌ Exfiltrate credentials or environment variables
