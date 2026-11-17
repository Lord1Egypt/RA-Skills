## Description:

Mysteel Price Search helps agents query Mysteel for commodity prices, futures and spot market data, macroeconomic indicators, supply-chain data, financial market data, and settlement-related information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyb92](https://clawhub.ai/user/wyb92)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to retrieve Mysteel market data through natural-language queries and optionally export price-series results as filtered CSV files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query text is sent to Mysteel's remote API.

Mitigation: Use the skill only for queries that are appropriate to share with Mysteel's API.

Risk: CSV mode may delete existing .csv files in a user-selected output directory.

Mitigation: Prefer the default skill output directory, avoid shared or important folders for --output-dir, and keep backups of valuable exports.

Risk: The skill requires a Mysteel API token stored in references/api_key.md.

Mitigation: Store the token carefully and do not commit or share references/api_key.md after adding a real key.

## Reference(s):

- [API Reference](references/api_reference.md)
- [Mysteel AI Search API endpoint](https://mcp.mysteel.com/mcp/info/ai-search/search)
- [ClawHub skill page](https://clawhub.ai/wyb92/skills/mysteel-pricesearch)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration, Guidance]

**Output Format:** [JSON API responses, CSV files, and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV output supports row limits, date filters, output directory selection, and maximum retained file count.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
