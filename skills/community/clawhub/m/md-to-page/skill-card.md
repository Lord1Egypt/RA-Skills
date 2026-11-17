## Description:

Convert Markdown files into styled, scrollable wide-screen HTML pages with dark/light themes, animations, and rich directive components for web articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lz-web3](https://clawhub.ai/user/lz-web3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to convert Markdown notes, outlines, and long-form articles into shareable styled HTML pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may preserve unsafe content from untrusted Markdown.

Mitigation: Use trusted Markdown sources and review generated HTML before publishing or sharing.

Risk: --embed-images can package local files referenced by crafted image paths into the generated output.

Mitigation: Avoid --embed-images for untrusted documents and inspect image paths before conversion.

Risk: Generated HTML is active web content rather than a sanitized document.

Mitigation: Share or host the output with the same review controls used for other web pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lz-web3/skills/md-to-page)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [HTML file with embedded CSS and JavaScript, plus terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional local image embedding, title and footer overrides, theme toggle, scroll animations, Markdown tables, file trees, and directive components.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
