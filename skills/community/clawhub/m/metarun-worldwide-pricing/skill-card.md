## Description:

Helps app publishers reprice iOS apps, in-app purchases, and subscriptions across App Store territories using affordability indexes or direct conversion through MetaRun.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iderasyh](https://clawhub.ai/user/iderasyh)

### License/Terms of Use:

MIT-0

## Use Case:

App publishers and developers use this skill to calculate, review, and apply territory-specific App Store prices for apps, in-app purchases, and subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect territory prices could change live App Store pricing.

Mitigation: Ask the user for the base price and territory, review the preview and price extremes, and apply only after explicit confirmation.

Risk: MetaRun may access and change App Store pricing using account credentials.

Mitigation: Use MetaRun only if trusted; in controlled environments, prefer a pinned or preinstalled CLI.

## Reference(s):

- [MetaRun agents](https://metarun.dev/agents)
- [ClawHub skill listing](https://clawhub.ai/iderasyh/skills/metarun-worldwide-pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with pricing summaries and optional CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Previews require user review and confirmation before price changes are applied.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
