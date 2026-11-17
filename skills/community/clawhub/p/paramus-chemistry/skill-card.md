## Description:

Hundreds of chemistry and scientific computing tools. Molecular weight, LogP, TPSA, SMILES validation, thermodynamics, polymer analysis, electrochemistry, DOE, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gressling](https://clawhub.ai/user/gressling)

### License/Terms of Use:


## Use Case:

Developers, researchers, and chemistry-focused users use this skill to route chemistry, molecular property, thermodynamics, materials science, electrochemistry, and scientific computing questions through Paramus tools and return calculated results with units.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chemistry inputs may be sent to Paramus cloud services when local processing is unavailable.

Mitigation: Prefer the local Paramus app for proprietary or regulated formulas, and confirm user consent before cloud calls.

Risk: The PARAMUS_API_TOKEN credential can be exposed through under-scoped connection flows or mishandling.

Mitigation: Protect and rotate the token, avoid printing it in logs or chat, and use it only for the intended Paramus cloud endpoint.

Risk: An unauthenticated localhost service could be impersonated by another local process.

Mitigation: Confirm the local Paramus app is running before relying on localhost responses.

## Reference(s):

- [Paramus Cloud](https://cloud1.paramus.ai)
- [ClawHub skill page](https://clawhub.ai/gressling/skills/paramus-chemistry)
- [Publisher profile](https://clawhub.ai/user/gressling)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured calculation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API setup guidance, JSON-RPC request examples, calculated values, units, and privacy notes.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
