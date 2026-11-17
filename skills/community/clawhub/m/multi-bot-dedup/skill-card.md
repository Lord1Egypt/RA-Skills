## Description:

Deduplicates Feishu multi-bot replies so the same user message receives only one AI response across multiple bot channels within the configured window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottrao635-svg](https://clawhub.ai/user/scottrao635-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill in OpenClaw Feishu deployments where one user message can arrive through multiple bot channels. It guides the agent to reply once, update local deduplication state, or intentionally return NO_REPLY for a duplicate message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores small local per-sender deduplication records.

Mitigation: Install it only in Feishu/OpenClaw multi-bot setups that need this behavior, and keep deduplication state limited to sender, timing, and message-hash records.

Risk: Near-duplicate replies may be intentionally skipped during the 30-second window.

Mitigation: Honor the documented exceptions for new topics, messages after the time window, and explicit repeat requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottrao635-svg/skills/multi-bot-dedup)

## Skill Output:

**Output Type(s):** [guidance, configuration, text]

**Output Format:** [Markdown behavioral guidance with JSON state records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a 30-second deduplication window and a hash of the first 50 characters; may advise NO_REPLY for duplicate messages.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
