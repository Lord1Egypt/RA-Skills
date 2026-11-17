## Description:

Paradiz helps agents answer VK lodging inquiries by calculating prices from a price sheet, preparing short customer replies, and supporting booking or hold records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keeper1978](https://clawhub.ai/user/keeper1978)

### License/Terms of Use:


## Use Case:

External-facing booking and hospitality staff use this skill to price Paradiz lodging requests from dates, guest counts, and room choices, then draft VK replies and manage booking records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes real-looking guest records and lead data.

Mitigation: Remove packaged guest records before use and apply retention and deletion rules for customer data.

Risk: Booking workflows can send guest details to Telegram and depend on Telegram credentials.

Mitigation: Use dedicated Telegram credentials, disclose and minimize customer data sent to Telegram, and confirm the configured recipient before enabling notifications.

Risk: The skill can act as a booking and CRM helper that writes booking files and interacts with SQLite maintenance scripts.

Mitigation: Review database-maintenance scripts and backup behavior before running write operations in a production booking environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keeper1978/skills/paradiz)
- [Publisher profile](https://clawhub.ai/user/keeper1978)
- [Price template](artifact/references/price_template.csv)
- [Price data](artifact/references/prices.csv)
- [Human-readable price data](artifact/references/prices_human_utf8.csv)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or file outputs from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce VK response text, booking journal entries, JSONL hold or booking records, Word booking documents, SQLite updates, and Telegram notifications when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
