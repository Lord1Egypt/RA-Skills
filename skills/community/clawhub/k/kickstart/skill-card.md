## Description:

Kickstart helps an OpenClaw agent set up workspace memory, core instruction files, sub-agent templates, heartbeat patterns, automation scaffolding, and API setup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jordymaui](https://clawhub.ai/user/jordymaui)

### License/Terms of Use:


## Use Case:

External OpenClaw users and developers use this skill to bootstrap or improve an agent workspace with persistent memory, safety rules, personas, sub-agent context templates, heartbeat checks, and automation setup patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain personal or sensitive workspace context.

Mitigation: Review and customize the copied memory files before use, keep sensitive values out of memory, and follow the included rule to load long-term memory only in direct sessions.

Risk: Heartbeat and cron-style automation can perform recurring background checks or notifications.

Mitigation: Enable automation only when desired, set quiet hours and rotation limits, and require explicit approval for external messages, public posts, and file edits.

Risk: Companion skills and integrations can expand the agent's authority.

Mitigation: Pin or separately review companion skills before installation, and review API configuration files for secret-handling requirements.

## Reference(s):

- [ClawHub Kickstart Skill Page](https://clawhub.ai/jordymaui/skills/kickstart)
- [Publisher Profile](https://clawhub.ai/user/jordymaui)
- [Kickstart Setup Guide](references/setup-guide.md)
- [Compaction Survival Guide](references/compaction-survival.md)
- [Memory Architecture](references/memory-architecture.md)
- [Context Bundle Protocol](references/context-bundle-protocol.md)
- [Automation Patterns](references/automation-patterns.md)
- [API & Integration Checklist](references/api-checklist.md)
- [Model Strategy](references/model-strategy.md)
- [Soul Library](references/soul-library.md)
- [Next Steps](references/next-steps.md)
- [Publisher Launch Link](https://x.com/jordymaui)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace file templates, setup walkthroughs, and automation patterns for an OpenClaw agent.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
