---
name: HIIC-skill-vetter
version: 1.0.0
description: Practical skill vetting workflow for AI agents. Prioritizes clear yes/no risk judgments, concise conclusions, and business-aware risk tolerance before installing a skill.
---

# HIIC Skill Vetter

A practical, business-aware vetting workflow for OpenClaw skills.

Goal: give a **short, clear conclusion** about whether a skill is safe to use, without over-penalizing normal capabilities like external API access, scheduled tasks, screenshots, or documented platform credentials.

---

## When to Use

Use this skill when:
- the user asks whether a skill is safe
- the user wants a quick vet before installing a skill
- the user wants a concise risk conclusion instead of a long report
- the user wants a portfolio-wide skill review

---

## Core Policy

### Default stance
A skill is considered **safe by default** unless there is evidence of one of the following:
- privilege escalation
- hidden or unrelated sensitive-data access
- hidden external exfiltration
- dynamic execution of untrusted input
- obvious behavior beyond the claimed scope

### Important calibration rules
The following **do not automatically make a skill unsafe**:
- documented external API access
- reading `.env`, tokens, cookies, or API keys that are clearly required for the skill's purpose
- cron / session / service / screenshot / browser state features
- package installation steps that are explicit and relevant
- platform/account integration when it is the point of the skill

These should usually be treated as:
- normal capability, or
- caution item, not rejection

---

## Judgment Standard

Output should be short and explicit.

Use this format:

```text
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [name]
Source: [local / GitHub / ClawHub / other]
───────────────────────────────────────
RISKS:
• External Access: [Yes / No]
• Sensitive Access: [Yes / No / Required for stated purpose]
• Dynamic Execution: [Yes / No]
• Privilege Escalation: [Yes / No]
• Scope Mismatch: [Yes / No]
───────────────────────────────────────
RISK LEVEL: [🟢 LOW / 🟡 MEDIUM / 🟠 HIGH]
VERDICT: [✅ SAFE TO INSTALL / ⚠️ INSTALL WITH CAUTION / 🛑 HUMAN REVIEW RECOMMENDED]
NOTES: [1-3 short lines]
═══════════════════════════════════════
```

Keep the conclusion concise.
Do not generate a long audit unless the user explicitly asks.

---

## Decision Rules

### ✅ SAFE TO INSTALL
Use when:
- no privilege escalation found
- no suspicious unrelated sensitive access found
- no hidden exfiltration found
- behavior matches the skill's stated purpose

Typical examples:
- weather skills
- summarizers
- search tools
- GitHub helpers
- browser helpers
- document tools

### ⚠️ INSTALL WITH CAUTION
Use when:
- the skill touches accounts, cookies, cloud resources, tokens, or publishing flows
- but that access is clearly related to the skill's purpose
- and there is no evidence of malicious or hidden behavior

Typical examples:
- social publishing tools
- cloud storage tools
- document platform integrations
- account-bound automation tools

### 🛑 HUMAN REVIEW RECOMMENDED
Use when:
- there is real ambiguity about scope
- or the skill reads sensitive material not clearly required
- or the skill contains dynamic execution, suspicious remote behavior, or unclear hidden logic

Do **not** use this level just because a skill uses tokens, APIs, cron, screenshots, or service config for legitimate reasons.

---

## What Actually Counts as High Risk

Treat these as strong warning signals:
- `sudo`, privileged system modification, or elevated install requirements
- `eval`, `exec`, `bash -c`, `sh -c`, subprocess execution with untrusted input
- reading unrelated secrets or private files without business justification
- hidden telemetry or undocumented outbound endpoints
- obvious mismatch between claim and implementation
- encoded/obfuscated payloads tied to execution or exfiltration

---

## Practical Review Workflow

1. Read `SKILL.md`
2. Review helper scripts and config
3. Identify whether sensitive/platform access is **required for the stated purpose**
4. Look for actual high-risk behavior
5. Return a short conclusion

If a repeatable scan helps, use:

```bash
python3 vet_scan.py <skill-dir>
python3 vet_scan.py <skill-dir> --format json
```

---

## Review Philosophy

- Business-required permissions are not automatic red flags.
- A platform integration skill will naturally touch platform credentials.
- A browser automation skill will naturally touch cookies/session state.
- A cloud skill will naturally touch API keys and remote resources.
- The question is not “does it have permissions?”
- The question is: **“does it use those permissions in a way that is expected, explicit, and limited to its purpose?”**

---

## Remember

Aim for good judgment, not paranoia theater.

If there is no concrete sign of malicious or over-scoped behavior, do not overcall risk.
