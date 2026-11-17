## Description:

Ad intelligence and app analytics assistant for searching ad creatives, analyzing apps, viewing rankings, tracking download and revenue estimates, and getting market insights via AdMapix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockyzhuo](https://clawhub.ai/user/rockyzhuo)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, app publishers, and analysts use this skill to query AdMapix for ad creative discovery, competitive app intelligence, rankings, download and revenue estimates, and market reports from natural-language prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AdMapix may receive user queries and hosted report contents.

Mitigation: Install only when this data sharing is acceptable for the intended use case.

Risk: Credential handling may store or forward API keys.

Mitigation: Configure credentials manually, avoid pasting API keys into chat, use narrowly scoped and rotatable keys, and rotate any key previously shared with the skill.

Risk: Unsafe shell-command construction was reported by the security evidence.

Mitigation: Review generated shell commands before execution and defer installation until the command construction issue is fixed if the environment is sensitive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rockyzhuo/skills/my-admapix)
- [AdMapix Website](https://www.admapix.com)
- [Creative Search API Reference](artifact/references/api-creative.md)
- [Product and Company API Reference](artifact/references/api-product.md)
- [Ranking API Reference](artifact/references/api-ranking.md)
- [Download and Revenue API Reference](artifact/references/api-download-revenue.md)
- [App Distribution API Reference](artifact/references/api-distribution.md)
- [Market Analysis API Reference](artifact/references/api-market.md)
- [Parameter Mapping Reference](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with API-derived summaries, tables, setup snippets, H5 result links, or hosted HTML report links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include localized Chinese or English output; download and revenue values are third-party estimates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
