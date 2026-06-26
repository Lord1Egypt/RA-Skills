## Description: <br>
Analyzes website URLs, HTML files, or screenshots to extract design tokens and generate Google design.md-compatible DESIGN.md documentation with optional HTML previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to turn an existing web page, local HTML file, or screenshot into a structured DESIGN.md design specification. The generated document captures colors, typography, spacing, shapes, component guidance, and preview HTML for review or export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inputs can include web pages, local files, or screenshots that may contain private or sensitive information. <br>
Mitigation: Analyze only content the user is authorized to share and review generated DESIGN.md and preview files before publishing or reusing them. <br>
Risk: Generated preview HTML may reference third-party font CDN domains such as fonts.loli.net and gstatic.loli.net. <br>
Mitigation: Review preview HTML and replace, self-host, or remove external font links when they are not appropriate for the deployment environment. <br>
Risk: Optional validation and export examples use npx, which can execute external packages. <br>
Mitigation: Run validation or export commands only in a trusted environment and confirm the package source before execution. <br>


## Reference(s): <br>
- [Google design.md specification](https://github.com/google-labs-code/design.md) <br>
- [DESIGN.md template](references/design-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown DESIGN.md with YAML front matter, optional HTML preview files, and inline validation/export commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include light and dark preview HTML; generated preview font links should be reviewed before publishing.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
