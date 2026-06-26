## Description: <br>
Call 100+ LLM providers through LiteLLM's unified API for model comparison, task-based routing, cost optimization, and fallback access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ishaan-jaff](https://clawhub.ai/user/ishaan-jaff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to call and compare LLMs across providers, route prompts to task-appropriate or lower-cost models, and use LiteLLM proxy settings when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, system messages, and related metadata may be sent to a selected LLM provider or LiteLLM proxy. <br>
Mitigation: Use only approved providers or proxies for sensitive work and avoid sending secrets, regulated data, or confidential code unless the destination is authorized. <br>
Risk: API keys and proxy credentials are required for provider access and could be exposed if mishandled. <br>
Mitigation: Store keys in environment variables or approved secret managers, rotate them when needed, and avoid committing credentials to skill artifacts or prompts. <br>
Risk: Unpinned LiteLLM installations can change behavior as dependencies update. <br>
Mitigation: Pin the LiteLLM dependency in managed environments and monitor usage costs and provider routing. <br>


## Reference(s): <br>
- [LiteLLM provider documentation](https://docs.litellm.ai/docs/providers) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; helper script output is plain text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send prompts, system messages, and related metadata to the selected LLM provider or LiteLLM proxy.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
