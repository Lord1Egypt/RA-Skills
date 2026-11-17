## Description:

Pod AI (callpod.ai). Use this skill for ANY Pod AI request — reading, creating, and updating data. Whenever a task involves Pod AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Pod AI through an OOMOL-connected account, including creating outbound voice-agent calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructs running remote CLI installers, and the external installers and CLI implementation were not verified.

Mitigation: Review the CLI separately and use a verified release where available before installing it.

Risk: Creating an outbound call changes external state and contacts a phone number.

Mitigation: Confirm the exact call payload and its effect with the user before running the action.

## Reference(s):

- [Pod AI API documentation](https://www.callpod.ai/docs/api-reference/introduction)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Pod AI homepage](https://callpod.ai/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use action-specific JSON payloads; inspect the live action schema before execution.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
