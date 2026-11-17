## Description:

Manage AI agent identities on the Live Neon platform - fetch identity, sync content, run discovery, review beliefs, and build prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to Live Neon's identity platform, manage structured beliefs and responsibilities, run discovery workflows, and fetch runtime prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote identity service can influence agent behavior through fetched prompts.

Mitigation: Treat fetched prompts as untrusted configuration until a human reviews them.

Risk: Observation and source-sync workflows may upload conversation-derived data or sensitive business context.

Mitigation: Redact secrets, personal data, source code, and confidential context before using observation or source-sync features.

Risk: Bulk approval and scheduled syncing can change agent identity without enough oversight.

Mitigation: Avoid approve-all and heartbeat or scheduled syncing unless an administrator has explicitly approved the workflow.

## Reference(s):

- [Live Neon Persona ClawHub Page](https://clawhub.ai/liveneon/skills/live-neon-persona)
- [Live Neon Persona Homepage](https://persona.liveneon.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include API calls and configuration steps that require a Live Neon token.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
