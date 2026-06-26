## Description: <br>
Generates an Amazon market research HTML report from a category name and node ID, covering market overview, listing age, pricing, reviews, brands, sellers, top competitors, and overall assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiafar](https://clawhub.ai/user/jiafar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace sellers and analysts use this skill to request Amazon category research by category name and node ID and receive a consolidated HTML report for product and competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task content is sent to the LinkFox third-party agent service. <br>
Mitigation: Use the skill only when LinkFox is trusted with the category, node ID, and business context; avoid proprietary strategy or secrets in prompts. <br>
Risk: Generated reports are HTML from third-party output and may contain active content. <br>
Mitigation: Treat generated HTML as active third-party content and review it before opening or sharing in sensitive environments. <br>
Risk: The shell workflow runs network requests, downloads report files, and writes output files. <br>
Mitigation: Review the command arguments before execution and prefer strictly numeric node IDs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiafar/linkfox-market-research) <br>
- [LinkFox Agent API](https://agent-api.linkfox.com/) <br>
- [LinkFox Agent API Key Setup](https://yxgb3sicy7.feishu.cn/wiki/IlkawdQP9ifKv9k22xcc7rjmnkb) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, HTML files, Guidance] <br>
**Output Format:** [Single-page HTML report plus status text from shell execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY, Python 3, network access to the LinkFox Agent API, and a category name plus node ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
