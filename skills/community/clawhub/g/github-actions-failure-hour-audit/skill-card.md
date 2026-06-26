## Description: <br>
Audit GitHub Actions failure timing by day/hour to surface recurring outage windows and staffing hotspots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze exported GitHub Actions workflow runs, identify recurring failure windows, and tune staffing, dashboarding, or CI failure gates around high-risk hours. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit can include repository, workflow, branch, run URL, run ID, and local file path details in reports. <br>
Mitigation: Set RUN_GLOB narrowly, review output before sharing, and avoid publishing JSON reports that expose internal repository or workflow metadata. <br>
Risk: The script reads local GitHub Actions JSON exports and executes local Bash/Python code. <br>
Mitigation: Run it only in workspaces where local execution is acceptable and review the skill artifact before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daniellummis/github-actions-failure-hour-audit) <br>
- [Publisher Profile](https://clawhub.ai/user/daniellummis) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Text or JSON audit report, with optional shell-command examples and environment-variable configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and one or more critical windows are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
