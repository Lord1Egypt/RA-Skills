## Description:

Native Sentry helps agents read Sentry issues, events, and production errors through the Sentry REST API using a read-only token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeninja23](https://clawhub.ai/user/codeninja23)

### License/Terms of Use:


## Use Case:

Developers and production support engineers use this skill to inspect recent Sentry issues, retrieve issue and event details, and summarize production error health without leaving the agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable Sentry base URL could send the Sentry token to an untrusted host if it is misconfigured or influenced.

Mitigation: Use only trusted HTTPS Sentry hosts for SENTRY_BASE_URL or --base-url, and avoid overriding the default endpoint unless self-hosting requires it.

Risk: Sentry data may include sensitive production details, including stack traces or personal data.

Mitigation: Use narrowly scoped read-only tokens, keep default redaction enabled, avoid --no-redact in shared or logged environments, and request stack traces only when needed.

## Reference(s):

- [Native Sentry on ClawHub](https://clawhub.ai/codeninja23/skills/native-sentry)
- [Sentry](https://sentry.io)
- [Sentry auth tokens](https://sentry.io/settings/account/api/auth-tokens/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sentry API responses are redacted for emails and IP addresses by default; stack traces require an explicit include flag.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
