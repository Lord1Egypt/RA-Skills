## Description:

Korean stock market analyst Telegram bot that monitors KOSPI/KOSDAQ, tracks watchlists, delivers AI briefings, and answers market questions in Korean, Chinese, and English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbtsm](https://clawhub.ai/user/lbtsm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to deploy a Telegram bot for Korean equity monitoring, watchlist tracking, market briefings, disclosure lookup, and multilingual market Q&A. It supports data-backed responses and optional LLM analysis for market context, comparisons, and risk/opportunity summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User message text and conversation history may be retained or logged without prominent disclosure.

Mitigation: Disclose retention behavior before deployment, restrict logs, and disable or minimize conversation storage where policy requires.

Risk: The bundled briefing wrapper references a fixed deployment path and can load another deployment's secrets.

Mitigation: Remove or fix run_briefing.sh before scheduling it, and run scheduled jobs under an unprivileged service account.

Risk: Telegram, LLM, OpenNews, Twitter, and DART tokens are production secrets.

Mitigation: Store tokens in a dedicated secret manager or protected environment, avoid committing them, and rotate credentials after exposure.

Risk: Optional cron jobs can broadcast market briefings or alerts to configured recipients.

Mitigation: Confirm recipient IDs and make cron-based broadcasts an explicit opt-in deployment step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lbtsm/skills/mapulse-korea)
- [Publisher profile](https://clawhub.ai/user/lbtsm)
- [Artifact README](artifact/README.md)
- [Data sources reference](artifact/docs/data-sources.md)
- [Architecture reference](artifact/docs/architecture.md)
- [Deployment reference](artifact/docs/deployment.md)
- [DART Open API](https://opendart.fss.or.kr)
- [Daum Finance](https://finance.daum.net)
- [Naver Finance mobile API](https://m.stock.naver.com/api)
- [6551 OpenNews API](https://ai.6551.io/open/news_latest)
- [6551 OpenTwitter API](https://ai.6551.io/open/twitter_search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Telegram-ready text and Markdown responses with setup commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include market summaries, stock analysis, alerts, briefing text, and operational setup steps.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
