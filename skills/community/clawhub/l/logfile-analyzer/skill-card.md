## Description: <br>
Analyze application logs to produce actionable error digests with pattern detection, severity classification, trend analysis, and remediation recommendations across common log formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and incident responders use this skill to analyze selected application logs, group recurring failures, classify severity, detect trends, and generate remediation-oriented summaries for incident review, health checks, CI, or reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Application logs may contain tokens, user data, internal URLs, or other sensitive operational details. <br>
Mitigation: Analyze only the specific files or directories needed for the task and review generated summaries before sharing them outside the intended operational context. <br>


## Reference(s): <br>
- [Error Pattern Reference](references/error-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Text, JSON, or Markdown reports with severity summaries, grouped patterns, trends, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return CI-friendly exit codes and filter results by time range, severity, format, and ignored regex patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
