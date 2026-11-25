## Description:

Audit only the dependencies a pull request adds — typosquats and lookalike package names, packages that do not exist on npm or PyPI, newborn or barely-downloaded packages, and dependencies added but never imported. Use when asked to check, review or gate a PR's new dependencies in package.json, requirements.txt, pyproject.toml or package-lock.json, when reviewing dependency changes before merging, or when a PR adds a suspicious-looking package name. Not for auditing dependencies a project already has (only added ones are checked), for scanning AI-agent skills (use skillscan), or for checking workflow run: commands (use ci-command-truth).

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to review dependencies newly introduced by a pull request before merging. It checks registry evidence, package age and download activity, name similarity, and whether the added dependencies are imported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented pip, pipx, and uv install commands fetch the tool from an unpinned Git repository, creating a supply-chain exposure.

Mitigation: Review and use a specific reviewed commit, and limit the repository access, permissions, and credentials available during installation and use.

## Reference(s):

- [PhantomDep PR Gate on ClawHub](https://clawhub.ai/raktikoo/skills/phantomdep-pr-gate)
- [PhantomDep installation and source repository (as listed by the skill)](https://github.com/RakTikoo/phantomdep-pr-gate)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Dependency audit report in JSON or PR-comment Markdown, with command-line verdicts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are based on added dependencies; offline registry values remain unknown unless registry fixtures are supplied.]

## Skill Version(s):

0.3.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
