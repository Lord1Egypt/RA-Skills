## Description: <br>
Runs autonomous iterative delivery loops for coding tasks using plan -> execute -> check -> review -> commit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[melonlee](https://clawhub.ai/user/melonlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Hepha when they explicitly want an agent to run small autonomous implementation loops, maintain planning artifacts, validate changes, and commit each verified sub-task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous coding loops can make broad project changes or commits if the requested scope is unclear. <br>
Mitigation: Run on a dedicated branch or disposable worktree, define files in scope, and review .autopilot artifacts and generated commits before pushing. <br>
Risk: Web or browser validation may touch authenticated sessions or network resources during research and review. <br>
Mitigation: Set clear limits for network use, authenticated browser sessions, and stop conditions before enabling the skill. <br>


## Reference(s): <br>
- [Planning Task Decomposition](references/planning_task-decomposition.md) <br>
- [Validation Quality Gates](references/validation_quality-gates.md) <br>
- [Decomposition Patterns](references/decomposition-patterns.md) <br>
- [Progress Template](references/progress-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/melonlee/hepha-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status updates and project-local files, with code edits, shell commands, validation notes, and Git commits when checks pass.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates .autopilot backlog, progress, and decision-log artifacts during autonomous loops.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
