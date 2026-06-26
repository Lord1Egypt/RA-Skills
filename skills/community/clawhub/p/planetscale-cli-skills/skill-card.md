## Description: <br>
Provides PlanetScale CLI command references, workflows, and automation scripts for managing databases, branches, deploy requests, backups, credentials, and organizations from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vince-winkintel](https://clawhub.ai/user/vince-winkintel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to plan and run PlanetScale CLI workflows for schema changes, branch management, deploy requests, backups, authentication, and CI/CD service-token setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide or run operations that deploy, delete, promote, revert, or otherwise change real PlanetScale databases. <br>
Mitigation: Require the agent to show the exact organization, database, branch, diff, and command before execution; confirm backups or rollback plans before deletion, promotion, deploy, or revert operations. <br>
Risk: The skill can use sensitive PlanetScale service token credentials for CI/CD authentication. <br>
Mitigation: Store tokens only in a secret manager or CI secret store, avoid echoing token values, and rotate or revoke tokens when they are no longer needed. <br>
Risk: Automation scripts can create deploy requests and optionally deploy schema changes. <br>
Mitigation: Avoid automatic deploys unless the pipeline has approval gates and a clear rollback process. <br>


## Reference(s): <br>
- [PlanetScale CLI documentation](https://planetscale.com/docs/reference/planetscale-cli) <br>
- [PlanetScale CLI GitHub repository](https://github.com/planetscale/cli) <br>
- [ClawHub release page](https://clawhub.ai/vince-winkintel/planetscale-cli-skills) <br>
- [Branch command reference](pscale-branch/references/commands.md) <br>
- [Automation scripts guide](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash, YAML, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the PlanetScale CLI and authentication; bundled shell scripts may execute pscale operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
