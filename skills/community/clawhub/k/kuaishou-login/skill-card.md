## Description:

Automates QR-code login to the Kuaishou Creator Platform by opening the login page, capturing the QR code, monitoring login state, and returning success or timeout status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[action2227](https://clawhub.ai/user/action2227)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators can use this skill to guide an agent through QR-code login to the Kuaishou Creator Platform and receive login status updates with screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live login QR code and authenticated page screenshots may be exposed through agent output or logs.

Mitigation: Use only in a trusted local environment where screenshots and logs are not shared.

Risk: Anyone who can see the returned QR code during its validity window may be able to initiate the login flow.

Mitigation: Prefer scanning directly in the user's own browser session, then close or log out of the session after use.

## Reference(s):

- [Kuaishou Creator Platform](https://creator.kuaishou.com/)
- [ClawHub skill page](https://clawhub.ai/action2227/skills/kuaishou-login)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Screenshots]

**Output Format:** [Markdown status text with browser screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a QR-code screenshot, then either a login-success screenshot or a timeout message after up to 120 seconds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
