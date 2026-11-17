## Description: <br>
NeuroCache Pro helps agents use a local associative memory layer with spreading activation, Hebbian reinforcement, contradiction handling, snapshots, and cross-project memory transfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add persistent associative memory for recalling project decisions, tracing causal links, identifying conflicting memories, and moving selected context across projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local memory layer can retain project and user context across sessions. <br>
Mitigation: Avoid storing secrets, credentials, regulated data, or confidential client information in the memory store. <br>
Risk: Cross-project memory transplant can move sensitive or irrelevant context into another project. <br>
Mitigation: Review transplant filters and selected memories before using migrated context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/neurocache-pro) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to install, configure, query, maintain, snapshot, and migrate a local neural-memory store.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
