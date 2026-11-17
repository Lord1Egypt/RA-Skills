## Description:

Kobe is a prompt-based knowledge skill that activates on Kobe Bryant, Black Mamba, jersey-number, or Mamba Mentality references to provide detailed information about Kobe Bryant's career, achievements, legacy, and philosophy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask natural-language questions about Kobe Bryant's NBA career, statistics, iconic moments, Mamba Mentality, post-retirement work, and cultural legacy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms such as #8, #24, and general basketball references could trigger the skill when the user did not intend a Kobe Bryant-specific response.

Mitigation: Use narrower activation rules that require Kobe Bryant, Black Mamba, Mamba Mentality, Lakers context, or another explicit Kobe-related signal.

Risk: The skill is a read-only knowledge source with no code, persistence, data access, or hidden behavior, so no security-sensitive execution risk was identified in the server scan.

Mitigation: Review and scan the artifact before deployment, and keep the skill limited to answering Kobe Bryant-related prompts.

## Reference(s):

- [ClawHub Kobe skill page](https://clawhub.ai/wscats/skills/kobe)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses to natural-language prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No tool calls, file writes, shell commands, API calls, data access, persistence, or credential handling are produced by the skill.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
