## Description:

通过自然语言查询 A 股实时行情、公司基本信息、F10 财务数据和个股技术指标等授权范围内的基础金融数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtht-tech](https://clawhub.ai/user/gtht-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve authorized A-share market, company, F10 financial, technical-indicator, and capital-flow data from the Lingxi financial data service. It is intended for objective financial data lookup, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a reusable financial-data API key in gtht-entry.json.

Mitigation: Prefer QR authorization, protect the stored credential file, and delete it when access is no longer needed.

Risk: The skill depends on remote gateway calls to a financial-data service.

Mitigation: Install only if the publisher is trusted and review or lock down gateway-config.json and GTHT_GATEWAY_CONFIG before use.

Risk: Financial lookup results could be mistaken for investment advice.

Mitigation: Present outputs as objective reference data and preserve the required disclaimer that results do not constitute investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gtht-tech/skills/lingxi-financialsearch-skill)
- [Lingxi app API key activity page](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=lingxi&webEnv=web2&islingxishare=1)
- [Junhong app API key activity page](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=junhong&webEnv=web2&isyyzshare=1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown text with command snippets and JSON-backed financial data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authorization links, query conditions, data dates, and the required financial-data disclaimer.]

## Skill Version(s):

1.11.3 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
