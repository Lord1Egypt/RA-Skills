## Description: <br>
HTML to Image helps an agent capture public webpage screenshots or convert raw HTML and optional CSS into hosted image output through the OOMOL HTML to Image connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need to generate image URLs from public webpages or supplied HTML/CSS without calling the HTML to Image API directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup path includes an installer command that runs local shell code. <br>
Mitigation: Review the OOMOL CLI installer or use the official install guide before installing the CLI. <br>
Risk: HTML, CSS, and URLs sent to the connector may contain sensitive information and outputs are hosted image URLs. <br>
Mitigation: Use only the intended HTML to Image account or API key, and avoid sending private secrets in HTML, CSS, or URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-html-to-image) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [HTML to Image homepage](https://html2img.com) <br>
- [OOMOL CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Skill icon](https://static.oomol.com/logo/third-party/html_to_image.svg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses return JSON containing data and meta.executionId; image outputs are hosted URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
