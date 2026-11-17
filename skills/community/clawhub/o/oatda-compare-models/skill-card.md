## Description:

OATDA Compare Models sends one prompt to multiple LLM providers through OATDA's unified AI gateway and returns side-by-side model outputs with token usage and cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devcsde](https://clawhub.ai/user/devcsde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to benchmark multiple LLMs on the same prompt, compare answer quality, and review cost and token usage across providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented shell pattern can let arbitrary prompt text affect shell syntax when prompts are copied from untrusted sources.

Mitigation: Build request JSON with structured escaping, such as jq --arg, or use a scoped HTTP client instead of interpolating prompts directly into shell commands.

Risk: Model-comparison requests can include secrets, personal data, proprietary documents, or credentials in prompts.

Mitigation: Send sensitive information only when disclosure through the model-comparison request is intended and approved.

## Reference(s):

- [OATDA Homepage](https://oatda.com)
- [OATDA Compare API](https://oatda.com/api/v1/compare)
- [OATDA API Keys](https://oatda.com/dashboard/api-keys)
- [OATDA Credits Dashboard](https://oatda.com/dashboard/credits)
- [OATDA Compare Models ClawHub Release](https://clawhub.ai/devcsde/skills/oatda-compare-models)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OATDA_API_KEY; comparison requests may include up to 8 models and can return batch JSON or SSE stream results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
