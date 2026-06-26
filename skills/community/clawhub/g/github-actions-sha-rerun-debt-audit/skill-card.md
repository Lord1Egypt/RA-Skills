## Description: <br>
Audit rerun debt by commit SHA to find commits that repeatedly burn CI minutes across workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to analyze exported GitHub Actions run data, identify commits that repeatedly trigger reruns or failed outcomes, and prioritize CI reliability work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may include repository names, run URLs, branch names, or commit SHAs from GitHub Actions exports. <br>
Mitigation: Treat generated reports as potentially sensitive and limit sharing to the intended engineering or CI operations audience. <br>
Risk: A broad RUN_GLOB may scan unintended local JSON files. <br>
Mitigation: Scope RUN_GLOB to the intended GitHub Actions export directory before running the audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-sha-rerun-debt-audit) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, json, shell commands, guidance] <br>
**Output Format:** [Text report or JSON report generated from GitHub Actions run export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally exit non-zero when FAIL_ON_CRITICAL=1 and critical SHA rerun-debt groups are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
