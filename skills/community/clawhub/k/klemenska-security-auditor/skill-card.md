## Description: <br>
Scan and audit installed skills for security risks, suspicious patterns, and permission overreach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klemenska](https://clawhub.ai/user/klemenska) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan OpenClaw skill directories before installation or during periodic reviews, generate audit reports, compare skills, and identify permission overreach or suspicious patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can include source-line snippets from scanned skills. <br>
Mitigation: Review generated reports before sharing them, especially when scanned skills may contain sensitive local code or configuration. <br>
Risk: Broad scans may read more local skill files than intended. <br>
Mitigation: Run audits against specific skill directories and avoid broad or sensitive filesystem paths. <br>
Risk: A clean scan result is advisory and may miss issues. <br>
Mitigation: Use the output as one input to review, not as a replacement for manual code review or a complete security assessment. <br>


## Reference(s): <br>
- [Permissions Reference Guide](references/permissions.md) <br>
- [Security Audit Rules](references/rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/klemenska/klemenska-security-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Analysis, Guidance] <br>
**Output Format:** [Terminal text and Markdown reports with risk levels, issue lists, permissions, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a Markdown report when report output is requested; detailed scans can return nonzero exit status for medium, high, or critical findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
