## Description:

Analyzes co-filed patent relationships for a company or university, identifying external partners, joint-patent counts, collaboration topics, and recent activity in an Excel-compatible table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts and research partnership teams use the skill to map a company's or university's co-applicant network and identify potential industry–academia partners from jointly filed patent records.

### Deployment Geography for Use:

China, the United States, Europe, Japan, South Korea, and WIPO jurisdictions, subject to PatentMax database coverage.

## Known Risks and Mitigations:

Risk: Searches send query details to PatentMax and may incur charges.

Mitigation: Keep confidential invention details out of searches and disclose or confirm applicable charges before querying.

Risk: Paid API keys could be exposed through chat or unsafe destinations.

Mitigation: Do not share keys in chat; verify the destination and redirects, and use protected credential storage.

Risk: Unvalidated cache filenames may lead to unsafe file access.

Mitigation: Validate cache filenames and constrain cache paths before supplying a paid key or running the workflow.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/patent-collaboration-map)
- [PatentMax API and console](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [Analysis, Files]

**Output Format:** [Excel-compatible CSV table (UTF-8 with BOM)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists external partners before affiliates, includes joint-patent counts, recent filing dates, activity and collaboration topics, and flags uncertain affiliations.]

## Skill Version(s):

1.0.2 (source: frontmatter, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
