## Description:

Generates draft non-disclosure agreement templates, including mutual and unilateral NDA documents, from command-line inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use this skill to generate draft NDA templates for review before legal execution. It supports quick local drafting workflows for mutual and unilateral confidentiality agreements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated NDA drafts could be mistaken for legal advice or used without jurisdiction-specific review.

Mitigation: Treat generated agreements as draft reference material and consult a qualified attorney before execution.

Risk: The bundled utility can store user-entered party names, deal details, or confidential business information in plaintext local files.

Mitigation: Avoid entering sensitive information until the storage behavior is reviewed, and inspect or remove local nda-generator data files after use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown-like NDA draft output to stdout, with command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated NDA drafts are local text outputs; the bundled utility can retain arbitrary user input in plaintext local files.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
