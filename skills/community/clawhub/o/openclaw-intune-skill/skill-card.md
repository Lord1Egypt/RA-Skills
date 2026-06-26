## Description: <br>
A comprehensive skill enabling OpenClaw agents to manage Microsoft Intune through the Microsoft Graph API, including devices, apps, policies, compliance, users, groups, reporting, Autopilot, scripts, and remote actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MattiaCirillo](https://clawhub.ai/user/MattiaCirillo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
IT administrators, MSPs, and automation engineers use this skill to let an OpenClaw-compatible agent query, report on, and administer Microsoft Intune environments through Microsoft Graph. It supports tenant device, app, policy, compliance, enrollment, user, group, and reporting workflows, including high-impact administrative actions that require human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad Microsoft Intune and Microsoft Graph tenant administration capability. <br>
Mitigation: Install only when agent-based Intune administration is intended, use a dedicated app registration, and grant only the permissions required for the workflows being used. <br>
Risk: Client credentials and application permissions can enable unattended tenant changes if mishandled. <br>
Mitigation: Protect and rotate the client secret, test outside production first, and require human approval before write actions. <br>
Risk: High-impact operations include script upload, group and RBAC changes, Conditional Access changes, report exports, and destructive device actions. <br>
Mitigation: Require explicit human approval for these operations and apply the skill's confirmation rules before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MattiaCirillo/openclaw-intune-skill) <br>
- [Kaffee & Code](https://kaffeeundcode.com) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Microsoft Graph Intune API documentation](https://learn.microsoft.com/en-us/graph/api/resources/intune-graph-overview) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown summaries and tables with Microsoft Graph API request guidance and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INTUNE_TENANT_ID, INTUNE_CLIENT_ID, and INTUNE_CLIENT_SECRET; uses OAuth client credentials and Microsoft Graph application permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
