## Description:

Searches and reads Iru (Kandji) user and blueprint data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

IT administrators and operations teams use this skill to look up Kandji users and blueprints through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run an installer whose remote contents have not been verified.

Mitigation: Review the installer and chosen CLI release, then require approval for installation changes.

Risk: Setup may introduce changes to other agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 as documented upstream and review any skill-directory changes.

Risk: The deployed connector behavior is unverified, and its connection may expose more data than needed.

Mitigation: Restrict the OOMOL connection to required data and inspect the live action schema before sending a request.

## Reference(s):

- [Iru (Kandji) homepage](https://www.iru.com/)
- [Kandji API documentation](https://api-docs.kandji.io/)
- [oo CLI command documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Kandji connector results as JSON, summarized in text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookups for Kandji users and blueprints.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
