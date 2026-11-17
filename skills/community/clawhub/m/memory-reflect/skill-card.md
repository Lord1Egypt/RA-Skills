## Description:

Memory Reflect reviews recent conversations and daily notes, extracts durable insights, and consolidates them into long-term memory when triggered by cron, heartbeat, or explicit request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phernandez](https://clawhub.ai/user/phernandez)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users use this skill to periodically or manually distill recent activity into durable memory, update MEMORY.md, and append a reflection log to the daily note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private recent activity and update long-term memory during background runs.

Mitigation: Use it only where that behavior is expected, and require explicit confirmation or a reviewable diff before MEMORY.md is changed.

Risk: Unreviewed reflection can preserve inaccurate, stale, or duplicate information in long-term memory.

Mitigation: Review MEMORY.md changes and the daily-note reflection log after runs, especially when the skill flags uncertainty.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/phernandez/skills/memory-reflect)
- [ClawHub publisher profile](https://clawhub.ai/user/phernandez)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with code-style tool call examples and file update instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update MEMORY.md and append a daily-note reflection log when executed by an agent.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
