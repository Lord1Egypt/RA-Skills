## Description:

AeroLeads (aeroleads.com). Use this skill for ANY AeroLeads request — searching and reading data. Whenever a task involves AeroLeads, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve prospect details, contact information, company data, education, skills, and related profile data from a public LinkedIn profile through AeroLeads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses remote CLI installers that were not verified.

Mitigation: Review the setup and install a verified oo CLI release yourself before use.

Risk: The CLI may synchronize installed agent skills more broadly than these instructions describe, and the hosted connector implementation was not verified.

Mitigation: Decide whether to set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI, and review the connector behavior before using it.

Risk: OOMOL-mediated contact lookups may consume credit.

Mitigation: Check the account's available credit and use the lookup when its cost is acceptable.

## Reference(s):

- [AeroLeads](https://aeroleads.com)
- [AeroLeads API documentation](https://aeroleads.com/api)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector requests and returned prospect data, with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned profile fields depend on AeroLeads response data.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
