## Description:

OnceHub (oncehub.com). Use this skill for ANY OnceHub request — searching and reading data. Whenever a task involves OnceHub, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using OnceHub through an OOMOL-connected account can ask an agent to find and read booking pages, bookings, and event types. The agent inspects each action's input schema before making a read request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded software without a clear approval or verification step.

Mitigation: Manually install a verified, pinned CLI release, review the setup and automatic skill-synchronization controls, and explicitly approve local changes.

Risk: OOMOL mediates access to the connected OnceHub account.

Mitigation: Connect only the OnceHub account and permissions needed for the requested work.

## Reference(s):

- [OnceHub](https://www.oncehub.com/)
- [OnceHub API documentation](https://developers.oncehub.com/docs/overview/authentication)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [OnceHub records returned as JSON and summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only actions are documented; setup and authentication guidance is included.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
