## Description:

Moses Coordinator monitors the local OpenClaw Gateway WebSocket for session events, checks Primary to Secondary to Observer sequencing, and logs detected violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a local coordinator that watches OpenClaw session events and records sequence violations for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent background execution can keep the coordinator running beyond an interactive review session.

Mitigation: Prefer foreground/manual use and avoid enabling launchd KeepAlive unless continuous monitoring is required.

Risk: The coordinator invokes a separate moses-governance audit script that is not bundled in this artifact.

Mitigation: Review and verify the external audit script before allowing this coordinator to execute it.

Risk: The skill monitors and logs sequence violations but should not be treated as complete blocking governance enforcement.

Mitigation: Use it as a review and alerting layer, and keep independent governance checks for enforcement decisions.

Risk: Runtime dependency installation can introduce unpinned package changes.

Mitigation: Install dependencies in a pinned virtual environment before running the coordinator.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunrisesillneversee/skills/moses-coordinator)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs local operator messages and audit-log entries when run as a daemon.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
