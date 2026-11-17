## Description:

jyml helps agents convert YAML and JSON files with the jyml CLI, including file output, custom output paths, indentation, and structured JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waldekmastykarz](https://clawhub.ai/user/waldekmastykarz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need an agent to convert YAML and JSON configuration files, API specs, workflow files, or API responses with the jyml command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running the jyml npm package, especially through unpinned npm or npx commands, executes third-party code.

Mitigation: Verify the intended jyml package and version before use, prefer pinned npm exec commands such as npm exec --package=jyml@<version>, and use isolation when converting sensitive configuration files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/waldekmastykarz/skills/jyml)
- [Publisher profile](https://clawhub.ai/user/waldekmastykarz)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce converted YAML or JSON files through the jyml CLI, or structured JSON to stdout when using --json.]

## Skill Version(s):

0.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
