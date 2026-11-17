## Description:

WhatsApp bridge for OpenClaw - send/receive messages, auto-reply agents, QR pairing, message search, contact sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xs4m1337](https://clawhub.ai/user/0xs4m1337)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect OpenClaw agents to WhatsApp for message sending, incoming DM auto-replies, chat history search, and contact synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says setup installs unverified remote code and binary artifacts.

Mitigation: Review and verify the upstream installer and binary before installation.

Risk: The release security summary says the skill runs persistently and allows private WhatsApp messages to drive a capable agent.

Mitigation: Use a dedicated least-privileged OpenClaw agent, restrict replies with an allowlist, and confirm service removal steps before linking a real WhatsApp account.

Risk: The release security guidance warns against shared temporary storage for queues and logs.

Mitigation: Place queue and log data in a private directory and tighten file permissions.

## Reference(s):

- [OpenClaw WhatsApp API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/0xs4m1337/skills/openclaw-whatsapp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, YAML configuration, API examples, and operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operating instructions for a local WhatsApp bridge and OpenClaw auto-reply workflow.]

## Skill Version(s):

0.3.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
