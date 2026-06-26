## Description: <br>
Sensibo helps an agent list linked Sensibo devices, inspect device and AC state, and update AC state through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Sensibo devices from an agent after the oo CLI is installed, the OOMOL account is signed in, and Sensibo is connected. It supports device discovery, state inspection, and confirmed AC state updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update AC state for a Sensibo device through the `set_ac_state` write action. <br>
Mitigation: Confirm the exact device, payload, and intended AC state with the user before running any write action. <br>
Risk: The skill requires access to an OOMOL-connected Sensibo account and depends on the local `oo` CLI installation. <br>
Mitigation: Review the `oo` CLI installation path, connect only the intended Sensibo account, and use the connector only for requested Sensibo actions. <br>


## Reference(s): <br>
- [Sensibo homepage](https://home.sensibo.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-sensibo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read actions may run directly; write actions require confirming the exact Sensibo device and AC state before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
