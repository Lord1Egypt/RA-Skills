## Description:

Search [Gumtree UK](https://www.gumtree.com/) jobs and part-time listings with bb-browser from the user’s role, location, and hours—structured JSON plus first-image Markdown for scanning vacancies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salamankakit](https://clawhub.ai/user/salamankakit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Gumtree UK employment listings by role, location, contract type, and job category, then inspect listing details with structured results and image previews.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: The listing adapter can fetch arbitrary URLs when given a full URL.

Mitigation: Restrict listing lookups to Gumtree URLs and run the tool in a constrained environment when possible.

Risk: Installation uses a global bb-browser dependency and persistent local adapter files.

Mitigation: Pin the bb-browser version, review the bundled JavaScript before installation, and keep the adapter files under change control.

Risk: Job listings may contain inaccurate employer, pay, or right-to-work information.

Mitigation: Verify employer identity, pay, and right-to-work requirements through official channels before acting on a listing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/salamankakit/skills/gumtree-uk-jobs)
- [Gumtree UK](https://www.gumtree.com/)
- [bb-browser package](https://www.npmjs.com/package/bb-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [JSON search and listing records with Markdown image previews and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Gumtree search and listing retrieval; requires bb-browser and local adapter files.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
