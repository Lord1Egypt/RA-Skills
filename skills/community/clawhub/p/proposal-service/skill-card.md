## Description: <br>
Proposal Service inspects duplicate pending proposals and creates trigger-driven OpenClaw proposals in public.openclaw_proposals for the current closed-loop workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EcosincronIA](https://clawhub.ai/user/EcosincronIA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining an OpenClaw closed-loop workspace use this skill to check for equivalent pending stale-missions proposals and create a new proposal only when the current database state warrants it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The create command writes a pending proposal to the configured OpenClaw database. <br>
Mitigation: Run the duplicate-check command first and confirm the database container points to the intended local OpenClaw workspace. <br>
Risk: The bundled script uses a hardcoded agent identity when inserting proposals. <br>
Mitigation: Verify the agent identity is appropriate for the target environment before creating a proposal. <br>


## Reference(s): <br>
- [Proposal Service on ClawHub](https://clawhub.ai/EcosincronIA/proposal-service) <br>
- [EcosincronIA publisher profile](https://clawhub.ai/user/EcosincronIA) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output and agent guidance for running the bundled shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate against the intended OpenClaw workspace database and should be run explicitly by the agent or user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
