## Description: <br>
股票分析 AI 工具 | 智能投资简报生成器 - 自动生成个股分析报告、市场热点追踪、持仓监控。支持 A股/港股/美股，实时股价查询，技术分析，研报生成。一键生成专业 Markdown 投资报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate stock, market, and portfolio monitoring briefs from Tavily search results. It is intended to produce concise Markdown investment research summaries for A-share, Hong Kong, and U.S. equities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted stock or name inputs may be interpolated into a local shell command. <br>
Mitigation: Use only trusted stock/name inputs and prefer an updated release that uses argument arrays instead of shell interpolation. <br>
Risk: The skill depends on a separate tavily-search helper installed in the user's OpenClaw skills directory. <br>
Mitigation: Verify the helper is installed from a trusted source before running this skill. <br>
Risk: Reports can be written to a user-provided output path. <br>
Mitigation: Avoid writing reports to important existing files or sensitive locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/investment-brief-generator) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write reports to a user-specified output file when --output is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
