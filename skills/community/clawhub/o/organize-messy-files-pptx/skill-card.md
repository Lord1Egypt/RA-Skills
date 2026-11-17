## Description:

Presentation creation, editing, and analysis for creating new PowerPoint files, modifying presentation content, working with layouts, adding comments or speaker notes, and related .pptx tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and end users use this skill when an agent needs to create, inspect, edit, or validate PowerPoint presentations. It supports HTML-to-PPTX creation workflows, template-based slide replacement, raw OOXML editing, and thumbnail-based visual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run local conversion tools and recommend global or privileged dependency installation.

Mitigation: Use an isolated workspace or container, prefer local pinned dependencies, and avoid global or sudo installation unless explicitly approved.

Risk: The skill edits Office archives and replacement workflows can clear or change presentation content.

Mitigation: Keep backups of source presentations, validate edited files before use, and review output thumbnails for layout or content loss.

Risk: Untrusted Office or HTML inputs can expand the risk of local file-processing workflows.

Mitigation: Avoid untrusted inputs or process them in a sandboxed environment with limited filesystem access.

## Reference(s):

- [HTML to PowerPoint Guide](artifact/html2pptx.md)
- [Office Open XML Technical Reference for PowerPoint](artifact/ooxml.md)
- [ClawHub Skill Page](https://clawhub.ai/lnj22/skills/organize-messy-files-pptx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and file-oriented workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to produce or modify PPTX files, JSON inventories, HTML slide files, extracted OOXML directories, and thumbnail images.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
