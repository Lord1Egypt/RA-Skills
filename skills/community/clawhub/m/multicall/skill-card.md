## Description:

Multicall is packaged as a blockchain multicall analysis skill, but server security evidence says it actually provides shell commands for local entry and configuration management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers can use this card to evaluate a ClawHub skill release that claims blockchain multicall analysis but, according to server security evidence, behaves as a local data-management CLI. It should not be used for blockchain or protocol security analysis until the documented purpose matches the implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill name and documentation claim blockchain multicall analysis, while server security evidence says the artifact actually manages local stored entries and configuration.

Mitigation: Do not use it as a multicall or blockchain analysis skill until the name, documentation, and behavior are aligned.

Risk: Server security guidance reports a configuration-update weakness that can lead to local command execution.

Mitigation: Avoid running configuration commands with untrusted input and replace the sed-based configuration update with a non-interpreted safe write path before deployment.

Risk: The artifact persists user-provided entries locally and can delete or export that local data.

Mitigation: Do not store sensitive notes, keys, incident details, or protocol data in this skill, and review persistence, deletion, and export behavior before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/multicall)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, list, search, remove, export, and configure local entries under the MULTICALL_DIR data directory.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
