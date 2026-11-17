## Description:

Self-reflection, self-criticism, self-learning, and self-organizing memory help an agent evaluate its work, catch mistakes, and improve across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theo-jobs](https://clawhub.ai/user/theo-jobs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add local self-reflection and correction-driven memory so agents can record explicit feedback, organize reusable preferences, and cite memory sources in later work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory and steering-file edits can change agent behavior across sessions.

Mitigation: Review setup edits before applying them, keep the operating mode conservative when appropriate, and periodically inspect or delete ~/self-improving/ contents.

Risk: Memory files may retain sensitive or unwanted information if boundaries are not followed.

Mitigation: Do not store credentials, medical data, financial data, third-party information, or location and access patterns; use the documented forget and export flows for audit and removal.

Risk: Optional always-on self-improvement behavior may be broader than some users intend.

Mitigation: Skip SOUL.md core-drive text and HEARTBEAT automation unless continuous self-improvement behavior is explicitly desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theo-jobs/skills/hamster-self-improving)
- [Skill homepage](https://clawic.com/skills/self-improving)
- [Security boundaries](artifact/boundaries.md)
- [Setup guide](artifact/setup.md)
- [Learning mechanics](artifact/learning.md)
- [Memory operations](artifact/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on local memory files under ~/self-improving/ and optional steering-file edits.]

## Skill Version(s):

1.2.9 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
