## Description:

This skill lets agents read, create, and update Novu data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read and update Novu subscriber data and trigger Novu workflows through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI installation instructions can run downloaded installation code.

Mitigation: Review and explicitly approve CLI installation separately; prefer a verified, fixed release.

Risk: The connected Novu account can be used to change subscribers and trigger notifications.

Mitigation: Limit the account's permissions and confirm subscriber changes and notification triggers.

## Reference(s):

- [Novu](https://novu.co)
- [Novu API documentation](https://docs.novu.co/api-reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Novu action results as JSON, with shell commands and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that create or update subscribers or trigger workflows can change Novu data or send notifications.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
