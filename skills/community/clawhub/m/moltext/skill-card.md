## Description:

Compile legacy documentation on internet into agent-native memory context using the Moltext.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uditakhourii](https://clawhub.ai/user/uditakhourii)

### License/Terms of Use:


## Use Case:

Developers and agents use Moltext to compile large web documentation sources into dense Markdown context for tool, library, or application learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run a mutable npm CLI.

Mitigation: Review before installing, use a sandbox or project-local install, and pin and verify the moltext package version.

Risk: Compiled documentation may introduce untrusted or misleading content into agent context.

Mitigation: Fetch only trusted HTTPS documentation and inspect generated files before using them as reference material.

Risk: Command-line usage may expose sensitive values or write generated context to unintended paths.

Mitigation: Choose output paths carefully and avoid passing API keys directly on the command line.

## Reference(s):

- [Moltext GitHub repository](https://github.com/UditAkhourii/moltext)
- [OpenClaw documentation](https://docs.molt.bot/)
- [ClawHub Moltext skill page](https://clawhub.ai/uditakhourii/skills/moltext)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown context files from fetched documentation.]

## Skill Version(s):

1.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
