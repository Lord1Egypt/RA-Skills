## Description:

Work with the LinkdAPI Python SDK to fetch LinkedIn professional profile, company, job, and search data using uv-managed ephemeral Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foontinz](https://clawhub.ai/user/foontinz)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to write short Python scripts that call LinkdAPI for authorized LinkedIn profile, company, job, and search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable LinkedIn personal-data lookups, including contact information or bulk enrichment.

Mitigation: Use it only for authorized professional-data lookups with a lawful purpose, avoid unnecessary contact-info or bulk enrichment, and keep returned personal data minimal.

Risk: Generated uv scripts may install and run an unpinned third-party LinkdAPI SDK.

Mitigation: Run scripts in a constrained environment, pin and review the LinkdAPI package version before use, and expose only the required API key.

## Reference(s):

- [LinkdAPI documentation](https://linkdapi.com/docs)
- [ClawHub skill page](https://clawhub.ai/foontinz/skills/linkdapi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce temporary uv Python scripts and concise summaries of API results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
