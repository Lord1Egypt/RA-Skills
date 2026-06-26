## Description: <br>
黄金投资分析工具，提供实时金价查询、技术指标分析、新闻基本面分析功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FMouseBoy](https://clawhub.ai/user/FMouseBoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to gather current gold-market search results and produce a gold investment analysis covering price, technical indicators, fundamentals, and risk notes. It is intended for informational analysis, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gold-related queries and source searches may be sent to Tavily. <br>
Mitigation: Avoid including private financial details in prompts or queries, and install only if outbound Tavily search is acceptable. <br>
Risk: The artifact includes and automatically falls back to a shared Tavily API key. <br>
Mitigation: Set your own TAVILY_API_KEY before use; the publisher should remove and rotate the embedded key. <br>
Risk: Generated market analysis may be incomplete, stale, or mistaken and could be misread as financial advice. <br>
Mitigation: Treat outputs as informational, verify important claims against trusted market data, and consult a qualified professional for investment decisions. <br>


## Reference(s): <br>
- [Gold Technical Indicators Reference](references/technical-indicators.md) <br>
- [Tavily](https://tavily.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis report with source links and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires outbound Tavily searches when the search script is used; reports should be treated as informational.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
