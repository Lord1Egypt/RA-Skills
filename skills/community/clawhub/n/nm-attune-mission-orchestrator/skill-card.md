## Description: <br>
Orchestrates full project lifecycle by auto-detecting state and routing to the correct phase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to start or resume project work across brainstorming, specification, planning, and execution phases with state detection, phase routing, checkpoints, and recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish GitHub issues, modify project files, and guide automated workflow changes. <br>
Mitigation: Use it only in repositories where those changes are acceptable, and require manual review before any external-facing GitHub issue is published. <br>
Risk: The skill can reduce review checkpoints based on casual natural-language phrases or auto behavior. <br>
Mitigation: Avoid enabling auto behavior unless checkpoint skipping is understood, and review the selected constraint profile before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-attune-mission-orchestrator) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, JSON examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide project file changes, .attune state updates, plan-review artifacts, and dependent skill invocations.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
