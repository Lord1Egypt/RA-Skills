## Description:

Reply once per round and never create participant loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chizumystic](https://clawhub.ai/user/chizumystic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of host-mediated multi-agent chats use this skill to let participant agents join, leave, check status, and reply once per forwarded group-chat round without contacting the user directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may self-join or leave a group chat in contexts where participant control matters.

Mitigation: Require explicit host or user approval for join and leave actions in sensitive chats.

Risk: Group-chat participation can expose forwarded conversation context to an additional agent.

Mitigation: Install only for host-mediated group chats where the added participant is intended to receive the forwarded context.

Risk: Duplicate replies or participant-to-participant messages can create noisy loops.

Mitigation: Enforce one reply per round, send replies only to the host, and ignore rounds already answered.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chizumystic/skills/groupchat-participant)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Concise text responses, host-directed chat commands, and optional JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Participant replies are limited to one response per group-chat round; join, leave, and status commands are sent only to the host.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
