## Description:

Find a professional's work email from their name and company domain using OpenMerch; this is contact discovery, not email verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kernel-gd](https://clawhub.ai/user/kernel-gd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up a single professional work email from a first name, last name, and company domain. It returns the discovered contact data with confidence, cost, and job metadata, but it does not verify deliverability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends names, company domains, and the OpenMerch API key to OpenMerch for paid lookups.

Mitigation: Install only when that data sharing is acceptable, use an appropriate OpenMerch key, and review returned job cost metadata.

Risk: Changing OPENMERCH_BASE_URL can redirect lookup data and credentials away from the default OpenMerch endpoint.

Mitigation: Leave OPENMERCH_BASE_URL unset for normal use, or set it only to a trusted OpenMerch HTTPS endpoint with a suitable test key.

Risk: The skill finds likely work email addresses but does not verify deliverability.

Mitigation: Treat results as contact discovery output and perform separate verification before relying on deliverability.

## Reference(s):

- [OpenMerch documentation](https://docs.openmerch.dev)
- [OpenMerch API endpoint](https://api.openmerch.dev)
- [ClawHub skill page](https://clawhub.ai/kernel-gd/skills/openmerch-contact-discovery)
- [Publisher profile](https://clawhub.ai/user/kernel-gd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and JSON contact lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One lookup per run; normalized result includes any returned email, name, domain, position, LinkedIn URL, score, raw provider output, cost_usd, and job_id.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
