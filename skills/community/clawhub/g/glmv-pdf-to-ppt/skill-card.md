## Description:

Convert a PDF, such as a research paper, report, or other document, into a polished multi-slide HTML presentation with a structured outline JSON and summary markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zai-org](https://clawhub.ai/user/zai-org)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and researchers use this skill when they need an agent to convert a local or URL-hosted PDF into a slide deck with extracted visuals, a slide outline, and a written summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download user-provided PDF URLs and process full document contents.

Mitigation: Prefer local PDFs, restrict network and workspace access, and avoid using untrusted URLs unless the execution environment is isolated.

Risk: Output file handling and slide HTML generation need review before processing untrusted documents.

Mitigation: Constrain generated filenames and output paths, escape user-controlled HTML content, and review generated slides before sharing.

Risk: The skill writes presentation files and cropped images into the workspace.

Mitigation: Run it in a restricted workspace with pinned dependencies and inspect the generated files before moving them into trusted projects.

## Reference(s):

- [GLM-V PDF-to-PPT homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-pdf-to-ppt)
- [ClawHub skill page](https://clawhub.ai/zai-org/skills/glmv-pdf-to-ppt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands plus generated JSON, HTML, PNG, and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a timestamped ppt/<pdf_stem>_<timestamp>/ directory containing outline.json, cropped images, slide HTML files, index.html, and summary.md.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
