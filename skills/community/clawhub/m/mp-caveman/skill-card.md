## Description:

Mp Caveman switches the assistant into an ultra-compressed communication mode that removes filler, articles, and pleasantries while preserving technical accuracy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other ClawHub users use this skill when they want terse, token-conscious responses for routine technical or operational work. It keeps technical terms, code blocks, and exact error text intact while allowing fuller wording for warnings or complex instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent terse responses can omit context that a user may need for safety-critical, destructive, or complex tasks.

Mitigation: Use "stop caveman" or "normal mode" before tasks that need fuller explanations; the skill also allows fuller wording for warnings and complex instructions.

Risk: Users may forget the terse mode is still active after activation.

Mitigation: Disable the mode with "stop caveman" or "normal mode" when detailed rationale or step-by-step explanation is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/mp-caveman)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise natural-language responses, often Markdown for technical answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Code blocks and exact error text remain unchanged; fuller wording may be used for security warnings, irreversible action confirmations, and complex instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
