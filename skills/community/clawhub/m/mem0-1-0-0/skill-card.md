## Description:

Mem0 adds a conversational memory layer for Clawdbot that stores, searches, lists, and deletes user preferences, patterns, and context through Mem0-backed scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:

ISC

## Use Case:

Developers and agent operators use this skill to give Clawdbot persistent conversational memory for recalling user preferences, prior context, and interaction patterns. It supports memory search, creation, listing, deletion, and configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived memories are stored persistently and may include personal or sensitive information.

Mitigation: Avoid storing secrets or sensitive personal data, and keep memory writes limited to explicit user requests or clearly useful preferences and context.

Risk: Memory text and search queries are processed through OpenAI-backed services.

Mitigation: Install only where that processing is acceptable for the user and organization, and ensure OPENAI_API_KEY access is controlled.

Risk: The scripts expose user-selectable memory access and bulk deletion controls.

Mitigation: Restrict who can invoke the scripts, remove or lock down the --user option, and add confirmation before bulk deletion.

## Reference(s):

- [Mem0 integration patterns](references/integration-patterns.md)
- [ClawHub skill page](https://clawhub.ai/sieyer/skills/mem0-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts can emit JSON when JSON_OUTPUT is set.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
