## Description:

Anticipates needs, keeps work moving, and improves through use so the agent gets more proactive over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to make an agent anticipate next steps, recover active task context, maintain local proactive state, and follow through within learned boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local proactive notes under ~/proactivity may accumulate sensitive user or project details.

Mitigation: Review those files periodically and avoid storing secrets in proactive memory or state.

Risk: Workspace behavior files such as AGENTS, TOOLS, SOUL, or HEARTBEAT can alter how the agent behaves if edited without careful review.

Mitigation: Require explicit approval and review the exact shown snippets before allowing edits outside ~/proactivity.

Risk: Proactive follow-up can cross user boundaries if high-impact actions are treated as routine.

Mitigation: Require approval before external communication, spending, deletion, scheduling changes, or commitments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/proactivity)
- [Skill homepage](https://clawic.com/skills/proactivity)
- [Setup guide](setup.md)
- [Memory template](memory-template.md)
- [Migration guide](migration.md)
- [Opportunity signals](signals.md)
- [Execution patterns](execution.md)
- [Boundary learning](boundaries.md)
- [State routing](state.md)
- [Recovery flow](recovery.md)
- [Heartbeat rules](heartbeat-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local state files under ~/proactivity and workspace integration snippets that require approval before edits outside ~/proactivity.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
