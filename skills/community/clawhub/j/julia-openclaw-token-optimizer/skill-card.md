## Description:

Scans LLM pricing, benchmarks candidate models, and recommends or applies OpenClaw model-selection configuration changes to reduce token spend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronmda](https://clawhub.ai/user/aaronmda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to compare current model pricing and performance, then tune model-selection settings for lower token costs while preserving task quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose or apply OpenClaw model-selection configuration changes without enough approval, scope, or rollback detail.

Mitigation: Require a dry-run recommendation first, review the exact patch, confirm authorization to apply it, and keep a rollback copy of prior modelSelection settings.

Risk: Pricing recommendations can become inaccurate if provider prices are stale or placeholder values are used.

Mitigation: Refresh provider pricing from current official pricing pages before benchmarking or changing configuration.

## Reference(s):

- [providers.md](providers.md)
- [OpenAI API Pricing](https://openai.com/api/pricing)
- [xAI Pricing](https://x.ai/pricing)
- [ClawHub Skill Page](https://clawhub.ai/aaronmda/skills/julia-openclaw-token-optimizer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown recommendations with pricing, speed, quality, and configuration patch details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed OpenClaw modelSelection changes for user review or application.]

## Skill Version(s):

1.0.0 (source: clawhub.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
