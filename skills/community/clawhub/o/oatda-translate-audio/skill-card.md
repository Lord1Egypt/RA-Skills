## Description:

Translate foreign-language audio into English text using OATDA's unified audio API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devcsde](https://clawhub.ai/user/devcsde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to translate uploaded or local foreign-language audio recordings into English text through OATDA's audio translation endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio recordings are uploaded to OATDA for processing, which may expose sensitive recording content to an external service.

Mitigation: Use the skill only for recordings the user intends to send to OATDA, and avoid sensitive audio unless that external upload is acceptable.

Risk: The skill requires an OATDA API key from the environment or credentials file.

Mitigation: Store the API key in OATDA_API_KEY or ~/.oatda/credentials.json and avoid printing the full key in outputs or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devcsde/skills/oatda-translate-audio)
- [OATDA](https://oatda.com)
- [OATDA audio models endpoint](https://oatda.com/api/v1/llm/models?type=audio)
- [OATDA translations endpoint](https://oatda.com/api/v1/llm/translations)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [English translation text returned from OATDA, with optional JSON, text, SRT, verbose JSON, or VTT response formats.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
