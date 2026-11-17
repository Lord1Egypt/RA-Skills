## Description:

Offloads suitable agent tasks to local LM Studio models for summarization, extraction, classification, rewriting, first-pass review, and brainstorming while reducing paid API usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t-sinclair2500](https://clawhub.ai/user/t-sinclair2500)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to discover local LM Studio models, select a model by task needs, and run suitable work through the LM Studio REST API. It is useful for reducing paid API usage and keeping selected processing local when model quality is sufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected task text can be sent to a configurable LM Studio API endpoint.

Mitigation: Keep the API URL on localhost unless the user intentionally trusts a remote server, and avoid secrets or regulated data without a clear policy.

Risk: Optional request and response logging can persist sensitive prompts or outputs.

Mitigation: Do not enable logging for sensitive prompts, and review any log path before retaining or sharing generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/t-sinclair2500/skills/lm-studio-subagents)
- [LM Studio](https://lmstudio.ai)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model output text, model_instance_id, response_id, token usage, and optional request or response logs.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
