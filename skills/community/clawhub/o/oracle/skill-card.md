## Description: <br>
Use the @steipete/oracle CLI to bundle a prompt plus the right files and get a second-model review (API or browser) for debugging, refactors, design checks, or cross-validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Oracle to package a focused prompt with selected repository files for second-model review of debugging questions, refactors, design checks, and cross-validation. The skill emphasizes previewing selected files, avoiding secrets, and treating returned analysis as advisory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected repository files may be sent to external AI services during Oracle runs. <br>
Mitigation: Use dry-run and files-report before execution, exclude secrets such as .env files, key files, and tokens, and prefer narrow file globs. <br>
Risk: The workflow depends on trusting the @steipete/oracle npm package and its browser or API execution path. <br>
Mitigation: Install only when that package is trusted for the workspace, review generated commands before execution, and require explicit consent for API runs that may incur usage costs. <br>
Risk: Remote browser hosting can expose automation access if bound broadly on the network. <br>
Mitigation: Avoid exposing the remote browser host on 0.0.0.0 unless network access is understood and controlled, and use a strong remote token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/oracle) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead an agent to invoke an external CLI that sends selected repository files to external AI services; outputs should be reviewed before relying on them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
