## Description:

Use this skill to read, create, update, and delete data in CentralStationCRM (centralstationcrm.de).

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an OOMOL-connected CentralStationCRM account can use this skill to read, search, create, update, and delete CRM records through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance directs users to run an online CLI installer, while the installer and runtime behavior have not been verified.

Mitigation: Review and install the CLI separately before enabling the skill.

Risk: The skill can change or delete CRM records through the connected account.

Mitigation: Limit connected-account permissions and require approval for write and destructive actions.

## Reference(s):

- [CentralStationCRM homepage](https://centralstationcrm.de)
- [CentralStationCRM API documentation](https://api.centralstationcrm.net/api-docs/index.html)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON request payloads and connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Payload fields follow the live action schema.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
