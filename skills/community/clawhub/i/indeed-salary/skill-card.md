## Description:

Look up salary for an Indeed job posting via RolesAPI.com using a job key or pasted Indeed URL, returning salary range, currency, period, and employer-versus-estimate provenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need salary information for specific Indeed postings by job key or pasted URL, including whether the salary came from the employer or an estimate. It is not intended for market-wide salary averages or full job-detail retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends specific Indeed job keys or pasted Indeed URLs to RolesAPI using a user-provided API key.

Mitigation: Install and use it only when that data sharing is acceptable, and set ROLESAPI_KEY only in environments authorized to call RolesAPI.

Risk: Salary lookups may consume RolesAPI credits and can be rate limited.

Mitigation: Monitor account credits and rate limits before running repeated or comparison lookups.

Risk: The skill returns salary information for specific postings and may omit salary when the posting has none.

Mitigation: Use it only for explicit posting-level salary questions and avoid treating results as market-wide compensation averages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nikhonit/skills/indeed-salary)
- [RolesAPI Homepage](https://rolesapi.com)
- [RolesAPI Key Setup](https://rolesapi.com/app/keys)
- [RolesAPI Pricing](https://rolesapi.com/pricing/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and concise Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ROLESAPI_KEY; each successful salary lookup is documented as one credit.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
