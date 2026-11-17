## Description:

Validate PostCSS config files (.postcssrc, postcss.config.js, package.json#postcss) for plugin ordering, deprecated plugins, Tailwind integration, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate and audit PostCSS configuration files for frontend build pipelines, including plugin ordering, deprecated plugins, Tailwind integration, parser settings, and CI-friendly pass/fail checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validator reads local PostCSS-related configuration files selected by the agent or user.

Mitigation: Run it only against intended project config files and avoid passing unrelated files that may contain sensitive local data.

Risk: JavaScript and TypeScript PostCSS configs are detected but cannot be statically validated.

Mitigation: Use JSON-based PostCSS configuration for full validation or manually review JS/TS configs before relying on the result.

Risk: Validation findings and suggestions may be incomplete or need project-specific interpretation.

Mitigation: Review findings before changing build configuration or enforcing results in CI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/postcss-config-validator)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; validator results can be text, JSON, or summary output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CI-friendly exit codes: 0 for no errors, 1 for one or more errors, and 2 for file not found or invalid input]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
