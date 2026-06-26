## Description: <br>
Converts Markdown documents into WeChat Official Account-ready HTML with configurable themes, fonts, colors, code highlighting, math rendering, and diagram support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[italks](https://clawhub.ai/user/italks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and automation workflows use this skill to convert Markdown articles into styled HTML that can be copied into the WeChat Official Account editor. It is suited for repeatable article formatting, custom theme reuse, and batch-oriented publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The formatter may automatically install dependencies during normal conversion. <br>
Mitigation: Review package.json and package-lock.json, install dependencies manually, and run conversion with --no-auto-install. <br>
Risk: Browser-based rendering and Markdown input processing can increase exposure when handling untrusted files. <br>
Mitigation: Run the skill in an isolated project, container, or sandbox, especially for untrusted Markdown content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/italks/md-wechat) <br>
- [Configuration reference](references/config-reference.md) <br>
- [Theme reference](references/theme-reference.md) <br>
- [marked Markdown parser](https://marked.js.org/) <br>
- [KaTeX math rendering](https://katex.org/) <br>
- [Mermaid diagram rendering](https://mermaid.js.org/) <br>
- [doocs/md inspiration project](https://github.com/doocs/md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated HTML or JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML is intended for WeChat Official Account copy-paste workflows; configuration extraction can produce reusable JSON style settings.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
