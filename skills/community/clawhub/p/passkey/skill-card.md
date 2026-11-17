## Description:

Implement WebAuthn passkeys avoiding critical security and compatibility pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement passkey authentication with WebAuthn while avoiding common security, compatibility, storage, registration, authentication, user experience, and testing pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passkey authentication affects account security, and framework-specific details can change over time.

Mitigation: Validate recommendations against the target framework, current WebAuthn library documentation, and the application's recovery and risk requirements before deployment.

Risk: Incorrect passkey ceremony configuration can create replay, phishing, cloned-authenticator, compatibility, or account recovery risks.

Mitigation: Review challenge uniqueness and expiry, origin validation, sign-count handling, trusted library usage, fallback access, and cross-browser testing before production use.

## Reference(s):

- [Passkey skill page](https://clawhub.ai/ivangdavila/skills/passkey)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with implementation notes and code or configuration recommendations when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable skill code; recommendations should be reviewed against the target framework and current WebAuthn library documentation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
