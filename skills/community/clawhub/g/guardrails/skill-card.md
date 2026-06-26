## Description: <br>
Helps users configure security guardrails for an OpenClaw workspace through discovery, risk classification, an interactive interview, document generation, and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dgriffin831](https://clawhub.ai/user/dgriffin831) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw workspace users use this skill to create, review, and monitor workspace-specific guardrail policies. It scans local workspace context, classifies skill risks, asks contextual questions, and produces guardrail documentation and configuration for ongoing review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect workspace metadata, selected file contents, memory-log matches, and interview answers, and may send that context to OpenAI or Anthropic. <br>
Mitigation: Use it only in controlled workspaces, avoid entering secrets, require review before LLM-backed steps, and use limited API keys for sensitive environments. <br>
Risk: Generated GUARDRAILS.md and guardrails-config.json files may contain sensitive local policy details or workspace context. <br>
Mitigation: Review generated files before keeping or sharing them, remove sensitive values, and store them with workspace-appropriate access controls. <br>
Risk: Setup and review modes can write GUARDRAILS.md and guardrails-config.json into the workspace. <br>
Mitigation: Preserve the documented user confirmation step before writes and inspect generated changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dgriffin831/guardrails) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>
- [Guardrails template](artifact/templates/guardrails-template.md) <br>
- [Configuration schema](artifact/schemas/config.schema.json) <br>
- [Risk schema](artifact/schemas/risks.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown GUARDRAILS.md content, JSON guardrails-config.json, JSON monitoring reports, and conversational setup or review guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Setup and review modes can write GUARDRAILS.md and guardrails-config.json after user confirmation; monitor mode emits a JSON status report.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and CHANGELOG, released 2026-02-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
