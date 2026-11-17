## Description:

AI Self-Improving Agent v2 helps an agent learn from mistakes, user corrections, best practices, and successful complex tasks through passive memory capture, proactive checks, and reusable skill generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiqingge](https://clawhub.ai/user/haiqingge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve lessons from errors, corrections, and successful workflows so future sessions can check relevant memory and propose reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory logging can persist secrets, credentials, private code, sensitive prompts, or internal paths.

Mitigation: Avoid recording sensitive information and review memory entries before sharing or using them in broader workflows.

Risk: Generated skill files can persist unreviewed agent instructions.

Mitigation: Manually review generated SKILL.md files before allowing them to load, auto-trigger, or influence future agent behavior.

Risk: The generated-skill writer can write outside the intended directory according to the security evidence.

Mitigation: Fix the skill-name path validation issue before using this skill in shared or untrusted workflows.

## Reference(s):

- [Self Improving Agent ClawHub listing](https://clawhub.ai/haiqingge/skills/haiqing-self-improving-agent)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated SKILL.md content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists memory logs and generated skill definitions in OpenClaw directories when its helper scripts are run.]

## Skill Version(s):

2.0.0 (source: frontmatter, skill.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
