## Description:

Guides users through Infini basic API and webhook integration with sandbox-first steps and runnable Node.js or Python examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cola234](https://clawhub.ai/user/cola234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide Infini payment integration, including Hosted Checkout, request signing, sandbox testing, webhook setup, troubleshooting, and production switch-over preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide uses a third-party webhook test receiver during sandbox testing.

Mitigation: Use only synthetic sandbox data and prefer a controlled webhook test endpoint when possible.

Risk: Payment webhook replay protection guidance is incomplete for production use.

Mitigation: Before going live, add timestamp freshness checks, duplicate event rejection, idempotent order handling, and constant-time signature comparison.

Risk: Users may treat the beginner integration guide as complete production security guidance.

Mitigation: Review the integration with production payment security requirements before handling real customers or production-derived identifiers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cola234/skills/infini-api)
- [Infini English Overview](https://developer.infini.money/docs/en/1-overview)
- [Infini Chinese Documentation](https://developer.infini.money/docs/zh)
- [Infini English Documentation](https://developer.infini.money/docs/en)
- [Infini API Notes](references/api-notes.md)
- [Infini Basic Integration Workflow](references/workflow.md)
- [Infini Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline code blocks and step-by-step status blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese or English guidance; defaults to sandbox and waits for user confirmation before advancing action steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
