## Description:

Linguapop (linguapop.eu). Use this skill for ANY Linguapop request — reading, creating, and updating data. Whenever a task involves Linguapop, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to look up available Linguapop placement-test languages and create candidate invitations. It can also send invitation emails and configure kiosk codes or callback and return URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute downloaded CLI code, and the installer has not been inspected.

Mitigation: Review and approve the CLI installation separately; prefer a pinned release with verified integrity.

Risk: OOMOL mediates Linguapop requests and connected credentials.

Mitigation: Use the connected account only for intended Linguapop tasks and review the requested action details before running it.

Risk: Invitations can email candidates and can configure callback or return destinations.

Mitigation: Confirm candidate details, email delivery, and callback destinations before sending an invitation.

## Reference(s):

- [Linguapop](https://www.linguapop.eu/)
- [Linguapop API documentation](https://docs.linguapop.eu/api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-linguapop)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Connector action results as JSON, with shell commands and JSON payloads for actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read available languages or create placement-test invitations, optionally sending email or setting kiosk and callback details.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
