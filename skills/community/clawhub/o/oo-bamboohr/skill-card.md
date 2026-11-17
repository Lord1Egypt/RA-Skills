## Description:

Use BambooHR to search and read data from the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and HR operations teams use this skill to retrieve company details, employee records, employee lists, and available employee fields from a connected BambooHR account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup relies on downloaded installer content whose exact contents and version were not verified.

Mitigation: Review and verify the CLI installation independently before running it.

Risk: Startup synchronization may add managed skills and broaden agent behavior.

Mitigation: Decide whether managed skill synchronization is wanted; the upstream instructions document OO_SKILLS_SYNC_DISABLED=1 to suppress it.

Risk: Connected BambooHR records may contain employee data, and OOMOL handles credentials server-side.

Mitigation: Connect an appropriately restricted BambooHR account and consider OOMOL's role in handling employee data.

## Reference(s):

- [BambooHR API documentation](https://documentation.bamboohr.com/)
- [BambooHR](https://www.bamboohr.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Natural-language answers and structured JSON data retrieved from BambooHR]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only company and employee information]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
