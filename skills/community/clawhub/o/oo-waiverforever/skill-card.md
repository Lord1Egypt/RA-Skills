## Description:

Use WaiverForever through a connected account to read, create, and update waiver data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to find account information, list templates, search and retrieve waivers, and create waiver requests or signing links through a connected WaiverForever account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs downloaded code and may make broader changes to other agent skills.

Mitigation: Review and install the CLI separately, and inspect any proposed changes to other skills before enabling the integration.

Risk: Write actions can create signing links or waiver request groups in the connected account.

Mitigation: Confirm the exact payload and effect with the user before running a write action.

## Reference(s):

- [WaiverForever API documentation](https://docs.waiverforever.com/)
- [WaiverForever](https://www.waiverforever.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Text]

**Output Format:** [Shell commands with JSON inputs and JSON or text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the connected WaiverForever account; write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
