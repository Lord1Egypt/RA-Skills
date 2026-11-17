## Description:

Shared MiniMax / MMX CLI operating rules for XiaoMei, DaLong, YuanQi, and the main coordinator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep MiniMax/MMX capability mapping, quota interpretation, and multi-agent workflow rules consistent across related agent guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to propagate rule changes across shared guidance, memory, learnings, and other agents' rules.

Mitigation: Require reviewable diffs and explicit confirmation before applying persistent or team-wide guidance changes.

Risk: Incorrect MiniMax/MMX quota or routing guidance could become shared across multiple agents.

Mitigation: Verify MiniMax/MMX facts against the shared source of truth before rollout and keep role-specific guidance minimal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1yihui/skills/minimax-team-rules)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only guidance; no executable payload.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
