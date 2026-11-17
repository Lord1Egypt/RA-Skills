## Description:

Bundles multiple Markdown files into a self-contained offline HTML document browser with directory navigation, full-text search, generated table of contents, and cross-document links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyan521](https://clawhub.ai/user/shiyan521)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, project teams, and external users use this skill to package a directory of Markdown documents into one portable HTML browser for offline reading, search, navigation, and sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can preserve unsafe Markdown links that may execute script when opened or clicked.

Mitigation: Use the skill only with trusted Markdown directories and do not share or open generated HTML from untrusted Markdown until link and image URL sanitization is fixed.

Risk: The generated HTML packages the full selected Markdown document set into one shareable file, which can expose secrets or private notes.

Mitigation: Review the source Markdown for secrets or private content before bundling and treat the generated HTML as containing the complete source document set.

## Reference(s):

- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [ClawHub skill page](https://clawhub.ai/shiyan521/skills/markdown-bundle-browser)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash commands; generated self-contained HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML embeds the selected Markdown document set and should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
