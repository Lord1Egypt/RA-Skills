## Description:

Generates professional presentations in interactive HTML and editable PowerPoint (.pptx) formats, with support for market analysis, product introductions, competitor analysis, data visualization, navigation, and a dark technology visual style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chao980](https://clawhub.ai/user/chao980)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, business users, and content creators use this skill to assemble presentation content and generate both browser-ready HTML slides and editable PPTX files for reports, product introductions, market analysis, competitor analysis, and SWOT presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PPTX generator can automatically install an unpinned Python package.

Mitigation: Run the skill in a constrained workspace or virtual environment and install dependencies explicitly from trusted pinned sources before use.

Risk: Generated HTML can execute untrusted slide content when supplied from JSON or web-sourced data.

Mitigation: Avoid untrusted slide data until the HTML generator escapes inserted content, and review generated HTML before opening or sharing it.

Risk: The preview workflow can start a local HTTP server.

Mitigation: Bind preview use to the local machine and do not expose the preview server beyond the local environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chao980/skills/ppt-generator-smb)
- [Publisher Profile](https://clawhub.ai/user/chao980)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus generated HTML and PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create browser-ready HTML slides, editable PowerPoint files, and local screenshot previews.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
