## Description: <br>
Read Sentry issues, events, and production errors via the Sentry REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeninja23](https://clawhub.ai/user/codeninja23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect Sentry production diagnostics, list recent issues and events, retrieve issue details, and request stack traces when needed using a read-only Sentry token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sentry diagnostics can expose production error data and sensitive user or application details. <br>
Mitigation: Use a dedicated read-only Sentry token, keep redaction enabled by default, and avoid --no-redact in shared or logged sessions. <br>
Risk: Stack traces may reveal sensitive implementation details. <br>
Mitigation: Request stack traces only when needed and only in a trusted environment. <br>


## Reference(s): <br>
- [Native Sentry on ClawHub](https://clawhub.ai/codeninja23/native-sentry) <br>
- [Sentry](https://sentry.io) <br>
- [Sentry Auth Tokens](https://sentry.io/settings/account/api/auth-tokens/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; helper commands return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENTRY_AUTH_TOKEN. PII is redacted by default, and stack traces are omitted unless requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
