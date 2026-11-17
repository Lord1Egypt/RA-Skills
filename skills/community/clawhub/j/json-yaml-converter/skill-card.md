## Description:

Converts JSON input into YAML output for agent workflows, with optional configuration for processing mode, retries, and skipped steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation builders, and workflow operators use this skill to convert JSON payloads into YAML for configuration, integration, and data exchange tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broader powers than expected for JSON-to-YAML conversion, including command execution, file writing, API key usage, and external integrations.

Mitigation: Install only in a restricted agent environment and grant read, write, shell, and credential access only when those capabilities are explicitly needed for the workflow.

Risk: Unnecessary API credentials or shell access can expand the impact of malformed input or unintended agent actions.

Mitigation: Prefer a local converter path for routine transformations, avoid providing API keys for simple conversions, and review generated commands or file writes before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/json-yaml-converter)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON/YAML examples and optional shell configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce YAML conversion results, execution summaries, troubleshooting guidance, and configuration instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
