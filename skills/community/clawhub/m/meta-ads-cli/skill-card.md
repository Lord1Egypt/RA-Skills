## Description:

Control Meta/Facebook/Instagram ads through Meta's official `meta ads ...` CLI for read-only audits, reporting, safe planning, and approved one-step mutations of campaigns, ad sets, ads, creatives, catalog/product assets, datasets/pixels, and insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT

## Use Case:

Developers, marketers, and operations teams use this skill to inspect Meta ad accounts, produce campaign performance reports, prepare safe command plans, and execute approved single-step changes through the official Meta Ads CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform spend-affecting ad changes and asset mutations.

Mitigation: Use read-only Meta tokens for reporting, require fresh specific approval for each write, verify the exact account, object ID, and values, and run one mutation followed by verification before continuing.

Risk: A reusable approval value could allow unintended writes if left in the environment.

Mitigation: Avoid setting `META_ADS_AGENT_APPROVED`; pass approval text only for the single reviewed command or plan step that needs it.

Risk: Budget, activation, and destructive actions carry higher operational risk.

Mitigation: Require the relevant extra gate (`--allow-budget`, `--allow-active`, or `--allow-destructive`) only after reviewing the object state and intended before/after values.

Risk: The skill depends on the pinned Meta Ads CLI package and can expose ad-account metadata through command output or logs.

Mitigation: Install dependencies from locked and hash-verified sources, keep persistent logging disabled unless needed, and protect or delete logs that include account IDs, object IDs, or result metadata.

## Reference(s):

- [Meta Ads CLI overview](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/ads-cli-overview)
- [meta-ads 1.0.1 on PyPI](https://pypi.org/project/meta-ads/1.0.1/)
- [meta-ads 1.0.1 PyPI JSON metadata](https://pypi.org/pypi/meta-ads/1.0.1/json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, JSON, Configuration]

**Output Format:** [Markdown summaries and JSON command plans with guarded shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should separate recommendations from executed changes and include redacted commands, object IDs, before/after values, and verification results for writes.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
