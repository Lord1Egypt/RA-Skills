## Description:

The Clawhub OctoFlow skill helps agents use OctoFlow for GPU-accelerated computation, data analysis, media processing, machine learning tasks, and natural-language generation of Vulkan-backed GPU programs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikedconcepcion](https://clawhub.ai/user/mikedconcepcion)

### License/Terms of Use:

MIT

## Use Case:

Developers and technical agents use this skill to run GPU-oriented OctoFlow commands, configure OctoFlow as an MCP server, and produce data analysis, image processing, machine learning, and GPU compute workflows from natural-language task descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a native OctoFlow binary.

Mitigation: Install only from a trusted OctoFlow release source and verify the exact platform artifact hash before use.

Risk: Examples can grant broad local file access when using permission flags such as --allow-read=. or --allow-write=.

Mitigation: Prefer exact --allow-read and --allow-write paths or a dedicated task directory instead of granting access to the full working directory.

Risk: OctoFlow can save local preferences and corrections under user-level or project-level memory paths.

Mitigation: Use --no-memory when local preference or correction storage is not desired.

Risk: Running the MCP server makes OctoFlow available as a long-running agent tool.

Mitigation: Enable the MCP server deliberately and only in environments where long-running tool access is expected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mikedconcepcion/skills/octoflow)
- [OctoFlow Documentation](https://octoflow-lang.github.io/octoflow/)
- [OctoFlow GitHub Repository](https://github.com/octoflow-lang/octoflow)
- [OctoFlow v1.5.8 GitHub Release Downloads](https://github.com/octoflow-lang/octoflow/releases/download/v1.5.8/)
- [OctoFlow v1.5.8 SHA256SUMS](https://github.com/octoflow-lang/octoflow/releases/download/v1.5.8/SHA256SUMS.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and OctoFlow code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local OctoFlow execution, MCP server configuration, file permission flags, and hash-verification steps.]

## Skill Version(s):

1.5.8 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
