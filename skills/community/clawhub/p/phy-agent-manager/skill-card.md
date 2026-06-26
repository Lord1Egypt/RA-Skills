## Description: <br>
Meta-orchestrator that analyzes tasks and creates execution plans using subagents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to classify complex work, choose suitable subagents, and produce a staged execution plan before approving follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated plans may recommend file changes, security review, or subagent activity that affects project data. <br>
Mitigation: Review each generated plan and approve only the phases and subagent prompts that fit the task and data-access expectations. <br>
Risk: Planning output can be incomplete or misclassify task complexity and risk. <br>
Mitigation: Check the classification, selected agents, and checkpoints before using the plan to guide execution. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/PHY041/phy-agent-manager) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with tables, checkpoints, and inline command prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning guidance only; users review the plan before approving execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
