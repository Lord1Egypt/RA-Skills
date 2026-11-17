## Description:

Use Mocean to read account data and manage SMS through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to check Mocean balances, delivery status, pricing, and number information, and to send SMS through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes remote CLI installers, and the CLI may install additional agent skills.

Mitigation: Review the CLI setup, use a verified and pinned release, and explicitly approve installation. For compatible versions, set OO_SKILLS_SYNC_DISABLED=1 before running oo.

Risk: Sending SMS can incur charges, and OOMOL processes submitted data.

Mitigation: Confirm the exact recipients, message text, and charges before sending, and account for OOMOL processing the submitted data.

## Reference(s):

- [Mocean API documentation](https://moceanapi.com/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Mocean](https://moceanapi.com)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON connector results and concise text or Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Mocean action and its live input schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
