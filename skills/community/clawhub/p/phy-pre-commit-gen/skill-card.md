## Description:

Generates a tailored .pre-commit-config.yaml by analyzing a project's language stack, existing linting tools, CI setup, and current pre-commit configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate or audit pre-commit configurations that match the languages, formatters, linters, security hooks, and CI signals present in a project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated configuration can change a repository's pre-commit behavior or overwrite an existing .pre-commit-config.yaml when explicitly requested.

Mitigation: Run with --dry-run first, keep the default output path unless a broader path is intentional, and use --overwrite only after reviewing the current file.

Risk: Generated hook repositories and autoupdate results may introduce unwanted checks or CI failures if accepted without review.

Mitigation: Review generated hook repos and pre-commit autoupdate diffs before running hooks across all files or enabling them in CI.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-pre-commit-gen)
- [Publisher Profile](https://clawhub.ai/user/phy041)
- [Canlah AI Homepage](https://canlah.ai)
- [pre-commit Documentation](https://pre-commit.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print a dry-run preview, write .pre-commit-config.yaml, or emit audit findings for an existing pre-commit configuration.]

## Skill Version(s):

1.0.3 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
