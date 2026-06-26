## Description: <br>
Search the web or X/Twitter using xAI Grok server-side tools through the xAI Responses API, with structured JSON results and citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notabhay](https://clawhub.ai/user/notabhay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run Grok-backed web search, X/Twitter search, chat, vision chat, and model listing from local Node.js scripts when they need current results, X posts, or citation URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, chat prompts, and any image file explicitly named by the user are sent to xAI using the configured API key. <br>
Mitigation: Use a dedicated revocable xAI API key where possible, avoid sensitive prompts or images unless acceptable, and monitor provider usage. <br>
Risk: The self-test and normal skill commands make real xAI API calls. <br>
Mitigation: Run the self-test and commands only when intended, and account for provider usage or billing in the target environment. <br>


## Reference(s): <br>
- [xAI Search tools](https://docs.x.ai/docs/guides/tools/search-tools) <br>
- [xAI Tools overview](https://docs.x.ai/docs/guides/tools/overview) <br>
- [xAI API reference](https://docs.x.ai/docs/api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [Pretty JSON search results, citation URL lists, or plain text chat output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and XAI_API_KEY; search output includes query, mode, results, and citations, with optional raw provider payloads on stderr for debugging.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
