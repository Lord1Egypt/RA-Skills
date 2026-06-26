## Description: <br>
Create tokens on-chain, check fee earnings, check Kibi Credit balance, trigger agent credit reload, and interact with KibiBot's Agent API and Kibi LLM Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kibiagent](https://clawhub.ai/user/kibiagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent work with KibiBot account data, token creation, fee and portfolio lookup, credit balance checks, optional credit reloads, and LLM gateway configuration or calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent create tokens and trigger wallet-funded Kibi Credit reloads through KibiBot. <br>
Mitigation: Use a dedicated least-privilege API key, leave Agent Reload disabled unless needed, and require explicit review before each token creation or reload. <br>
Risk: Credit reloads can spend configured trading-wallet funds when Agent Reload is enabled. <br>
Mitigation: Set low reload limits and require the agent to show the amount, source wallet, quota impact, and remaining daily limit before triggering a reload. <br>


## Reference(s): <br>
- [KibiBot Agent API reference](references/api.md) <br>
- [KibiBot website](https://kibi.bot) <br>
- [KibiBot Agent API](https://api.kibi.bot/agent/v1) <br>
- [Kibi LLM Gateway](https://llm.kibi.bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets, API request examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated KibiBot API actions when the user provides an API key and has enabled the relevant permissions.] <br>

## Skill Version(s): <br>
1.5.2 (source: server release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
