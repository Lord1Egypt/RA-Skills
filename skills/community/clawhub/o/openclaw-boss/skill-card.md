## Description: <br>
Openclaw Boss analyzes local OpenClaw memories, profile files, and conversation history to generate strict, humorous personal profile and performance-style reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winston-wwzhen](https://clawhub.ai/user/winston-wwzhen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to review personal work patterns, technical strengths, safety posture, and growth areas from local OpenClaw history. It supports ad hoc self-analysis plus weekly or monthly profile reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads private OpenClaw memories, profile files, session history, prior reports, and related local memory tooling. <br>
Mitigation: Install and run only in a trusted local environment; review the files it can access before use. <br>
Risk: Scheduled reports may rely on onload or cron behavior that repeatedly processes personal data. <br>
Mitigation: Verify whether any .onload or cron entry is created, prefer user-level scheduling, and remove scheduled jobs that are not needed. <br>
Risk: Generated reports may contain sensitive personal details and inferred traits. <br>
Mitigation: Review report contents before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/winston-wwzhen/openclaw-boss) <br>
- [Analysis Dimensions](references/analysis-dimensions.md) <br>
- [Security Notes](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with ASCII score cards and inline shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local report files and print full personal profile reports to stdout.] <br>

## Skill Version(s): <br>
5.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
