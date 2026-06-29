## Description: <br>
Zero-dependency Bash environment health check for Linux, macOS, containers, and K8s pods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a local, container, or Kubernetes shell environment, including OS details, current user, common runtime and tool versions, network context, workdir status, optional config presence, and PVC remount signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may print selected environment variable values and local environment details during diagnostics. <br>
Mitigation: Run it only in shells where exposed environment values are acceptable, and avoid production, CI, or Kubernetes contexts that may contain tokens unless the script is changed to mask values by default. <br>
Risk: PVC checks write local snapshot state under the configured snapshot directory. <br>
Mitigation: Choose a snapshot directory appropriate for the workspace and review generated snapshot files before relying on them for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songhonglei/hello-env) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output with status lines and diagnostic guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a Bash diagnostic script and may create PVC snapshot files when PVC monitoring is enabled.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
