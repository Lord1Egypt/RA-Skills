## Description:

Privacy pipeline for OpenClaw that uses regexes and a local Qwen2.5 LLM through Ollama to replace common PII in text with placeholder tokens before external AI processing.

This skill is for research and development only.

## Publisher:

[solmas](https://clawhub.ai/user/solmas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using OpenClaw use this skill to manually anonymize prompts or workflow inputs by replacing common PII patterns and likely person names before sending text to external AI services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive text can be sent to a configurable HTTP model endpoint.

Mitigation: Keep OLLAMA_URL pinned to a trusted local Ollama instance and avoid untrusted remote endpoints.

Risk: The skill may return only partially scrubbed data while appearing anonymized.

Mitigation: Manually review anonymized output before forwarding it to external APIs, especially for regulated or customer PII.

Risk: The deprecated v1 script should not be relied on for current workflows.

Mitigation: Use privacy-anonymize-v2.sh for controlled manual workflows and avoid privacy-anonymize.sh.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solmas/skills/openclaw-pii-anonymizer)
- [Publisher profile](https://clawhub.ai/user/solmas)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text with placeholder tokens, plus Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a single text input up to 10000 characters; may fall back to regex-only output if the local Ollama endpoint is unavailable.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
