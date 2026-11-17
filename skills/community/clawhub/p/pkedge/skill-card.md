## Description:

Monitor Polymarket prediction markets, spot mispricings between crowd probabilities and real-world evidence, track whale positioning from the top-50 leaderboard wallets, and detect fresh wallet insider signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franks33](https://clawhub.ai/user/franks33)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce Polymarket market intelligence, including daily scans, single-market analysis, whale-position summaries, and fresh-wallet alerts. It is intended for informational analysis and explicitly frames outputs as not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to run local Node scripts and scheduled jobs that are not included in the artifact.

Mitigation: Inspect the referenced scripts before running npm install or node cron.js, and deploy scheduled jobs only after reviewing the local project.

Risk: Telegram bot credentials are required for delivery channels.

Mitigation: Store credentials in a local environment file, limit access to the bot and channel tokens, and rotate them if exposed.

Risk: Broad conversational triggers can cause market alerts or analysis to be sent unintentionally.

Mitigation: Use explicit pkedge trigger phrases and review delivery configuration before enabling automated alerts.

Risk: Prediction-market signals can be mistaken for trading advice.

Mitigation: Keep outputs informational, include the skill's not-financial-advice disclaimer, and avoid direct buy or sell recommendations.

## Reference(s):

- [Polymarket](https://polymarket.com)
- [ClawHub skill page](https://clawhub.ai/franks33/skills/pkedge)
- [Publisher profile](https://clawhub.ai/user/franks33)
- [Polymarket Gamma markets API](https://gamma-api.polymarket.com/markets?active=true&limit=200)
- [Polymarket CLOB order book API](https://clob.polymarket.com/book?token_id={tokenId})
- [Polymarket leaderboard API](https://data-api.polymarket.com/v1/leaderboard?timePeriod=ALL&orderBy=PNL&limit=50)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text market intelligence digests, alerts, analysis summaries, and setup instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include the skill's financial-risk disclaimer and avoid direct trading recommendations.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
