## Description: <br>
Guides OpenClaw agents to continuously advance optimization and multi-step project work through planning, progress reporting, verification, and closure rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KarasawaYikiho](https://clawhub.ai/user/KarasawaYikiho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to keep OpenClaw agents moving through multi-step optimization, project, and troubleshooting tasks until there is a verified outcome or a clearly stated blocker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad continuous-work triggers can cause an agent to keep editing or optimizing beyond the user's intended scope. <br>
Mitigation: Specify the exact target directory and desired stopping condition before invoking the skill. <br>
Risk: Optimization workflows may include file changes, generated reports, and broad rewrites. <br>
Mitigation: Require a plan before edits and explicit approval before deletions or large rewrites. <br>
Risk: The skill's completion rules can keep the agent active after technical work is complete. <br>
Mitigation: Tell the agent to stop after the final summary when no further follow-up is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KarasawaYikiho/openclawcontinuouswork) <br>
- [Reference Map](References/ReferenceMap.md) <br>
- [General Continuous Work Rules](References/GeneralRules.md) <br>
- [Continuous Execution Directive](References/ContinuousExecutionDirective.md) <br>
- [Optimization Rules](References/OptimizationRules.md) <br>
- [Optimization Directive](References/OptimizationDirective.md) <br>
- [Optimization Checklist](References/OptimizationChecklist.md) <br>
- [Acceptance Template](References/AcceptanceTemplate.md) <br>
- [Quality Scoring Rubric](References/QualityRubric.md) <br>
- [Module System](References/ModuleSystem.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with optional shell commands, generated reports, JSON configuration, and Python utility script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update skill reference files and generated reports when an agent follows the optimization workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
