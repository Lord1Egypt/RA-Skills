## Description:

Webex (webex.com). Use this skill for ANY Webex request — reading, creating, updating, and deleting data. Whenever a task involves Webex, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read and manage Webex meetings, people, rooms, teams, memberships, messages, recordings, and transcripts through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can execute downloaded installer code without a separate approval step.

Mitigation: Verify the oo CLI release and installer separately, check automatic skill-installation settings, and explicitly approve local changes.

Risk: The connected account may expose Webex data, and write or delete actions can change or remove it.

Mitigation: Review the account connection and data access, confirm exact write payloads, and get explicit approval before destructive actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Webex API documentation](https://developer.webex.com/docs/getting-started)
- [Webex](https://www.webex.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Text or Markdown summaries, JSON action data, and VTT or plain-text meeting transcripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the selected Webex action.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
