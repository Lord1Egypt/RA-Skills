# Incident Postmortem

**Platforms:** Claude · Openclaw · Codex
**Domain:** DevOps / SRE

## Purpose

A conversational postmortem facilitator for engineering teams. Guides the team through a structured, blameless retrospective after any production incident and produces a complete postmortem document — covering timeline reconstruction, root cause analysis, impact quantification, and concrete action items.

## When to Use

- After any production incident (P0–P3) that needs a written postmortem
- When the incident is resolved but the team hasn't had time to write it up
- When the team wants structured guidance through the root-cause analysis
- When the postmortem needs to be shareable with non-technical stakeholders

## What It Does

1. Collects incident severity, type, time window, affected services, and customer impact
2. Routes to the right RCA focus areas based on incident type (infrastructure outage, application error, security incident, data integrity, performance degradation, third-party dependency)
3. Reconstructs a chronological timeline with key milestones: Origin · Detection · Escalation · Diagnosis · Mitigation · Resolution
4. Quantifies impact: affected users, MTTD, MTTR, SLA breach, and regulatory obligations
5. Walks through a guided 5 Whys root-cause analysis using the selected focus areas
6. Generates a complete postmortem document with summary, impact metrics, timeline, root cause, contributing factors, what went well, and what could be improved
7. Reviews and finalizes action items — ensuring each has a specific description, an owner, a due date, and a priority tier

## Note

This skill facilitates the postmortem process — it does not replace engineering judgment or legal review. For incidents that trigger regulatory obligations (GDPR, HIPAA, PCI-DSS, SOC 2), consult your legal or compliance team before making public disclosures. Never include customer PII, credentials, or internal secrets in the document.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.