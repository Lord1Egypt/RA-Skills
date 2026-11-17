## Description:

Route any prompt to the best-performing LLM using peer-reviewed council rankings from LLM Council.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashtiwariasu](https://clawhub.ai/user/ashtiwariasu)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to select a suitable LLM for a prompt using LLM Council rankings, then optionally call the selected model through OpenRouter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be sent to LLM Council and, when using the chaining example, to OpenRouter and downstream model providers.

Mitigation: Avoid secrets, regulated data, proprietary code, and private files unless organizational approval covers those disclosures and billing implications.

Risk: The skill does not present a clear privacy confirmation before routing full prompt text to external services.

Mitigation: Review the skill before installation and add an explicit confirmation or disclosure step if users may provide confidential prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ashtiwariasu/skills/llmcouncil-router)
- [Publisher profile](https://clawhub.ai/user/ashtiwariasu)
- [LLM Council](https://llmcouncil.ai)
- [LLM Council developers](https://llmcouncil.ai/developers)
- [LLM Council route API](https://clawbot.llmcouncil.ai/v1/route)
- [OpenRouter chat completions API](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, bash, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LLMCOUNCIL_API_KEY; OpenRouter chaining also requires OPENROUTER_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
