## Description:

Enables a manager agent to self-diagnose, identify defects, track improvements, audit skill health, and record diagnostic findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjl1004](https://clawhub.ai/user/wjl1004)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add Chinese-language self-diagnostic routines that review recent behavior, memory discipline, skill integrity, and health signals for a manager agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for automatic heartbeat, daily, and every-task behavior that can run without direct user invocation.

Mitigation: Require explicit invocation or host-level limits before enabling automatic triggers.

Risk: The skill can read agent memory, behavioral files, and installed skill information during diagnostics.

Mitigation: Run it with least-privilege file access and review the permitted diagnostic scope before installation.

Risk: The skill can write persistent diagnostic notes to an evolution log.

Mitigation: Review the log path and require confirmation for persistent writes in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjl1004/skills/manager-self-evolution)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Text and Markdown diagnostic summaries with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent diagnostic notes to an evolution log when checks find issues.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
