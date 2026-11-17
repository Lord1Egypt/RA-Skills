## Description:

Superchat (superchat.com). Use this skill for ANY Superchat request — reading, creating, and updating data. Whenever a task involves Superchat, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Superchat users use this skill to inspect channels and contacts, search contacts, create or update contacts, and send email, text, or WhatsApp template messages through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run an unverified remote CLI installer that may automatically install and synchronize agent skills.

Mitigation: Review and approve CLI installation separately, including automatic skill installation and synchronization; prefer a pinned, verified release.

Risk: Sending messages and changing contacts can affect external users or workspace data.

Mitigation: Retain confirmation before messages or contact changes, and confirm the exact payload and effect before write actions.

## Reference(s):

- [oo CLI Repository](https://github.com/oomol-lab/oo-cli)
- [Superchat](https://www.superchat.com)
- [Superchat API Documentation](https://developers.superchat.com/docs/getting-started-send-your-first-message)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text]

**Output Format:** [oo CLI commands with JSON payloads and responses, followed by natural-language results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas are checked before calls; write actions require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
