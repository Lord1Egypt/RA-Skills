## Description:

Connect OpenClaw agents to iMessage, RCS, and SMS without a Mac or phone using Claw Messenger's relay server and API key authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demegire](https://clawhub.ai/user/demegire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect agents to iMessage, RCS, and SMS through Claw Messenger, including setup, configuration, status checks, service switching, and inbound-message policy guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm install instructions can expose users to supply-chain changes after review.

Mitigation: Review the package before installation and pin a specific reviewed version where possible.

Risk: The cm_live API key authorizes messaging for the user's account.

Mitigation: Keep the key out of version control, store it only in the local OpenClaw configuration, and rotate or revoke it from the dashboard when needed.

Risk: Open inbound direct-message handling may allow unwanted senders to reach the agent.

Mitigation: Use the pairing or allowlist DM policy unless open inbound messages are explicitly required.

Risk: Message content and metadata pass through a managed relay service.

Mitigation: Review the privacy policy and pricing terms before routing sensitive or high-volume messaging through the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/demegire/skills/imessage-claw-messenger)
- [Claw Messenger documentation](https://clawmessenger.com/docs)
- [npm package](https://www.npmjs.com/package/@emotion-machine/claw-messenger)
- [Claw Messenger privacy policy](https://clawmessenger.com/privacy)
- [Claw Messenger pricing](https://clawmessenger.com/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API key handling, DM policy, service switching, and Claw Messenger relay configuration details.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
