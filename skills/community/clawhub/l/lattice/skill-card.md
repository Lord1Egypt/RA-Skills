## Description: <br>
Initialize and manage Lattice organizations, a file-based operating system for AI agent teams that supports stable, long-running iterative development through an 8-phase pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CNF6682](https://clawhub.ai/user/CNF6682) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent-team operators use Lattice to scaffold file-backed organizations, departments, projects, and pipeline state for long-running multi-agent development work. It is intended for workflows that need persistent project memory, phased execution, model escalation, peer consultation, and cron-scheduled orchestration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous cron-driven pipeline activity can modify the selected repository over time. <br>
Mitigation: Use a dedicated repository path, review the generated PIPELINE_STATE.json and cron schedule, and keep human review around sensitive changes. <br>
Risk: Pipeline files and organization memory can accidentally capture sensitive operational details. <br>
Mitigation: Keep secrets out of ORG and pipeline files, and review generated organization and project files before use. <br>
Risk: Peer consult and auto-triage may make unsuitable decisions for sensitive work. <br>
Mitigation: Disable or tighten peer consult and auto-triage when confidentiality, compliance, or high-impact changes require stricter human control. <br>


## Reference(s): <br>
- [Lattice ClawHub release](https://clawhub.ai/CNF6682/lattice) <br>
- [Pipeline framework design](artifact/templates/ORG/PROJECTS/pipeline-framework/DESIGN.md) <br>
- [Pipeline guide](artifact/templates/ORG/PIPELINE_GUIDE.md) <br>
- [Pipeline guide for sub-agents](artifact/templates/ORG/PROJECTS/pipeline-framework/templates/PIPELINE_GUIDE_FOR_SUBAGENTS.md) <br>
- [Orchestrator prompt template](artifact/templates/ORG/PROJECTS/pipeline-framework/templates/ORCHESTRATOR_PROMPT.template.md) <br>
- [Pipeline state template](artifact/templates/ORG/PROJECTS/pipeline-framework/templates/PIPELINE_STATE.template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates, JSON configuration, and operational instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scaffolded organization and project files, pipeline state configuration, cron setup instructions, and concise status summaries.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
