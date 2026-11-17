## Description:

Diagnoses and helps fix mimo-v2.5-pro and related Mimo model API failures involving 400 Param Incorrect responses, rejected request schemas or tool payloads, and schema-format provider runtime failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgugeng](https://clawhub.ai/user/lgugeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to troubleshoot OpenClaw provider configuration, Mimo API connectivity, tool calling support, model naming, and related log evidence when Mimo requests fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic commands read local OpenClaw provider credentials and send test requests to the configured API endpoint.

Mitigation: Confirm that ~/.openclaw/openclaw.json points to a trusted provider endpoint and use only non-sensitive test prompts.

Risk: Suggested fixes may modify OpenClaw model configuration, including enabling toolCall for Mimo models.

Mitigation: Back up openclaw.json and review the proposed configuration change before applying it.

## Reference(s):

- [mimo API error reference](artifact/references/errors.md)
- [ClawHub release page](https://clawhub.ai/lgugeng/skills/mimo-api-fix)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic API calls and local OpenClaw configuration edits for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
