## Description:

Email verification skill for MailCheck API - verify emails, bulk processing, authenticity analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bnuyts](https://clawhub.ai/user/bnuyts)

### License/Terms of Use:

MIT

## Use Case:

Developers, security teams, and operations teams use this skill to verify individual or bulk email addresses and analyze message headers for spoofing, phishing, and fraud signals through the MailCheck API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email addresses, bulk lists, and full headers may contain personal or sensitive information that is sent to the external MailCheck API.

Mitigation: Use the skill only for data you are authorized to process through MailCheck, and avoid submitting sensitive full headers unless third-party processing is approved.

Risk: API keys passed directly in commands may be exposed in logs, prompts, or command history.

Mitigation: Set MAILCHECK_API_KEY in the environment instead of passing keys as command parameters.

Risk: The security evidence recommends workplace or regulated deployments receive extra review before installation.

Mitigation: Complete organizational review before installing or using the skill in workplace, regulated, or compliance-sensitive environments.

## Reference(s):

- [MailCheck API documentation](https://api.mailcheck.dev/docs)
- [ClawHub skill page](https://clawhub.ai/bnuyts/skills/mailcheck-email-verification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured command responses from MailCheck API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MAILCHECK_API_KEY when available and supports single email, bulk email, and header authenticity analysis inputs.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
