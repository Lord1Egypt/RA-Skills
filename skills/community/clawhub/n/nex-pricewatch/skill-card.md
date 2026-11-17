## Description:

Monitor competitor and supplier website prices using CSS, XPath, or regex selectors; track changes with alerts, view history and trends, and export data locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners, agencies, resellers, and developers use this skill to configure local competitor and supplier price monitoring, review pricing trends, receive threshold-based alerts, and export price history for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured targets can fetch unrestricted URLs, including local or internal network addresses.

Mitigation: Only add trusted public pricing URLs and avoid localhost, private-network, cloud metadata, and file-like targets.

Risk: Fetched pricing content, raw extracted text, exports, and HTML snapshots may be stored on disk.

Mitigation: Review and protect ~/.nex-pricewatch, delete snapshots or exports that contain sensitive content, and install only where local storage is acceptable.

Risk: Optional Telegram alerts may send price alert content to Telegram when enabled.

Mitigation: Enable Telegram only when alert content is appropriate for that external service and keep bot tokens and chat IDs in protected environment variables.

## Reference(s):

- [Nex Pricewatch ClawHub page](https://clawhub.ai/nexaiguy/skills/nex-pricewatch)
- [Nex AI homepage](https://nex-ai.be)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local SQLite data, HTML snapshots, JSON exports, CSV exports, and optional Telegram alert messages when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
