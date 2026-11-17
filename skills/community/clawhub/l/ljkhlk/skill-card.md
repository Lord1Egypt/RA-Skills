## Description:

Analyze test coverage gaps by comparing test files against source modules to identify untested code paths and critical functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jk625x](https://clawhub.ai/user/jk625x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare source modules with tests, identify untested public paths, and prioritize coverage gaps by risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests shell capability even though the inspected instructions describe a coverage-reporting workflow that mainly requires reading project files.

Mitigation: Install only if shell access is acceptable, or ask the publisher to remove shell permission and keep the skill to read-only filesystem access.

Risk: Coverage-gap findings may be incomplete when a project uses test naming conventions or exported APIs outside the documented patterns.

Mitigation: Review the generated report against the repository's actual test runner, coverage configuration, and module conventions before acting on the suggested gaps.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown coverage gap report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sorted by risk level with source files, untested exports, and suggested test outlines.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
