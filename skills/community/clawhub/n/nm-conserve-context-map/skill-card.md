## Description:

Generates a compressed project context map to avoid expensive Read/Grep calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill at the start of a session or before feature work to summarize repository structure, dependencies, entry points, imports, routes, environment variables, and high-blast-radius files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented scanner command can execute Python code from the repository being scanned, which is unsafe for untrusted repositories.

Mitigation: Use the skill only on repositories you trust, or change the invocation to use a fixed, verified scanner path outside the target project.

Risk: The scanner may generate .codesight/ files during analysis.

Mitigation: Review or disable .codesight/ file generation when read-only analysis is required.

Risk: Broad automatic activation can run the scanner in contexts where repository trust has not been established.

Mitigation: Narrow triggers or require explicit user confirmation before running the scanner on unfamiliar projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conserve-context-map)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown project overview or JSON scanner output, with optional .codesight Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports section-specific output, blast-radius checks, token-budget limiting, cache control, and optional wiki article generation.]

## Skill Version(s):

1.9.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
