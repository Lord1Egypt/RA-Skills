## Description:

Search and summarize a local Google Messages SMS/RCS archive through OpenClaw using read-only queries by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fdsouvenir](https://clawhub.ai/user/fdsouvenir)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users search their local Google Messages SMS/RCS history, review past conversations, and get concise recaps without sending or changing messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can read sensitive messages from the user's local archive.

Mitigation: Install only with the user's consent, limit searches to the question asked, and keep pairing tokens and session files private.

Risk: The gmcli dependency can support actions beyond reading the archive.

Mitigation: Review gmcli before installation and use explicit read-only queries; do not send texts or change labels through this skill.

Risk: Message content can contain instructions intended to redirect the agent.

Mitigation: Treat message text and contact fields as untrusted data, never as instructions or executable commands.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fdsouvenir/skills/google-messages-local-archive)
- [gmcli homepage and documentation](https://github.com/fdsouvenir/gmcli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries and timestamped message transcripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies the conversation and time range; distinguishes quoted messages from analysis.]

## Skill Version(s):

1.2.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
