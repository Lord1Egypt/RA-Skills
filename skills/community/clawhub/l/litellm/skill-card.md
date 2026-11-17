## Description:

Call 100+ LLM providers through LiteLLM's unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ishaan-jaff](https://clawhub.ai/user/ishaan-jaff)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to call, compare, and route prompts across LLM providers through LiteLLM's unified API, including direct provider calls or a configured LiteLLM proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt contents and system messages may be sent to the configured LiteLLM proxy or upstream model provider.

Mitigation: Use approved providers or proxies, avoid secrets or regulated data unless authorized, and review provider data-handling requirements before use.

Risk: The skill relies on provider or proxy API keys for external LLM calls.

Mitigation: Keep API keys in controlled environment variables or a secrets manager, and avoid embedding credentials in prompts, scripts, or shared logs.

## Reference(s):

- [LiteLLM provider documentation](https://docs.litellm.ai/docs/providers)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; helper script output is plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script accepts prompt, model, system message, JSON output, temperature, and max-token options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
