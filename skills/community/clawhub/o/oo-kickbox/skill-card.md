## Description:

Search and read Kickbox data, including disposable email checks and email verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check whether email addresses or domains are disposable and verify email deliverability through a connected Kickbox account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup executes remote installer code whose effects could not be inspected, and automatic skill synchronization may broaden changes to an agent's skills.

Mitigation: Review and preinstall a verified oo CLI release before agent execution, and check its automatic skill synchronization settings.

Risk: Email addresses submitted for checks are processed by OOMOL and Kickbox.

Mitigation: Submit only email addresses you intend OOMOL and Kickbox to process.

## Reference(s):

- [Kickbox](https://kickbox.com/)
- [Kickbox API documentation](https://docs.kickbox.com/docs/using-the-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads; JSON action responses and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
