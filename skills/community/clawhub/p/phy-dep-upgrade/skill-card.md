## Description:

Dependency audit and upgrade planner for Node.js, Python, Rust, Go, and Ruby projects that scans for outdated packages, vulnerability CVEs, and breaking changes, then produces a prioritized upgrade plan with exact commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit dependency health across Node.js, Python, Rust, Go, and Ruby projects and plan vulnerability fixes or safe package upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit and outdated-check commands may contact package registries or other networked dependency sources.

Mitigation: Review commands before running them and treat audit results as dependent on the configured package registries and local package manager behavior.

Risk: Fix or upgrade commands can rewrite lockfiles, dependency manifests, or installed packages.

Mitigation: Commit or otherwise back up the project before applying changes, then rerun audits and tests after each upgrade batch.

Risk: Helper tools such as npm-check-updates, pip-audit, cargo-audit, govulncheck, and bundler-audit may be installed or executed from package ecosystems.

Mitigation: Prefer trusted local installations and pinned versions for helper tools before relying on their output or generated commands.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-dep-upgrade)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown report with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized severity sections, CVE details, breaking-change notes, and copy-pasteable package manager commands.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
