## Description: <br>
A comprehensive AI model routing system that automatically selects the optimal model for any task, supports multiple AI providers, stores local API keys, and recommends models based on task type, complexity, and cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[digitaladaption](https://clawhub.ai/user/digitaladaption) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to classify tasks, choose cost-appropriate AI models, and configure local routing across supported providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup wizard stores AI provider API keys on the local machine. <br>
Mitigation: Configure only approved provider keys, keep ~/.model-router restricted to the current user, rotate keys regularly, and avoid sharing the directory. <br>
Risk: Routed tasks may send private or regulated data to third-party model providers. <br>
Mitigation: Verify each provider is approved for the data being routed and avoid sending sensitive work to providers that have not been reviewed. <br>
Risk: Documented model aliases and provider mappings may not match the intended models. <br>
Mitigation: Review and correct the alias-to-model mapping before relying on automated routing decisions. <br>


## Reference(s): <br>
- [Model Router on ClawHub](https://clawhub.ai/digitaladaption/model-router) <br>
- [Usage Examples](references/USAGE_EXAMPLES.md) <br>
- [Model Specifications Reference](references/model-specs.md) <br>
- [Anthropic Documentation](https://docs.anthropic.com) <br>
- [OpenAI Documentation](https://platform.openai.com/docs) <br>
- [Gemini Documentation](https://ai.google.dev/docs) <br>
- [Moonshot Documentation](https://platform.moonshot.cn/docs) <br>
- [Z.ai Documentation](https://api.z.ai/docs) <br>
- [GLM Documentation](https://open.bigmodel.cn/dev/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell command examples, local JSON configuration, and optional classifier JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local provider configuration and API key files under ~/.model-router when the setup wizard is run.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
