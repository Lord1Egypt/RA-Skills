## Description: <br>
Group GitHub Actions failures by pipeline phase (setup/build/test/lint/deploy/security) with minute impact to prioritize fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to analyze exported GitHub Actions run JSON and prioritize failing workflow phases by failed minutes and failure count. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad RUN_GLOB patterns can include nearby GitHub Actions JSON exports that contain sensitive project data. <br>
Mitigation: Set RUN_GLOB to a narrow directory or file pattern containing only exports intended for this audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-failure-phase-audit) <br>
- [Publisher profile](https://clawhub.ai/user/daniellummis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Text report or JSON object with summary, hotspots, and critical_hotspots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reporting mode exits 0; fail-gate mode exits 1 when FAIL_ON_CRITICAL=1 and critical hotspots exist.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
