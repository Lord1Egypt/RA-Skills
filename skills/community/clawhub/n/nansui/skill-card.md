## Description:

Collects ride receipt emails from Gmail, stores them locally, extracts structured ride data through a loopback OpenClaw Gateway, loads ride records into SQLite, generates ride-behavior insights, and exports an anonymized DataHive-ready CSV for supported ride providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nandaniawug](https://clawhub.ai/user/nandaniawug)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to build a local ride receipt database, audit spending and route behavior, and produce a shareable anonymized ride report without exposing raw receipt emails or direct identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ride receipts can contain sensitive financial, location, route, and account information, and fetched email HTML is stored locally in data/ride-insights/emails.json.

Mitigation: Run the skill only in a private workspace or single-user environment and delete data/ride-insights/emails.json when raw receipts are no longer needed.

Risk: Extraction sends raw per-email JSON, including receipt HTML when present, to the active Gateway-backed model.

Mitigation: Use only the required loopback Gateway hosts and confirm user consent before extraction.

Risk: The anonymized CSV is a derived mobility dataset and may still reveal travel patterns when shared or opened in other tools.

Mitigation: Review the CSV before opening it in spreadsheet software or sharing it externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nandaniawug/skills/nansui)
- [ClawHub / OpenClaw homepage](https://clawhub.com)
- [DataHive AI](https://datahive.ai)
- [DataHive missions blog](https://datahive.ai/blog/)
- [Provider Gmail queries](references/provider_queries.json)
- [Ride SQLite schema](references/schema_rides.sql)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands plus local JSON, SQLite, and CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default extraction cap is 50 emails unless the user explicitly approves more; anonymized CSV excludes raw receipt content and direct identifiers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
