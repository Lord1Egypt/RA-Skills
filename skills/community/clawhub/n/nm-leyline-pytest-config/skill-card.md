## Description:

Provides standardized pytest config, reusable fixtures, and CI integration patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up or audit pytest infrastructure for Python projects, including pytest configuration, reusable fixtures, test markers, coverage settings, and CI patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CI workflow examples may introduce broad triggers or unintended coverage upload.

Mitigation: Review generated GitHub Actions workflows before committing them and remove Codecov unless external coverage upload is intended.

Risk: Unpinned GitHub Actions examples can drift as upstream actions change.

Mitigation: Consider pinning GitHub Actions to commit SHAs when adopting the workflow examples.

Risk: The sample GitRepository.add_file helper can write paths supplied by tests.

Mitigation: Harden the helper before using it with untrusted test input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-pytest-config)
- [ClawHub publisher profile](https://clawhub.ai/user/athola)
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TOML, Python, YAML, Makefile, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces pytest configuration patterns, fixture templates, CI workflow examples, and review guidance for Python test infrastructure.]

## Skill Version(s):

1.9.19 (source: server release evidence; artifact frontmatter reports 1.9.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
