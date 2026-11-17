## Description:

Sync provider model lists into OpenClaw config with dry-run preview, confirmation, and apply flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-joey](https://clawhub.ai/user/c-joey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to preview and synchronize upstream provider model lists into local OpenClaw configuration. It helps normalize model capability fields, preserve local overrides when requested, and apply reviewed configuration updates with backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored provider credentials can be sent to a caller-chosen endpoint when provider-config credentials are combined with an explicit endpoint.

Mitigation: Do not combine stored provider credentials with custom endpoints; avoid --use-provider-config with an explicit --endpoint until origin and HTTPS validation are added.

Risk: Apply mode can modify OpenClaw configuration, including pruning provider agent aliases.

Mitigation: Run dry-run first, review the displayed changes and alias deletions, and apply only in a private or administrator-controlled context.

Risk: The skill is published by a third-party user and has a suspicious security verdict.

Mitigation: Install only if the publisher is trusted and invocation can be controlled.

## Reference(s):

- [Provider Patterns](artifact/references/provider-patterns.md)
- [Field Normalization](artifact/references/field-normalization.md)
- [Safety Rules](artifact/references/safety-rules.md)
- [Gemini Notes](artifact/references/gemini.md)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown or JSON summaries with shell commands and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run, check-only, and apply modes; apply mode can write OpenClaw configuration and creates a backup before updating.]

## Skill Version(s):

2.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
