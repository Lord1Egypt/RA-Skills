## Description:

Search and read JazzHR applicants, jobs, and users through the connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting and HR teams use the skill to search and read JazzHR applicants, jobs, and users through an already connected account. It returns requested records for the agent to present or summarize.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute downloaded code and change installed agent skills through startup synchronization.

Mitigation: Review and approve CLI installation separately, use a verified release, and consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Using the connected service exposes recruiting requests and JazzHR account data to OOMOL processing.

Mitigation: Confirm OOMOL is authorized to process recruiting requests and access the connected JazzHR account.

## Reference(s):

- [JazzHR](https://www.jazzhr.com)
- [JazzHR API documentation](https://www.resumatorapi.com/v1/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Natural-language summaries and JSON results from JazzHR queries, using oo CLI shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only applicant, job, and user records; queries may be filtered by supported fields.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
