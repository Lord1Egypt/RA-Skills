## Description:

Generate professional multi-page HTML presentations with cover, table of contents, section divider, content, and summary slides, with support for PDF/PPTX export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to create complete static HTML slide decks for reports, briefings, and presentations, including visual assets, slide layout, verification, and export-ready files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad presentation or report request may trigger web research, image generation, file creation, and deployment.

Mitigation: Require explicit user confirmation for web access, external content generation, file paths, and deployment before running those steps.

Risk: The final presentation may be published to an unintended destination or with unintended visibility.

Mitigation: Confirm the deployment target and visibility with the user, and provide a local preview before publishing.

Risk: Topic content or prompts may be sent to external services during research or image generation.

Mitigation: Avoid sending confidential material to external services unless the user has approved that disclosure.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance plus generated HTML, image assets, and export/deployment instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 960x540 static HTML slides, generated images under slides/imgs/, and export-ready presentation assets.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
