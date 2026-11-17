## Description:

Converts external documents (PDF, DOCX, PPTX, XLSX, HTML) into editable markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and documentation maintainers use this skill to import PDFs, office documents, spreadsheets, slide decks, and HTML into editable markdown for rewriting, cleanup, or project integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad document-related wording.

Mitigation: Use it only when external-file conversion to markdown is intended, and review whether the activation matches the user's request.

Risk: The skill can write a converted markdown draft to a target path.

Mitigation: Review or confirm the output path before allowing the draft file to be written.

Risk: Imported external documents can include embedded instructions or conversion artifacts.

Mitigation: Apply the documented sanitization and cleanup steps, including stripping instruction tags, bounding external content, and marking unclear sections for review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-doc-importer)
- [ClawHub publisher profile](https://clawhub.ai/user/athola)
- [clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe)

## Skill Output:

**Output Type(s):** [markdown, files, guidance]

**Output Format:** [Markdown document drafts with conversion notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a draft markdown file to a user-confirmed target path and report conversion limitations.]

## Skill Version(s):

1.9.19 (source: server release metadata; artifact frontmatter lists 1.9.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
