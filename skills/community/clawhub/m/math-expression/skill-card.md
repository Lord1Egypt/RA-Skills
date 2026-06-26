## Description: <br>
Evaluates math-only Wolfram Language expressions for symbolic algebra, calculus, linear algebra, series, asymptotics, exact values, high-precision numerics, and ODE/PDE solutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pansuestc](https://clawhub.ai/user/pansuestc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to translate a concrete math request into one Wolfram Language expression, evaluate it locally, and return exact, numeric, verification, and Wolfram version details. It is intended for math-only tasks, not general programming-language expression evaluation or business calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expressions are evaluated by a local WolframKernel and depend on the local Python wolframclient package. <br>
Mitigation: Install the dependency from a trusted source and run the skill only with a trusted local WolframKernel. <br>
Risk: The optional unsafe mode can allow filesystem, network, or process-related Wolfram symbols. <br>
Mitigation: Keep the default safety guard enabled for normal use and use --allow-unsafe only with trusted input in an isolated environment. <br>
Risk: Using the skill outside math-only expressions can produce misleading or inappropriate results. <br>
Mitigation: Use it only for explicit mathematical evaluation, simplification, solving, or numeric approximation requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pansuestc/math-expression) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON describing exact results, numeric results, verification status, runtime version, warnings, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-expression evaluation with optional precision, timeout, JSON output, verification controls, and unsafe-symbol override.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
