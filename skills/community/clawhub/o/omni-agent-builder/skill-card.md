## Description: <br>
Builds OpenClaw agent workspaces and multi-agent teams with secure defaults, workspace files, memory workflow guidance, evaluation prompts, and CLI setup support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ollieb89](https://clawhub.ai/user/ollieb89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to design or iterate on OpenClaw agent workspaces, including single-agent and Planner/Executor/Critic multi-agent setups. It helps produce workspace files, safety guardrails, memory rules, and acceptance tests for local agent deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the scaffold in an existing directory can overwrite generated workspace files. <br>
Mitigation: Run the scaffold only in a fresh or backed-up directory and review generated files before use. <br>
Risk: Memory files can capture private preferences, project details, or other sensitive context if users do not set boundaries. <br>
Mitigation: Define privacy rules for MEMORY.md and daily logs, avoid storing credentials or private keys, and do not load private memory in group or shared-channel contexts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ollieb89/omni-agent-builder) <br>
- [OpenClaw Workspace Reference](artifact/references/openclaw-workspace.md) <br>
- [Workspace Templates Reference](artifact/references/templates.md) <br>
- [Agent Architecture Reference](artifact/references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with fenced workspace file contents and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a directory tree and installation notes when packaging a generated workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
