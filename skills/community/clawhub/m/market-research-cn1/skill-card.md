## Description: <br>
市场调研分析助手。根据用户提供的调研主题（行业、产品或市场），生成结构化的市场分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaomxxx](https://clawhub.ai/user/xiaomxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business analysts use this skill to produce structured Chinese-language market research reports for industries, products, or geographic markets. It supports market overview, target users, competitors, product and business models, trends, risks, and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live retrieval may send research topics to third-party RSS, news, search, and result pages. <br>
Mitigation: Do not use confidential market plans, internal project names, or proprietary research topics unless third-party disclosure is acceptable. <br>
Risk: The fallback crawler can write retrieved research content to a local JSON file. <br>
Mitigation: Use the output file option intentionally and review saved content before sharing or committing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaomxxx/market-research-cn1) <br>
- [36Kr AI information source](https://www.36kr.com/information/AI/) <br>
- [Huxiu information source](https://www.huxiu.com/) <br>
- [TMTPost information source](https://www.tmtpost.com/) <br>
- [Ifanr information source](https://www.ifanr.com/) <br>
- [Wired AI information source](https://www.wired.com/tag/artificial-intelligence/) <br>
- [The Verge AI information source](https://www.theverge.com/ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown report with optional shell commands and optional JSON crawler output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to up to 5 retrieved items unless the user specifies a count.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata; frontmatter reports 1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
