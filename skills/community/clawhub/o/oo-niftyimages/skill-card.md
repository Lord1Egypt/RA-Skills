## Description:

Use a connected NiftyImages account to search and read image, widget, user, and usage data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and NiftyImages account operators use this skill to retrieve images, widgets, users, and account statistics. It guides the agent to check an action's live input schema before making a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation may execute unverified downloaded code and add other skills to the agent.

Mitigation: Inspect the installer before use, install a fixed CLI version, and disable automatic skill synchronization if only this integration is wanted.

Risk: Connecting NiftyImages authorizes OOMOL to mediate account access, while the hosted connector implementation was not supplied for review.

Mitigation: Review the requested access before connecting and use the integration only if you are comfortable with OOMOL mediating that account access.

## Reference(s):

- [NiftyImages](https://niftyimages.com/)
- [NiftyImages API documentation](https://api.niftyimages.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions with oo CLI commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
