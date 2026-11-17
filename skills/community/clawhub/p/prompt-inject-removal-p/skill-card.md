## Description:

A prompt-only sanitization skill that summarizes untrusted external content while removing or marking obvious prompt injection attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to process untrusted web pages, articles, blogs, emails, or files into concise sanitized summaries before the information is used in a conversation or workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt-based sanitization is not a complete security boundary for sophisticated prompt injection.

Mitigation: Use narrow fetch or browser permissions where possible, isolate the sanitization step for high-risk content, and review summaries before taking write, send, or delete actions.

Risk: A sanitized summary can still carry malicious, misleading, or action-triggering content into the main agent.

Mitigation: Treat summaries from untrusted sources as reviewable data and avoid state-changing actions based only on the sanitized output.

Risk: The artifact includes defensive examples of prompt-injection phrases that scanners may flag.

Mitigation: Review scanner findings in context and confirm that flagged phrases are negative constraints rather than executable instructions.

## Reference(s):

- [Prompt Inject Removal security documentation](references/security.md)
- [Hardened sanitization prompt](PROMPT.md)
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/prompt-inject-removal-p)
- [Metadata homepage](https://clawhub.ai/Quarantiine/prompt-inject-removal)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise sanitized summary text, optionally containing the marker [INJECTION_ATTEMPT_REMOVED]]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external API keys are required; output should omit conversational prefaces and conclusions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
