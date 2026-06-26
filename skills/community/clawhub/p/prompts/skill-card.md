## Description: <br>
Deep prompt engineering workflow--task spec, constraints, examples, evaluation sets, iteration protocol, regression testing, and safety alignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and teams shipping LLM workflows use this skill to define prompt success criteria, specify constraints and output formats, build evaluation sets, iterate prompt changes, and monitor regressions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt eval sets, production logs, and monitored outputs may contain sensitive user or business data. <br>
Mitigation: Apply normal privacy controls to eval data, logs, and monitoring outputs, and review any shared artifacts for sensitive content. <br>
Risk: Prompt changes can introduce quality regressions, omissions, or misleading outputs if shipped without evaluation. <br>
Mitigation: Use the skill's staged workflow to define success criteria, freeze evaluation cases, run regressions, and canary prompt changes before broad rollout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawkk/prompts) <br>
- [Publisher profile](https://clawhub.ai/user/clawkk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with checklists, rubrics, and prompt-engineering workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of prompt templates, evaluation criteria, and monitoring checklists; does not install code, hooks, credentials, or privileged actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
