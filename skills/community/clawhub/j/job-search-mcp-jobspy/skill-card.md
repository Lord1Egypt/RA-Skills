## Description: <br>
Search and compare job listings across multiple boards using a configured JobSpy MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NikkiJasmine](https://clawhub.ai/user/NikkiJasmine) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Job seekers and recruiting workflows use this skill to find, filter, and compare job postings by role, location, company, salary availability, remote status, recency, and Easy Apply support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job search criteria and related profile information may be shared with external job-board services through the configured MCP server. <br>
Mitigation: Connect only to a JobSpy MCP server and job-board integrations that the user trusts. <br>
Risk: Runtime setup installs Python packages for the MCP workflow. <br>
Mitigation: Use a virtual environment and consider pinning dependency versions before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NikkiJasmine/job-search-mcp-jobspy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted, configured JobSpy MCP server and access to selected job-board integrations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
