## Description:

Migrates memories, preferences, writing style, workflow data, and tool preferences from other AI assistants into OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myclaw-ai](https://clawhub.ai/user/myclaw-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to import memory, preferences, writing style, tool preferences, and workflow context from prior AI assistants. It supports prompt-guided migration from cloud assistants and local file scanning for supported local agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local-agent path asks the agent to read broad local AI configuration and memory files.

Mitigation: Use local auto-scan only after selecting the exact files to import, and review and redact the migration preview before writing memory files.

Risk: ChatGPT export ZIPs can contain sensitive conversation history, and the security evidence flags the ZIP parser as unsafe for sensitive exports.

Mitigation: Do not upload untrusted ZIP files; import only trusted exports and remove sensitive data before accepting the migration.

Risk: Imported rules or preferences may change future agent behavior.

Mitigation: Review all imported rules and remove entries that should not influence future agent sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myclaw-ai/skills/openclaw-memory-transfer)
- [MyClaw.ai](https://myclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, memory-file updates, and structured JSON from the ChatGPT export parser]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Imported data is shown for user review before memory files are written.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
