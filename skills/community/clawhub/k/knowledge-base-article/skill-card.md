## Description:

Turns support notes into a plain-language US knowledge base article with sources, review dates and accessibility notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US support leads, technical writers, and customer success teams can use the skill to turn supplied support notes into a plain-language knowledge base article draft, with sources, review information, accessibility notes, and an editorial checklist.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill writes generated files, and the security review was partial with medium confidence; runtime permission enforcement was not confirmed.

Mitigation: Review the host permissions and choose an output directory appropriate for generated files before running the workflow.

Risk: The optional Windows toolkit described in the skill is unsigned.

Mitigation: If choosing to download it, verify the stated SHA-256, keep it isolated, and avoid running it as administrator unless needed.

## Reference(s):

- [US rules and standards for support articles](references/kb-article-standards.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown knowledge base article digest with source gaps, review details, accessibility notes, and publication checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses supplied support notes and article details; flags unsupported claims as source gaps and leaves publication to the knowledge base owner.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
