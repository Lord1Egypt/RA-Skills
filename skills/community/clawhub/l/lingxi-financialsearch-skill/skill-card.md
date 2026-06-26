## Description: <br>
国泰海通证券-灵犀金融数据查询skill，通过自然语言查询A股实时行情、公司基本信息、F10财务数据、个股技术指标等金融数据，只能查询A股基础行情，遵循沪深交易所行情转发规则，不提供研报数据，仅提供授权范围内基础行情数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gtht-tech](https://clawhub.ai/user/gtht-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query authorized A-share market data, company information, F10 financial metrics, technical indicators, and related objective financial data through natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles API keys and device-identifying data, and the key may remain in a shared local JSON file until cleared. <br>
Mitigation: Install only if the publisher and GTHT/GTJA service endpoints are trusted, prefer QR authorization over sending an API key in chat, use the least-privileged key available, and clear credentials with the documented clear command when no longer needed. <br>
Risk: The skill returns financial data that users could mistake for investment advice. <br>
Mitigation: Keep responses limited to objective data, preserve the required disclaimer, and direct users outside the skill when requested information is beyond its documented scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gtht-tech/lingxi-financialsearch-skill) <br>
- [GTHT Lingxi authorization and API key page](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=lingxi&webEnv=web2&islingxishare=1) <br>
- [GTHT Junhong authorization and API key page](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=junhong&webEnv=web2&isyyzshare=1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline Node.js commands and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Financial responses must remain objective, include the skill's required financial-data disclaimer, and avoid investment advice.] <br>

## Skill Version(s): <br>
1.11.3 (source: evidence release version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
