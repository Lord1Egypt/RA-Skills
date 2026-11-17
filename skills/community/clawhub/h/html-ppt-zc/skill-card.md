## Description:

Generates PPTX slide decks, with an optional HTML presentation export, from a title and body text using python-pptx.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn structured title and paragraph text into PPTX slide decks for reports, briefings, or presentations. It can also produce browser-viewable HTML presentations when that output path is appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML presentations may be unsafe when built from untrusted text.

Mitigation: Prefer PPTX output for ordinary use and avoid opening or sharing generated HTML until input escaping is reviewed.

Risk: HTML output may rely on remote font or CDN resources.

Mitigation: Remove remote dependencies or explicitly accept them before using HTML output in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/skills/html-ppt-zc)
- [Publisher profile](https://clawhub.ai/user/openclawzhangchong)
- [jsDelivr SRI guidance](https://www.jsdelivr.com/using-sri-with-dynamic-files)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated PPTX or HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python; python-pptx is required for PPTX output and jinja2 is optional for HTML export.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
