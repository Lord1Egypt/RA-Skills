## Description: <br>
Trajectory compiler that converts real OpenClaw session traces or raw trajectory logs into a parameterized, reusable Skill via trace interception, DAG abstraction, schema and code synthesis, and registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[la1850](https://clawhub.ai/user/la1850) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert concrete OpenClaw tool-use traces into reusable parameterized Skills with generated schemas, run plans, executable scripts, and documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process real local OpenClaw session history and persist derived executable Skills. <br>
Mitigation: Use a narrow session or time window, inspect and redact traces before compilation, and avoid traces containing secrets, customer data, financial or account actions, or public-posting workflows. <br>
Risk: Generated schemas, plans, and run scripts may encode sensitive values or unsafe behavior from the original trace. <br>
Mitigation: Compile first to a temporary staging directory and review the generated schema, plan, run-flow, and run.js before copying or refreshing the generated Skill into an active Skills directory. <br>


## Reference(s): <br>
- [Meta-Skill ClawHub Page](https://clawhub.ai/la1850/meta-skill) <br>
- [Pipeline](references/pipeline.md) <br>
- [Trajectory Compiler Spec](references/compiler-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Generated Skill files, JSON schemas, Markdown run-flow documentation, and executable JavaScript scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a generated skill identifier, schema preview, and run-flow path; generated artifacts should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
