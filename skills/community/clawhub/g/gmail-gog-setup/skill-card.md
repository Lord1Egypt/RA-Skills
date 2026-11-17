## Description:

Set up Gog CLI for Gmail access and authenticate agent mailboxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Gmail access for agent mailboxes through Gog CLI, including OAuth client setup, authentication, verification, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup asks users to install an unverified Gog executable system-wide.

Mitigation: Verify the Gog release with a trusted checksum or signature and prefer a user-local install path before use.

Risk: The setup requires handling Gmail OAuth credentials and a keyring password.

Mitigation: Use a dedicated Gmail account, store secrets outside shell history and shared environments, unset the password after authentication, and revoke OAuth access when it is no longer needed.

## Reference(s):

- [Gmail Gog Setup on ClawHub](https://clawhub.ai/stefanferreira/skills/gmail-gog-setup)
- [stefanferreira ClawHub profile](https://clawhub.ai/user/stefanferreira)
- [Gog CLI](https://gogcli.sh/)
- [Google Cloud OAuth setup](https://console.cloud.google.com/)
- [OpenClaw Gmail Pub/Sub docs](/automation/gmail-pubsub.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Gog CLI binary and Gmail OAuth credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
