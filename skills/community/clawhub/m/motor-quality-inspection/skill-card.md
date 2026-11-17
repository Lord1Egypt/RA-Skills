## Description:

A Chinese-language motor quality inspection assistant that generates GJB-style inspection procedures and reports for incoming, process, finished-product, and outgoing quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongjie666888](https://clawhub.ai/user/yongjie666888)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers and manufacturing teams use this skill to draft motor inspection procedures, checklists, and report templates across IQC, PQC, FQC, and OQC workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report script writes directly to the path passed with --output, which can overwrite an existing local file.

Mitigation: Choose the output path deliberately and avoid pointing it at important existing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yongjie666888/skills/motor-quality-inspection)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and plain-text inspection report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled report script supports user-selected inspection type and optional local file output.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
