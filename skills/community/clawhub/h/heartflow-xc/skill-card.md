## Description:

HeartFlow is a cognitive and self-healing agent layer that adds reasoning, local memory, psychology and verification checks, and command-line or daemon interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a local cognitive layer for reasoning, persistent memory, self-checking, and HeartFlow command or daemon workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory and memory-injection behavior can place user text into future system-prompt context.

Mitigation: Use the skill only in trusted single-user environments, review stored memory before reuse, and avoid enabling the Hermes memory-injection plugin in shared or untrusted projects.

Risk: Host-level code execution is available with weak isolation.

Mitigation: Do not pass untrusted code to codeExecutor or self-initiated execution paths; run the skill with least privilege and external sandboxing when execution features are needed.

Risk: Daemon use introduces a local long-running interface that depends on shutdown-token configuration.

Mitigation: Set SHUTDOWN_TOKEN before using the daemon and avoid daemon mode in shared environments unless socket access and process ownership are controlled.

Risk: Semantic-search features depend on the npm dependency tree.

Mitigation: Audit and update npm dependencies before relying on semantic-search functionality.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/heartflow-xc)
- [Publisher profile](https://clawhub.ai/user/yun520-1)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JavaScript and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local setup, memory, daemon, plugin, and code-execution guidance depending on the user's request.]

## Skill Version(s):

2.9.1 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
