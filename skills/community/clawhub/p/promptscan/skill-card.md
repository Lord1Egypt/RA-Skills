## Description:

Scan untrusted agent instructions, code, or tool output for prompt injection using promptscan. Use when asked to check incoming content before an agent acts on it; not for general code review or model training.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xdewy](https://clawhub.ai/user/0xdewy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check untrusted instructions, files, pull request changes, code, or tool output for prompt injection before acting on that content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Promptscan can miss prompt injection, and a SAFE result could be mistaken for approval to act on the scanned content.

Mitigation: Treat scan results as advisory; check coverage, model identity, and threshold, then review untrusted content in context before acting.

## Reference(s):

- [Server-resolved source repository path](https://github.com/0xdewy/promptscan/tree/master/skills/promptscan)
- [promptscan on ClawHub](https://clawhub.ai/0xdewy/skills/promptscan)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [JSON scan results with concise Markdown analysis and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Check scan coverage, findings, model identity, and threshold; interpret results in context.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
