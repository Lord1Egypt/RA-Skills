## Description:

Memphis helps OpenClaw agents maintain local-first persistent memory, semantic recall, decision tracking, encrypted vault entries, and multi-agent collaboration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elathoxu-crypto](https://clawhub.ai/user/elathoxu-crypto)

### License/Terms of Use:

MIT

## Use Case:

Developers, teams, researchers, and agent builders use Memphis to give OpenClaw agents persistent local memory, searchable project context, decision records, and optional collaboration features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and auto-journaling can capture sensitive project, personal, customer, or proprietary information.

Mitigation: Disable or tightly scope auto_journal, define redaction and retention rules before use, and avoid recording secrets or sensitive workspace content unless storage controls have been reviewed.

Risk: Vault retrieval and secret storage can expose credentials if password handling, local file permissions, or sharing behavior are misconfigured.

Mitigation: Use environment-backed vault passwords, restrict local file access, and review every vault retrieval path before using Memphis in sensitive workspaces.

Risk: Share-sync, IPFS, partner messaging, and multi-agent workflows can disclose memories or decisions outside the local workspace.

Mitigation: Keep network sharing, partner messaging, and daemon mode disabled by default, enable them only for trusted peers, and review shared chains before synchronization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elathoxu-crypto/skills/memphis)
- [Memphis documentation](https://github.com/elathoxu-crypto/memphis/tree/master/docs)
- [Memphis repository](https://github.com/elathoxu-crypto/memphis)
- [Memphis support issues](https://github.com/elathoxu-crypto/memphis/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing instructions for installing, initializing, journaling, recalling, decision tracking, vault use, backups, and optional sharing.]

## Skill Version(s):

3.0.0 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
