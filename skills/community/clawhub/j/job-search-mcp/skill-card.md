## Description:

Search for jobs across LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs, Bayt, Naukri, and BDJobs using the JobSpy MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amoghpurohit](https://clawhub.ai/user/amoghpurohit)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search, filter, and compare job listings across supported job boards through a configured JobSpy MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job searches query third-party job sites and can expose personal job-search criteria.

Mitigation: Use only the search details needed for the task and avoid sensitive personal information unless necessary.

Risk: The skill relies on externally installed MCP software and packages.

Mitigation: Install and run the MCP server in a virtual environment or container, and prefer pinned package versions or a reviewed commit.

Risk: Proxy use and third-party job-site access can affect privacy expectations and site-term compliance.

Mitigation: Review proxy configuration, privacy expectations, and applicable job-site terms before using those access paths.

## Reference(s):

- [JobSpy MCP server repository](https://github.com/chinpeerapat/jobspy-mcp-server.git)
- [Example MCP calls](artifact/example_calls.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks; MCP job-search responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include job titles, companies, job URLs, locations, salary data, posting dates, platform details, and error guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
