## Description:

Watches desktop activity, maintains a real-time task stack, detects forgotten tasks after interruptions, and gently reminds the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huilingp](https://clawhub.ai/user/huilingp)

### License/Terms of Use:

MIT

## Use Case:

Developers and knowledge workers use this skill to monitor local desktop activity, maintain a task stack, detect likely forgotten tasks after interruptions, and receive context-rich reminders or focus reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Continuous local logging of active applications, window titles, and optional ActivityWatch data can expose sensitive work context.

Mitigation: Review before installing, configure excluded apps and working hours, restrict local file permissions, and use cleanup retention before relying on privacy claims.

Risk: Optional screenshot capture can emit raw screen images for analysis.

Mitigation: Keep screenshot capture disabled unless explicitly needed, use only trusted analysis paths, and avoid enabling it around sensitive screens.

Risk: Some documented privacy controls may not be enforced by the provided scripts.

Mitigation: Independently verify exclusions, working-hour behavior, retention, and installer provenance in the target environment.

## Reference(s):

- [Intent Guardian ClawHub Skill Page](https://clawhub.ai/huilingp/skills/intent-guardian)
- [Heartbeat Integration Guide](references/heartbeat-integration.md)
- [Forgetting Detection Algorithm Reference](references/forgetting-detection.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON/JSONL-backed summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce proactive reminders, task stack summaries, daily focus reports, setup snippets, and local data-management guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
