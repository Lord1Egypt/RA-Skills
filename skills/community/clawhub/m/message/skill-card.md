## Description:

Communicate across channels without social disasters, with escalation rules, tone calibration, and platform-aware formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Employees, external users, and agents use this skill to draft or adapt messages across email, chat, and social platforms while preserving channel norms, recipient context, and human approval for high-stakes communications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to review recent message history to match tone and context.

Mitigation: Limit supplied conversation history to what is necessary for the current draft and avoid including unrelated sensitive content.

Risk: Using generated messages without review can create unintended commitments or mishandle financial, legal, HR-sensitive, or public communications.

Mitigation: Keep explicit human approval for real sends and for any financial terms, legal matters, HR-sensitive topics, high-stakes relationships, or public posts.

Risk: A draft may use the wrong channel, timing, or platform formatting for the recipient and urgency.

Mitigation: Check the recipient, channel, urgency, local send time, and platform formatting before using a draft.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/message)
- [Escalation rules](artifact/escalation.md)
- [Platform-specific formatting](artifact/platforms.md)
- [Tone and context matching](artifact/tone.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text guidance for drafted messages, escalation decisions, channel selection, and platform-aware formatting.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend human review before sending high-stakes, legal, financial, HR-sensitive, or public communications.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
