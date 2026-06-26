## Description: <br>
Complete development workflow suite from Y Combinator CEO Garry Tan's gstack that routes gstack commands to specialized workflows for product ideation, code review, testing, QA, and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsg12te-del](https://clawhub.ai/user/dsg12te-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to choose and run a gstack workflow for product planning, code review, QA, release preparation, and related software delivery tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad user phrases may be routed into code-changing or release workflows without strong upfront consent boundaries. <br>
Mitigation: Prefer explicit slash commands and require confirmation before edits, merges, pushes, PR creation, deployment, or other release steps. <br>
Risk: The skill may inspect git state and propose or apply code changes. <br>
Mitigation: Review generated diffs and commands before execution, and run project tests before accepting changes. <br>
Risk: Workflow context may be saved locally under .workbuddy/gstack-state. <br>
Mitigation: Review or clear .workbuddy/gstack-state when the project contains sensitive plans, code context, or customer information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dsg12te-del/gstack-skills) <br>
- [Publisher profile](https://clawhub.ai/user/dsg12te-del) <br>
- [Original gstack project referenced by the skill](https://github.com/garrytan/gstack) <br>
- [Y Combinator reference](https://www.ycombinator.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and reports with optional code blocks, shell commands, and JSON routing or workflow-state output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect git state, route slash commands to specialized skills, and write local workflow state under .workbuddy/gstack-state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog text reference 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
