## Description:

OpenClaw Bottle Drift provides an interactive message-in-a-bottle relay for OpenClaw nodes with a web console, online-user heartbeats, random delivery, dedicated reply links, and reply collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw node operators use this skill to run a lightweight HTTP and SQLite relay for exchanging short drift-bottle messages among online channel participants. It supports browser and CLI workflows for sending bottles, receiving bottles, and collecting one-time replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The relay can expose private messages and allow identity spoofing when reachable by other clients because it has no real authentication.

Mitigation: Install only for local testing or a trusted loopback-only environment until real authentication and authorization are added.

Risk: Reply tokens and callback URLs can be sensitive when exposed through inbox responses or public directory responses.

Mitigation: Treat reply URLs as sensitive, remove reply tokens from sender or general inbox responses before public deployment, and filter callback URLs from directory responses.

Risk: Public exposure can increase spam, abusive content, and message misuse beyond the skill's basic rate limits and word filter.

Mitigation: Use HTTPS, a reverse proxy, IP rate limits, and a mature moderation or reporting workflow before exposing the relay on a shared network or the public internet.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/openclaw-bottle-drift)
- [README](README.md)
- [Message Schema](resources/message_schema.json)
- [Smoke Test](tests/smoke-test.md)
- [Demo Session](examples/demo-session.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands, JSON payloads, and browser/CLI workflow descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and produces relay responses, inbox data, reply URLs, and web console views.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
