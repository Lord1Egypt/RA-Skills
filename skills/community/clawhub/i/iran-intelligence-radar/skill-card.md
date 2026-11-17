## Description:

Monitors Persian-language X activity related to Iran, translates posts, scores escalation risk, and generates Markdown intelligence reports with optional alerts and daily briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthuronai](https://clawhub.ai/user/arthuronai)

### License/Terms of Use:


## Use Case:

Journalists, OSINT teams, geopolitical analysts, and monitoring operations use this skill to scan Persian-language social signals, identify high-engagement Iran-related narratives, translate relevant posts, and produce briefing-ready intelligence summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Failed searches can fall back to realistic mock intelligence that may be mistaken for live OSINT.

Mitigation: Clearly label or disable mock fallback data before operational use, and block fallback-generated reports from billing, persistence, and alerts unless explicitly configured for testing.

Risk: Reports, translations, and escalation scores may be forwarded to Telegram, SkillPay, translation providers, or alert destinations.

Mitigation: Strictly configure outbound integrations, verify what content is sent to each provider, and disable channels that are not required for the deployment.

Risk: Per-scan billing uses local cooldown protection and may charge users before search results are confirmed as live data.

Mitigation: Use provider-side idempotency or transactional billing state before enabling real-user charges, and verify billing behavior around retries and fallback execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arthuronai/skills/iran-intelligence-radar)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown intelligence reports, structured scan results, translated text, alert messages, and briefing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes escalation scores, alert levels, trending signals, tweet rows, optional Telegram alerts, payment-required responses, and daily briefing content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
