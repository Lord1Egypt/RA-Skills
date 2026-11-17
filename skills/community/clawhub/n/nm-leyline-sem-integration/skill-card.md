## Description:

Provides sem semantic-diff detection, install-on-first-use, and fallback patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building or maintaining skills that consume git diffs use these patterns to detect sem, offer installation, and normalize semantic or standard git diff output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the optional sem CLI runs a third-party tool installation command.

Mitigation: Review the installation source and use the documented standard git diff fallback if you prefer not to install sem.

## Reference(s):

- [sem project](https://github.com/Ataraxy-Labs/sem)
- [Leyline plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-leyline-sem-integration)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides sem detection, installation options, and git diff fallback patterns.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
