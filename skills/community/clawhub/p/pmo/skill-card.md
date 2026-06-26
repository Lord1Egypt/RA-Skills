## Description: <br>
PMO is an OpenClaw project-management skill that connects to tools such as GitHub Issues and Notion to summarize portfolio status, generate weekly reports, and surface cross-project risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guytogay](https://clawhub.ai/user/guytogay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering managers, and project teams use this skill to review portfolio health, sync project status from configured tools, generate weekly reports, and identify stale projects or cross-project risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub access tokens are required for repository issue syncing. <br>
Mitigation: Use least-privilege tokens supplied through environment variables and avoid passing tokens directly on the command line. <br>
Risk: Local PMO memory files can contain internal project metadata, event history, and risk summaries. <br>
Mitigation: Review memory/PMO contents before sharing or backup, and avoid storing sensitive customer, financial, or personnel details in those files. <br>
Risk: Configured alert channels can send project or risk summaries to external recipients. <br>
Mitigation: Enable Telegram, Feishu, or similar channels only after confirming recipients and payload sensitivity. <br>


## Reference(s): <br>
- [PMO ClawHub listing](https://clawhub.ai/guytogay/pmo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and tables, JSON from helper scripts, and YAML or command examples for configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local PMO project, event, risk, and cache files and may send configured alerts when enabled.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release metadata; artifact frontmatter reports 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
