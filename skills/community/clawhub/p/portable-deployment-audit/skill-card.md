## Description: <br>
Read-only security auditing for OpenClaw deployments, repositories, and local project directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OTweihan](https://clawhub.ai/user/OTweihan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run read-only security reviews of deployment directories, server checkouts, workspaces, or repositories before release, after setup, during periodic hardening checks, or in CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports can reveal sensitive local paths, hostnames, and security findings. <br>
Mitigation: Keep generated reports private and share them only with people authorized to review the target environment. <br>
Risk: The skill inspects files under the requested target directory. <br>
Mitigation: Run it only on directories you are authorized to inspect and pass an explicit --target when auditing outside the current directory. <br>
Risk: Findings are advisory and may require environment-specific interpretation. <br>
Mitigation: Review findings before making changes and use --allow-port or --exclude-dir to suppress expected local configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/OTweihan/portable-deployment-audit) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Text or JSON audit report with findings, counts, and remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only file inspection; JSON reports include the local hostname; --strict can return a non-zero exit code for CI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
