## Description: <br>
Transforms project briefs into testable specifications with user stories and acceptance criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill after brainstorming to turn a project brief into a specification with requirements, user stories, acceptance criteria, and scope boundaries before planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may create or update docs/specification.md. <br>
Mitigation: Review the generated specification before using it as implementation input. <br>
Risk: The workflow may automatically continue into the planning phase after specification completion. <br>
Mitigation: Use --standalone or explicitly ask the agent to stop after specification when planning should not start. <br>


## Reference(s): <br>
- [Attune plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-attune-project-specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown specification guidance and saved documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update docs/specification.md and continue into the planning phase unless run standalone or explicitly stopped.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
