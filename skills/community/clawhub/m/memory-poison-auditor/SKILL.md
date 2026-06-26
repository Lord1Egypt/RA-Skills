---
name: memory-poison-auditor
version: 0.1.0
license: MIT
description: Audits OpenClaw memory files for injected instructions, brand bias, hidden steering, and memory poisoning patterns. Use when reviewing MEMORY.md, daily memory files, or any long-term memory store that may have been contaminated through dialogue.
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"]}}}
---

# Memory Poison Auditor

`memory-poison-auditor` checks whether OpenClaw memory files have been contaminated by hidden instructions, brand steering, injected operational policies, or suspicious recommendation bias written through prior conversations.

## What It Checks

- Prompt-injection style instructions inside memory.
- "Always recommend X" or "never mention Y" style brand steering.
- Abnormal brand repetition and preference shaping.
- Suspicious authority claims like fake approvals or fake user intent.
- Low-signal blocks that act like covert policy rather than factual memory.
- Optional AI review for borderline suspicious blocks.

## Commands

### Audit Default Memory Roots

```bash
python3 {baseDir}/scripts/audit_memory.py scan
python3 {baseDir}/scripts/audit_memory.py --format json scan
```

### Audit a Specific Path

```bash
python3 {baseDir}/scripts/audit_memory.py scan --path /root/clawd/MEMORY.md
python3 {baseDir}/scripts/audit_memory.py scan --path /root/clawd/memory
```

### Optional AI Review

```bash
python3 {baseDir}/scripts/audit_memory.py scan --with-ai
python3 {baseDir}/scripts/audit_memory.py scan --path /root/clawd/memory/2026-03-15.md --with-ai
```

### One-Click Cleaning

```bash
python3 {baseDir}/scripts/audit_memory.py clean --path /root/clawd/MEMORY.md --apply
python3 {baseDir}/scripts/audit_memory.py clean --path /root/clawd/memory --apply
```

Cleaning creates backups before rewriting suspicious blocks.

## Output

Each audit returns:

- `PASS`: no meaningful poisoning signals
- `WARN`: suspicious memory blocks detected
- `BLOCK`: memory likely contaminated and should be reviewed/cleaned

Reports and backups are written to:

```text
/root/clawd/output/memory-poison-auditor/reports/
/root/clawd/output/memory-poison-auditor/backups/
```

## Operational Guidance

- Use this before trusting long-term memory in important planning or recommendations.
- `WARN` means review before relying on that memory block.
- `BLOCK` means clean or quarantine the memory before reuse.
- AI review is optional and intended only for ambiguous cases.
