## Description:

23-validator bash security chain validated in production Claude Code deployments. Every check closed a real attack vector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebrierfox](https://clawhub.ai/user/thebrierfox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add shell-command safety guidance for OpenClaw agents, including validation categories, setup steps, and enforcement-mode recommendations for Bash and Zsh execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package claims production-grade shell validation but the submitted artifact contains only a summary and does not include the referenced full architecture/specification or validator logic.

Mitigation: Verify the missing specification or implementation before relying on the skill for shell-command enforcement.

Risk: Users may overestimate protection if the skill is deployed as prompt-level guidance without confirmed runtime enforcement.

Mitigation: Treat the skill as under-specified safety guidance until deployment tests prove command interception, refusal behavior, and audit or strict mode operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thebrierfox/skills/paid-bash-security-v1-1)
- [OpenClaw Bash Safety primer](https://clawhub.ai/skills/free-bash-safety-primer)
- [Production Agent Ops bundle](https://clawhub.ai/skills/production-agent-ops-battle-tested-architecture-pack)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, activation checks, enforcement-mode guidance, and validator-category summaries.]

## Skill Version(s):

1.1.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
