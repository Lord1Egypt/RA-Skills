## Description: <br>
OpenClaw adaptation of @mvanhorn's last30days skill. Research any topic from the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, and web. Includes watchlists, briefing generation, and historical query mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keylimesoda](https://clawhub.ai/user/keylimesoda) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to research recent community signals, maintain watchlists, generate briefings, and query stored history across social, web, and market sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use local X browser cookies or AUTH_TOKEN/CT0 session credentials. <br>
Mitigation: Prefer explicit API keys where possible, keep the secrets file private, and install only when this credential access is acceptable. <br>
Risk: Research topics and URLs may be sent to third-party search or social-data services. <br>
Mitigation: Avoid sensitive topics unless provider disclosure is acceptable, and review configured providers before running searches. <br>
Risk: Research reports and findings may be retained locally. <br>
Mitigation: Review and delete the local data directory periodically according to the user's retention needs. <br>


## Reference(s): <br>
- [OpenClaw Skill README](artifact/README.md) <br>
- [Attribution and Provenance](artifact/ATTRIBUTION.md) <br>
- [Research Workflow Reference](artifact/variants/open/references/research.md) <br>
- [Watchlist Workflow Reference](artifact/variants/open/references/watchlist.md) <br>
- [Briefing Workflow Reference](artifact/variants/open/references/briefing.md) <br>
- [History Workflow Reference](artifact/variants/open/references/history.md) <br>
- [Upstream last30days-skill Repository](https://github.com/mvanhorn/last30days-skill) <br>
- [ClawHub Skill Page](https://clawhub.ai/keylimesoda/last30days-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON from helper scripts, and shell commands for setup and execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist reports, findings, briefings, logs, and SQLite history under the configured OpenClaw workspace data directory.] <br>

## Skill Version(s): <br>
1.0.0-openclaw.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
