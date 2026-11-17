## Description:

Extract images from PDF files with three modes: original quality, 800x800 web-ready images, and compressed images under 50KB for social sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jnbno1163](https://clawhub.ai/user/jnbno1163)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to extract images from local PDF catalogs, marketing files, or other PDF documents and prepare them for print, e-commerce, websites, or social media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local PDF processing can act on unintended documents if the configured input folder is too broad.

Mitigation: Edit the configured PDF and output folders before running so only intended local documents are processed.

Risk: Image extraction depends on PyMuPDF and Pillow packages installed in the runtime environment.

Mitigation: Install the skill in a dedicated virtual environment and consider pinning PyMuPDF and Pillow to reviewed versions.

## Reference(s):

- [Configuration reference](artifact/references/config.md)
- [ClawHub skill page](https://clawhub.ai/jnbno1163/skills/pdf-image-extractor)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local PyMuPDF and Pillow scripts that write extracted image files to configured output folders.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
