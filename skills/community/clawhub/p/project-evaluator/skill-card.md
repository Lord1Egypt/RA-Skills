## Description: <br>
描述一个项目想法，AI 从市场、技术、商业和风险四个维度进行系统评估，并输出评估报告、竞品速查和 MVP 建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product builders, startup founders, and PMs use this skill to assess whether a project idea is worth pursuing. It generates a Chinese-language evaluation across market demand, technical feasibility, business model, risks, competitors, MVP scope, and final recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project ideas are sent to the configured LLM provider. <br>
Mitigation: Use only with project details suitable for that provider and configure the endpoint and matching API key explicitly before running. <br>
Risk: An unrelated OPENAI_API_KEY can be sent to the default DeepSeek endpoint. <br>
Mitigation: Unset unrelated API keys or set OPENAI_API_BASE and LLM_MODEL deliberately so credentials match the selected provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antonia-sz/project-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY or DEEPSEEK_API_KEY and sends project ideas to the configured LLM endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
