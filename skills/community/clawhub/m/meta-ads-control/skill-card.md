## Description: <br>
Use this skill when the user wants to inspect, report on, create, update, pause, resume, budget, target, upload assets for, or troubleshoot Meta, Facebook, or Instagram ads via the Marketing API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, marketers, and advertising operators use this skill to manage Meta ad accounts, campaign structure, targeting, creative assets, and performance reporting through agent-guided Marketing API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Meta access token to perform high-impact ad account actions, including changes that affect spend, delivery, audiences, creatives, or account data. <br>
Mitigation: Use least-privileged Meta tokens, start with non-production ad accounts where possible, require dry-runs and explicit human approval for write operations, and verify state after changes. <br>
Risk: A misconfigured Graph API base URL could expose token-backed requests to an unintended host. <br>
Mitigation: Keep META_GRAPH_BASE set to the official Meta Graph API host unless a trusted reviewer approves a different endpoint. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tristanmanchester/meta-ads-control) <br>
- [Publisher Profile](https://clawhub.ai/user/tristanmanchester) <br>
- [API Guide](references/API-GUIDE.md) <br>
- [Field Sets and Reporting Defaults](references/FIELDS.md) <br>
- [Workflow Playbook](references/WORKFLOWS.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [OpenClaw Notes](references/OPENCLAW.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to use dry-run and confirmation flows before write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
