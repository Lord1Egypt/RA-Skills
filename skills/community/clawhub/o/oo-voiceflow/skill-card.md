## Description:

Voiceflow (voiceflow.com). Use this skill for ANY Voiceflow request — reading, creating, and updating data. Whenever a task involves Voiceflow, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Voiceflow project users use this skill to inspect environments and knowledge bases, start conversation sessions, and send actions through their OOMOL-connected Voiceflow account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup instructions run a remote CLI installer without separate approval or integrity checks.

Mitigation: Review and approve CLI installation separately, and prefer a verified fixed release.

Risk: Voiceflow requests pass through OOMOL, which injects connected credentials server-side.

Mitigation: Account for this data path when deciding what information to send, and retain confirmation before actions that change Voiceflow state.

## Reference(s):

- [Voiceflow](https://www.voiceflow.com)
- [Voiceflow API authentication documentation](https://docs.voiceflow.com/api-reference/authentication)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured JSON action inputs and responses with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response content varies by Voiceflow action.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
