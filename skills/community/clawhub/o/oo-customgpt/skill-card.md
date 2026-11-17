## Description:

CustomGPT.ai (customgpt.ai). Use this skill for ANY CustomGPT.ai request — reading, creating, and updating data. Whenever a task involves CustomGPT.ai, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to inspect CustomGPT agents, conversations, documents, and messages, and to create conversations or send messages through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs remote CLI installation code without a separate approval or integrity check; installer behavior is unverified.

Mitigation: Review and approve the CLI installation separately before using the skill, including whether it installs other agent skills.

Risk: Requests pass through OOMOL, and write actions can change CustomGPT.ai state.

Mitigation: Understand that requests pass through OOMOL and keep the required confirmations for CustomGPT writes.

## Reference(s):

- [CustomGPT.ai](https://customgpt.ai)
- [CustomGPT API documentation](https://docs.customgpt.ai/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [CustomGPT.ai skill release](https://clawhub.ai/oomol/skills/oo-customgpt)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Markdown with inline shell commands and JSON payload examples; connector results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use action names and JSON inputs matching the live connector schema; reads return account data, while write actions create conversations or send messages.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
