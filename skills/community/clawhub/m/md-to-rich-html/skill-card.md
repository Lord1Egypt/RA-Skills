## Description:

Turn Markdown files or folders into a polished, human-readable, self-contained HTML page by having the agent understand the document, choose an appropriate information design, generate custom HTML/CSS/JS, and validate the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[441126098](https://clawhub.ai/user/441126098)

### License/Terms of Use:

MIT

## Use Case:

Developers and technical writers use this skill to transform one Markdown file or a folder of Markdown documents into a self-contained HTML page with clearer structure, hierarchy, and responsive reading affordances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may include content derived from sensitive Markdown inputs or embedded diagrams/scripts.

Mitigation: Review the generated HTML before sharing, especially when source Markdown contains private information or embedded executable content.

Risk: The skill reads the Markdown files or folders selected for conversion.

Mitigation: Run it only on intended input paths and avoid including unrelated confidential files in the conversion folder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/441126098/skills/md-to-rich-html)
- [Project homepage](https://github.com/441126098/md-to-rich-html)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Self-contained HTML with inline CSS and optional JavaScript, typically accompanied by concise Markdown status or validation notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-selected Markdown files or folders and writes portable HTML output unless external assets are requested.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
