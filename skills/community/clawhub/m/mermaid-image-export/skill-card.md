## Description: <br>
Mermaid diagram image export using mermaid-cli. When Claude needs to export Mermaid diagrams as high-quality images (PNG, SVG, PDF) for documentation, presentations, print materials, or web embedding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallnest](https://clawhub.ai/user/smallnest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation authors use this skill to convert Mermaid diagrams into PNG, SVG, or PDF assets for documentation, presentations, print materials, and web embedding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The batch helper can run arbitrary shell commands through an under-scoped command option. <br>
Mitigation: Install only in a controlled workspace, avoid passing untrusted values to --mermaid-cmd, and prefer direct mmdc usage. <br>
Risk: Browser/Puppeteer troubleshooting may involve no-sandbox or host security workarounds. <br>
Mitigation: Do not follow no-sandbox or SELinux-disabling steps on a sensitive host unless exports run in an isolated test or CI environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smallnest/mermaid-image-export) <br>
- [Mermaid CLI Image Export Skill](SKILL.md) <br>
- [Mermaid Image Export Skill for Claude](README.md) <br>
- [Mermaid-CLI Image Export Overview](references/overview.md) <br>
- [Installation Guide](references/installation.md) <br>
- [Usage Guide](references/usage.md) <br>
- [Format Specifications](references/formats.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [PNG, SVG, or PDF image files plus Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Mermaid .mmd input with options for format, theme, scale, background, dimensions, custom CSS, and config files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
