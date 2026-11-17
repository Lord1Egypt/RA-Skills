## Description:

Run email marketing campaigns via Kit (formerly ConvertKit). Manage subscribers, create broadcasts and sequences, handle tags and segments, track email stats, and automate workflows with webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to manage Kit email marketing through an agent, including subscribers, tags, broadcasts, sequences, forms, analytics, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on ClawLink for OAuth-backed access to the user's Kit account.

Mitigation: Install only after accepting the ClawLink trust boundary, review the ClawLink plugin and service, and revoke the Kit connection when it is no longer needed.

Risk: Write operations can change subscriber data, tags, broadcasts, forms, custom fields, account colors, and webhooks.

Mitigation: Preview and explicitly confirm the target resource and intended effect before executing any write operation.

Risk: Destructive or high-impact actions can unsubscribe subscribers, delete tags or broadcasts, or immediately send or schedule email campaigns.

Mitigation: Confirm destructive actions separately and verify broadcast timing, audience, and content before execution.

## Reference(s):

- [Kit API Documentation](https://api.kit.com/)
- [Kit Broadcasts Guide](https://kit.com/creators/broadcasts)
- [Kit Sequences Guide](https://kit.com/creators/sequences)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active Kit account and ClawLink connection; write actions require explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
