## Description: <br>
Step-by-step guide for integrating Moonshot AI (Kimi) and Kimi Code models into Clawdbot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evgyur](https://clawhub.ai/user/evgyur) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to configure Clawdbot with Moonshot AI and Kimi Code model providers, including API keys, model aliases, verification commands, and troubleshooting steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if copied into shared terminals, logs, or unprotected configuration files. <br>
Mitigation: Use environment variables or a protected env file, and avoid printing full keys in shared terminals or logs. <br>
Risk: The included test script makes live requests to external Moonshot and Kimi endpoints. <br>
Mitigation: Run the test script only when a live external API request is intended and approved. <br>
Risk: Prompts or code sent through configured providers may leave the local environment. <br>
Mitigation: Send only data that the organization permits Moonshot or Kimi providers to process. <br>


## Reference(s): <br>
- [Configuration Examples](references/config-examples.md) <br>
- [Moonshot AI Documentation](https://platform.moonshot.cn/docs) <br>
- [Kimi Code API](https://api.kimi.com/coding/docs) <br>
- [Clawdbot Model Providers](https://docs.clawd.bot/concepts/model-providers) <br>
- [ClawHub Skill Page](https://clawhub.ai/evgyur/kimi-integration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and JSON5 code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes provider configuration snippets, environment variable setup, model selection commands, and an optional live API connection test script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
