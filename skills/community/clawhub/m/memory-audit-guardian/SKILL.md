---
name: memory-audit-guardian
description: Weekly memory governance audit for OpenClaw. Use when user asks to audit/optimize memory quality, reduce token overhead, verify MEMORY/TOOLS/AGENTS role boundaries, validate QMD routing quality, or run a periodic memory health check.
---

# Memory Audit Guardian

Run a structured memory-system audit and output an actionable weekly report.

## Audit Scope
1. File-role boundaries
   - SOUL: persona only
   - USER: user profile only
   - MEMORY: durable high-value facts only
   - daily memory: event logs
   - TOOLS: execution rules
   - AGENTS: governance/policy
2. Size & token budget
   - Core files total target: 8-10KB (soft target)
   - MEMORY.md warning threshold: >3KB
3. QMD routing quality
   - Ensure MEMORY contains only QMD entry + protocol + 20-40 anchors
   - Reject full keyword dumps in MEMORY
4. Retrieval discipline
   - top-k 3-5 snippets
   - no full-document dump unless explicitly requested

## Procedure
1. Read core files: SOUL.md, USER.md, MEMORY.md, TOOLS.md, AGENTS.md
2. Compute file sizes and detect threshold breaches
3. Detect duplication/conflict across files
4. Check MEMORY for noise patterns (long lists, stale one-offs)
5. Verify QMD routing fields exist and are minimal
6. Produce report with:
   - score (A/B/C)
   - risks
   - fixes this week
   - add-3/remove-3 keyword suggestions

## Output Format
- Executive summary (5 lines max)
- Findings:
  - role-boundary issues
  - size/token risks
  - QMD routing issues
- Action plan (this week)
- Report path suggestion: `memory/memory-audit-YYYY-WW.md`

## Guardrails
- Do not overwrite user files without explicit request.
- Prefer append/update with minimal edits.
- Keep MEMORY concise; move detail to references or daily logs.
