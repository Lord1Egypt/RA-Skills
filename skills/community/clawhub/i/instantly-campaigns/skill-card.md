## Description:

Run scalable cold email campaigns via Instantly.ai. Manage email accounts, build lead lists, create and activate multi-step outreach sequences, track analytics, and automate follow-ups with condition-based branching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External sales and marketing teams use this skill to operate Instantly cold email workflows from an agent, including account management, lead lists, campaign sequences, analytics, inbox placement, webhooks, and follow-up automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad credential-bearing Instantly tools include API-key administration and password-returning reads.

Mitigation: Verify the ClawLink plugin source and version, connect the least-privileged Instantly account available, and avoid API-key or password-returning tools unless they are explicitly needed.

Risk: Write and destructive operations can affect campaigns, leads, sequences, webhooks, account warmup, and workspace configuration.

Mitigation: Use read, list, search, get, and describe operations to reduce ambiguity, then preview and explicitly confirm the target resource and intended effect before execution.

Risk: Email sending, lead enrichment, data jobs, and inbox placement tests may incur cost or rate-limit impact under the connected Instantly plan.

Mitigation: Confirm plan limits and expected costs before bulk actions, and start with scoped checks or small batches before larger operations.

## Reference(s):

- [ClawHub Instantly Skill](https://clawhub.ai/hith3sh/skills/instantly-campaigns)
- [Instantly API Documentation](https://developer.instantly.ai/)
- [Instantly Warmup Guide](https://www.instantly.io/warmup)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands and ClawLink tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide read and write operations against a connected Instantly workspace; writes require preview and explicit confirmation.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
