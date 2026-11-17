## Description:

Install, update, and safely configure the OpenClaw Zulip channel plugin from ClawHub or npm; use for bot credentials, access policies, opt-in features, drain recovery, and setup verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ftlc-ian](https://clawhub.ai/user/ftlc-ian)

### License/Terms of Use:

MIT

## Use Case:

Developers and administrators use this skill to install and configure a Zulip channel for OpenClaw, restrict who can invoke it, and verify the integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a plugin grants capabilities from an external package.

Mitigation: Confirm the publisher and review plugin capabilities before installation or update.

Risk: Exposed bot credentials or broad chat access can permit unauthorized use.

Mitigation: Keep the API key in the gateway service environment or SecretRef and allowlist explicit trusted Zulip emails.

Risk: Reaction triggers, topic history, and forwarded execution approvals can expand access or expose context.

Mitigation: Enable these features only when needed; scope access policies and approvers and review topic-history privacy settings.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ftlc-ian/skills/openclaw-zulip-channel)
- [ClawHub plugin listing](https://clawhub.ai/ftlc-ian/plugins/openclaw-channel-zulip)
- [Plugin configuration README](https://github.com/FtlC-ian/openclaw-channel-zulip/blob/main/README.md)
- [Plugin changelog](https://github.com/FtlC-ian/openclaw-channel-zulip/blob/main/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorization before installation or configuration changes.]

## Skill Version(s):

2026.10.13 (source: ClawHub release and setup guide)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
