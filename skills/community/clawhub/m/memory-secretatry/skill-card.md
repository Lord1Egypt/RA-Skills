## Description: <br>
Provides intelligent memory management, duplicate task detection, success-case extraction, work pattern analysis, and reminder generation for workspace memory notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhm2084](https://clawhub.ai/user/yhm2084) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw workspace users use this skill to inspect local memory notes, find similar past tasks, extract reusable success cases, analyze work patterns, generate reminders, and create shareable status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans local memory notes and generated reports may summarize sensitive workspace information. <br>
Mitigation: Use it only in workspaces where local memory-note analysis is acceptable, and review generated files under memory/secretary and any share-report output before sharing. <br>
Risk: Optional cron-style daily checks can perform recurring unattended analysis of workspace memory notes. <br>
Mitigation: Enable scheduled checks only when recurring analysis is intended and appropriate for the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yhm2084/memory-secretatry) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Guidance] <br>
**Output Format:** [Python dictionaries, local JSON report files, Markdown share reports, and human-readable reminders.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python standard-library modules and may write reports under memory/secretary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md, and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
