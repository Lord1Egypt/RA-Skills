## Description: <br>
Generates NIO stock analysis reports for US and Hong Kong listings, including price, technical analysis, news sentiment, market sentiment, and trading recommendation sections. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[zhishuiyu](https://clawhub.ai/user/zhishuiyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to generate structured NIO analysis reports for the US and Hong Kong listings. Because the security evidence says the skill presents simulated market data as analysis, outputs should be treated as demonstration reports rather than live market intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents simulated prices, news, sentiment, target prices, stop losses, and trading recommendations in a way that could be mistaken for live market intelligence. <br>
Mitigation: Label outputs as simulated demonstration reports and do not use them for investment decisions unless the publisher replaces mock data with verified live sources and clear data provenance. <br>
Risk: Trading recommendations may mislead users if interpreted as financial advice. <br>
Mitigation: Keep the investment-risk disclaimer visible and require human review against independent, authoritative market data before acting on any recommendation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhishuiyu/nio-enhanced-analysis) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [analyze_nio.py](artifact/analyze_nio.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, analysis, guidance] <br>
**Output Format:** [Console text report and saved JSON analysis file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports us, hk, and all market arguments; outputs include simulated prices, sentiment, technical analysis, and trading recommendation fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
