## Description:

Python package creation and PyPI distribution via pyproject.toml and entry points

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create Python libraries and command-line tools, configure projects with pyproject.toml and entry points, manage dependencies with uv, and prepare packages for PyPI distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing steps can make uploaded artifacts public.

Mitigation: Review the package contents and destination before running publishing steps.

Risk: The recursive cleanup command removes the build and distribution directories.

Mitigation: Confirm the working directory and intended directories before running the cleanup command.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-parseltongue-python-packaging)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python, TOML, YAML, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
