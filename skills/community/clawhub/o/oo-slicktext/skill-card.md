## Description:

Operate SlickText through a connected OOMOL account to read, create, update, and delete contact data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a SlickText brand use the skill to retrieve and manage contacts through their connected OOMOL account. It supports contact reads and user-approved create, update, and delete actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run an unverified CLI installer and may introduce broader agent changes without separate approval.

Mitigation: Review the CLI release and verify its integrity before installation; check its automatic skill installation and update behavior before running it.

Risk: Contact creation, updates, and deletion change SlickText data.

Mitigation: Confirm the exact action and payload with the user before writes, and obtain explicit approval for deletions.

## Reference(s):

- [SlickText API documentation](https://api.slicktext.com/docs/v2/overview)
- [SlickText](https://www.slicktext.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with shell command examples and JSON payloads or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read contact data or propose contact changes; write and destructive actions require user approval.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
