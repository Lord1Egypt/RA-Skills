## Description:

Odaily Skill helps agents retrieve and structure Odaily crypto news, market data, upcoming events, Polymarket whale signals, and raw API module outputs for crypto-market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odaily](https://clawhub.ai/user/odaily)

### License/Terms of Use:

MIT-0

## Use Case:

External crypto-market users and developers use this skill to ask an agent for current Odaily news, crypto market analysis, upcoming event watchlists, Polymarket whale-trade signals, and raw article or newsflash data. Outputs are informational and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The invocation pattern can discover and run local code from an unintended similarly named directory.

Mitigation: Install the skill into a controlled path and invoke the expected artifact directory directly instead of relying on broad path discovery.

Risk: The skill can reinstall unpinned Python dependencies during use.

Mitigation: Pin dependencies and install them in a managed virtual environment before deployment.

Risk: The skill makes outbound calls to crypto, news, and market-data APIs, and may write whale-trade data to Supabase when credentials are configured.

Mitigation: Run in an isolated environment with network access reviewed and only configure Supabase credentials when persistence is intended.

Risk: Crypto-market outputs may be time-sensitive, incomplete, or misleading if upstream APIs fail or markets move quickly.

Mitigation: Treat outputs as informational, verify important signals against primary sources, and avoid using the skill as investment advice.

## Reference(s):

- [Odaily Skill on ClawHub](https://clawhub.ai/odaily/skills/odaily-skill)
- [Odaily](https://www.odaily.news)
- [Odaily Newsflash API](https://web-api.odaily.news/newsflash/page)
- [CoinGecko](https://www.coingecko.com)
- [Polymarket](https://polymarket.com)
- [Odaily Seer](https://t.me/Odaily_Seer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline tables, source links, timestamps, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes live-data summaries, source links, market analysis, and non-investment-advice disclaimers.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter reports 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
