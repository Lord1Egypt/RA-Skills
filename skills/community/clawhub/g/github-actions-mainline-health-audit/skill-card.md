## Description: <br>
Audit GitHub Actions mainline branch reliability by scoring failure rate, consecutive failures, and stale-success risk for critical workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to analyze exported GitHub Actions run data for protected branch workflow reliability, stale-success risk, and critical failure patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can include repository names, branches, SHAs, run IDs, and run URLs from private or sensitive repositories. <br>
Mitigation: Keep RUN_GLOB limited to the intended exported run files and review generated reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-mainline-health-audit) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, json, shell commands, guidance] <br>
**Output Format:** [Text report or JSON summary with scored workflow groups and critical group details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and python3. Reads local GitHub Actions run JSON exports selected by RUN_GLOB and can exit nonzero when FAIL_ON_CRITICAL=1.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
