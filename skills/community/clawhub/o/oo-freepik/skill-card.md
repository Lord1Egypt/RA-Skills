## Description:

Search Magnific (Freepik) resources and retrieve resource details or download URLs through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Magnific's stock images and templates, inspect resource details, and create download URLs through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unpinned remote code and may add persistent agent skills without clearly disclosing that scope.

Mitigation: Review and approve a specific CLI release before automatic setup; consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking oo.

Risk: Using the connected service requires OOMOL account authorization and may incur service charges.

Mitigation: Confirm the intended OOMOL account connection and review applicable service charges before use.

## Reference(s):

- [Magnific resources API documentation](https://docs.magnific.com/api-reference/resources/images-and-templates-api)
- [Magnific (Freepik)](https://www.magnific.com/freepik)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [Markdown guidance with shell commands, JSON request payloads, and action responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action response content depends on the requested Magnific resource operation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
