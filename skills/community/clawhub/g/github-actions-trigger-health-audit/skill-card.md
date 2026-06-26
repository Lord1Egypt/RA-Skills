## Description: <br>
Audit GitHub Actions run health by trigger event and workflow so flaky or noisy automation sources are easy to prioritize. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to analyze exported GitHub Actions run data, identify trigger events and workflows with high failure or cancellation rates, and produce reports or automation gates for prioritizing reliability work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs shell and Python code over local GitHub Actions export files and may be used in automation gates. <br>
Mitigation: Review the command and environment variables before execution, run it on intended JSON exports only, and keep FAIL_ON_CRITICAL disabled until threshold behavior is confirmed. <br>
Risk: Reports may include repository, branch, workflow, and run URL details from the input JSON. <br>
Mitigation: Treat generated text or JSON reports as potentially sensitive operational data and share them only with audiences allowed to view the underlying GitHub Actions metadata. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/daniellummis/github-actions-trigger-health-audit) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, json, shell commands] <br>
**Output Format:** [Text report or JSON summary with grouped metrics and critical group details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit with status 1 when FAIL_ON_CRITICAL=1 and any group meets the configured critical threshold.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
