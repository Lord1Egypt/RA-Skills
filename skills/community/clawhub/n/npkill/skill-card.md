## Description: <br>
Clean up node_modules and .next folders to free up disk space using npkill, with interactive, dry-run, and cautious automated cleanup options for JavaScript and Next.js workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AshirbadGudu](https://clawhub.ai/user/AshirbadGudu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to identify and remove accumulated node_modules and Next.js .next build folders so local workspaces recover disk space while preserving review steps before deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: npkill can delete dependency and build folders, including broad automated deletion if run from the wrong directory. <br>
Mitigation: Prefer dry-run and interactive mode, verify selected folders before deletion, and avoid automated deletion from broad directories. <br>
Risk: The skill depends on the external npkill npm package being installed globally. <br>
Mitigation: Verify the npm package before global installation and keep installation scoped to trusted development environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require npkill to be installed separately and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
