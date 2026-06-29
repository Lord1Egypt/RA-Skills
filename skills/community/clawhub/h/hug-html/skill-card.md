## Description: <br>
Generates self-contained HTML templates and editable grid-based HTML layouts using atomic components, cell merging, style presets, built-in templates, and post-generation audit checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content builders use this skill to create local, self-contained HTML cards, dashboards, information panels, QR-code panels, and visual-editor variants from grid specs, built-in templates, or reusable component modules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML can include scripts that execute in the browser. <br>
Mitigation: Review generated HTML and any supplied templates or specs before opening, sharing, or deploying the file. <br>
Risk: QR-code content may be sent to a third-party QR image service. <br>
Mitigation: Do not place secrets, credentials, private URLs, or internal identifiers in QR-code content. <br>
Risk: Generated layouts may contain misleading or incorrect content if template inputs are wrong. <br>
Mitigation: Validate visible text, links, QR targets, image sources, and interaction behavior before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/hug-html) <br>
- [Usage guide](artifact/references/guide.md) <br>
- [Module library](artifact/references/module-library.md) <br>
- [Architecture](artifact/references/architecture.md) <br>
- [Permissions](artifact/references/permissions.md) <br>
- [Changelog](artifact/references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON grid specifications, and generated self-contained HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for local files under the skill data/output directory; generated HTML should be reviewed before opening or sharing.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter, _meta.json, server release evidence, changelog released 2026-06-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
