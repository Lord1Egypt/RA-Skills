## Description: <br>
Hug HTML helps agents generate and edit self-contained grid-based HTML cards and dashboards using composable components, built-in templates, style presets, optional visual editing, and post-generation audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create single-page HTML cards, information panels, app promotion layouts, calendar dashboards, and editable grid templates from structured specifications or generated HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR-code generation can send QR contents to an external service despite offline or self-contained claims. <br>
Mitigation: Avoid placing secrets, internal URLs, tokens, or private contact data in QR-code content; review QR usage before deployment and use trusted offline alternatives when required. <br>
Risk: Custom specs or scripts can influence generated HTML and file outputs. <br>
Mitigation: Use custom specs and scripts only from trusted sources, then audit generated HTML before sharing or deploying it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ldxs001/skills/hug-html) <br>
- [Guide](artifact/references/guide.md) <br>
- [Architecture](artifact/references/architecture.md) <br>
- [Module Library](artifact/references/module-library.md) <br>
- [Style Presets](artifact/references/style-presets.md) <br>
- [Permissions](artifact/references/permissions.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and generated self-contained HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML may include editable data fields, grid specifications, style presets, and optional visual editor output.] <br>

## Skill Version(s): <br>
3.3.0 (source: ClawHub release evidence; artifact frontmatter reports 3.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
