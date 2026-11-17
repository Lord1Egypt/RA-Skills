## Description:

Automated Planning utilities for loading PDDL domains and problems, generating plans using classical planners, validating plans, and saving plan outputs, with support for standard PDDL parsing, plan synthesis, and correctness verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and planning engineers use this skill to build reproducible PDDL benchmark workflows that load domain and problem files, synthesize a classical plan, validate goal satisfaction, and save plan outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-selected PDDL files and can write a plan file to a chosen output path.

Mitigation: Run it in a constrained workspace and review the output path before saving generated plans.

Risk: The provided artifact references proprietary LICENSE.txt terms that were not included in the evidence, while server release metadata reports MIT-0.

Mitigation: Confirm the exact release license and any referenced terms before deployment or redistribution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Code, Guidance, Files]

**Output Format:** [Markdown with inline Python examples and plan-file output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-selected PDDL files and write a plan file to the requested output path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
