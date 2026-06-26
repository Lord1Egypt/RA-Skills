## Description: <br>
Create, modify, generate, and deploy websites, web apps, dashboards, SaaS products, internal tools, interactive web pages, Weixin mini programs, and games on the Baidu Miaoda platform using natural-language instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seiriosplus](https://clawhub.ai/user/seiriosplus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, modify, generate, and publish Miaoda-hosted web products and content documents from natural-language prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Miaoda API key and sends prompts, app details, and workflow state to Miaoda. <br>
Mitigation: Use only the intended Miaoda account key, keep the API base URL on the official Miaoda endpoint, and avoid placing secrets or private data in prompts. <br>
Risk: The skill can consume Miaoda account credits when generating, modifying, or publishing applications. <br>
Mitigation: Require explicit user approval before generation or publishing actions that may consume credits. <br>
Risk: The skill can publish generated applications to a public production URL. <br>
Mitigation: Review generated content, app status, and deployment intent before running publish commands or sharing production URLs. <br>
Risk: Conversation history and trajectory output may contain sensitive project details. <br>
Mitigation: Review and redact history or trajectory output before sharing it outside the trusted workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/seiriosplus/miaoda-app-builder) <br>
- [Miaoda Official Website](https://www.miaoda.cn) <br>
- [Miaoda API Endpoint](https://api.miaoda.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Miaoda app IDs, conversation IDs, trajectory/status JSON, preview URLs, and production deployment URLs.] <br>

## Skill Version(s): <br>
1.0.12 (source: release evidence and CLI script version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
