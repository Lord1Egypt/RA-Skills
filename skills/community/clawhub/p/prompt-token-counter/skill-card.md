## Description:

Count tokens and estimate costs for 300+ LLM models. Primary use: audit OpenClaw workspace token consumption (memory, persona, skills).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobudaoyuema](https://clawhub.ai/user/zhaobudaoyuema)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to count prompt tokens, estimate model API costs, compare token usage across models, and audit OpenClaw workspace files that contribute to context size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can fetch arbitrary HTTP or HTTPS URLs when URL input is used.

Mitigation: Prefer local files or inline text; use URL input only after confirming the URL is trusted and appropriate to fetch.

Risk: API-mode benchmarking can send prompt text to an external model provider.

Mitigation: Use local benchmarking for private content, and run API-mode benchmarks only with text that is approved for the configured provider.

Risk: Workspace audits may read memory, persona, and skill files that contain sensitive information.

Mitigation: Review files before counting them and avoid cost or benchmark workflows that transmit private workspace content externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobudaoyuema/skills/prompt-token-counter)
- [Project repository listed by artifact metadata](https://github.com/Zhaobudaoyuema/prompt-token-counter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown with optional shell commands and tabular summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs token counts and optional cost estimates; OpenAI token counts use tiktoken when installed, while other model counts are formula-based approximations.]

## Skill Version(s):

1.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
