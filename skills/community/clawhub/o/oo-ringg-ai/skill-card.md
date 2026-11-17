## Description:

Ringg AI (ringg.ai). Use this skill for ANY Ringg AI request — reading, creating, and updating data. Whenever a task involves Ringg AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to inspect Ringg AI workspaces, assistants, calls, voices, and caller numbers, and to initiate outbound calls through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may run downloaded code that was unavailable for inspection, and automatic skill synchronization may introduce broader agent changes.

Mitigation: Review and approve installation separately, use a vetted fixed release, and check automatic synchronization before use. OO_SKILLS_SYNC_DISABLED can disable startup synchronization.

Risk: Initiating an outbound call can contact an unintended person or use unintended call details.

Mitigation: Connect only the intended Ringg AI account and confirm the outbound call details before initiating the call.

## Reference(s):

- [Ringg AI](https://www.ringg.ai)
- [Ringg AI API documentation](https://docs.ringg.ai/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON action payloads and text or JSON connector responses, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results and outbound call actions; actions that change state require user confirmation as described in the skill.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
