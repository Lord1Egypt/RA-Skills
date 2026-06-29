## Description: <br>
Orchestrates full project lifecycle by auto-detecting state and routing to the correct phase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to start, resume, or complete project workflows that move through brainstorming, specification, planning, and execution phases. It is best suited for structured project lifecycle orchestration, not single-phase code review, debugging, or research tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reduce oversight from ordinary autonomy phrases or auto-mode behavior. <br>
Mitigation: Run in supervised mode for sensitive work and avoid broad autonomy phrases unless reduced checkpoints are intended. <br>
Risk: The skill may create GitHub issues during backlog triage. <br>
Mitigation: Use --no-auto-issues unless remote issue creation is explicitly desired. <br>
Risk: The skill persists workflow state and history in .attune files, which may contain sensitive project context. <br>
Mitigation: Review .attune state and history files before committing, publishing, or sharing the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-attune-mission-orchestrator) <br>
- [Attune plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline command examples, generated project artifacts, and JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project documents, code, tests, GitHub issues, and .attune state/history files depending on mission phase and flags.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
