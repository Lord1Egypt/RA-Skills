## Description:

This skill gives agents a local self-reflection and memory workflow for evaluating work, learning from corrections, and improving future execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users and developers use this skill to maintain local execution-improvement memory from explicit corrections, self-reflection, and confirmed reusable patterns. It helps an agent retrieve relevant preferences or lessons before non-trivial work and update local memory after feedback or meaningful outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can shape future agent behavior across tasks.

Mitigation: Install only when persistent self-improvement memory is desired, and review learned entries regularly through the skill's memory inspection and export flows.

Risk: Setup steps may change agent steering files or workspace configuration.

Mitigation: Require exact diffs and explicit approval before edits to AGENTS.md, SOUL.md, workspace config, or HEARTBEAT.md.

Risk: Automatic memory writes could capture sensitive or inappropriate information.

Mitigation: Avoid storing secrets, sensitive personal data, third-party details, or instructions that change safety or permission rules; delete or decline unsafe entries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-self-improving)
- [Skill Homepage](https://clawic.com/skills/self-improving)
- [Security Boundaries](artifact/boundaries.md)
- [Learning Mechanics](artifact/learning.md)
- [Memory Operations](artifact/operations.md)
- [Setup Guide](artifact/setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory files under ~/self-improving/ and may propose edits to AGENTS.md, SOUL.md, workspace config, or HEARTBEAT.md.]

## Skill Version(s):

1.2.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
