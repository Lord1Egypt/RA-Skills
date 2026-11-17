## Description:

Configure OpenRouter model routing with provider auth, model selection, fallback chains, and cost-aware defaults for stable multi-model workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to connect OpenAI-compatible workflows to OpenRouter, choose task-specific models, define fallback chains, and keep routing cost-aware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt content is sent to OpenRouter when routed inference is requested.

Mitigation: Use the skill only when OpenRouter is intended for the task and avoid sending sensitive prompt content unless that use is approved.

Risk: API keys could be exposed if copied into chat, logs, or memory notes.

Mitigation: Keep OPENROUTER_API_KEY in the local environment and record only auth pass/fail status in notes.

Risk: Routing changes can increase spend or degrade reliability if applied broadly without checks.

Mitigation: Set monthly and per-task budget limits, change one routing layer at a time, and verify changes with representative prompts.

Risk: Provider outages, rate limits, latency spikes, or model quality changes can disrupt workflows.

Mitigation: Cap retries, use fallback models from different provider families where possible, and log incident fingerprints for repeat handling.

## Reference(s):

- [Open Router Skill Page](https://clawhub.ai/ivangdavila/skills/open-router)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions)
- [Setup](setup.md)
- [Auth and Provider](auth-and-provider.md)
- [Routing Playbooks](routing-playbooks.md)
- [Fallback Reliability](fallback-reliability.md)
- [Cost Guardrails](cost-guardrails.md)
- [Memory Template](memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local routing notes under ~/open-router/ when the user chooses to maintain persistent OpenRouter preferences.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
