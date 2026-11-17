## Description:

傳送定位點或 Google Maps 網址，查詢附近台灣停車場即時空位，附 Apple Maps / Google Maps 一鍵導航連結。支援 Telegram、LINE、iMessage。

This skill is ready for commercial/non-commercial use.

## Publisher:

[harperbot](https://clawhub.ai/user/harperbot)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and drivers in Taiwan use this skill to find nearby off-street parking, check real-time availability when supported by TDX data, and get Apple Maps or Google Maps navigation links.

### Deployment Geography for Use:

Taiwan

## Known Risks and Mitigations:

Risk: The skill includes an unverified self-updater that can fetch and replace local skill files from a remote repository.

Mitigation: Review update.sh and the exact remote code before running updates; disable automatic updates or pin reviewed versions for shared or commercial deployments.

Risk: The skill accepts map URLs from messages and may follow short-link redirects while resolving coordinates.

Mitigation: Restrict accepted URLs to known Google Maps hosts and prefer direct coordinates from trusted messaging channels.

Risk: The skill uses local TDX credentials and token caching.

Mitigation: Store credentials in environment variables with limited access, harden token cache permissions, or disable token caching on shared systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harperbot/skills/openclaw-parking-query)
- [ClawHub Publisher Profile](https://clawhub.ai/user/harperbot)
- [TDX Transport Data Platform](https://tdx.transportdata.tw)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text or Markdown parking listings with map URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TDX API credentials; returns up to five nearby parking results sorted by distance.]

## Skill Version(s):

1.0.0 (source: server release metadata and parking_query.py version comment)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
