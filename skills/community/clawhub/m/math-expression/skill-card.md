## Description:

Evaluates single Wolfram Language expressions for symbolic math, calculus, high-precision numeric computation, linear algebra, series, asymptotics, and differential equations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pansuestc](https://clawhub.ai/user/pansuestc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to translate math-focused requests into one Wolfram Language expression, evaluate it, and return exact, numeric, verification, and version details. It is intended for concrete mathematical manipulation, not general code execution or business calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wolfram expression evaluation can expose local file, process, and network capabilities through an incomplete safety gate.

Mitigation: Run only in an isolated environment with no sensitive files, credentials, or unrestricted network access available to WolframKernel.

Risk: Unsafe Wolfram symbols can be allowed with the --allow-unsafe option.

Mitigation: Keep the default safety blocking enabled and do not expose --allow-unsafe to ordinary user requests.

Risk: Dependency behavior can vary when runtime packages are not pinned.

Mitigation: Prefer pinned dependencies and review the installed Wolfram and wolframclient versions before deployment.

## Reference(s):

- [Math Expression ClawHub skill page](https://clawhub.ai/pansuestc/skills/math-expression)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or text containing Wolfram Language expressions, exact results, numeric approximations, verification status, and Wolfram version details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on Python 3, wolframclient, and a locally available WolframKernel.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
