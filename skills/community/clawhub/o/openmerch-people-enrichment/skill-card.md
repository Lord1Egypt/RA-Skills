## Description:

Retrieve a full personal profile, including name, email address, LinkedIn URL, title, and employer, for a single person using an Apollo person ID through the paid OpenMerch API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kernel-gd](https://clawhub.ai/user/kernel-gd)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, recruiting, and operations users can enrich one known Apollo person ID at a time with contact and employment profile data when they have a lawful basis to process that data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A modified OPENMERCH_BASE_URL can redirect the OpenMerch API key and lookup data to an untrusted endpoint.

Mitigation: Keep OPENMERCH_BASE_URL unset for normal use, allow only trusted HTTPS staging endpoints with separate test keys, and run in an environment where other users cannot alter that variable.

Risk: The skill returns personal contact data and uses a paid external API.

Mitigation: Install only when you trust OpenMerch, have a lawful basis for enrichment, and accept that each enrichment can consume OpenMerch account balance or credits.

## Reference(s):

- [OpenMerch documentation](https://docs.openmerch.dev)
- [ClawHub skill page](https://clawhub.ai/kernel-gd/skills/openmerch-people-enrichment)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Normalized JSON profile data and concise status or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always reports job_id; includes cost_usd and profile fields only when returned by the upstream job.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
