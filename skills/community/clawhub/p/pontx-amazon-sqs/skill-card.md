## Description:

Integrate Amazon SQS safely through Pontx for queue discovery, SDK or CLI setup, consumer reliability decisions, FIFO or standard queue choices, visibility timeouts, DLQs, polling, and explicitly approved queue mutations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Amazon SQS through Pontx, inspect queue topology, generate SDK or CLI guidance, and design reliable producers and consumers. It is also used to preview queue-changing operations and require explicit approval before direct calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queue-changing Amazon SQS actions can affect production state if the wrong account, region, queue, message, or action is approved.

Mitigation: Use a redacted preview for the exact unchanged input, require explicit approval, and discard the confirmation token if any material input changes.

Risk: AWS credentials, message bodies, receipt handles, and confirmation tokens may expose sensitive operational data if included in source, logs, shell history, diagnostics, or chat.

Mitigation: Configure caller-owned credentials and region outside source and chat, and redact sensitive message and token details from examples and diagnostics.

Risk: Incorrect SQS consumer semantics can cause duplicate processing, lost ordering assumptions, repeated retries, or unresolved poison messages.

Mitigation: Choose standard or FIFO semantics deliberately, make processing idempotent where required, tune visibility timeouts, delete only after durable success, and use a dead-letter queue with a redrive policy.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/pontjs/skills/pontx-amazon-sqs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and code guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted previews, explicit approval prompts, and reliability guidance for Amazon SQS operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
