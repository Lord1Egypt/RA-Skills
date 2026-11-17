## Description:

Generates Excel reports for Chinese government procurement opportunities and sends them by SMTP email for the govb business workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangpengle](https://clawhub.ai/user/zhangpengle)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and agents use this skill to fetch Chinese government procurement opportunity data, filter it by date or keywords, produce an Excel summary, and send the report to configured recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends real email using stored SMTP credentials.

Mitigation: Verify SMTP recipients and sender settings before each send, protect the EMAIL_* configuration file, and test with an override recipient before operational use.

Risk: The runtime depends on an unbundled govb_fetcher component that was not available for review.

Mitigation: Install only from a trusted source and pin dependencies before using the skill in production.

Risk: The configuration loader checks the current working directory for .env before the user config directory.

Mitigation: Run the skill from a trusted working directory or use a fixed, user-private configuration path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangpengle/skills/goverment-bidding-email)
- [Publisher profile](https://clawhub.ai/user/zhangpengle)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text guidance and CLI commands; runtime output includes SMTP email and Excel files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EMAIL_* configuration, govb-email and govb-fetcher commands, and an available govb_fetcher runtime component.]

## Skill Version(s):

0.1.4 (source: server release evidence; artifact metadata declares 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
