## Description:

Manages context overflow by handing off to a fresh subagent at 80% usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to checkpoint ongoing work and arrange continuation by a fresh agent when context is running low.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handoff guidance may carry forward settings that skip permission checks and user confirmations.

Mitigation: Review the inherited execution mode and flags before continuing; keep permission checks and user confirmation enabled for consequential actions.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-conserve-clear-context)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)

## Skill Output:

**Output Type(s):** [Files, Markdown, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown session checkpoints with continuation guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checkpoint path can be configured; the default is .claude/session-state.md.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
