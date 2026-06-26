## Description: <br>
Use Nate Jones OB1 Agent Memory from OpenClaw with provenance, scope, review, and use-policy discipline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[natebjones](https://clawhub.ai/user/natebjones) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect OpenClaw tasks to OB1 persistent memory while preserving scope, provenance, review status, and usage reporting. It guides recall before meaningful work and compact write-back after completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory write-back may retain sensitive project, customer, credential, transcript, or large-code details if agents store too much information. <br>
Mitigation: Confirm storage and retention expectations before sensitive work, keep project scoping enabled, and write only compact summaries with source references. <br>
Risk: Recalled memory may be stale, inferred, conflicting, or outside the appropriate project or team scope. <br>
Mitigation: Use project-scoped recall by default, exclude unconfirmed memory unless needed, respect each memory's use_policy, and ask for confirmation when conflicts matter. <br>
Risk: Agent-written memories could become hidden instructions if promoted before review. <br>
Mitigation: Treat agent-written memories as evidence by default and promote decision memories to instruction only when user-confirmed or imported from a trusted source. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with tool names and structured workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recall, write-back, review, and reporting guidance for agents using OB1 memory tools.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and artifact metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
