## Description:

liuyao-xueer opens a Chinese-style Liuyao divination page where users enter a question, cast six yao lines, and receive either an offline reading or a streamed LLM interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clara-wang-2023](https://clawhub.ai/user/clara-wang-2023)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to run a browser-based Liuyao divination flow for personal questions, with optional API-backed model interpretation and an offline fallback reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the user's question and API key to a configured model endpoint.

Mitigation: Use only low-privilege disposable API keys with spending limits, avoid sensitive personal questions, and configure only trusted endpoints.

Risk: The authoritative security scan reports an injection issue that could expose secrets.

Mitigation: Prefer offline mode until user input is sanitized and the page adds clear consent and endpoint validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clara-wang-2023/skills/liuyao-xueer)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration]

**Output Format:** [Browser UI text with optional streamed model response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can operate offline with a basic reading; optional model configuration accepts an API key, endpoint, and model name.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
