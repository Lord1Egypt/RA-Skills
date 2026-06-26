## Description: <br>
竞品分析神器 v1.0。输入你的产品和竞品列表，自动生成结构化竞品分析报告，含对比矩阵、战略建议、风险预警。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyjaixiao](https://clawhub.ai/user/hyjaixiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as founders, product managers, investors, strategy teams, freelancers, and students use this skill to create competitor analysis reports for product planning, due diligence, fundraising preparation, and market research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deep-analysis mode can send product, market, strengths, and competitor details to the configured OpenAI-compatible API. <br>
Mitigation: Use only trusted API endpoints, avoid submitting confidential strategy unless approved, and run template mode when external API sharing is not acceptable. <br>
Risk: Generated reports may contain confidential business strategy and are saved to the configured output directory. <br>
Mitigation: Keep the output directory private and apply normal access controls before sharing or storing reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hyjaixiao/hyjaixiao-competitor-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report saved as a .md file, with command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be generated through an OpenAI-compatible API when OPENAI_API_KEY is configured, or as a template report when no API key is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
