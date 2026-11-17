## Description:

Helps OpenClaw users reduce token usage and API costs by recommending smaller context bundles, routing tasks to cheaper model tiers, optimizing heartbeat intervals, and tracking token budgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloud-dark](https://clawhub.ai/user/cloud-dark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators using OpenClaw use this skill to control agent token spend, model selection, heartbeat behavior, and local budget visibility in routine and high-volume workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because its documentation and wrapper include actions that may affect local workspace files.

Mitigation: Review the RTK companion instructions and workspace write behavior before installation, and back up any existing HEARTBEAT.md before using heartbeat-related commands.

Risk: The RTK companion guidance includes a curl-to-shell installer path for an external tool.

Mitigation: Avoid that installer unless you independently trust and verify it; prefer a reviewed package-manager or cargo install path when appropriate.

Risk: Optional multi-provider configuration can require third-party API keys and networked model providers when manually applied.

Mitigation: Apply those configuration examples only after reviewing the provider, credential, and network implications for the target environment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cloud-dark/skills/oot)
- [Publisher profile](https://clawhub.ai/user/cloud-dark)
- [Declared homepage](https://github.com/Cloud-Dark/oot)
- [Alternative AI Providers & Models](references/PROVIDERS.md)
- [RTK Integration Guide](references/RTK.md)
- [Cronjob Model Selection Guide](assets/cronjob-model-guide.md)
- [Token optimization config patches](assets/config-patches.json)
- [Security Documentation](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON recommendations, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some usage paths generate local files or write local OpenClaw workspace state; optional provider configuration may require external credentials when manually applied.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog report 1.4.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
