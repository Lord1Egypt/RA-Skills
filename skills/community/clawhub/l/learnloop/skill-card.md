## Description:

Continuous learning protocol for Claude that captures corrections, errors, and user preferences into native auto-memory so the next session remembers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Learnloop to help Claude Code capture corrections, failed command lessons, user preferences, project constraints, and external references as local memories for future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes auto-loaded future-session memories from broad conversation cues without requiring explicit per-item approval.

Mitigation: Require the agent to ask before saving each memory, avoid storing sensitive personal, business, credential, or private system details, and periodically inspect and delete stale memory entries.

Risk: Stale memories can mislead future work if paths, commands, or project facts change.

Mitigation: Verify recalled paths, functions, flags, and repo state against the current workspace before acting, then update or delete stale memories.

## Reference(s):

- [Learnloop ClawHub homepage](https://clawhub.ai/skills/learnloop)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown status messages with file paths and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Claude project memory files and MEMORY.md entries when activated.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
