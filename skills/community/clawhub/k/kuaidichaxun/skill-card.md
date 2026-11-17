## Description:

Compares estimated domestic courier prices in China across more than 30 shipping channels using bundled route, weight, and volumetric-weight price data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angerfl](https://clawhub.ai/user/angerfl)

### License/Terms of Use:

MIT-0

## Use Case:

External users, e-commerce sellers, and shipping support agents use this skill to estimate and compare domestic China courier costs from origin, destination, weight, and package dimensions.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Courier prices and claimed discounts are estimates from bundled data and may differ from final platform prices.

Mitigation: Tell users to verify the final price on the actual shipping platform before purchasing.

Risk: The skill is China-focused and may not support international routes or unsupported address formats.

Mitigation: Keep use to domestic China courier price checks and ask for supported origin, destination, weight, or dimensions when inputs are incomplete.

Risk: Bundled price data can become stale and affect channel ranking.

Mitigation: Treat rankings as point-in-time estimates and refresh the bundled data before relying on results operationally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/angerfl/skills/kuaidichaxun)
- [Artifact README](artifact/README.md)
- [Example queries](artifact/examples/example_queries.md)
- [Address mapping data](artifact/references/address_mapping.json)
- [Courier channel price data](artifact/references/all_channels_prices.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with courier price tables, fee statistics, and source notes from local script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled data for estimates; no network access or credential use is indicated by the security evidence.]

## Skill Version(s):

1.0.8 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
