## Description:

Google Ads CLI helps agents analyze Google Ads performance, inspect account structure, pull campaign, ad group, keyword, conversion, and billing data, and run custom GAQL queries through google-ads-open-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, analysts, and developers use this skill to explore Google Ads accounts, produce performance reports, audit conversions, and answer campaign questions with built-in commands or GAQL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query Google Ads data available to the configured OAuth and developer tokens.

Mitigation: Use credentials scoped to the accounts needed for the task and avoid exposing broader account access than required.

Risk: Google Ads credentials or queried account data may be exposed through shared logs, shell history, or copied command output.

Mitigation: Keep credentials out of shared logs, prefer credential files or environment variables managed by the user, and redact sensitive account details before sharing results.

Risk: The skill depends on the third-party google-ads-open-cli package.

Mitigation: Install only trusted, pinned, or reviewed package versions before using the skill in sensitive Google Ads environments.

## Reference(s):

- [google-ads-open-cli documentation](https://github.com/Bin-Huang/google-ads-open-cli)
- [Google Ads API overview](https://developers.google.com/google-ads/api/docs/start)
- [GAQL reference](https://developers.google.com/google-ads/api/docs/query/overview)
- [GAQL grammar](https://developers.google.com/google-ads/api/docs/query/grammar)
- [Resource field reference (v23)](https://developers.google.com/google-ads/api/fields/v23/overview)
- [GAQL query cookbook](https://developers.google.com/google-ads/api/docs/query/cookbook)
- [Segmentation rules](https://developers.google.com/google-ads/api/docs/reporting/segmentation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should convert Google Ads micros into currency units before presenting monetary values.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
