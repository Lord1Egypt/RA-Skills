## Description:

An AI-first knowledge management system with evolvable memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryren2024](https://clawhub.ai/user/terryren2024)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Memory Work to set up a Markdown-based personal memory workspace where an agent can structure weekly focus, materials, tools, skills, and long-term notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to become a persistent personal-memory workspace that can read, summarize, and update local notes.

Mitigation: Review the package before installing, define clear privacy and retention rules, and narrow startup and skill triggers to the minimum needed.

Risk: The artifact gives broad persistent read/write authority over personal notes.

Mitigation: Require explicit approval before deletion, bulk reorganization, memory/profile writes, or sharing content outside the workspace.

Risk: The package includes an unrelated family-information file that should not be in a public skill package.

Mitigation: Remove the family-information file before public release or installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terryren2024/skills/memory-work)
- [Project Homepage](https://github.com/yiliqi78/memory-work)
- [Titans: Learning to Memorize at Test Time](https://arxiv.org/abs/2501.00663)
- [MemSkill: Transferrable and Evolvable Memory Skill Library](https://arxiv.org/abs/2501.03313)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown workspace files and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local memory, profile, focus, materials, tools, and skill-library notes when authorized by the host agent or user.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
