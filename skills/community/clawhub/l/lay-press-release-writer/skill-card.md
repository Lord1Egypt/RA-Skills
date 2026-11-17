## Description:

Transform academic papers into university press releases for general audiences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Communications teams, researchers, and agents use this skill to turn academic paper text or abstracts into university-style press releases for general audiences, alumni, or media. It helps draft headlines, leads, body copy, researcher quotes, institutional boilerplate, and media contact information while keeping assumptions and limits explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite any writable local file when an unrestricted --output path is supplied.

Mitigation: Run it in a sandboxed workspace and use only reviewed relative output paths until output-path restrictions prevent accidental overwrites.

Risk: A stress-case audit recorded weak boundary handling for staying within the declared press-release-writing scope.

Mitigation: Require enough source paper text to support the release and review all scientific claims against the source before publication.

## Reference(s):

- [Audit Reference](artifact/references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/lay-press-release-writer)

## Skill Output:

**Output Type(s):** [text, json, markdown, shell commands, guidance]

**Output Format:** [Structured JSON press release output, with optional Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires paper_text; optional metadata includes paper title, authors, institution, publication venue, target audience, tone, and output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
