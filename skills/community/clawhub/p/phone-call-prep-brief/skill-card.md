## Description:

Build a one-page call brief before an AI agent or human places or takes an important phone call: objective, talking points, consent/disclosure checklist, voicemail script, and fallback plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruti3](https://clawhub.ai/user/ruti3)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and agent operators use this skill to prepare concise call briefs before important outbound, inbound, or callback phone conversations. It turns call goals, context, boundaries, voicemail needs, and recording-disclosure considerations into a one-page markdown checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may include passwords, payment details, SSNs, medical record numbers, or full account numbers in call context.

Mitigation: Ask only for necessary call-planning details and exclude secrets or regulated identifiers from the brief.

Risk: A call brief could be mistaken for legal guidance about regulated outreach, recording consent, or jurisdiction-specific obligations.

Mitigation: Keep consent and regulated-call notes high level, treat the brief as a checklist, and require separate confirmation of legal obligations.

Risk: The skill could be misused to support impersonation, fraud checks bypass, unlawful robocalls, or misrepresentation.

Mitigation: Maintain explicit do-not-say boundaries and decline planning that involves impersonation, unlawful outreach, or bypassing verification.

Risk: Calls involving minors, vulnerable adults, healthcare, financial products, debt collection, or other high-stakes topics may need human oversight.

Mitigation: Recommend human review and define a human escalation path before an agent speaks in high-stakes or sensitive scenarios.

## Reference(s):

- [Phone Call Prep Brief on ClawHub](https://clawhub.ai/ruti3/skills/phone-call-prep-brief)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown one-page call brief with a summary table, talking points, boundaries, voicemail script when applicable, recording and consent notes, assumptions, and a pre-dial checklist.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only output; no code execution, network access, credential handling, or telephony API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
