## Description: <br>
Plan and track cryptographic key rotations for API keys, encryption keys, signing keys, and service credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inventory credentials, prioritize rotations by age and exposure, draft rotation runbooks, and verify service health after key changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inventory commands may expose secret names, credential locations, or other sensitive operational details in generated reports. <br>
Mitigation: Run discovery in an authorized environment, redact sensitive values before sharing output, and store reports in approved security tooling. <br>
Risk: Rotation runbooks can affect production authentication if steps are executed without coordination. <br>
Mitigation: Use change management, backups, staged rollout, service health checks, and rollback plans before revoking or replacing live credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/key-rotation-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tabular reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning guidance, inventory report templates, rotation runbooks, verification checklists, and reminder schedules.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
