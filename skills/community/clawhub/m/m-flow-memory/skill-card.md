## Description:

M-Flow Memory helps agents add, index, search, and distill memory using the M-Flow framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sora-mury](https://clawhub.ai/user/sora-mury)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to integrate M-Flow memory workflows for adding, indexing, searching, and distilling session or knowledge content across agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided content may be stored and indexed in M-Flow memory with unclear retention and access controls.

Mitigation: Use the skill only when persistence is intended, and confirm where M-Flow stores data, how records are deleted, and which users or agents can search them before handling sensitive content.

Risk: The skill imports a sibling local M-Flow package through a path insertion mechanism.

Mitigation: Install and run it only in a trusted workspace, and ensure the sibling m_flow dependency path is not writable by untrusted users.

## Reference(s):

- [M-Flow Memory ClawHub listing](https://clawhub.ai/sora-mury/skills/m-flow-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, bash, and environment configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local M-Flow APIs and persist user-provided memory content when used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
