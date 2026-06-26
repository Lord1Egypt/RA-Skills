## Description: <br>
Audit GitHub Actions workflow conclusion volatility to surface unstable pipelines before they become chronic failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to audit GitHub Actions run exports, identify workflows whose conclusions frequently change, and decide whether unstable pipelines should be reported or gated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enabling the fail gate can intentionally fail a CI job when critical workflow volatility is detected. <br>
Mitigation: Run in reporting mode first, review the configured thresholds, and enable FAIL_ON_CRITICAL only where that gate is expected. <br>
Risk: Incomplete or mismatched workflow run exports can produce misleading volatility results. <br>
Mitigation: Collect the intended GitHub Actions JSON fields and review repository, branch, and workflow filters before using the report for decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daniellummis/github-actions-conclusion-volatility-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples; runtime output is text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local GitHub Actions workflow run JSON files and can exit nonzero when FAIL_ON_CRITICAL=1 finds critical instability.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
