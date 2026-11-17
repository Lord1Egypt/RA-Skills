## Description:

Search and read Clari Copilot workspace data, including calls, scorecards, topics, and users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Clari Copilot users can retrieve call details and list calls, scorecards, topics, and workspace users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions provide an installer for CLI code that was not verified.

Mitigation: Review and approve the installer separately, and use a pinned, verified CLI release before running it.

Risk: Automatic skill synchronization could affect an existing agent environment.

Mitigation: Check the CLI's synchronization behavior before running it in an established environment.

Risk: The connected service provides access to private Clari call data and connection credentials through OOMOL.

Mitigation: Use an organization-approved connection and confirm the account and data access are appropriate before retrieving call information.

## Reference(s):

- [Clari Copilot product page](https://www.clari.com/products/copilot/)
- [Clari Copilot API documentation](https://api-doc.copilot.clari.com/)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action responses and text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data depends on the connected Clari Copilot account and the selected read action.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
