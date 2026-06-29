## Description: <br>
Use when the user wants to create Caliper evals for a skill, iterate on a skill using evals, or run the full create-to-test-to-improve cycle for a skill they want to measure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edonadei](https://clawhub.ai/user/edonadei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create Caliper evaluation specs, add missing coverage to existing evals, run validation and test passes, and iterate until a skill is ready to ship. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or updated eval YAML can include setup, cleanup, and assert commands that run against local files. <br>
Mitigation: Review generated evals and command blocks before allowing writes or Caliper runs. <br>
Risk: Running evals against a target skill may touch sensitive files or credentials if the target skill or eval is configured that way. <br>
Mitigation: Run evals in a controlled workspace and avoid exposing credentials or sensitive paths to the target skill. <br>


## Reference(s): <br>
- [Grill Skill Reference](artifact/REFERENCE.md) <br>
- [ClawHub skill page](https://clawhub.ai/edonadei/skills/grill-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with YAML eval specifications and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Caliper .eval.yaml files beside the target skill and report Caliper validation or run results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
