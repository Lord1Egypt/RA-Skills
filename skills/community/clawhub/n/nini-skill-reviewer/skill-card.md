## Description: <br>
Skill Reviewer audits and validates Claude Code skills for structure, content quality, cross-platform and cross-agent compatibility, prerequisite declarations, and trigger accuracy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niracler](https://clawhub.ai/user/niracler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to review agent skill directories before publishing or installing them. It combines local structure validation, skill-creator content review, and compatibility checks into a single Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Bash and Python validation scripts, so users may execute commands in an unintended repository or skill directory. <br>
Mitigation: Review the bundled scripts before use and run the skill only from the repository or skill directory intended for audit. <br>
Risk: Review completeness depends on a trusted skill-creator helper being available for the content quality step. <br>
Mitigation: Confirm the skill-creator helper is available and trusted before relying on the final review report. <br>


## Reference(s): <br>
- [Compatibility Checklist](references/compatibility-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/niracler/nini-skill-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with a status table and severity-grouped findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include validation command output, manual compatibility findings, and prerequisite guidance.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
