## Description: <br>
Scan npm packages used in a repository for risk, maintenance health, and upgrade concerns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoffrey-xiao](https://clawhub.ai/user/geoffrey-xiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review JavaScript and npm dependency risk in a repository, including direct and transitive dependencies, audit findings, stale packages, broad version ranges, and upgrade concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read package manifests and lockfiles and run package manager audit or listing commands. <br>
Mitigation: Use it in repositories where dependency metadata can be reviewed, and inspect proposed commands before execution. <br>
Risk: Upgrade and fix recommendations can have dependency compatibility or build impact. <br>
Mitigation: Review proposed dependency changes for blast radius and run project tests before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geoffrey-xiao/npm-package-scan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review with severity sections and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not modify dependency versions or remove packages unless explicitly asked; may run package manager audit and listing commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
