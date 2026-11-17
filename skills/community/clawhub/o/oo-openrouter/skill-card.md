## Description:

Operate OpenRouter through an OOMOL-connected account, including retrieving account and model information and creating chat responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to retrieve OpenRouter account, model, provider, and generation information, and to create chat or message requests through their connected OOMOL account. It inspects an action's schema before submitting JSON input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat generation may incur costs, although the skill labels it as a safe read.

Mitigation: Explicitly authorize the model, prompt content, and spending limits before generation requests.

Risk: Setup directs users to an installer whose behavior and automatic agent-skill installation were not verified.

Mitigation: Verify and install the CLI yourself, then review its automatic agent-skill installation behavior before use.

Risk: Prompts pass through OOMOL to OpenRouter and model providers.

Mitigation: Avoid including sensitive prompt content unless you are comfortable with those data flows.

## Reference(s):

- [OpenRouter](https://openrouter.ai)
- [OpenRouter API documentation](https://openrouter.ai/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [OpenRouter skill listing](https://clawhub.ai/oomol/skills/oo-openrouter)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector responses and generated chat text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests use JSON input; chat generation may incur provider costs.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
