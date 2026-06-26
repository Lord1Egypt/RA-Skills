## Description: <br>
Tracks, updates, deletes, and analyzes job applications through the Placed career platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajitsingh25](https://clawhub.ai/user/ajitsingh25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this skill to manage their application pipeline on Placed, including adding applications, listing and filtering opportunities, updating statuses, deleting records, and reviewing application analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Placed API key and may store it in a local credentials file. <br>
Mitigation: Use a revocable API key and protect or avoid persisting the credentials file. <br>
Risk: The skill can update or delete job application records. <br>
Mitigation: Require the agent to preview and confirm update or delete actions before execution. <br>


## Reference(s): <br>
- [Placed homepage](https://placed.exidian.tech) <br>
- [Placed Job Tracker API Reference](references/api-guide.md) <br>
- [ClawHub skill listing](https://clawhub.ai/ajitsingh25/placed-job-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Placed API responses for application records, status updates, deletion results, and analytics summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
