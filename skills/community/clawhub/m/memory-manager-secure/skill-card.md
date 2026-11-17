## Description:

Automatically creates and maintains an OpenClaw MEMORY.md long-term memory file with scheduled updates, rule-based filtering, optional LLM analysis, and sensitive-data detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zx0018](https://clawhub.ai/user/zx0018)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to initialize a MEMORY.md file and keep selected session-derived events organized through manual commands or scheduled updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain conversation-derived details in MEMORY.md.

Mitigation: Review stored content periodically, purge stale or sensitive entries, and keep MEMORY.md permissions restrictive.

Risk: When an API key is configured, selected session-log lines may be sent to the configured LLM provider endpoint.

Mitigation: Use a trusted HTTPS provider URL, use a dedicated low-privilege API key, and disable scheduled updates until the script and provider settings are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zx0018/skills/memory-manager-secure)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash command snippets and generated MEMORY.md content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update MEMORY.md and OpenClaw cron configuration in the user's workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
