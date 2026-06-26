## Description: <br>
Plane Flow helps an agent read and update a local or self-hosted Plane workspace for project, backlog, issue, and sprint management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uncooldog](https://clawhub.ai/user/uncooldog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users use this skill to manage Plane backlogs, issues, assignments, cycles, and project summaries through normal requests after an administrator configures the Plane connection. Administrators and technical owners use the bundled helpers to validate credentials, configure environment variables, and debug local Plane connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an authenticated Plane API token to create or change Plane records. <br>
Mitigation: Install only where the Plane API token is appropriately scoped, and confirm ambiguous or high-impact write requests before executing them. <br>
Risk: Attachment support can read and upload local files named in user requests or image directives. <br>
Mitigation: Upload only files explicitly selected by the user, and review untrusted notes for image directives or local file paths before processing them. <br>
Risk: The skill depends on sensitive Plane connection settings in the host environment. <br>
Mitigation: Have an administrator configure PLANE_BASE_URL, PLANE_API_TOKEN, and PLANE_WORKSPACE_ID for a trusted Plane instance before business users rely on the skill. <br>


## Reference(s): <br>
- [ClawHub Plane Flow listing](https://clawhub.ai/uncooldog/plane-flow) <br>
- [Plane Flow README](README.md) <br>
- [Plane Flow CLI Usage](references/cli-usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON-style command output from bundled Python helpers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Plane records and upload explicitly selected local attachments through the configured Plane instance.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence and README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
