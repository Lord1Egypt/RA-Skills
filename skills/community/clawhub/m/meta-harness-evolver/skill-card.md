## Description: <br>
Meta-Harness Evolver runs an OpenClaw outer loop that proposes, evaluates, logs, and reports candidate changes to an agent harness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tylerdotai](https://clawhub.ai/user/tylerdotai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw agent harnesses use this skill to run scheduled or manual outer-loop experiments that propose harness edits, score them against benchmark scenarios, preserve traces, and report results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically alter live OpenClaw operating files. <br>
Mitigation: Evaluate candidates in an isolated workspace copy and require human approval before applying changes to live harness files. <br>
Risk: The Discord reporter may send internal evolution details outside the local workspace. <br>
Mitigation: Review and gate the Discord reporting step before enabling scheduled runs. <br>
Risk: Benchmark scores are heuristic and may not predict real task quality. <br>
Mitigation: Treat scores as decision support and review candidate traces before promoting a harness. <br>


## Reference(s): <br>
- [Harness Spec](references/harness-spec.md) <br>
- [Benchmark Design](references/benchmark-design.md) <br>
- [Evolution Logic](references/evolution-logic.md) <br>
- [ClawHub Release Page](https://clawhub.ai/tylerdotai/meta-harness-evolver) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, JSON scores, execution traces, and candidate harness configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes evolution artifacts under ~/hoss-evolution/ and may post a Markdown summary to Discord when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
