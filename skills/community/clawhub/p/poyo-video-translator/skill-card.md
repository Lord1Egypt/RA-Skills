## Description:

Video Translator on PoYo / poyo.ai helps agents prepare and submit asynchronous PoYo video translation jobs, then explain status polling, callbacks, and subtitle output handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user has chosen PoYo Video Translator and needs help preparing payloads, curl commands, server-side integration notes, async status polling, webhook handling, or response parsing for video speech translation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys could be exposed if placed in browser code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid echoing authorization headers or secrets.

Risk: Video URLs, callback URLs, task IDs, subtitles, or generated output URLs may contain private or policy-sensitive data.

Mitigation: Review payloads before submission and avoid logging or sharing private media data unless the PoYo account and data policy allow it.

Risk: Submitting a payload sends media references to the external PoYo service.

Mitigation: Make live API calls only when the user explicitly requests submission, confirms the payload, and provides a safe server-side environment.

## Reference(s):

- [PoYo Video Translator model page](https://poyo.ai/models/video-translator)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [PoYo Video Translator API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and bash curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model id, media URL summary, language choices, payload details, returned task_id, and next-step guidance for polling or webhook handling.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
