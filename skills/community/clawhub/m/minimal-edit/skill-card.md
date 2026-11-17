## Description:

SurgeonEdit helps agents make minimal, tone-preserving local edits to existing Chinese or English text while preserving structure, length, emphasis, and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianzhiceng297-boop](https://clawhub.ai/user/tianzhiceng297-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and teams use this skill to revise, correct, delete, soften, reword, or de-AI specific parts of existing Chinese or English documents without turning a local edit into a rewrite.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential document text can be exposed by surrounding systems if passed as command-line arguments.

Mitigation: Follow the skill guidance to pass sensitive text through files or stdin when using the optional audit script.

## Reference(s):

- [Minimal Edit Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Clean revised text, with optional Markdown or shell commands when the user asks for self-check guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled audit script is a local self-check aid; it reads only named files or stdin and does not use the network.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
