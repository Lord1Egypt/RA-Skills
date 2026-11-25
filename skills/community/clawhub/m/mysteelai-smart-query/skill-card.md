## Description:

Enables natural-language queries for commodity prices, macroeconomic and supply-chain indicators, and financial-market data through Mysteel, with historical comparisons and CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longocc](https://clawhub.ai/user/longocc)

### License/Terms of Use:

MIT-0

## Use Case:

Commodity analysts, procurement teams, and market researchers use it to retrieve and compare current or historical commodity, macroeconomic, supply-chain, and financial-market data, then review structured results or CSV exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When an API key is supplied with --api-key, the skill writes it in plaintext to references/api_key.md for later use.

Mitigation: Prefer the mysteel_skill_auth_key environment variable, restrict access to the skill directory, and remove any saved key file when it is no longer needed.

Risk: CSV export cleanup removes CSV files older than 24 hours and removes files over the configured maximum (100 by default) from the output directory.

Mitigation: Use a dedicated --output-dir, adjust --max-files for the data you need to retain, and keep separate copies of important exports.

## Reference(s):

- [API Reference](artifact/references/api_reference.md)
- [Mysteel homepage](https://www.mysteel.com)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV files]

**Output Format:** [JSON query results, CSV data files, and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV exports support row limits, date filters, and an output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
