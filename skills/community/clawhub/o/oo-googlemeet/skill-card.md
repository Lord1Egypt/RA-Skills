## Description:

Operate Google Meet to read, create, and update meeting spaces and retrieve conference records, participants, recordings, smart notes, and transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to manage Google Meet spaces and retrieve conference details, participants, recordings, smart notes, and transcripts through a connected Google account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unpinned remote code without a separate user approval step.

Mitigation: Review and install a verified oo CLI release separately before use; decide whether to disable automatic agent-skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Sensitive meeting data passes through OOMOL, and the remote installer and hosted connector implementation were not verified.

Mitigation: Connect only the intended Google account and scopes.

## Reference(s):

- [oo CLI command documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Google Meet API reference](https://developers.google.com/workspace/meet/api/reference/rest/v2)
- [Google Meet](https://workspace.google.com/products/meet/)

## Skill Output:

**Output Type(s):** [API calls, JSON data, Guidance]

**Output Format:** [JSON responses and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include action data and an execution ID.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
