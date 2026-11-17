## Description:

This skill fetches AI model pricing data from multiple API platforms, calculates model ratios, completion ratios, and group ratios with a unified pricing formula, and outputs standardized JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengmengkaizmk](https://clawhub.ai/user/zhengmengkaizmk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect pricing data from configured AI API platforms, normalize it into model, completion, and group ratios, and review changes against a local snapshot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts configured pricing endpoints during fetch operations.

Mitigation: Review references/pricing_urls.json before running and only use endpoints you trust.

Risk: Full runs can overwrite data/latest_snapshot.json with newly fetched pricing data.

Mitigation: Use --no-snapshot when persistence is not desired or review snapshot changes before committing them.

Risk: The script prints multiple labeled JSON blocks rather than one parseable JSON document.

Mitigation: Post-process the labeled sections separately instead of treating stdout as a single JSON object.

## Reference(s):

- [Pricing Rules](artifact/model-pricing-calculator/references/pricing_rules.md)
- [Pricing URL Configuration](artifact/model-pricing-calculator/references/pricing_urls.json)
- [12AI Pricing](https://new.12ai.org/pricing)
- [PackyAPI Pricing](https://www.packyapi.com/pricing)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and labeled JSON blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full runs may update data/latest_snapshot.json unless --no-snapshot is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
