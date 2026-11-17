## Description:

Parse YAML/JSON/TOML front-matter from strings or files using the gray-matter library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content engineers use this skill to parse, inspect, strip, add, and stringify front-matter in Markdown and related content files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First use may download and install the gray-matter package from the configured npm registry automatically.

Mitigation: Review before installing, prefer pinned dependencies, and run the skill in an environment where npm registry access and installed packages are controlled.

Risk: Automatic dependency installation can change the local environment and execute newly downloaded code.

Mitigation: Use a preinstalled, reviewed dependency set or update the skill to fail with setup instructions instead of running npm install during parsing.

## Reference(s):

- [gray-matter API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read files or stdin and can emit parsed front-matter data, stripped content, boolean test results, excerpts, or stringified front-matter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
