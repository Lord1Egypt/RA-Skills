## Description: <br>
Audit and score OpenClaw AgentSkills against structural compliance, quality standards, and OpenClaw-specific architecture patterns, producing a 0-100 score, A-F grade, dimensional breakdown, and actionable improvement recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haseo-ai](https://clawhub.ai/user/haseo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to evaluate OpenClaw AgentSkills for structural compliance, triggering quality, workflow design, sub-agent design, and conciseness. It produces bilingual audit reports with scores and prioritized recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports are saved locally by default and may retain secrets or private implementation details from audited skills. <br>
Mitigation: Avoid auditing skills that contain secrets or private implementation details unless local retention under ~/.openclaw/workspace/skill-audit-reports is acceptable; review reports before sharing. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/haseo-ai/oc-skill-audit) <br>
- [Scoring Rubric](artifact/references/scoring-rubric.md) <br>
- [Scoring Rubric (Korean)](artifact/references/scoring-rubric.ko.md) <br>
- [Scoring Rubric (Japanese)](artifact/references/scoring-rubric.ja.md) <br>
- [Scoring Rubric (Chinese)](artifact/references/scoring-rubric.zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown audit report and response summary card] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces bilingual reports when appropriate and saves timestamped audit files under ~/.openclaw/workspace/skill-audit-reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
