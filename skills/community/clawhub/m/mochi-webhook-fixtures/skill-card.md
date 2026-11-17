## Description:

Deduplicate selected webhook events by event ID and export replay fixtures without sending network requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers use the skill to deduplicate selected webhook events and create local replay fixtures for review or testing. It does not deliver events to a live service or provide production idempotency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook payloads may contain secrets or personal information, and exported fixtures remain on disk until removed.

Mitigation: Remove sensitive data before sharing fixtures, restrict access to exports, and delete them when no longer needed.

Risk: A local fixture export could be mistaken for production idempotency or live event delivery.

Mitigation: Treat outputs as test fixtures; use a separately authorized destination and replay strategy for live delivery.

## Reference(s):

- [Input contract](references/input.md)
- [中文用法](references/zh-CN.md)
- [MochiLab homepage](https://mochilab.bz)
- [ClawHub release](https://clawhub.ai/hznetnewpower/skills/mochi-webhook-fixtures)

## Skill Output:

**Output Type(s):** [Files, JSON, JSON Lines, Guidance]

**Output Format:** [JSON request and report, JSON Lines fixture file, and brief textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local fixture and report files in a new exports directory; does not send or replay events.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
