## Description: <br>
Uses the Moonshot Kimi API built-in web search tool to perform live web searches for Chinese and English queries and requires MOONSHOT_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChrisBDZ](https://clawhub.ai/user/ChrisBDZ) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to ask Kimi/Moonshot for current web search answers from an agent workflow. It is intended for real-time information lookup when a Moonshot API key and Python runtime are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the third-party Moonshot/Kimi API. <br>
Mitigation: Avoid using the skill with passwords, API keys, confidential code, customer data, or unreleased business information. <br>
Risk: A Moonshot API key is required for operation. <br>
Mitigation: Store the key in MOONSHOT_API_KEY or protected user configuration, and prefer environment-variable storage on shared machines. <br>


## Reference(s): <br>
- [Kimi Search on ClawHub](https://clawhub.ai/ChrisBDZ/kimi-search) <br>
- [Moonshot Open Platform](https://platform.moonshot.cn) <br>
- [Moonshot Web Search Guide](https://platform.moonshot.cn/docs/guide/use-web-search) <br>
- [Moonshot Chat Pricing](https://platform.moonshot.cn/docs/pricing/chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON object containing the original query, Kimi's answer, and token usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOONSHOT_API_KEY and sends search queries to the Moonshot/Kimi API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
