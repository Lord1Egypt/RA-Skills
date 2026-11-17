## Description:

Enables SMS verification-code login or registration by sending a phone code and exchanging the submitted code for an authenticated session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guolai806](https://clawhub.ai/user/guolai806)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user requests phone-number login, SMS-code login, or phone-number registration against the configured SMS login service. It guides the agent through requesting a verification code, submitting the code, and handling common error responses without exposing complete tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured SMS login endpoint receives phone numbers and SMS verification codes.

Mitigation: Use only a trusted, approved HTTPS endpoint and make users explicitly confirm that their phone number and SMS code will be sent to that service.

Risk: Login responses, cookie jars, or tokens may expose full session credentials.

Mitigation: Avoid printing raw login responses or cookie jars, redact tokens from all output, and show at most a short token prefix when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guolai806/skills/login-digitalme)
- [ClawHub publisher profile](https://clawhub.ai/user/guolai806)
- [Clawdis primary environment](http://180.184.28.174:30080)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash curl examples and JSON response handling notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SMS_LOGIN_BASE_URL plus curl and jq; handles phone numbers, SMS codes, cookies, and tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
