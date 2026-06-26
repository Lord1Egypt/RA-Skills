## Description: <br>
评估企业护城河类型和强度，帮助价值投资者判断企业是否具备持续竞争优势。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, investors, and analysts use this skill to evaluate a company's brand, network effects, switching costs, scale advantages, and franchise rights for long-term value-investing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto market queries, wallet addresses, or portfolio lookup inputs may be sent to Hive's remote MCP service if those connector behaviors are used. <br>
Mitigation: Inspect endpoint schemas before invocation, avoid sensitive wallet or portfolio data unless approved, and require explicit review before any endpoint that could write to an account or change data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/moat-evaluator) <br>
- [护城河理论参考](references/moat-theory.md) <br>
- [护城河分析模板](templates/moat-analysis-template.md) <br>
- [腾讯控股护城河分析示例](examples/tencent-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown analysis with tables; the skill also defines a JSON result shape.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include moat type evidence, strength scores, total score, trend, investment advice, risks, and key metrics.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
