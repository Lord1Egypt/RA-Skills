## Description:

Md Wechat converts Markdown files into WeChat Official Account-ready HTML with inline styling, themes, code highlighting, math rendering, diagrams, and reusable configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[italks](https://clawhub.ai/user/italks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and automation workflows use this skill to convert Markdown articles into styled HTML that can be copied into the WeChat Official Account editor. It also helps reuse article styling by extracting configuration from previously rendered HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use can automatically install npm or pip dependencies.

Mitigation: Review package metadata and lockfiles, install dependencies manually where possible, and run conversions with --no-auto-install.

Risk: Mermaid rendering uses a headless browser and remote JavaScript with the browser sandbox disabled.

Mitigation: Process Mermaid content only in an isolated environment and avoid rendering untrusted Markdown diagrams.

Risk: Untrusted Markdown or extracted HTML configuration can influence generated output.

Mitigation: Use trusted source documents and reviewed configuration files, then inspect generated HTML before publishing or pasting into WeChat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/italks/skills/md-wechat)
- [Configuration reference](references/config-reference.md)
- [Theme reference](references/theme-reference.md)
- [marked](https://marked.js.org/)
- [KaTeX](https://katex.org/)
- [highlight.js](https://highlightjs.org/)
- [Mermaid](https://mermaid.js.org/)
- [doocs/md](https://github.com/doocs/md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, configuration JSON, and generated HTML file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a styled HTML output file and, on first use, a default md-config.json file.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
