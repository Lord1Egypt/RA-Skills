## Description:

Detect prompt injection attacks and adversarial inputs in user text before passing it to your LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aunicall](https://clawhub.ai/user/aunicall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to inspect single or batched user-provided text for prompt injection, jailbreak attempts, instruction overrides, and related adversarial inputs before forwarding content to an LLM-backed application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted prompts and batch inputs may be sent to a configurable remote Prompt Inspector endpoint.

Mitigation: Use the skill only for text you are allowed to send to Prompt Inspector or a trusted self-hosted service, and use HTTPS endpoints only.

Risk: API keys can be supplied on the command line or through environment-backed configuration.

Mitigation: Prefer the PMTINSP_API_KEY environment variable over inline --api-key usage and rotate keys if they may have been exposed.

Risk: JSON results and progress output can include submitted text, verdicts, categories, request IDs, and related operational details.

Mitigation: Treat generated JSON and logs as potentially sensitive and avoid batch files containing secrets or regulated data.

## Reference(s):

- [Prompt Inspector product information](references/product-info.md)
- [Prompt Inspector usage guide](references/usage.md)
- [Prompt Inspector FAQ](references/faq.md)
- [Prompt Inspector website](https://promptinspector.io)
- [Prompt Inspector API documentation](https://docs.promptinspector.io)
- [ClawHub skill page](https://clawhub.ai/aunicall/skills/prompt-inspector)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, Guidance]

**Output Format:** [Human-readable text or JSON containing request ID, safety verdict, risk score, threat categories, and latency]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-text and line-delimited batch inspection through Python or Node.js helper scripts.]

## Skill Version(s):

0.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
