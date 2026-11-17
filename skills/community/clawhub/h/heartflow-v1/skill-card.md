## Description:

HeartFlow 心虫 is a cognitive and self-healing engine that adds structured reasoning, memory, verification, and reflection workflows for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a local cognitive layer for memory, reasoning, self-checking, and reflection around agent responses and workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports host code execution, local persistence, prompt-level memory injection, optional daemon use, and outbound network capability.

Mitigation: Install only after reviewing those capabilities, run in a constrained environment, and avoid exposing sensitive credentials.

Risk: Security evidence says a stale vulnerable dependency should be updated or removed before production use.

Mitigation: Update or remove the stale vulnerable dependency and rescan the release before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/heartflow-v1)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)
- [audit-zombie.js](artifact/references/audit-zombie.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local memory or state files, inject prompt-level memory, use an optional daemon, and perform outbound network operations when invoked.]

## Skill Version(s):

2.9.0 (source: SKILL.md frontmatter, package.json, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
