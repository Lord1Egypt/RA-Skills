## Description:

Converts Notion HTML exports into an interactive mind map HTML file with search, zoom, expand and collapse controls, and Notion page link actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infniu](https://clawhub.ai/user/infniu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users who export Notion workspaces as HTML use this skill to convert the exported index into a browsable, searchable mind map. The agent runs the bundled parser and HTML generator, then returns the generated mindmap file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted Notion export could inject JavaScript into the generated mindmap.html.

Mitigation: Review before installing, use only trusted exports, and open generated HTML in an isolated folder or browser context.

Risk: Generated files are written into the working directory and could overwrite existing mindmap_data.json or mindmap.html files.

Mitigation: Run the conversion in a separate folder and keep backups of important files before generation.

Risk: A custom Notion base URL changes the links embedded in the generated mind map.

Mitigation: Validate any custom Notion base URL before running the generator or sharing the output.

## Reference(s):

- [Notion Mind Map Reference](README.md)
- [ClawHub skill page](https://clawhub.ai/infniu/skills/notion-to-mindmap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated files: mindmap_data.json and self-contained mindmap.html]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BeautifulSoup4 and a trusted Notion HTML export as input.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
