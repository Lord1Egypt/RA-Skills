## Description:

Track, analyze, and optimize LLM API spending across providers including OpenAI, Anthropic, Google, and DeepSeek.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to inspect LLM API spend, compare provider and model costs, set budget thresholds, and receive cost reduction guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect API spending data and use provider credentials from environment variables.

Mitigation: Run it only in environments where use of the configured provider API keys and billing or usage data is approved.

Risk: Budget settings and usage history may be retained in local OpenClaw files.

Mitigation: Review or delete ~/.openclaw/cost-tracker.json and ~/.openclaw/cost-data when local retention is not desired.

## Reference(s):

- [API Cost Optimization Guide](references/optimization-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, command examples, JSON configuration snippets, and plain-text recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use provider API keys from environment variables and local usage history to generate summaries.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
