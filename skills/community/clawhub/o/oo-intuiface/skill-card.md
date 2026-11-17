## Description:

Use Intuiface through a connected OOMOL account to find running experiences and send Web Trigger messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Intuiface users use this skill to list running experiences and send Web Trigger messages through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute downloaded CLI installer code whose exact behavior has not been verified.

Mitigation: Review setup first, prefer a verified fixed CLI release, and explicitly approve installation changes.

Risk: Automatic skill synchronization may change skills installed for other agents.

Mitigation: Disable automatic synchronization with OO_SKILLS_SYNC_DISABLED=1 if it is not intended, and review synchronization changes.

Risk: Sending a Web Trigger message changes state in selected running Intuiface experiences.

Mitigation: Connect only the intended Intuiface account and confirm the exact message payload and effect before sending.

## Reference(s):

- [Intuiface Web Triggers API documentation](https://support.intuiface.com/hc/en-us/articles/360007180132-Using-the-Web-Triggers-API)
- [Intuiface homepage](https://www.intuiface.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-intuiface)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Intuiface account and the live action schema.]

## Skill Version(s):

1.0.4 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
