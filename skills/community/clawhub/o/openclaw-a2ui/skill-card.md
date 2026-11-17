## Description:

OpenClaw A2UI adds rich HTML card rendering to OpenClaw webchat replies and provides templates plus installation guidance for the skill-ui-bridge plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suuuy](https://clawhub.ai/user/suuuy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to produce structured webchat replies as rich card-style HTML and to install or troubleshoot the UI bridge needed to render those cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin edits the OpenClaw control UI and registers persistent plugin state.

Mitigation: Install only in trusted OpenClaw environments, review the plugin changes before use, and use the bundled uninstall flow if the UI bridge must be removed.

Risk: Raw HTML rendering and expanded sanitizer allowlists can expose browsers to unsafe content if the sanitizer, manifest access, or allowlist design is too broad.

Mitigation: Review sanitizer behavior, authorization and CORS handling, and cross-skill allowlist boundaries before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suuuy/skills/openclaw-a2ui)
- [A2UI component reference](https://a2ui.org/reference/components/)
- [HTML card template reference](references/html-card-templates.md)
- [A2UI HTML template library](references/html-templates.md)
- [ui-config.json reference](references/ui-config-schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown containing raw HTML card markup, inline code examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [HTML cards require an outer class="a2ui" marker and the skill-ui-bridge plugin to render in OpenClaw webchat.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md changelog, released 2026-03-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
