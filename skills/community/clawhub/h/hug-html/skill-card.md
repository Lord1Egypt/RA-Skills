## Description:

Generates self-contained HTML templates and editable grid-based cards using atomic components, cell merging, style presets, content filling, and post-generation audit guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use hug-html to generate, assemble, edit, and fill self-contained HTML cards, dashboards, and grid-based templates from built-in or custom specifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can behave as active content when templates or specs include JavaScript.

Mitigation: Review generated HTML and any custom spec scripts before sharing or deploying; preview in a controlled browser context.

Risk: QR-code content, image URLs, or remote image references can expose secrets, private URLs, or personal data.

Mitigation: Use non-sensitive QR and image content, and review links before embedding them in generated HTML.

Risk: The skill writes output files and supports user template save-as names.

Mitigation: Use explicit safe output paths, avoid untrusted save-as names, and review destination paths before execution.

Risk: Prompts and documentation are primarily Chinese, and some commands may require local correction.

Mitigation: Validate commands in the target environment and translate or review operational prompts before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/hug-html)
- [Guide](artifact/references/guide.md)
- [Module library](artifact/references/module-library.md)
- [Examples](artifact/references/examples.md)
- [Style presets](artifact/references/style-presets.md)
- [Permissions](artifact/references/permissions.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated self-contained HTML or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML may include inline CSS, inline JavaScript, QR/image content, and local file outputs.]

## Skill Version(s):

3.3.1 (source: SKILL.md frontmatter, _meta.json, evidence release, changelog released 2026-07-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
