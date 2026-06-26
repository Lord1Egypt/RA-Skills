## Description: <br>
Route any prompt to the best-performing LLM using peer-reviewed council rankings from LLM Council. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashtiwariasu](https://clawhub.ai/user/ashtiwariasu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to select an LLM for a specific prompt or task, then optionally call the selected model through OpenRouter using the returned model identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt content is sent to LLM Council for routing, and may also be sent to OpenRouter when using the chaining example. <br>
Mitigation: Avoid sending secrets, private documents, regulated data, or proprietary prompts unless those services' data handling terms have been reviewed and approved. <br>
Risk: API keys are required and quota usage can be consumed by automated routing or chained model calls. <br>
Mitigation: Use dedicated API keys stored in environment variables, scope access where possible, and monitor usage against the configured service tiers. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/ashtiwariasu/llmcouncil-router) <br>
- [LLM Council](https://llmcouncil.ai) <br>
- [LLM Council Developers](https://llmcouncil.ai/developers) <br>
- [LLM Council Routing API](https://clawbot.llmcouncil.ai/v1/route) <br>
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON] <br>
**Output Format:** [Markdown with API examples, shell commands, Python code, and JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an LLMCOUNCIL_API_KEY environment variable; the optional OpenRouter chaining example also requires OPENROUTER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
