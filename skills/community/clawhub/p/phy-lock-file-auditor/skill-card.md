## Description: <br>
Lockfile security and integrity auditor for JavaScript, Python, Go, and Rust projects that detects phantom dependencies, lockfile drift, integrity hash anomalies, conflicting version pins, and yanked or unpublished package versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit dependency lockfiles for supply-chain integrity issues before merging, releasing, or refreshing dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some audit findings can be advisory or imprecise, especially Cargo phantom dependency and Poetry drift results. <br>
Mitigation: Review reported findings against the relevant manifest and lockfile before treating them as security issues. <br>
Risk: Suggested fixes such as regenerating lockfiles or adding CI and pre-commit hooks can change dependency state or project workflow behavior. <br>
Mitigation: Inspect generated commands and review resulting diffs before applying, committing, or deploying changes. <br>


## Reference(s): <br>
- [Phy Lock File Auditor on ClawHub](https://clawhub.ai/PHY041/phy-lock-file-auditor) <br>
- [PHY041 publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with audit findings, inline code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local advisory analysis; no external API is required by the skill.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
