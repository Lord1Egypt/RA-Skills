## Description: <br>
Detect duplicate GitHub Actions run bursts by workflow/branch/commit and quantify wasted rerun minutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to audit exported GitHub Actions run JSON for duplicate workflow bursts, quantify wasted CI minutes, and optionally fail automation when critical duplication is detected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports can include repository names, branch names, commit SHAs, run URLs, and timing data from local GitHub Actions exports. <br>
Mitigation: Review the input JSON files and generated reports before sharing them, and run the skill only on exports intended for CI hygiene analysis. <br>
Risk: Critical duplicate findings can make automation exit non-zero when FAIL_ON_CRITICAL is enabled. <br>
Mitigation: Tune warning and critical thresholds in report mode before using the skill as a CI gate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-duplicate-run-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Text report or JSON report emitted by a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configurable with environment variables for input glob, filters, duplicate thresholds, output format, and optional critical-finding exit behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
