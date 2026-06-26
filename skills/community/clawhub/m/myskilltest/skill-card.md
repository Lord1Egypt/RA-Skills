## Description: <br>
Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, and reading, injecting, or running secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shouone](https://clawhub.ai/user/Shouone) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to set up 1Password CLI workflows, authenticate safely, and run or inject secrets without exposing them unnecessarily. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples can print secrets or write them to local files. <br>
Mitigation: Avoid unmasked secret output, prefer `op run` or `op inject`, use restrictive permissions for any generated secret files, and delete temporary secret-bearing files when finished. <br>
Risk: Generated configuration or key files may contain sensitive material. <br>
Mitigation: Do not commit generated config or key files, and review local outputs before sharing logs, code, or artifacts. <br>


## Reference(s): <br>
- [1Password CLI get-started documentation](https://developer.1password.com/docs/cli/get-started/) <br>
- [get-started.md](references/get-started.md) <br>
- [cli-examples.md](references/cli-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/Shouone/myskilltest) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 1Password CLI (`op`) and recommends running `op` commands inside a dedicated tmux session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
