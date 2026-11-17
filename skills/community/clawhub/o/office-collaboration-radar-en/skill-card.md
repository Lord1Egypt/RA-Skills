## Description:

Extract an evidence-linked collaboration status card from chat logs, meeting notes, and project updates when a user explicitly requests one.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamyeed](https://clawhub.ai/user/yamyeed)

### License/Terms of Use:

MIT-0

## Use Case:

Project teams use this skill to turn user-supplied English collaboration records into evidence-linked status cards covering progress, decisions, actions, risks, dependencies, and items for human review. It can also produce a radar chart and structured exports when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incomplete, tentative, or conflicting source records could lead to unsupported status claims or action details.

Mitigation: Tie claims to source snippets, use Not provided when facts are absent, and review conflicts flagged by the skill before sharing.

Risk: Pattern-based redaction may not catch every credential or sensitive detail in supplied records.

Mitigation: Pre-redact live credentials, customer data, and sensitive HR material, then inspect generated cards and exports before sharing.

## Reference(s):

- [Office Collaboration Radar EN on ClawHub](https://clawhub.ai/yamyeed/skills/office-collaboration-radar-en)
- [Office Collaboration Radar (Chinese package)](https://clawhub.ai/yamyeed/skills/office-collaboration-radar)

## Skill Output:

**Output Type(s):** [Markdown, JSON, CSV, SVG]

**Output Format:** [Evidence-linked status card in Markdown or JSON, with optional CSV or mapping JSON exports and an SVG radar chart]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence snippets are limited to 80 characters; common PII and credential patterns are redacted.]

## Skill Version(s):

0.1.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
