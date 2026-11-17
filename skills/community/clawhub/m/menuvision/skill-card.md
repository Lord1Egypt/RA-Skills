## Description:

Build beautiful HTML photo menus from restaurant URLs, PDFs, or photos using Gemini Vision and AI image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ademczuk](https://clawhub.ai/user/ademczuk)

### License/Terms of Use:


## Use Case:

External users, developers, and restaurant operators use MenuVision to turn restaurant menu URLs, PDFs, or photos into structured menu data, generated food images, and a responsive HTML photo menu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Menu content, page screenshots, and generated prompts are sent to Gemini during extraction and image generation.

Mitigation: Use the skill only with menu content that is appropriate to send to Gemini, and avoid confidential or internal material.

Risk: The optional GitHub Pages publishing flow uses a personal access token and may expose generated HTML and images to the destination repository.

Mitigation: Use a token scoped to one repository, confirm the target repository before publishing, and prefer a safer credential method than URL-embedded PAT authentication.

Risk: URL extraction is not scoped to public restaurant sites.

Mitigation: Run URL extraction in a constrained environment and do not provide untrusted, private, or internal URLs.

## Reference(s):

- [MenuVision ClawHub listing](https://clawhub.ai/ademczuk/skills/menuvision)
- [MenuVision homepage](https://github.com/ademczuk/MenuVision)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python code, shell commands, JSON menu data, generated images, and HTML output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce portable single-file HTML or deployable HTML with a companion images directory.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
