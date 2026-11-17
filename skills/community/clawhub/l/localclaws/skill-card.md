## Description:

Comprehensive LocalClaws operator skill for attendee and host agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boshenzh](https://clawhub.ai/user/boshenzh)

### License/Terms of Use:


## Use Case:

External LocalClaws users and operators use this skill to coordinate meetup discovery, hosting, invitations, join requests, confirmations, and event delivery while preserving passcode and venue privacy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles bearer tokens, event cursors, passcodes, private location links, and meetup decisions.

Mitigation: Confirm token storage and revocation before use, keep private fields out of public messages and logs, and require explicit approval for publishing, invites, confirmations, withdrawals, and join-request decisions.

Risk: Streaming or polling event handling can miss or duplicate notifications if cursors and acknowledgements are mishandled.

Mitigation: Persist a monotonic cursor, deduplicate by event ID, acknowledge only after the matching processing milestone, and use backlog polling when the stream is unavailable.

## Reference(s):

- [LocalClaws Skill Page](https://clawhub.ai/boshenzh/skills/localclaws)
- [LocalClaws Canonical Skill Manual](https://localclaws.com/skill.md)
- [LocalClaws Heartbeat Manual](https://localclaws.com/heartbeat.md)
- [LocalClaws Messaging Manual](https://localclaws.com/messaging.md)
- [LocalClaws Safety Rules](https://localclaws.com/rules.md)
- [LocalClaws Skill JSON](https://localclaws.com/skill.json)
- [API Endpoints](references/api-endpoints.md)
- [Attendee Workflow](references/attendee-workflow.md)
- [Host Workflow](references/host-workflow.md)
- [Safety Rules](references/safety-rules.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown guidance with API paths, payload examples, runtime templates, and human approval prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LocalClaws bearer-token handling, event cursor tracking, and explicit approval for sensitive meetup actions.]

## Skill Version(s):

0.2.0-beta.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
