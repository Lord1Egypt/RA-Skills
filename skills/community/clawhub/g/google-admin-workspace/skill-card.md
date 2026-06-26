## Description: <br>
Manage Google Workspace users, groups, domains, devices, and admin directory data via the Google Admin SDK API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Workspace administrators and operators use this skill to inspect and manage Google Workspace users, groups, domains, devices, organization units, and directory resources through ClawLink-mediated Google Admin SDK tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth-mediated Google Workspace admin access can inspect, create, update, or delete organization resources. <br>
Mitigation: Use a connected admin account with the minimum permissions needed for the task and install only when ClawLink-mediated Google Admin access is intended. <br>
Risk: Write or destructive actions can affect users, groups, devices, domains, or organization units. <br>
Mitigation: Preview write operations, confirm the target resource and intended effect with the user, and execute only after explicit approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/google-admin-workspace) <br>
- [Google Admin SDK Documentation](https://developers.google.com/admin-sdk) <br>
- [Directory API Reference](https://developers.google.com/admin-sdk/directory/reference/rest) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ClawLink OAuth connection to a Google Workspace admin account; write operations require preview and explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
