## Description: <br>
Audit GitHub Actions runs for fail-then-success retry recovery patterns to quantify flaky rerun waste. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze exported GitHub Actions workflow run data, identify fail-then-success retry patterns, and prioritize flaky reruns by wasted minutes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can expose repository, branch, commit, run, and URL details from GitHub Actions exports. <br>
Mitigation: Use only GitHub Actions JSON files that are appropriate for local reports or CI logs, and review generated output before sharing it. <br>
Risk: CI fail gates based on retry waste thresholds can block workflows when critical recoveries are detected. <br>
Mitigation: Set WARN_WASTE_MINUTES, CRITICAL_WASTE_MINUTES, and FAIL_ON_CRITICAL intentionally for the repository's tolerance before enabling enforcement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-retry-recovery-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Text report or JSON summary with ranked recoveries and critical recovery groups] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit with a non-zero status when FAIL_ON_CRITICAL=1 and critical recoveries are present.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
