## Description: <br>
Converts a specification into a phased, dependency-ordered implementation plan for use after specification is complete and before execution begins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn completed specifications into architecture notes, task breakdowns, dependency ordering, acceptance criteria, estimates, sprint plans, and implementation risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically continue from planning into an execution phase without asking for confirmation. <br>
Mitigation: Use `--standalone` or explicitly tell the agent to stop after creating `docs/implementation-plan.md` when only planning output is desired. <br>
Risk: Generated plans may contain incorrect architecture assumptions, task dependencies, estimates, or acceptance criteria. <br>
Mitigation: Review the implementation plan before execution and confirm dependencies, risk mitigations, and acceptance criteria against the original specification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-attune-project-planning) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown planning document with task lists, dependency notes, acceptance criteria, estimates, and inline command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save an implementation plan to docs/implementation-plan.md and continue to an execution phase unless the user requests standalone planning or stops after planning.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
