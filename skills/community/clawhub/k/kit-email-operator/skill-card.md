## Description:

AI-powered tool to create, personalize, schedule, send, and track professional email campaigns using Kit API integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevjade](https://clawhub.ai/user/kevjade)

### License/Terms of Use:


## Use Case:

Creators, marketers, and business operators use this skill to draft brand-matched email campaigns, create Kit broadcasts, target tags or segments, schedule sends, and review campaign performance. It supports welcome, nurture, sales, announcement, re-engagement, and educational email workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use powerful Kit credentials with broad email and account authority.

Mitigation: Use narrowly scoped Kit credentials when possible and keep sends in draft or test mode until audience, subject, send time, and recipient count are confirmed.

Risk: Stored Kit credentials could remain exposed if workspace files or prior stored versions are accessible.

Mitigation: Avoid entering secrets in command-line arguments, limit workspace access, and rotate credentials if they were previously stored with this version.

Risk: Connecting broad memory or voice files can expose unrelated business context to email generation.

Mitigation: Connect only purpose-specific voice guides or memory files and review generated personalization before sending.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/kevjade/skills/kit-email-operator)
- [Kit Email Marketing Operator README](artifact/README.md)
- [Setup Guide](artifact/SETUP.md)
- [Installation Guide](artifact/INSTALLATION.md)
- [Email Marketing Best Practices](artifact/references/email-best-practices.md)
- [Kit Personalization Tags Reference](artifact/references/kit-personalization.md)
- [Email Sequence Templates](artifact/references/sequence-templates.md)
- [Subject Line Formulas](artifact/references/subject-line-formulas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown responses with email drafts, subject line options, setup guidance, JavaScript API examples, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform Kit API actions when configured with credentials and user approval; otherwise produces drafts, analysis, and guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
