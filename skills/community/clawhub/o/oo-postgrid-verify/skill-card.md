## Description:

Use PostGrid Verify to look up, parse, autocomplete, and verify address information through the OOMOL connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to look up, parse, autocomplete, and standardize US and Canadian postal addresses through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic setup path can run changing remote code and add persistent agent skills beyond this integration.

Mitigation: Install a verified oo CLI release separately and review its automatic skill-installation behavior; OO_SKILLS_SYNC_DISABLED is documented as a startup synchronization control.

Risk: Address inputs are processed through OOMOL and PostGrid.

Mitigation: Submit only address data that is appropriate to process through both services.

## Reference(s):

- [PostGrid Verify address verification](https://www.postgrid.com/address-verification/)
- [PostGrid Verify API documentation](https://avdocs.postgrid.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON inputs and connector response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Address actions cover the United States and Canada.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
