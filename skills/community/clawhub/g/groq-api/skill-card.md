## Description:

Build and debug Groq API chat and speech workflows with low-latency routing, structured outputs, and production-safe patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build, route, and troubleshoot Groq API chat, tool-calling, structured-output, and speech transcription workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation preferences stored in global agent memory may affect later sessions beyond the local Groq workflow.

Mitigation: Review the memory behavior before installing and prefer explicit invocation or local-only memory under ~/groq-api/ unless broad persistent activation is intended.

Risk: Prompts and audio are sent to Groq endpoints for inference and transcription.

Mitigation: Use the skill only for content the user is comfortable sending to Groq, and avoid persisting sensitive prompts in local logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/groq-api)
- [Groq API base URL](https://api.groq.com/openai/v1)
- [Groq models endpoint](https://api.groq.com/openai/v1/models)
- [Groq chat completions endpoint](https://api.groq.com/openai/v1/chat/completions)
- [Groq audio transcriptions endpoint](https://api.groq.com/openai/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON request examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GROQ_API_KEY from the environment and curl/jq examples for Groq API requests.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
