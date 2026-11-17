## Description:

Privacy pipeline for OpenClaw that uses Ollama to scrub names, emails, file paths, IP addresses, and related PII before external model calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solmas](https://clawhub.ai/user/solmas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to anonymize memory, workspace, and tool-call text before sending prompts or snippets to external LLM services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw sensitive text can be sent to a configurable Ollama endpoint without destination or transport controls.

Mitigation: Install only when the Ollama endpoint is controlled, and keep OLLAMA_URL on localhost or a trusted encrypted endpoint.

Risk: Secrets or malformed input may be exposed until JSON request construction is fixed with a serializer.

Mitigation: Avoid feeding secrets to the skill until JSON construction uses a serializer such as jq.

Risk: Automatic processing of memory or workspace content can broaden exposure if enabled without review.

Mitigation: Use caution with cron or HEARTBEAT-style processing, limit the processed scope, and review what content is sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solmas/skills/openclaw-pii-anonymizer-latest)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text anonymized output with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input is capped at 10000 characters by privacy-anonymize.sh.]

## Skill Version(s):

1.0.2 (source: server release metadata and script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
