## Description:

A CRM sales assistant for finance and tax prospecting that scores leads, researches companies through Qichacha, identifies intent signals, drafts sales pitches, and proposes follow-up actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and developers use this skill to support finance and tax CRM workflows: finding prospects, scoring leads, preparing customer briefs, drafting outreach, and planning follow-up tasks before CRM write or messaging actions are executed by other installed tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Qichacha API credentials could be sent to a configured endpoint that is not the official service.

Mitigation: Use the official HTTPS Qichacha endpoint unless a private endpoint is fully trusted and controlled.

Risk: Stored Qichacha key and secret values could be exposed or reused outside the intended environment.

Mitigation: Protect the key and secret as credentials, restrict access to plugin configuration, and rotate them if exposure is suspected.

Risk: Draft next actions could lead to bulk CRM creation, email, or group-message workflows if executed without review.

Mitigation: Preview proposed arguments and require explicit user confirmation before companion tools perform CRM writes or messaging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-crm-agent)
- [Qichacha OpenAPI](https://openapi.qcc.com/)
- [@huo15/huo15-huihuoyun-odoo](https://www.npmjs.com/package/@huo15/huo15-huihuoyun-odoo)
- [Prospect research notes](artifact/docs/v02-prospect-research.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured tool responses with lead scores, company details, intent signal summaries, sales briefs, pitch variants, follow-up plans, next-action drafts, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Company search and detail lookup require user-provided Qichacha credentials. CRM write, email, and group-message actions are proposed as drafts and require explicit user confirmation before execution by companion tools.]

## Skill Version(s):

0.2.1 (source: SKILL.md frontmatter, package.json, openclaw.plugin.json, changelog, evidence release; released 2026-05-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
