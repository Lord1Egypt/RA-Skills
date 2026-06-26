## Description: <br>
A data-driven health management agent for diet tracking, nutrition analysis, health scoring, supplement tracking, reports, multilingual output, multi-user isolation, timezone-aware records, and optional GitHub backup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longerian](https://clawhub.ai/user/longerian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to record meals, supplements, sleep, exercise, and body metrics, then receive health scoring, food defense-system analysis, and daily, weekly, monthly, or yearly reports. Users who opt in can back up health records to a GitHub repository they control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private health records in local OpenClaw memory. <br>
Mitigation: Use it only in environments where storing personal health data locally is acceptable, and periodically review or delete stored records as needed. <br>
Risk: Optional GitHub backup can push health data using broad local Git access. <br>
Mitigation: Keep backup disabled unless scripts and destination are reviewed, use a private dedicated repository, and prefer dedicated credentials. <br>
Risk: Supplement dosing and nutrition guidance may be mistaken for medical advice. <br>
Mitigation: Treat outputs as tracking and informational support, and consult qualified medical professionals for clinical decisions. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/longerian/health-score-pro) <br>
- [Permissions declaration](PERMISSIONS.md) <br>
- [Usage examples](references/usage-examples.md) <br>
- [Analysis guide](references/analysis-guide.md) <br>
- [Health principles](references/principles.md) <br>
- [Food database](references/food-database.md) <br>
- [Chinese food database](references/chinese-food-database.md) <br>
- [Supplement database](references/supplement-database.md) <br>
- [OpenClaw Security Model](https://docs.openclaw.dev/security) <br>
- [ClawHub Permission Manifest RFC](https://github.com/openclaw/openclaw/issues/10890) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses, Markdown record files, configuration prompts, and optional shell-script backup actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should use the user's configured language and timezone.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata; artifact frontmatter 1.6.0 and manifest 1.5.0 differ) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
