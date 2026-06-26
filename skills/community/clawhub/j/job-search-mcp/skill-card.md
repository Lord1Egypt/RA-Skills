## Description: <br>
Search for jobs across LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs, Bayt, Naukri, and BDJobs using the JobSpy MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Amoghpurohit](https://clawhub.ai/user/Amoghpurohit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External job seekers, recruiters, and agents use this skill to search and compare job listings across multiple job boards with filters for role, location, salary, recency, job type, remote status, and easy-apply options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job-search terms, locations, and filters may be sent to external job sites through the JobSpy MCP server. <br>
Mitigation: Avoid including sensitive personal details in searches and use only job criteria that are appropriate to share with external services. <br>
Risk: The referenced JobSpy MCP server and its dependencies run locally in the user's agent environment. <br>
Mitigation: Install and run the server in a virtual environment, review its configuration, and keep dependencies scoped to the job-search workflow. <br>
Risk: Large or repeated searches can trigger job-board rate limits or timeouts. <br>
Mitigation: Keep result counts reasonable, start with smaller searches, paginate when needed, and prefer more reliable sources such as Indeed before expanding to stricter platforms. <br>


## Reference(s): <br>
- [JobSpy MCP Server](https://github.com/chinpeerapat/jobspy-mcp-server.git) <br>
- [Example MCP Calls](artifact/example_calls.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP tool names and structured job-search parameters; search results depend on external job-board availability and rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
