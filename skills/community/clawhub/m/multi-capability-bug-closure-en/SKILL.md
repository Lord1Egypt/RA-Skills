---
name: multi-capability-bug-closure
description: >-
  Unified bug investigation and closure by combining source code, database,
  server logs, and software platform query capabilities. Use when users require
  evidence-based conclusions from real data rather than static code analysis only.
---

# Multi-Capability Bug Closure Skill

## When to Use

Use this skill when the user requires:

- Proactive use of available capability systems to complete bug investigation
- Real evidence from databases and server logs
- Verifiable conclusions and root-cause analysis
- A full closure loop: locate -> prove -> conclude -> recommend

This skill must prioritize real runtime evidence and must not conclude from code reading alone.

## Mandatory Guiding Prompt (Keep Original Intent)

> Proactively use the currently available capability system. Complete problem localization and evidence-based reasoning by yourself (preferably with real database and server-side data), then provide conclusions and causes. Do not conclude based on code reading alone. Since you can query databases, server logs, and actual software platform operations, complete the full closed-loop investigation autonomously. I only care about final conclusions backed by evidence.

---

## Prerequisite Check: Four Capability Systems (Required)

Before each investigation, verify all four capabilities are available and readable:

1. Source code access capability (for understanding and localization)
2. Database read capability (for deep validation)
3. Server log download and analysis capability (for behavioral and timeline evidence)
4. Software platform query capability (for business-side verification)

### Validation Criteria

- **Source code capability**: can read related code files in the workspace (at least one core router/service file).
- **Database capability**: can execute at least one read-only SQL query (for example, `select 1`).
- **Server log capability**: can read log-skill configuration and access a target log directory or sample logs.
- **Platform query capability**: related platform skill is readable, and its docs/API description are readable.

### If Any Capability Is Missing (Must Notify User)

If any capability is missing, first notify that evidence closure cannot be guaranteed, then provide supplementation recommendations:

- Source code capability: provide relevant source context or key directories directly
- Database capability: add MCP services for the target system (Postgres/SQLite/Redis, etc.)
- Server log capability: install or add [server-log-analysis](https://clawhub.ai/hgvgfgvh/server-log-analysis)
- Platform query capability: add a query skill or MCP tools for the target business platform

Do not provide a final root-cause conclusion before capabilities are complete. Provide only an evidence-gap checklist.

---

## Standard Workflow (Required)

1. **Structure the problem**
   - Extract time window, service name, error keywords, and identifiers (SN/ID/traceId).
2. **Log-side evidence (server)**
   - Pull raw logs in the target time window.
   - Measure frequency, grouping, and continuity of anomalies.
3. **Database-side evidence**
   - Query object existence, relationships, status, and timestamps in key tables.
   - Cross-check across databases when needed.
4. **Code-side localization**
   - Locate exception enums, throw paths, and routing branch conditions.
   - Use code only to explain mechanism, not to replace real-data conclusions.
5. **Platform-side validation**
   - Validate object status and business configuration through platform queries.
6. **Merge the evidence chain**
   - Connect evidence in this order: logs -> database -> code mechanism -> platform validation.
7. **Output final conclusion**
   - Classify as data issue / code issue / configuration issue / environment issue.
8. **Provide fix recommendations and verification standards**
   - Give executable steps and clear pass criteria for closure.

---

## Output Template (Required)

```markdown
## Problem Summary
[One-sentence summary of symptom and impact]

## Key Evidence
- Log evidence: [time, service, key lines, frequency stats]
- Database evidence: [tables, conditions, query results]
- Code evidence: [trigger path and branch conditions]
- Platform evidence: [API/config validation results]

## Root-Cause Assessment
[Final root cause + category: data/code/config/environment]

## Confidence
[High/Medium/Low] + [reason]

## Fix Recommendations
1. [Actionable step]
2. [Actionable step]

## Verification Criteria
- [Metric 1, e.g. error count reaches zero]
- [Metric 2, e.g. mapping restored]
```

---

## Constraints

- Do not fabricate evidence.
- Do not skip database or log evidence and jump straight to conclusions.
- If a capability is unavailable, explicitly declare the evidence gap and request supplementation.
- For sensitive credentials, prefer environment variables or secret managers; do not expose plaintext in outputs.
