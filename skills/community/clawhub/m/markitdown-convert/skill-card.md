## Description:

Converts PDF, DOCX, XLSX, PPTX, and image documents to Markdown using MarkItDown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woai36d](https://clawhub.ai/user/woai36d)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to convert common office documents, PDFs, spreadsheets, slide decks, and images into Markdown for downstream review, knowledge-base ingestion, or batch workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill text attempts to make itself mandatory for all document-to-Markdown work.

Mitigation: Review or remove the global-use language before installing so agents can choose safer or more appropriate conversion paths when needed.

Risk: Conversion relies on broad mutable dependencies from markitdown[all].

Mitigation: Install in an isolated environment and prefer pinned dependency versions for repeatable, reviewable behavior.

Risk: Optional plugin execution can expand behavior beyond the base converter.

Mitigation: Avoid --plugins unless the installed plugins and input documents are trusted.

Risk: Document conversion may expose local document contents to installed conversion libraries or plugins.

Mitigation: Use the skill only for documents the user is comfortable converting locally and choose explicit output locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woai36d/skills/markitdown-convert)
- [ClawHub publisher profile](https://clawhub.ai/user/woai36d)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text written to stdout or to an output .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit command-line status or error messages; conversion depends on the installed markitdown[all] package and trusted local input files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
