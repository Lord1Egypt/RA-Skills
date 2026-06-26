## Description: <br>
Evaluates competing hypotheses with Occam's Razor to identify the simplest explanation that fits the scenario, using forensic, academic, or combined reasoning modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aleph23](https://clawhub.ai/user/aleph23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, investigators, and researchers use this skill to compare hypotheses, count assumptions, identify fallacies, and explain why one candidate explanation is more parsimonious than another. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may favor simpler explanations and underweight rare but important evidence in legal, forensic, medical, financial, or other high-stakes decisions. <br>
Mitigation: State constraints and evidence clearly, require domain expert review, and do not use the result as the sole basis for high-stakes decisions. <br>
Risk: A hypothesis can appear simpler because critical evidence was omitted or treated as irrelevant. <br>
Mitigation: Check that the preferred explanation accounts for all material observations and explicitly penalize assumptions that dismiss evidence without support. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aleph23/occams-razer-skill) <br>
- [Core reasoning instructions](references/instructions_core.md) <br>
- [Workflow logic](references/workflow_logic.yaml) <br>
- [Logical fallacies reference](references/fallacies.md) <br>
- [Example scenarios](references/example_scenarios.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured prose or JSON-style analysis with a preferred hypothesis, complexity analysis, rationale, and confidence score.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include assumption counts, fallacy checks, and confidence scoring for each hypothesis.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
