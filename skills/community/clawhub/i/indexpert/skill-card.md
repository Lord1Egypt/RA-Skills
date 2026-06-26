## Description: <br>
指数投资分析助手。解读A股/港股/美股指数行情、财经新闻关联指数、结合巴菲特/达利欧/林奇等9位大师框架给出投资视角。stock index / ETF / A股 / 基金 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pzc66momo](https://clawhub.ai/user/pzc66momo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to analyze A-share, Hong Kong, and U.S. stock indices or ETFs, connect financial news to related index themes, and compare index ideas through multiple investing frameworks. It is intended for educational market analysis and should not be used as personalized investment advice or a trade decision system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist risk preference, investment horizon, focus areas, corrections, and feature requests in local files. <br>
Mitigation: Review or clear the profile, memory, and learning files before reuse, and avoid sharing personal holdings, account details, or sensitive financial information. <br>
Risk: The skill can update its own guidance from conversation history, which may preserve incorrect or unwanted behavior. <br>
Mitigation: Review accumulated memory, routing, learning, error, and feature-request entries before deployment or continued use. <br>
Risk: Financial analysis may be incomplete, stale, or unsuitable for a user's individual circumstances. <br>
Mitigation: Treat outputs as educational market analysis, verify facts with authoritative sources, and require human judgment before any investment action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pzc66momo/indexpert) <br>
- [SKILL.md](SKILL.md) <br>
- [Index catalog](references/index_catalog.json) <br>
- [Trusted sources index](references/trusted_sources_index.json) <br>
- [Trusted sources media](references/trusted_sources_media.json) <br>
- [Expression style reference](references/expression/hulan.md) <br>
- [Master investing frameworks](references/masters/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown analysis with index recommendations, caveats, and investment-risk disclaimers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are index-focused, may include links for cataloged indices, and do not execute trades.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
