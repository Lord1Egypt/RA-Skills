## Description:

Token-efficient context format using LLMCOM specification - reduces token usage by 70-80% through compact object notation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shalinda-j](https://clawhub.ai/user/shalinda-j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to compact structured JSON-like context into LLMCOM notation, expand it back to dictionaries, and estimate token savings for agent requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom LLMCOM parsing is not a security boundary and may mishandle attacker-controlled text containing delimiters.

Mitigation: Use trusted structured input, validate or escape delimiters before parsing, and avoid using parsed output for security decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shalinda-j/skills/llmcom-token-optimizer)
- [LLMCOM GitHub repository](https://github.com/shalinda-j/LLMCOM)
- [Publisher profile](https://clawhub.ai/user/shalinda-j)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and shell snippets; generated artifacts are compact LLMCOM text and JSON-compatible dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes approximate token counts and savings percentages.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
