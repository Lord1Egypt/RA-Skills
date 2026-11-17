## Description:

Run approved long-running project work from file-backed state, continue through self-clearable tasks, pause cleanly at real gates, and recover across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebclawops](https://clawhub.ai/user/sebclawops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Project Loop to manage approved multi-step work that needs durable project state, validation, approval gates, pause/resume behavior, and recovery across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent watchdog cron can keep attempting recovery after a session ends.

Mitigation: Require explicit approval before any cron or watchdog setup, record its schedule and removal command, and remove the watchdog when the project reaches Done or Abandoned.

Risk: File-backed project state can drive long-running actions from stale or inconsistent state.

Mitigation: Keep project directories tightly controlled, verify state.json against actual outputs on every resume, and stop immediately if state.json cannot be updated.

Risk: Retrying denied obfuscated operations in smaller pieces may bypass safety controls.

Mitigation: Remove or override that instruction before deployment; do not retry operations denied for obfuscation without human review.

## Reference(s):

- [Project Loop ClawHub page](https://clawhub.ai/sebclawops/skills/project-loop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with file path templates, JSON state fields, and command-oriented operating rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces procedural operating guidance; does not generate binary assets.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
