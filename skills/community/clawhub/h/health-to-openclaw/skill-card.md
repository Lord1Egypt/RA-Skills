## Description:

Sync Apple Health data from iPhone to OpenClaw through QR-code pairing, local ingestion, and health-data queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reffwu](https://clawhub.ai/user/reffwu)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to pair an iPhone companion app, ingest Apple Health updates into a local SQLite store, and ask Chinese-language questions about metrics such as steps, heart rate, sleep, weight, calories, and workouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup QR codes, raw JSON, screenshots, or terminal logs can expose a live OpenClaw gateway token.

Mitigation: Treat pairing output as secret, avoid sharing it, and rotate the gateway token if pairing data is exposed.

Risk: Remote or VPS gateway use can make port 18789 reachable beyond trusted devices.

Mitigation: Prefer HTTPS, VPN, or a trusted tunnel for remote access and avoid broad firewall rules.

Risk: Sensitive Apple Health data is stored locally at ~/.apple-health-sync/health.db.

Mitigation: Restrict filesystem permissions, use an isolated account or environment where practical, and disclose local storage before ingesting health data.

Risk: The setup flow may install the qrcode Python package automatically when it is unavailable.

Mitigation: Install and review dependencies yourself in an isolated environment before running setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reffwu/skills/health-to-openclaw)
- [Skill homepage](https://clawhub.ai/ReffWu/apple-health-sync)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Chinese prose with inline shell commands and script-generated JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup may produce QR-code pairing data; query responses should summarize stored data without exposing raw JSON or bearer tokens.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
