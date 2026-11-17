## Description:

Summarize CodexBar local cost logs by model for Codex or Claude, including current or full breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Codex or Claude users can summarize local CodexBar cost logs by model, viewing either the current model or an all-model breakdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Usage summaries can reveal personal or organizational model usage and spending.

Mitigation: Keep source logs and generated summaries local, and review them before sharing.

## Reference(s):

- [CodexBar CLI quick reference](references/codexbar-cli.md)
- [CodexBar releases](https://github.com/steipete/CodexBar/releases)
- [CodexBar AUR package](https://aur.archlinux.org/packages/codexbar-cli)
- [Model Usage on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-model-usage)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text or JSON]

**Output Parameters:** [1D per-model summary; supports current or all models and an optional model selection.]

**Other Properties Related to Output:** [Reports costs by model; CodexBar does not split token counts by model.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
