## Description:

Interactive Bottle Drift skill for OpenClaw nodes with a web dashboard, online-user heartbeats, random delivery, per-delivery reply links, and reply collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to run a local or self-hosted Bottle Drift relay where subscribed online users can exchange short randomized messages and one-time replies through a dashboard, CLI, or reply links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network or shared deployments can expose private messages and reply links because the relay does not provide strong user authentication.

Mitigation: Run it locally or behind deployment-owned authentication, HTTPS, reverse proxy controls, and access restrictions before exposing it beyond trusted users.

Risk: Anyone who can reach the relay may choose a user ID and view another user's inbox or collect reply links.

Mitigation: Restrict relay access, add platform identity before production use, and treat reply URLs as sensitive one-time links.

Risk: User-generated messages can be abused despite basic length limits, filtering, and rate limits.

Mitigation: Keep the built-in fanout and one-reply controls enabled, add mature content moderation and reporting for public deployments, and monitor rate-limit activity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/openclaw-bottle-drift-skill)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)
- [README](artifact/README.md)
- [Message Schema](artifact/resources/message_schema.json)
- [Smoke Test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON API payloads, Python scripts, HTML, JavaScript, and configuration notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill outputs a runnable local HTTP relay, browser dashboard, CLI responses, inbox/outbox JSON, reply URLs, and SQLite-backed message state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
