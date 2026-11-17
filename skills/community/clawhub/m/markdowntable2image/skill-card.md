## Description:

Convert markdown tables and JSON data to PNG images for chat platforms where markdown tables render poorly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[umrzcz-831](https://clawhub.ai/user/umrzcz-831)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn markdown tables or structured JSON rows into shareable table images for chat platforms, reports, leaderboards, comparisons, and financial summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser rendering of untrusted tables or style options may allow network requests from Chromium.

Mitigation: Review untrusted table and style inputs, avoid exposing custom theme or style fields directly to untrusted users, and run Chromium where it cannot reach sensitive internal network services.

Risk: Installation runs Playwright setup and downloads Chromium.

Mitigation: Use a version-pinned install and review the package and install behavior before deployment.

## Reference(s):

- [Table2Image API Reference](references/api.md)
- [Table2Image Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/umrzcz-831/skills/markdowntable2image)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [PNG image files or image buffers, with JavaScript API examples and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports built-in and custom themes, column formatting, conditional cell styling, and markdown table detection.]

## Skill Version(s):

1.1.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
