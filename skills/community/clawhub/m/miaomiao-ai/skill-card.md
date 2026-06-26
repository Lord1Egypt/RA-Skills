## Description: <br>
Miaomiao AI Assistant routes chat requests to Link-AI for conversation, weather, news, package tracking, image generation, web search, summarization, charts, maps, and train-ticket queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agleameal](https://clawhub.ai/user/agleameal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call a Link-AI assistant from an agent for everyday information, generation, and lookup tasks through a single API-backed chat interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad auto-activation can route ordinary chats or sensitive prompts to Link-AI without clear user intent. <br>
Mitigation: Scope activation narrowly, confirm third-party routing before sending sensitive requests, and avoid private documents, secrets, regulated data, logistics details, or location and travel information unless the provider is trusted. <br>
Risk: The skill requires API credentials for Link-AI/Miaomiao. <br>
Mitigation: Use a dedicated API key, keep credentials out of prompts and logs, rotate keys periodically, and revoke keys that may have been exposed. <br>
Risk: Debug mode can print request parameters and response content. <br>
Mitigation: Keep debug mode disabled for real user data and scrub logs before sharing diagnostics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agleameal/miaomiao-ai) <br>
- [Link-AI platform](https://link-ai.tech) <br>
- [Link-AI chat completions endpoint](https://api.link-ai.tech/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON responses from the Link-AI chat completions API, with Python and shell snippets in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a third-party API using MIAOMIAO_API_KEY or LINKAI_API_KEY; supports optional streaming responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact CHANGELOG top entry is v1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
