## Description:

Production-validated OpenClaw skills built for production Claude Code deployments, covering compaction, loop termination, session memory, bash security, agent memory scoping, coordinator mode, and forked agent architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebrierfox](https://clawhub.ai/user/thebrierfox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this bundle for OpenClaw production-agent operations guidance, including context management, loop termination, memory persistence, bash safety, coordinator resume integrity, and forked-agent architecture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle may enable long-term memory and multi-agent workflows.

Mitigation: Install it only when those operations features are intended, review all phase files before use, and enable persistent memory deliberately.

Risk: Persistent memory can survive across sessions or environment resets when the memory directory environment variable is configured.

Mitigation: Set the memory environment variable only in environments where cross-session persistence is acceptable.

## Reference(s):

- [Paid Bundle V1.1 on ClawHub](https://clawhub.ai/thebrierfox/skills/paid-bundle-v1-1)
- [Context Death Spiral Prevention](https://clawhub.ai/skills/free-compaction-primer)
- [OpenClaw Bash Safety](https://clawhub.ai/skills/free-bash-safety-primer)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes phased architecture guidance and setup steps for OpenClaw environments.]

## Skill Version(s):

1.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
