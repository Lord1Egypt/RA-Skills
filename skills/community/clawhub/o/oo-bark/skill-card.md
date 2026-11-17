## Description:

Bark (bark.day.app). Use this skill for ANY Bark request — reading, creating, and updating data. Whenever a task involves Bark, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Bark account can use this skill to read server information and send notifications through the oo CLI. It guides the agent to inspect each action's input schema and seek confirmation before sending notifications that change state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute an unverified remote CLI installer.

Mitigation: Review and approve CLI installation separately, prefer a verified fixed release, and check whether setup installs or updates other agent skills.

Risk: Bark requests are mediated through OOMOL and may contain notification content or use connected-account access.

Mitigation: Consider the notification content and the connected-account access entrusted to OOMOL.

## Reference(s):

- [Bark skill release](https://clawhub.ai/oomol/skills/oo-bark)
- [OOMOL publisher profile](https://clawhub.ai/user/oomol)
- [Bark homepage](https://bark.day.app)
- [Bark API documentation](https://github.com/Finb/bark-server/blob/master/docs/API_V2.md)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and JSON responses, plus concise action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an already installed and connected oo CLI; write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
