## Description: <br>
JobGPT helps agents automate job search, auto-apply workflows, tailored resume generation, application tracking, salary intelligence, and recruiter outreach through the JobGPT MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[captainjackrana](https://clawhub.ai/user/captainjackrana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career assistants use this skill to search for roles, manage job hunts, apply to selected jobs, tailor resumes, track application status, review compensation data, and draft recruiter or referrer outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send resume, profile, salary, application, and outreach data to an external JobGPT service. <br>
Mitigation: Install only if you trust JobGPT with career data, and review the account, API key, and MCP server configuration before use. <br>
Risk: Auto-apply and outreach workflows can take real-world actions such as submitting job applications or contacting recruiters. <br>
Mitigation: Set narrow job criteria and daily limits, review jobs and generated resume or outreach content, and require explicit approval for each application, batch, or message. <br>
Risk: Auto-apply and resume generation workflows may consume JobGPT credits. <br>
Mitigation: Check available credits before running credit-consuming workflows and confirm the user wants to proceed. <br>


## Reference(s): <br>
- [JobGPT](https://6figr.com/jobgpt) <br>
- [JobGPT platform](https://6figr.com/jobgpt-ai) <br>
- [JobGPT MCP server](https://github.com/6figr-com/jobgpt-mcp-server) <br>
- [jobgpt-mcp-server npm package](https://www.npmjs.com/package/jobgpt-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration steps, and MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JobGPT account, JOBGPT_API_KEY, and the JobGPT MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
