## Description:

Use when a task broadly involves Halo CLI and the correct command area is not yet clear, or when shared rules are needed for profiles, JSON output, help discovery, config paths, and destructive actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruibaby](https://clawhub.ai/user/ruibaby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when working with Halo CLI and they need a shared starting point for command discovery, profile handling, JSON output, configuration paths, authentication expectations, and routing to more specific Halo CLI skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing @halo-dev/cli globally without a pinned package version.

Mitigation: Verify the package source and pin a reviewed version or install in a controlled environment before using it.

Risk: Halo authentication creates local profiles and stores credentials in the system keyring.

Mitigation: Use profiles only for trusted Halo instances and review profile selection before running authenticated commands.

Risk: Some non-interactive dangerous commands may require --force.

Mitigation: Read command-specific help and review the target profile, site, and action before using --force.

## Reference(s):

- [Halo website](https://www.halo.run)
- [ClawHub skill page](https://clawhub.ai/ruibaby/skills/halo-cli-shared)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI option names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes the halo binary is available and may recommend JSON output for automation.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
