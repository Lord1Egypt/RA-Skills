## Description:

Converts Markdown files into Word .docx documents with Chinese font optimization, table borders, and Pandoc-based formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sukimgit](https://clawhub.ai/user/sukimgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and document authors use this skill to convert Markdown drafts, reports, meeting notes, and project documentation into Word documents formatted for Chinese-language workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter writes a temporary Markdown file next to the source file during conversion, which can expose content or collide with other activity in shared writable directories.

Mitigation: Run conversions in trusted private directories and avoid source files stored in shared or untrusted writable locations.

Risk: Generated Word documents include an automatically appended date line that may be inappropriate for some deliverables.

Mitigation: Review generated documents before distribution and remove or adjust the date line when it does not match the intended document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sukimgit/skills/md2docx)
- [Publisher profile](https://clawhub.ai/user/sukimgit)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [Pandoc installation documentation](https://pandoc.org/installing.html)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance and Python or shell invocations that produce Word .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Pandoc and python-docx; converted documents are post-processed for Chinese fonts and table borders and currently include an appended date line.]

## Skill Version(s):

1.0.6 (source: server release, README.md, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
