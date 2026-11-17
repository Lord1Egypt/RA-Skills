## Description:

Analyzes Amazon keyword Share of Voice using Jungle Scout data, returning brand visibility across organic, sponsored, and combined search results, plus 30-day search volume, PPC bid median, and top ASIN click and conversion metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, analysts, and agents use this skill to assess which brands occupy Amazon keyword search results and compare organic visibility, sponsored visibility, PPC cost signals, and top ASIN conversion performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill includes LinkFox account onboarding, API-key creation, billing order actions, local data retention, and feedback reporting in addition to the advertised analytics workflow.

Mitigation: Review LinkFox account and billing steps before use, prefer managing API keys through the official LinkFox site, avoid storing secrets permanently in shell startup files when possible, and confirm paid actions before execution.

Risk: The security guidance warns against use where untrusted variables can set LINKFOX_* endpoint URLs or SESSION_ID.

Mitigation: Run the skill only in trusted environments with reviewed LINKFOX_* and SESSION_ID values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-junglescout-keyword-share-of-voice)
- [Jungle Scout Share of Voice API Reference](artifact/references/api.md)
- [LinkFox account and billing onboarding](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with tables and summaries; JSON API responses and saved JSON data files when the helper script is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One keyword per API call; helper script caches responses for 24 hours and writes full responses under a LinkFox session data directory.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
