## Description:

Captures agent learnings, errors, corrections, and feature requests in markdown logs for later review and promotion to durable project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragon-wlf](https://clawhub.ai/user/dragon-wlf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to capture corrections, command failures, knowledge gaps, and requested capabilities as structured markdown entries. Teams can review those entries and promote broadly useful learnings into project or agent memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and promoted memory entries can carry incorrect guidance or sensitive details into future agent sessions.

Mitigation: Review every proposed write to instruction or memory files, keep learning logs project-local unless intentionally shared, and redact secrets, raw transcripts, and command output.

Risk: Always-on or global hooks can create broad reminder injection and may inspect command output for error patterns.

Mitigation: Prefer project-local setup, avoid global hooks and empty matchers, enable only the reminder hook by default, and add error-output detection only in trusted environments.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/dragon-wlf/skills/min)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and optional hook code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-local learning logs and optional reminder output; users should avoid logging secrets or raw transcripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
