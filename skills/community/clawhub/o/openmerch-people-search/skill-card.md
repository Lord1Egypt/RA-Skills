## Description:

Searches for people at a company by domain and role keywords and returns obfuscated profile results with first name, last-name initial, title, company, cost, and job id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kernel-gd](https://clawhub.ai/user/kernel-gd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find people at a target company for a role keyword search. The returned person ids can be used with a companion enrichment skill when full profiles are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable API base URL can receive the OpenMerch API key and paid search requests.

Mitigation: Keep OPENMERCH_BASE_URL unset for normal use; set it only to a trusted HTTPS OpenMerch staging endpoint with non-production credentials.

Risk: People-search queries and the OpenMerch API key are sent to OpenMerch.

Mitigation: Install and run the skill only when sending company and role search queries to OpenMerch is acceptable for the intended use.

Risk: Each successful execution can consume paid OpenMerch account credits.

Mitigation: Review the /v1/plan result before execution and report the final cost_usd and job_id after completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kernel-gd/skills/openmerch-people-search)
- [OpenMerch documentation](https://docs.openmerch.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets; the reference script prints normalized JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results obfuscate last names, omit email addresses, include cost_usd and job_id, and represent one page of one OpenMerch job.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
