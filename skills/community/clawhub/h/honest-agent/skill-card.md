## Description:

Honest Agent guides an assistant to track commitments, run pre-response honesty checks, label media and file analysis sources, and keep local audit logs for accountability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[141553](https://clawhub.ai/user/141553)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make an agent explicitly track promises, avoid unsupported claims, and disclose uncertainty when handling text, files, images, or audio. It is intended for accountability workflows where persistent local commitment and honesty logs are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently records conversation-derived commitments and honesty logs across conversations.

Mitigation: Confirm who can access memory/honest-agent/, define a deletion process, and avoid recording sensitive content unless persistence is intended.

Risk: Broad automatic triggers may record commitments or logs when the user did not explicitly request tracking.

Mitigation: Consider limiting use to explicit commands or reviewing pending entries before retaining them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/141553/skills/honest-agent)
- [Publisher profile](https://clawhub.ai/user/141553)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Files]

**Output Format:** [Markdown guidance with local JSON record updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update honest-commitments.json and honest-logs.json under memory/honest-agent/.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
