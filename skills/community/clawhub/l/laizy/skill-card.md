## Description: <br>
Orchestrate repo-native, supervised software delivery with the Laizy CLI. Use when a user wants to bootstrap or continue a multi-step coding run with explicit planning, replanning, implementation, recovery, verification, and closeout artifacts, especially in repos using Claude Code, Codex, OpenClaw, or similar coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaolonggao521](https://clawhub.ai/user/xiaolonggao521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Laizy to coordinate supervised multi-step coding runs in local repositories, including planning, implementation, recovery, verification, and closeout through Laizy CLI artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct agents to run commands and push repository changes without an explicit review gate. <br>
Mitigation: Use a feature branch, inspect generated plans and commands, and require explicit approval before commits, pushes, watchdog scheduling, or deletion of old run artifacts. <br>
Risk: Laizy-driven automation may widen repository changes if supervisor artifacts are ignored. <br>
Mitigation: Follow the emitted supervisor bundle and execute exactly one bounded milestone, recovery action, verification command, or closeout action at a time. <br>


## Reference(s): <br>
- [Laizy GitHub Repository](https://github.com/XiaolongGao521/Laizy) <br>
- [Laizy Decision Map](references/decision-map.md) <br>
- [Planner-Needed Bootstrap Template](references/planner-bootstrap.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON artifact references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces bounded next-action guidance based on Laizy supervisor artifacts; generated run and verification artifacts are treated as local repository state.] <br>

## Skill Version(s): <br>
0.3.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
