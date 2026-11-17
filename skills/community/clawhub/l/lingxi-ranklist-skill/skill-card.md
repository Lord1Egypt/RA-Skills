## Description:

国泰海通证券-灵犀市场热榜查询 skill supports A-share market ranking queries for price movement, turnover, volume, turnover rate, market capitalization, valuation, volume ratio, and same-day capital net inflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtht-tech](https://clawhub.ai/user/gtht-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve and format A-share market ranking lists from GuoTai HaiTong Lingxi, including gainers, losers, volume, turnover, turnover rate, and same-day capital net inflow rankings. The skill requires brokerage API authorization before market data calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may request brokerage API authorization and save the resulting API key locally in plaintext.

Mitigation: Install only from a trusted publisher, run in a single-user environment, restrict permissions on stored gtht-entry.json files, redact logs, and rotate or clear the key if exposure is suspected.

Risk: The skill uses a MAC-derived device identifier during QR authorization and contacts GTHT gateway and authorization endpoints.

Mitigation: Use only in environments where those endpoints and identifiers are acceptable, and apply outbound gateway allowlisting and network monitoring before broader deployment.

Risk: The security evidence flags weak credential scoping and unsafe logging or storage practices.

Mitigation: Review logs and stored credential files carefully, and deploy only after credential redaction, file permissions, and gateway allowlisting have been verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gtht-tech/skills/lingxi-ranklist-skill)
- [GuoTai HaiTong ranklist gateway](https://zx.app.gtja.com:8443/mcp/hq-20200002)
- [GuoTai HaiTong Lingxi API key authorization activity](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=lingxi&webEnv=web2&islingxishare=1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown text with ranked market results and inline shell command examples when authorization or gateway calls are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a locally stored brokerage API key before market data queries; rankings are scoped to the A-share market endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 0.0.9)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
