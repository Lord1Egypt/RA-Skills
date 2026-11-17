## Description:

Wbiztool (wbiztool.com). Use this skill for ANY Wbiztool request — reading, creating, updating, and deleting data. Whenever a task involves Wbiztool, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to check WhatsApp message status and to send, schedule, or cancel messages through a connected Wbiztool account. It requires confirmation before sending, scheduling, or canceling messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can run downloaded software without separate approval or integrity checks, and the installer contents are unverified.

Mitigation: Prefer a separately reviewed CLI installation; get explicit approval for local changes, including any additional agent skills it installs.

Risk: Connecting Wbiztool authorizes OOMOL to handle account credentials and messaging requests.

Mitigation: Preserve the skill's required confirmations before sending, scheduling, or canceling messages.

## Reference(s):

- [Wbiztool skill page](https://clawhub.ai/oomol/skills/oo-wbiztool)
- [Wbiztool homepage](https://wbiztool.com/)
- [Wbiztool API documentation](https://wbiztool.com/docs/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON action responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch the live action schema before building payloads; confirm before write or destructive actions.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
