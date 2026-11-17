## Description:

Minimal anti-prompt-injection guardrail for OpenClaw agents that scans untrusted content, high-risk actions, and outbound text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durugy](https://clawhub.ai/user/durugy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add lightweight checks around untrusted external content, risky local actions, and outbound messages in OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detection can give false assurance when packaged without the core rule files.

Mitigation: Include the expected rule files and make missing detection rules fail closed before using the skill as a security gate.

Risk: Direct .env sourcing can execute shell code if the skill directory or config file is modified.

Mitigation: Replace shell sourcing with strict key-value parsing and restrict write access to runtime configuration before agent execution.

## Reference(s):

- [Artifact README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/durugy/skills/prompt-shield-lite)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and single-line JSON from shell script checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script checks return allow, warn, block, or usage-error exit codes; outbound scans may include sanitized_text.]

## Skill Version(s):

0.1.3 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
