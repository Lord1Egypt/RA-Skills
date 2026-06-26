## Description: <br>
Mac laptop clamshell mode assistant for checking compatibility and configuring closed-lid operation with Mac model and macOS version detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keenlycat](https://clawhub.ai/user/keenlycat) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Mac users use this skill to check macOS and MacBook compatibility, inspect power settings, and get shell-command guidance for closed-lid background operation or restoring defaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead users to make persistent administrator-level Mac power-setting changes. <br>
Mitigation: Review scripts and generated commands before running them, enter an administrator password only when intentionally changing system-wide power settings, and record current pmset -g settings first. <br>
Risk: Rollback and dry-run safety may be overstated by the artifact. <br>
Mitigation: Prefer the status check or temporary caffeinate mode first, and do not rely on documented --rollback or --dry-run options as implemented safety controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/keenlycat/mac-clamshell-mode) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest administrator-level macOS power-setting commands; users should review and approve changes before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
