## Description:

Automatically checks OpenClaw sessions, creates daily memory notes, periodically refines MEMORY.md, and can back up deleted sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justzerox](https://clawhub.ai/user/justzerox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to preserve useful session history as workspace memory, including daily summaries and periodic long-term memory refinement. It supports unattended heartbeat runs and manual invocation when users want current conversations summarized into memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically turns recent chat transcripts into persistent workspace memory, so injected, misleading, or sensitive session content may be carried forward.

Mitigation: Review generated Daily notes and MEMORY.md regularly, and treat generated memory as draft material that needs human review.

Risk: The skill can read recent session history and scan session files while writing memory, configuration, and state files in the workspace.

Mitigation: Limit processSessionsAfter and maxSessionsPerRun, and disable filesystem scanning or notifications when they are not needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/justzerox/skills/heartbeat-memory)
- [Configuration reference](references/config.md)
- [API reference](references/api.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [markdown, configuration, text, guidance]

**Output Format:** [Markdown memory files with JSON configuration and state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily notes under ./memory/daily/, updates ./MEMORY.md on the configured schedule, and may send completion notifications.]

## Skill Version(s):

0.0.7 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
