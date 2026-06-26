## Description: <br>
Guides agents working in the PPTAgent or BotSlide repository on slide generation, editing, export fidelity, preview behavior, prompt rules, and project versioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mrguanglei](https://clawhub.ai/user/Mrguanglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when modifying or debugging the PPTAgent/BotSlide repository, especially changes to fixed-size slide generation, HTML-to-PPTX export, preview flows, editing behavior, and project version APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation commands may install dependencies, start services, run Docker, or expose a development service on 0.0.0.0. <br>
Mitigation: Confirm the repository working directory and review Docker, pip, pnpm, Playwright, and uvicorn commands before execution. <br>
Risk: Slide-generation changes can break the 1280x720 fixed-canvas assumption or reduce HTML-to-PPTX export fidelity. <br>
Mitigation: Keep fixed slide dimensions and export constraints in scope, and validate with targeted preview or PPTX export checks when those paths are affected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mrguanglei/ppt-collab) <br>
- [Project map](references/project-map.md) <br>
- [Slide rules](references/slide-rules.md) <br>
- [Validation workflow](references/validation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify the changed layer, explain why the change belongs there, and include the smallest relevant validation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
