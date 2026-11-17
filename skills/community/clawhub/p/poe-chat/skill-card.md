## Description:

Poe Chat helps an agent call Poe models selected from @keywords such as @gemini, @gpt, or @claude, report the concrete model used, and optionally attach local files for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longmans](https://clawhub.ai/user/longmans)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to route prompt requests to specific Poe-hosted models, list available model IDs, and send prompts with optional file attachments through Poe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and uploaded files are sent to Poe for model processing.

Mitigation: Do not upload sensitive documents unless necessary, and review any file paths passed with --file before execution.

Risk: Supplying the Poe API key on the command line can expose it through shell history or process metadata.

Mitigation: Prefer the POE_API_KEY environment variable over --api-key.

Risk: Unpinned Python dependencies may change behavior across installations.

Mitigation: Pin fastapi-poe and requests versions before production use.

## Reference(s):

- [Poe models API](https://api.poe.com/v1/models)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files]

**Output Format:** [Markdown guidance with shell commands, JSON model listings, and Poe response text prefixed by the model used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print returned attachment metadata when Poe responses include attachments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
