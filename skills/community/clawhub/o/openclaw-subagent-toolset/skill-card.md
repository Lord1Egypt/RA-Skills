## Description:

Provides predefined constrained tool subsets for spawning sub-agents tailored to task types like Explore, Plan, Verification, Coding, and Secretary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to choose task-specific tool subsets when delegating work to sub-agents. It helps prompts communicate intended permissions for exploration, planning, verification, coding, and documentation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool subsets are soft prompt constraints and do not enforce sandbox boundaries.

Mitigation: Use platform-enforced permissions for strict isolation and review generated sub-agent prompts before execution.

Risk: Coding mode is documented as high privilege.

Mitigation: Use Coding mode only for user-directed coding tasks and review proposed commands or file edits in sensitive workspaces.

Risk: The Secretary tool subset contains a glob_search contradiction.

Mitigation: Resolve the Secretary tool list before relying on it for strict tool-boundary guidance.

## Reference(s):

- [OpenClaw Subagent Toolset on ClawHub](https://clawhub.ai/hanxiao-bot/skills/openclaw-subagent-toolset)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with tool subset lists and prompt text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces soft prompt constraints; it does not enforce sandbox boundaries by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
