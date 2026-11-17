## Description:

HuanZhi FA Pro gives Chinese-language startup founders fundraising readiness diagnosis, term-sheet red-flag analysis, negotiation guidance, and Capital EQ support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-innopower](https://clawhub.ai/user/ai-innopower)

### License/Terms of Use:

MIT-0

## Use Case:

External founders and startup operators use this skill to assess financing readiness, review term-sheet clauses, plan fundraising progress, and receive structured emotional support during investor outreach. It is oriented toward Chinese-language fundraising scenarios and should not replace legal, accounting, financial, or investment professionals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive BP, cap table, TS, and founder profile data may be retained locally under data/users or by host memory and reminder features.

Mitigation: Use redacted inputs unless local retention is acceptable, and require clear consent, deletion, and retention controls before operational use.

Risk: The artifact claims ClawHub audit status while the authoritative security verdict is suspicious.

Mitigation: Treat publisher security claims as unverified and review the skill, dependencies, and host permissions before installation.

Risk: Broad activation triggers and reminder behavior could surface fundraising guidance outside the user's intended context.

Mitigation: Narrow activation triggers, review scheduled-task settings, and confirm reminders before enabling them.

Risk: The skill provides fundraising, legal, financial, and term-sheet guidance that could be mistaken for professional advice.

Mitigation: Keep legal, accounting, financial, and investment decisions subject to qualified professional review.

Risk: Dependencies and network-facing preview content are under-scoped in the security evidence.

Mitigation: Pin or remove unused dependencies and inspect preview assets before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-innopower/skills/huanzhi-fa-skill-pro-v2-8-0)
- [Publisher Profile](https://clawhub.ai/user/ai-innopower)
- [System Prompt](artifact/references/system-prompt.md)
- [Knowledge Base](artifact/references/knowledge-base.md)
- [Response Templates](artifact/references/response-templates.md)
- [Output Schemas](artifact/references/outputs-schema.md)
- [Known Limitations](artifact/references/known-limitations.md)
- [Failure Handling](artifact/references/failure-handling.md)
- [Determinism Details](artifact/references/determinism-details.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with structured JSON outputs for fundraising diagnosis and term-sheet analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language responses are intended to be concise and may include local profile or progress data when the host enables file writes.]

## Skill Version(s):

2.8.6 (source: SKILL.md frontmatter and server release metadata; skill.json and CHANGELOG list earlier 2.8.1 artifacts)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
