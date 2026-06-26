## Description: <br>
国泰海通证券-灵犀研报搜索skill，查询国泰海通研究所专业研究报告，涵盖宏观策略、行业深度等，为投资分析提供专业研究支撑。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gtht-tech](https://clawhub.ai/user/gtht-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search GuoTai HaiTong Research Institute reports for macro strategy, industry analysis, market analysis, and investment-strategy research. The skill supports authorization and calls the GTHT research-report service when a user asks for research-report data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive API credentials and device identifiers. <br>
Mitigation: Install only when the publisher is trusted, prefer the QR/cloud authorization path instead of pasting an API key into chat, and clear local authorization when access is no longer needed. <br>
Risk: Users may be directed to external GTHT authorization domains. <br>
Mitigation: Verify the displayed GTHT domains before authorizing or entering credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gtht-tech/lingxi-researchreport-skill) <br>
- [GTHT Lingxi API key authorization page](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=lingxi&webEnv=web2&islingxishare=1) <br>
- [GTHT Junhong API key authorization page](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=junhong&webEnv=web2&isyyzshare=1) <br>
- [GTHT research-report MCP endpoint](https://zx.app.gtja.com:8443/mcp/researchReport/lingxi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and JSON service results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final responses include an investment-advice disclaimer from the skill instructions.] <br>

## Skill Version(s): <br>
1.11.3 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
