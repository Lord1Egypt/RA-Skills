## Description:

Scans prompts for prompt-injection attempts through Glitchward's LLM Shield API before they reach an LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eyeskiller](https://clawhub.ai/user/eyeskiller)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check non-sensitive user prompts and external content for prompt-injection signals before passing them to an LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanned prompt content is sent to Glitchward's external API.

Mitigation: Avoid secrets, credentials, personal or regulated data, and proprietary conversations unless the organization approves the data flow and retention model.

Risk: Placing untrusted prompt text directly into shell commands can cause unintended execution.

Mitigation: Pass prompt text as data using jq or a Python HTTP client rather than interpolating it into shell syntax.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/eyeskiller/skills/glitchward-shield)
- [Glitchward LLM Shield](https://glitchward.com/shield)
- [Glitchward prompt-injection pattern database](https://glitchward.com/llmpi)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown guidance with shell and Python examples; API results are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validation results include blocked status, risk score, and detected matches when applicable.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
