## Description:

Memory Distill extracts key information from conversations, condenses long dialogue into concise summaries, writes categorized memory files, supports retention cleanup, and can run manually, by Cron, or through HEARTBEAT triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve decisions, tasks, project details, preferences, and temporary notes from long sessions in structured memory files before resetting context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist private conversation details, personal preferences, project information, verification codes, and temporary links into files that outlive the current session.

Mitigation: Review and approve destination files, retention settings, and sensitive-content handling before running the skill, especially before enabling scheduled distillation.

Risk: Scheduled unattended runs can collect and write memory without a fresh user review at the time of execution.

Mitigation: Keep scheduled mode disabled until retention, cleanup, and sensitivity filters are confirmed; use manual runs for sensitive workspaces.

Risk: Old memory files can remain available to future sessions or other tools if cleanup is not configured or reviewed.

Mitigation: Use retention settings and periodic cleanup review, and avoid enabling automatic deletion unless the deletion policy is understood.

## Reference(s):

- [Memory Distill ClawHub skill page](https://clawhub.ai/systiger/skills/memory-distill)
- [distill-config.json](references/distill-config.json)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries, structured memory file entries, JSON configuration examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent memory files such as MEMORY.md, USER.md, and memory/YYYY-MM-DD.md; scheduled operation is configurable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
