## Description: <br>
This skill helps an agent use Placed career tools for resume-job matching, cover letters, interview preparation, LinkedIn profile generation, salary insights, salary negotiation, company research, resume gap analysis, and job application tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajitsingh25](https://clawhub.ai/user/ajitsingh25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career-support agents use this skill to call Placed API tools for resume optimization, job matching, application tracking, salary research, negotiation preparation, company research, and career-document generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Placed API key in ~/.config/placed/credentials. <br>
Mitigation: Use a dedicated API key, protect the credentials file, and delete it when the skill is no longer needed. <br>
Risk: Career information, including resumes, job descriptions, salary details, and application notes, may be sent to the Placed API. <br>
Mitigation: Share only the career data needed for the task and avoid unnecessary sensitive compensation or personal details. <br>
Risk: Job-application tracker tools can add, update, or delete application records. <br>
Mitigation: Require explicit user confirmation before creating, changing, or deleting job-application records. <br>


## Reference(s): <br>
- [Placed Career Tools API Reference](references/api-guide.md) <br>
- [Placed](https://placed.exidian.tech) <br>
- [Placed Career Tools on ClawHub](https://clawhub.ai/ajitsingh25/placed-career-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Placed API key and sends career data to the Placed API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
