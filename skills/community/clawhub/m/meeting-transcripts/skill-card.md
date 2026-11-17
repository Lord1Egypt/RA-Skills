## Description:

Capture meeting transcripts from Fireflies.ai via polling or webhooks, extract action items, decisions, and summaries, and write structured markdown to memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessewunderlich](https://clawhub.ai/user/jessewunderlich)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to set up Fireflies.ai transcript capture, fetch recent or specific meetings, and save meeting summaries, action items, decisions, and full transcripts as structured markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional webhook server can expose sensitive meeting capture if it is publicly reachable without strong authentication.

Mitigation: Configure a strong webhook secret, avoid public exposure without additional access controls, and review the deployment path before enabling webhooks.

Risk: Saved meeting transcripts may contain sensitive participant, business, or personal information.

Mitigation: Treat saved meeting files as sensitive untrusted data and define an appropriate retention or deletion process.

## Reference(s):

- [Fireflies.ai GraphQL API](https://api.fireflies.ai/graphql)
- [ClawHub skill page](https://clawhub.ai/jessewunderlich/skills/meeting-transcripts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files and JSON status messages, with setup guidance and shell commands in markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes meeting files under memory/meetings and may update polling state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
