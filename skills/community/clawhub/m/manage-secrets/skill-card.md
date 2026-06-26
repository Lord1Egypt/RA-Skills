## Description: <br>
Set or update environment secrets for a persona through the set-secret GitHub Actions workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aehrt55](https://clawhub.ai/user/aehrt55) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to update, rotate, or set environment secrets for a persona by dispatching the configured GitHub Actions workflow and monitoring its run status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Successful workflow runs can change deployed environment configuration. <br>
Mitigation: Confirm the target repository, persona, secret key, secret value, and workflow RBAC before dispatching the workflow. <br>
Risk: The workflow requires a GitHub PAT with permission to trigger Actions in the environment repository. <br>
Mitigation: Install only where AGENT_GITHUB_PAT and MANAGE_SECRETS_GITHUB_REPO are intended for this secret-management workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aehrt55/manage-secrets) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENT_GITHUB_PAT and MANAGE_SECRETS_GITHUB_REPO to be set before workflow dispatch.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
