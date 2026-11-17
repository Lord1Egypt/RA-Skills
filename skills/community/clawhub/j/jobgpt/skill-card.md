## Description:

Job search automation, auto apply, resume generation, application tracking, salary intelligence, and recruiter outreach using the JobGPT MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[captainjackrana](https://clawhub.ai/user/captainjackrana)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to JobGPT for job search, auto-apply workflows, tailored resume generation, application tracking, salary insights, and recruiter or referrer outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit real job applications through auto-apply workflows.

Mitigation: Require the agent to show the exact jobs, application materials, credit use, and job-hunt automation settings before triggering apply actions.

Risk: The MCP server uses a JobGPT API key and can access resume, profile, salary, and application data.

Mitigation: Install only for trusted users and environments, keep JOBGPT_API_KEY secret, and review requested actions before sharing sensitive career data.

Risk: The security summary flags unpinned MCP install commands.

Mitigation: Pin or otherwise verify npm package versions before installation where possible.

Risk: Recruiter or referrer outreach can contact real people.

Mitigation: Require explicit user confirmation after showing the complete message and recipient before calling send_outreach.

## Reference(s):

- [JobGPT](https://6figr.com/jobgpt)
- [JobGPT platform](https://6figr.com/jobgpt-ai)
- [JobGPT MCP server](https://github.com/6figr-com/jobgpt-mcp-server)
- [jobgpt-mcp-server npm package](https://www.npmjs.com/package/jobgpt-mcp-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, job summaries, resume and application details, and outreach drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include links to generated resumes, imported jobs, applications, or JobGPT account resources when returned by the MCP server.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
