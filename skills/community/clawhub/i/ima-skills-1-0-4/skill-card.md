## Description:

Provides agent guidance for managing IMA personal notes through the IMA OpenAPI, including searching notes, browsing notebooks, reading note content, creating notes, and appending content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzswk](https://clawhub.ai/user/yzswk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent search, read, create, and append content in their authenticated IMA personal notes. It is intended for personal note and knowledge-base workflows that require IMA OpenAPI credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent receives authenticated access to private IMA notes and can read note content.

Mitigation: Use credentials only when needed, scope access where possible, and avoid displaying note bodies in shared or group contexts.

Risk: Create and append operations can permanently modify personal notes.

Mitigation: Manually confirm the target note or folder and the exact content before any write operation.

Risk: Persisting API credentials in shell startup files can increase exposure if the environment is shared or compromised.

Mitigation: Prefer a secret manager or temporary environment injection for IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY.

## Reference(s):

- [IMA Notes API Reference](references/api.md)
- [IMA](https://ima.qq.com)
- [IMA Agent Interface](https://ima.qq.com/agent-interface)
- [ClawHub Skill Page](https://clawhub.ai/yzswk/skills/ima-skills-1-0-4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY environment variables for authenticated IMA OpenAPI requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
