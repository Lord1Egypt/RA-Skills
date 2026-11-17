## Description:

MailboxValidator (mailboxvalidator.com). Use this skill for ANY MailboxValidator request — searching and reading data. Whenever a task involves MailboxValidator, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using an OOMOL-connected account can check whether email addresses are disposable or free and validate a single address's deliverability signals through MailboxValidator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute installer code and startup synchronization can make persistent changes to installed agent skills.

Mitigation: Review setup before installing, use a verified oo CLI release, and set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

Risk: Email addresses submitted for validation pass through OOMOL to MailboxValidator.

Mitigation: Submit only addresses you are authorized to process and account for both services' data handling practices.

## Reference(s):

- [MailboxValidator](https://www.mailboxvalidator.com)
- [MailboxValidator single validation API documentation](https://www.mailboxvalidator.com/api-single-validation)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [MailboxValidator ClawHub release](https://clawhub.ai/oomol/skills/oo-mailbox-validator)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Email validation results depend on the selected action and its live input schema.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
