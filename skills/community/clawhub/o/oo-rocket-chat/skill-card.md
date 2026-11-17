## Description:

Connects an agent to Rocket.Chat to inspect rooms and messages and to post, update, or delete messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Rocket.Chat can inspect their profile, rooms, and messages, and post, edit, or delete messages through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded software without separate approval, and the installer and connector implementations were not verified.

Mitigation: Review automatic setup, install the CLI from a verified release, review the Rocket.Chat access granted to OOMOL, and keep confirmation requirements for posting, editing, and deleting messages.

## Reference(s):

- [Rocket.Chat homepage](https://www.rocket.chat)
- [Rocket.Chat API documentation](https://developer.rocket.chat/apidocs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-rocket-chat)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action requests and structured responses with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include reads, posting and editing messages, and message deletion; confirmation is required for writes and destructive actions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
