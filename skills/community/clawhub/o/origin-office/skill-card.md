## Description:

origin-office helps agents convert native DOCX and PPTX documents into Benxiang packages with structured objects, anchors, and SHA-256 verification for document integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill when DOCX or PPTX files need to become AI-anchorable, verifiable structure for document version tracking or clause-level citation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run unpinned code from a mutable external GitHub repository.

Mitigation: Pin the repository to a reviewed commit before use.

Risk: Document conversion commands may process sensitive local DOCX or PPTX files through unreviewed external code.

Mitigation: Run the npm workflow in a disposable, least-privileged sandbox without sensitive files or credentials mounted.

## Reference(s):

- [origin-office ClawHub page](https://clawhub.ai/dongsheng123132/skills/origin-office)
- [2origin repository](https://github.com/dongsheng123132/2origin.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and file path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of an external Node.js repository; resulting workflows may produce Benxiang packages, JSON, or Markdown.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
