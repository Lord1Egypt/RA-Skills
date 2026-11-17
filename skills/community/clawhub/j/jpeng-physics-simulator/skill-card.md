## Description:

Simulate physics experiments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to run physics-related simulation tasks and science operations through command-line workflow guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact asks for SIMULATION_API_KEY without identifying the external service or how submitted data is handled.

Mitigation: Use a test credential only after review, and avoid sensitive experiment inputs until the publisher documents the service, data flow, and activation scope.

Risk: The usage command references scripts/physics_simulator.py, but that script is not present in the artifact.

Mitigation: Treat the release as incomplete until the publisher supplies the missing script or updates the documentation to match the shipped files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-physics-simulator)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON result shape]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMULATION_API_KEY; the referenced simulator script is not present in the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
