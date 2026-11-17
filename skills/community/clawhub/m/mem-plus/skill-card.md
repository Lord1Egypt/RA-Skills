## Description:

Mem Plus helps an agent store, search, rank, and manage local personal memory with identity-aware and Chinese bigram boosts for precise recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars82311111](https://clawhub.ai/user/mars82311111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an AI assistant persistent local memory, retrieve relevant workspace context, remember new notes, wake up project context, and remove stored memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can index and return broad local workspace file contents, including files under ~/.openclaw/workspace.

Mitigation: Use it only in trusted local workspaces, review indexed files before search or mine operations, and keep secrets outside indexed paths.

Risk: Credential filtering may not prevent all sensitive local file content from being returned.

Mitigation: Do not store credentials in the workspace or persistent memory, and review retrieved results before sharing them outside the local agent session.

Risk: The forget command performs memory deletion that should be treated as permanent.

Mitigation: Confirm memory identifiers before deletion and keep separate backups for memories that must be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mars82311111/skills/mem-plus)
- [Publisher profile](https://clawhub.ai/user/mars82311111)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local persistent memory stores and can return indexed workspace content.]

## Skill Version(s):

1.6.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
