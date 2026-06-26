## Description: <br>
Deploy and manage cloud services on Ink (ml.ink): create projects, deploy services, provision databases, manage DNS and custom domains, configure workspaces, and monitor deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gluonfield](https://clawhub.ai/user/gluonfield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide agents through Ink cloud deployment and operations workflows, including service deployment, database provisioning, secret management, DNS setup, and deployment monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents into high-impact Ink cloud changes, including deploy, redeploy, delete, DNS, database, repository token, and secret-management operations. <br>
Mitigation: Verify the logged-in Ink account, workspace, project, repository, branch, and region, and require explicit user approval before running commands that change infrastructure, DNS, databases, repository tokens, or secrets. <br>


## Reference(s): <br>
- [Ink](https://ml.ink) <br>
- [Ink DNS](https://ml.ink/dns) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may use Ink CLI JSON output and should be reviewed before changing cloud resources.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
