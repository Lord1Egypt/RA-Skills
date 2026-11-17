## Description:

Prevent accidental participant pings and endless groupchat loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chizumystic](https://clawhub.ai/user/chizumystic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to host bounded multi-agent group chats, manage participants, and synthesize participant replies into a single user-facing response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Group-chat messages may be relayed to named participant agents.

Mitigation: Use explicit participant commands, check the participant list when needed, and end the chat when forwarding is no longer intended.

Risk: Participant agents may join or leave through the documented group-chat workflow.

Mitigation: Monitor participant changes and use add, remove, list, and end commands to keep the active participant set intentional.

Risk: Unbounded forwarding could create accidental participant pings or repeated group-chat loops.

Mitigation: Keep dispatch limited to explicit rounds, accept at most one reply per participant per round, and avoid forwarding synthesized replies back to participants.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or Markdown conversation responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May relay messages to named participant agents during explicit group-chat dispatch or join/leave commands.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
