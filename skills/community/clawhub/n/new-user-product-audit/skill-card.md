## Description:

Guides an agent through a first-time user's browser journey in ZenStory AI and produces an evidence-based Chinese product diagnostic report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT-0

## Use Case:

Product teams and authorized auditors use this skill to assess onboarding, creative workflows, usability, and AI writing quality through realistic new-user journeys, then prioritize findings supported by screenshots and reproduction steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser audits may change a live product or consume production resources.

Mitigation: Require explicit authorization before production use, respect message and time budgets, avoid payments, and clean up or label test content.

Risk: Test credentials, verification emails, screenshots, and logs may reveal sensitive information.

Mitigation: Use only synthetic identities, protect credentials and run artifacts, redact secrets from reports, and delete temporary verification data after the audit.

Risk: Disposable-email registration relies on an external mail.tm service.

Mitigation: Review the dependency before use and use operator-provided test accounts when disposable email is inappropriate.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/worldwonderer/skills/new-user-product-audit)
- [ZenStory run guidance](references/zenstory.md)
- [Audit scenario library](references/scenario-library.md)
- [Fiction quality rubric](references/fiction-quality-rubric.md)
- [Diagnostic report template](references/report-template.md)
- [Disposable inbox guidance](references/disposable-inbox.md)
- [mail.tm documentation](https://docs.mail.tm)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files]

**Output Format:** [Chinese Markdown diagnostic report with supporting screenshots and logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates observed facts from opinions; links evidence, severity, and prioritized recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
