## Description: <br>
Audits OpenClaw permissions and access rights from local OpenClaw configuration files, then produces a structured Markdown report with sensitive values masked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rushingai](https://clawhub.ai/user/rushingai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review what OpenClaw can access across configured API credentials, channels, gateway settings, tools, commands, device identity, and internal hooks before sharing or changing those permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report may reveal operational details such as enabled channels, permission scopes, gateway settings, and partial identifiers. <br>
Mitigation: Review the generated report before sharing it outside the intended audience. <br>
Risk: The skill requires access to local OpenClaw configuration and identity files to perform the audit. <br>
Mitigation: Install and run it only when that inspection is expected, and keep secret values masked in any report output. <br>


## Reference(s): <br>
- [OpenClaw Permissions Audit on ClawHub](https://clawhub.ai/rushingai/openclaw-permissions) <br>
- [rushingai publisher profile](https://clawhub.ai/user/rushingai) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Structured Markdown report with tables and grouped lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sensitive values are masked; missing, empty, or unreadable fields are called out in the report.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
