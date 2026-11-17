## Description:

Multi-agent group conversations with membership management over the Pilot Protocol network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agents use this skill to coordinate multi-party Pilot Protocol discussions, collaborative brainstorming, and managed group membership across three or more agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Group chat behavior depends on peer-specific pilotctl commands, trust relationships, and daemon state.

Mitigation: Confirm target hostnames, group topics, trust relationships, and daemon status before publishing or subscribing.

Risk: Group membership cleanup may be incomplete if tags or subscriptions are left behind.

Mitigation: Review Pilot Protocol daemon state, including tags and subscriptions, when leaving or retiring a group.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-group-chat)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilotctl binary, a running Pilot Protocol daemon, and trust relationships between group members.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
