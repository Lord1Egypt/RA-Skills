## Description:

Look up a company's profile by domain - industry, size, location, founding year, and funding data when available. Powered by OpenMerch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kernel-gd](https://clawhub.ai/user/kernel-gd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve a concise company profile for a known domain through OpenMerch, including firmographic fields and funding data when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OPENMERCH_BASE_URL can redirect requests containing the OpenMerch API key to a configured endpoint.

Mitigation: Leave OPENMERCH_BASE_URL unset for normal use, or set it only to a trusted HTTPS OpenMerch staging endpoint with a separate non-production key.

Risk: Lookups can consume credits from the user's OpenMerch account.

Mitigation: Review the live /v1/plan quote before execution and keep the max_cost bound from the plan response.

## Reference(s):

- [OpenMerch Documentation](https://docs.openmerch.dev)
- [ClawHub Skill Page](https://clawhub.ai/kernel-gd/skills/openmerch-company-brief)
- [Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Normalized JSON result with optional Markdown summary and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One company-domain lookup per run; domain, raw, and job_id are always present, while company details and cost_usd are included only when returned by OpenMerch.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
