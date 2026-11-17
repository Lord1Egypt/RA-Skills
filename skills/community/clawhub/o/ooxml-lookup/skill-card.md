## Description:

Helps inspect OOXML schema rules for Word, Excel, and PowerPoint files, including allowed elements, attributes, values, and validation errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shbernal](https://clawhub.ai/user/shbernal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this offline lookup to inspect OOXML schema constraints and explain validation errors while editing or debugging DOCX, XLSX, and PPTX XML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advanced direct SQL queries may yield raw schema rows without the interpretation provided by lookup commands.

Mitigation: Prefer the lookup commands; use the read-only SQL option only for intended schema queries and review the results.

Risk: The default Transitional profile or ambiguous names can produce an answer that does not apply to the document being inspected.

Mitigation: Select the Strict profile when appropriate and check variants or qualify names before applying results.

## Reference(s):

- [Publisher-provided v0.0.6 release changelog](https://github.com/shbernal/ooxml-ai-tooling/releases/tag/v0.0.6)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Text guidance and shell commands; lookup results are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a bundled offline schema database; lookups default to the Transitional profile.]

## Skill Version(s):

0.0.6 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
