## Description:

Use this skill for profileAPI requests to search and read data instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to look up a profileAPI person identifier and basic profile link from an email address or E.164 phone number through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented setup path can install or synchronize skills across agent applications, while the remote installer contents and exact release are unverified.

Mitigation: Review CLI setup separately before automatic installation and use OO_SKILLS_SYNC_DISABLED to opt out of synchronization.

Risk: Reverse lookup sends an email address or phone number to OOMOL and profileAPI.

Mitigation: Submit only email addresses or phone numbers you intend to share with those services.

## Reference(s):

- [profileAPI](https://profileapi.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON lookup results with a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on a connected profileAPI account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
