## Description: <br>
Analyzes customer support issue spreadsheets and produces weekly visual reports with trend comparisons, charts, alerts, and an uploaded report link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidunderwood7970](https://clawhub.ai/user/davidunderwood7970) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support operations teams use this skill to turn Excel-based customer service issue logs into weekly metrics, visual HTML reports, and public report links for review and follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated support reports may include names, unresolved issue details, and other internal support data that can become public when uploaded. <br>
Mitigation: Review and redact reports before upload; use private objects or signed links instead of public-read access. <br>
Risk: The artifact embeds Tencent COS credentials and defaults to public report publishing. <br>
Mitigation: Treat the embedded keys as compromised, rotate them before use, and replace them with least-privilege credentials managed outside the skill files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidunderwood7970/issue-analysis-agent) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [JSON analysis data, Markdown summaries, HTML reports, shell command guidance, and public report URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload generated support reports to Tencent COS when configured and executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
