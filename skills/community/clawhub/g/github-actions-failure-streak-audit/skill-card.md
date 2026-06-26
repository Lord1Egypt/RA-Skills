## Description: <br>
Detect consecutive GitHub Actions failure streaks by repo/workflow/branch to prioritize unstable pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to audit exported GitHub Actions runs, identify repeated CI failure streaks, and prioritize unstable workflows by streak length and runtime impact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad RUN_GLOB may include unintended GitHub Actions export files in the audit. <br>
Mitigation: Scope RUN_GLOB to the intended export directory before running the script. <br>
Risk: Collecting run JSON with gh can expose repository and workflow metadata to the local audit inputs. <br>
Mitigation: Use GitHub permissions appropriate for only the repositories being audited. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-failure-streak-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text report or JSON with summary, streaks, and critical_streaks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and critical failure streaks are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
