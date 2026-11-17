## Description:

Synchronizes OpenClaw memory files into co-occurrence and semantic vector stores and provides enhanced search over those memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whoisme007](https://clawhub.ai/user/whoisme007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect OpenClaw MEMORY.md and memory/*.md files with co-occurrence and semantic-vector search so agents can retrieve related memories with stable IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw memory files may contain private notes, credentials, customer data, or sensitive project details.

Mitigation: Review and scope memory files before syncing, and exclude sensitive files or workspaces from processing.

Risk: Co-occurrence and semantic-vector adapters may store memory content, memory IDs, search terms, or metadata outside the original memory files.

Mitigation: Confirm each adapter's storage location, retention behavior, remote-service use, and deletion process before enabling synchronization.

Risk: The release evidence says the skill broadly processes OpenClaw memory files without clear scoping controls.

Mitigation: Run it in an isolated workspace first and keep semantic or co-occurrence sync disabled until the intended files and adapters are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whoisme007/skills/memory-integration)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces adapter usage guidance, configuration details, and memory-search integration behavior for an agent.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
