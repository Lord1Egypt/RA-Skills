## Description:

Search and read buyer, product, purchase, sales, and account information in Digistore24 through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Digistore24 account use the skill to retrieve buyer, product, purchase, sales, and account details. Developers can use it to check the connector action schema before requesting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded code that has not been verified.

Mitigation: Review and install a verified oo CLI release yourself before setup.

Risk: Setup may install additional agent skills without clear user control.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before setup and review any skill installation changes.

Risk: The connected account may expose buyer and purchase data through retrieval actions.

Mitigation: Consider which buyer and purchase data the connected account can access before using the skill.

## Reference(s):

- [Digistore24 API documentation](https://digistore24.com/api/docs/index.html)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Shell commands, JSON]

**Output Format:** [JSON connector requests and responses, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves data through the connected Digistore24 account.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
