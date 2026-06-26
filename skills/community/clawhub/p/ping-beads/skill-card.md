## Description: <br>
Verify the bead daemon is alive and responsive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who use the beads system use this skill to check whether the local bead daemon is running and responsive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local PATH entry could point bd or ping-beads to an unintended command. <br>
Mitigation: Confirm that bd and ping-beads resolve to trusted local binaries before relying on the health check. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Xejrax/ping-beads) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local bd and ping-beads commands to be trusted and available in PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
