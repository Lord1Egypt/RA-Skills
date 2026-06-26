## Description: <br>
Local-only skill that fetches ride receipt emails from Gmail via gog, stores them in local JSON, sends raw receipt JSON/HTML to a loopback OpenClaw Gateway model for structured extraction, loads extracted rides into SQLite, generates ride-behavior insights, and exports an anonymized DataHive-ready CSV for Uber, Bolt, Lyft, Yandex, Free Now, Curb, or Via receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nandaniawug](https://clawhub.ai/user/nandaniawug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to build a local ride receipt database, audit ride spending and route patterns, generate concise ride-behavior insights, and export an anonymized report for sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles raw Gmail ride-receipt data, including potentially sensitive financial, location, and receipt HTML content. <br>
Mitigation: Grant access only after review, minimize stored fields where practical, and delete exported raw JSON files after use. <br>
Risk: Raw per-email JSON/HTML is sent to the configured Gateway-backed model for extraction. <br>
Mitigation: Confirm before extraction and use only a loopback Gateway host such as localhost, 127.0.0.1, or ::1. <br>
Risk: Generated ride databases and anonymized CSVs can still reveal sensitive travel patterns. <br>
Mitigation: Treat derived files as sensitive, review anonymized exports before sharing, and keep only the fields needed for the intended report. <br>


## Reference(s): <br>
- [Provider Gmail queries](artifact/references/provider_queries.json) <br>
- [Ride SQLite schema](artifact/references/schema_rides.sql) <br>
- [ClawHub skill page](https://clawhub.ai/nandaniawug/nansui) <br>
- [OpenClaw homepage](https://clawhub.com) <br>
- [DataHive AI](https://datahive.ai) <br>
- [DataHive missions blog](https://datahive.ai/blog/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files, JSON, CSV, SQLite] <br>
**Output Format:** [Markdown guidance with inline shell commands plus local JSON, SQLite, and CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local emails.json, rides.json, rides.sqlite, and anonymized_rides.csv artifacts; default Gateway extraction is capped at 50 emails unless the user approves more.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
