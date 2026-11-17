## Description:

OpenClaw Interaction Bridge connects OpenClaw agent state, approval requests, and notifications to external interaction surfaces such as the Snarling physical display and A/B buttons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snarflakes](https://clawhub.ai/user/snarflakes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this plugin to route agent activity, human approval requests, and notification feedback through a local external interface. It is suited for workflows where a person wants physical or out-of-band awareness and approval controls for agent actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Callback routes handle approval and notification feedback for agent workflows, and the release security summary flags weak callback security handling.

Mitigation: Use the plugin only with a trusted local Snarling service and do not expose callback routes beyond localhost unless transport authentication and session binding are fixed.

Risk: The approval secret protects callback requests and could be exposed through configuration mistakes or logs.

Mitigation: Set OPENCLAW_APPROVAL_SECRET explicitly, protect it as a credential, and restrict gateway logs and access to systems that need it.

Risk: Changing local endpoints to remote hosts increases the impact of spoofed callbacks or misrouted approval decisions.

Mitigation: Keep the default localhost endpoints for normal use; require authenticated transport and session binding before using remote callback or display targets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snarflakes/skills/openclaw-interaction-bridge)
- [Snarling Project](https://github.com/snarflakes/snarling)
- [Notification Policy](https://github.com/snarflakes/openclaw-interaction-bridge/blob/main/NOTIFICATION_POLICY.md)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Plain text tool results with structured callback feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Approval requests wait for an approve, reject, or timeout result; notifications can return reveal, dismiss, or timeout feedback when the external service responds.]

## Skill Version(s):

1.6.3 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
