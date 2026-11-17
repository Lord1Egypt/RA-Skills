## Description:

Access and manage Ashby ATS data including candidate profiles, job listings, and application details via API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams and agents use this skill to query Ashby ATS candidates, jobs, applications, and related details through the Pipeworx MCP gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive recruiting data may pass through a third-party MCP gateway without enough disclosed scoping or security detail.

Mitigation: Install only after organizational approval; restrict access to least-privilege, read-only use where possible; avoid retrieving full candidate profiles unless required; confirm credential handling, logging, retention, and revocation controls.

## Reference(s):


## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration]

**Output Format:** [MCP tool results and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return sensitive recruiting data such as candidate contact details, resumes, interview history, application stages, job descriptions, and hiring-stage information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
