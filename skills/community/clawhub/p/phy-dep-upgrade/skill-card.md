## Description: <br>
Dependency audit and upgrade planner for Node.js, Python, Rust, Go, and Ruby projects that scans for outdated packages, vulnerability CVEs, and breaking changes, then produces a prioritized upgrade plan with exact commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit project dependencies across common package ecosystems, identify vulnerable or outdated packages, and prepare prioritized upgrade steps with commands and breaking-change warnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package-changing commands can alter dependencies and lockfiles under broad dependency-audit triggers. <br>
Mitigation: Require explicit confirmation before running npm, pip, cargo, go, bundle, or other package-changing commands, and review proposed diffs before applying them. <br>
Risk: Forced or major-version upgrades can introduce breaking changes. <br>
Mitigation: Avoid forced fixes unless the breaking-change risk is understood, and run tests in an isolated branch or environment after changes. <br>


## Reference(s): <br>
- [Phy Dep Upgrade on ClawHub](https://clawhub.ai/PHY041/phy-dep-upgrade) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prioritized dependency findings, copy-pasteable package manager commands, and warnings for major-version upgrades.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
