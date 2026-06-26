## Description: <br>
国泰海通证券-灵犀智能选股 supports natural-language multi-factor A-share stock screening and historical backtesting of screening results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gtht-tech](https://clawhub.ai/user/gtht-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to screen A-share stocks with natural-language financial criteria and run historical backtests for selected strategies. The skill returns objective financial data and explicitly states that generated content is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles finance-related API keys and may store a GuoTai HaiTong/Lingxi API key in gtht-entry.json. <br>
Mitigation: Prefer the QR/cloud authorization path, review where gtht-entry.json is stored, and revoke or rotate any key shared in conversation or exposed in logs. <br>
Risk: Stock screening and historical backtesting outputs can be mistaken for investment advice or future return predictions. <br>
Mitigation: Preserve the required disclaimers and treat outputs as objective data or simulated historical results, not recommendations or promises of future performance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gtht-tech/lingxi-smartstockselection-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/gtht-tech) <br>
- [Lingxi authorization page](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=lingxi&webEnv=web2&islingxishare=1) <br>
- [Junhong authorization page](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=junhong&webEnv=web2&isyyzshare=1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown and JSON responses from Node.js tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Financial-search responses must include the required no-investment-advice disclaimer; backtest responses must include the required simulated-results disclaimer.] <br>

## Skill Version(s): <br>
1.11.3 (source: frontmatter, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
