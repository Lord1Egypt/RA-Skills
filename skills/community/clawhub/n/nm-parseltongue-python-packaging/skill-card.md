## Description:

Python package creation and PyPI distribution via pyproject.toml and entry points

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create and maintain distributable Python libraries and command-line tools. It provides guidance for project configuration, dependencies, entry points, build workflows, CI, and PyPI publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing to PyPI makes the built package contents public.

Mitigation: Review the built package contents before publishing; use TestPyPI when you need to verify a release first.

Risk: The cleanup example removes the build/ and dist/ directories.

Mitigation: Check those directories and confirm their contents are disposable before running the cleanup command.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/parseltongue)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Shell commands]

**Output Format:** [Markdown with Python, TOML, YAML, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and step-by-step packaging workflows]

## Skill Version(s):

1.10.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
