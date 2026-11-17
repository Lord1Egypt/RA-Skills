## Description:

Prompt Optimizer classifies user requests by complexity, rewrites prompts across role, context, task, constraints, and examples, and routes work to single or parallel agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyu9](https://clawhub.ai/user/liyu9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users install this skill to standardize prompt optimization, classify tasks from L1 to L4, choose implicit or explicit confirmation, and route complex work across multiple agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change shared OpenClaw prompt-handling behavior by appending rules to agent-notes.md.

Mitigation: Review artifact/rules/prompt-optimization.md before installation, back up agent-notes.md, and install only when persistent prompt-routing changes are intended.

Risk: Uninstalling the package may not remove appended memory rules.

Mitigation: Record the backup path created during installation and manually compare or restore agent-notes.md if the prompt-optimization behavior should be removed.

Risk: Broad task-classification and multi-agent routing rules may change expected agent responses.

Mitigation: Run the included L1-L4 validation cases after installation and verify the exact package slug and source before enabling it in a shared workspace.

## Reference(s):

- [Prompt Optimizer ClawHub Page](https://clawhub.ai/liyu9/skills/prompt-optimizer-100)
- [Core Prompt Optimization Rules](artifact/rules/prompt-optimization.md)
- [System Design Document](https://feishu.cn/docx/He9Gdnpd4oTydyxSAZYcVQ1dnTc)
- [PromptPilot Reference](https://www.producthunt.com/products/promptpilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with structured response templates and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append persistent prompt-handling rules to OpenClaw memory and influence routing across configured agents.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact documentation also labels the prompt system as V3.0/3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
