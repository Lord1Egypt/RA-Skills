## Description:

List available AI models from OATDA's providers with optional filtering by type (chat, image, video) or provider name, including supported parameters for image and video models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devcsde](https://clawhub.ai/user/devcsde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to list OATDA model availability, filter models by type or provider, and inspect supported parameters before calling related OATDA generation or completion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads an OATDA API key from the environment or ~/.oatda/credentials.json to authorize API requests.

Mitigation: Use it only in environments where OATDA access is intended, keep the API key scoped appropriately, and do not print the full key in agent output.

Risk: Model availability and supported parameters are specific to OATDA and may not reflect other providers' direct APIs.

Mitigation: Use returned model data as OATDA-specific availability guidance and verify provider-specific requirements before using models outside OATDA.

## Reference(s):

- [OATDA Homepage](https://oatda.com)
- [OATDA Models API](https://oatda.com/api/v1/llm/models)
- [ClawHub Skill Page](https://clawhub.ai/devcsde/skills/oatda-list-models)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration instructions]

**Output Format:** [Markdown with inline bash commands and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GET requests to OATDA and may return model IDs, provider names, display names, and supported_params from the API response.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
