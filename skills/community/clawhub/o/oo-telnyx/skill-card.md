## Description:

Telnyx (telnyx.com). Use this skill for ANY Telnyx request — reading, creating, and updating data. Whenever a task involves Telnyx, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to read Telnyx messaging profiles and messages, and to send SMS or MMS messages through their connected Telnyx account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs an unverified remote installer without a separate approval step; the remote installer and hosted connector implementation remain unverified.

Mitigation: Review the CLI installation before enabling the skill. Prefer a verified, pinned installation under your control, and check whether it installs or updates other agent skills.

Risk: The connected service intermediary handles credentials and requests.

Mitigation: Approve OOMOL as the intermediary and confirm message recipients and content before sending.

## Reference(s):

- [Telnyx website](https://telnyx.com/)
- [Telnyx API documentation](https://developers.telnyx.com/api-reference/overview)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses with concise guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that send messages require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
