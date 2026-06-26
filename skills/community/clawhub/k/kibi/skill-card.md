## Description: <br>
KibiBot lets agents create tokens on-chain, check fee earnings and Kibi Credit balances, trigger credit reloads, and interact with KibiBot's Agent API and LLM Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kibubot](https://clawhub.ai/user/kibubot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use KibiBot to manage token creation, inspect fee earnings, query account and wallet state, configure Kibi's LLM Gateway, and make authenticated Kibi API calls from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-funded credit reloads and on-chain token creation can spend funds or initiate irreversible actions if an agent proceeds without final user confirmation. <br>
Mitigation: Use a least-privileged Kibi API key, enable Agent Reload only when intended, and require explicit approval before credit reloads or token creation. <br>
Risk: LLM gateway usage routes prompts and responses through KibiBot and consumes Kibi Credits. <br>
Mitigation: Avoid sending secrets or regulated data through the gateway unless KibiBot's data handling and billing terms are acceptable, and monitor balances and daily limits. <br>
Risk: The security guidance notes VirusTotal was pending and calls for review before installation. <br>
Mitigation: Review the artifact and security notes before deployment, and scan the skill in the target environment before use. <br>


## Reference(s): <br>
- [KibiBot ClawHub listing](https://clawhub.ai/kibubot/kibi) <br>
- [KibiBot provider site](https://kibi.bot) <br>
- [KibiBot Agent API](https://kibi.bot/agent) <br>
- [KibiBot API keys](https://kibi.bot/settings/api-keys) <br>
- [Kibi LLM Gateway](https://kibi.bot/llm) <br>
- [OpenClaw setup](https://kibi.bot/llm/openclaw) <br>
- [Kibi Credits](https://kibi.bot/credits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and API request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated KibiBot API requests and OpenAI-compatible LLM gateway configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact SKILL.md states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
