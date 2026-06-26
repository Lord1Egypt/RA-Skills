## Description: <br>
Configure OpenRouter model routing with provider auth, model selection, fallback chains, and cost-aware defaults for stable multi-model workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to connect OpenAI-compatible workflows to OpenRouter, define routing and fallback policy by workload, and keep provider auth, reliability, and costs explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt content may be sent to OpenRouter when routed inference is requested. <br>
Mitigation: Use the skill only for prompts that are appropriate to share with OpenRouter and avoid sending sensitive data unless the user accepts that exposure. <br>
Risk: OpenRouter usage may incur cost and routing mistakes can increase spend. <br>
Mitigation: Set monthly and per-task budget ceilings before rollout, review spend by workload class, and reserve premium models for high-impact tasks. <br>
Risk: API keys or routing notes could be exposed if copied into chat or stored in local notes. <br>
Mitigation: Keep OPENROUTER_API_KEY in the environment, do not paste raw secrets into chat, and avoid storing secrets in ~/open-router/. <br>


## Reference(s): <br>
- [Open Router skill page](https://clawhub.ai/ivangdavila/open-router) <br>
- [OpenRouter model catalog endpoint](https://openrouter.ai/api/v1/models) <br>
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions) <br>
- [Setup guide](setup.md) <br>
- [Authentication and provider wiring](auth-and-provider.md) <br>
- [Routing playbooks](routing-playbooks.md) <br>
- [Fallback reliability](fallback-reliability.md) <br>
- [Cost guardrails](cost-guardrails.md) <br>
- [Memory template](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local notes under ~/open-router/ and requires OPENROUTER_API_KEY for OpenRouter verification requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
