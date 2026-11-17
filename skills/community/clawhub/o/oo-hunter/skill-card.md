## Description:

Hunter (hunter.io). Use this skill for ANY Hunter request — reading, creating, updating, and deleting data. Whenever a task involves Hunter, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Hunter through their OOMOL-connected account to search company domains, find and verify professional email addresses, enrich contact and company data, and manage leads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup may have local effects that are not sufficiently disclosed.

Mitigation: Review and approve CLI setup separately, verify the installer, and consider disabling automatic skill synchronization with the documented OO_SKILLS_SYNC_DISABLED setting.

Risk: Hunter requests are routed through OOMOL, and lead changes can affect account data.

Mitigation: Retain the skill's confirmation requirements for create and update actions, and get explicit approval before deleting a lead.

## Reference(s):

- [oo CLI repository (referenced by the skill)](https://github.com/oomol-lab/oo-cli)
- [Hunter](https://hunter.io)
- [Hunter API documentation](https://hunter.io/api-documentation/v2)
- [oo CLI controls documentation](https://raw.githubusercontent.com/oomol-lab/oo-cli/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes retrieved Hunter data; account-changing actions require confirmation, and deletion requires explicit approval.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
