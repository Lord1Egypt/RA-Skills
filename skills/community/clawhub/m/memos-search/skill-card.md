## Description:

Uses the MemOS REST API to save, read, list, search, and delete persistent memory records for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hope7709](https://clawhub.ai/user/hope7709)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to connect an agent to a controlled MemOS REST service for persistent memory storage, retrieval, search, listing, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad memory reads or searches may expose sensitive stored content.

Mitigation: Keep MEMOS_API_URL pointed at a trusted local or controlled service and avoid storing secrets unless the service's data handling is acceptable.

Risk: Delete operations remove both memory files and vector index entries.

Mitigation: Require explicit confirmation before deleting memory files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hope7709/skills/memos-search)
- [Publisher profile](https://clawhub.ai/user/hope7709)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the MEMOS_API_URL environment setting for the target MemOS REST service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
