## Description: <br>
Openclaw/Trae domestic web search option that uses the Volcengine web Q&A agent API to answer search questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexjunanjing-2](https://clawhub.ai/user/alexjunanjing-2) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agents use this skill to run Chinese-language web search and question answering through a configured Volcengine agent. It returns answer text with references, suggested follow-up questions, usage details, and error details when calls fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search questions are sent to Volcengine/feedcoopapi using the user's configured API credentials. <br>
Mitigation: Use a dedicated API key, monitor provider usage or billing, and avoid sending secrets, private source code, internal URLs, personal data, or regulated information unless external sharing is approved. <br>
Risk: The skill depends on external web search results and generated answers that may be incomplete, stale, or inaccurate. <br>
Mitigation: Review cited references and validate important answers before using them in operational or customer-facing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexjunanjing-2/openclaw-skill-search-web) <br>
- [Publisher profile](https://clawhub.ai/user/alexjunanjing-2) <br>
- [Volcengine web Q&A agent API documentation](https://www.volcengine.com/docs/85508/1510834?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with answer content, references, follow-up suggestions, token usage, and error details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports non-streaming and streaming responses when the Volcengine API key and bot ID environment variables are configured.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
