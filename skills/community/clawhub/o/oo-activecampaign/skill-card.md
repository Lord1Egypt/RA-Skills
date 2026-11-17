## Description:

Use the connected ActiveCampaign account to read, create, and update data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing ActiveCampaign accounts can retrieve contacts, lists, fields, and account details, and create or update contacts through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs a downloaded CLI installer, and its integrity was not verified in the supplied security review.

Mitigation: Review the installer and install the CLI from a verified release, requiring approval before software installation.

Risk: The skill accesses an ActiveCampaign account and can create or update contact records.

Mitigation: Use an appropriately scoped connection and confirm the exact contact changes before running the upsert action.

## Reference(s):

- [ActiveCampaign API authentication documentation](https://developers.activecampaign.com/reference/authentication)
- [ActiveCampaign](https://www.activecampaign.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-activecampaign)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON service responses with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contact creation or updates require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
