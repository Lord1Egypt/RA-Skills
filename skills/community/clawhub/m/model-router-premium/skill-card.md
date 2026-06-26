## Description: <br>
Route model requests based on configured models, costs and task complexity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrJootta](https://clawhub.ai/user/MrJootta) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to choose an appropriate LLM for a request from a configured model list, balancing task complexity, declared capabilities, caller preferences, and cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic routing may affect cost or send prompts to external providers listed in the model configuration. <br>
Mitigation: Review the models JSON before use and restrict it to approved providers and models. <br>
Risk: Heuristic routing may select a model that is too weak or too expensive for a task. <br>
Mitigation: Test routing behavior on representative tasks and tune model capabilities, cost scores, and caller overrides before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MrJootta/model-router-premium) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled router prints a selected model object and a short routing reason.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
