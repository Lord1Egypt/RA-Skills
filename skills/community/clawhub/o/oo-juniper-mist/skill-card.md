## Description:

Searches and reads Juniper Mist account data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Network administrators and support teams use the skill to inspect their Juniper Mist profile, organizations, sites, and site devices through read actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses remote CLI installers whose effects have not been verified.

Mitigation: Review the CLI installation separately and use a verified release before connecting an account.

Risk: The required CLI may affect other agent skills through startup synchronization.

Mitigation: Decide whether to allow additional skills; set OO_SKILLS_SYNC_DISABLED=1 to prevent startup synchronization.

Risk: The connected account may expose more Juniper Mist data than the task requires.

Mitigation: Use an account limited to the organizations, sites, and read permissions needed.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Juniper Mist product overview](https://www.juniper.net/us/en/products/networking/mist-ai.html)
- [Juniper Mist API documentation](https://www.juniper.net/documentation/us/en/software/mist/api/http/guides/overview/mist-apis/)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language summaries of Juniper Mist profile, organization, site, and device data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited to data accessible to the connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
