## Description: <br>
Browser automation for Kubernetes dashboards and web UIs. Use when interacting with Kubernetes Dashboard, Grafana, ArgoCD UI, or other web interfaces. Requires MCP_BROWSER_ENABLED=true. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rohitg00](https://clawhub.ai/user/rohitg00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and platform engineers use this skill to automate Kubernetes-related web dashboards, including Kubernetes Dashboard, Grafana, and ArgoCD, for navigation, interaction, screenshots, and content inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to send credentials or authorization headers to Kubernetes-related web dashboards. <br>
Mitigation: Use least-privilege, short-lived credentials and verify target URLs before sending headers or passwords. <br>
Risk: Screenshots and page content dumps can expose sensitive cluster, workload, or operational data. <br>
Mitigation: Avoid capturing sensitive pages and prefer local browser execution for sensitive clusters. <br>
Risk: Browser interactions in tools such as ArgoCD can trigger production-changing actions. <br>
Mitigation: Require explicit human confirmation before ArgoCD sync or other production-changing UI actions. <br>


## Reference(s): <br>
- [Kubernetes Skills on ClawHub](https://clawhub.ai/rohitg00/k8s-browser) <br>
- [Publisher profile: rohitg00](https://clawhub.ai/user/rohitg00) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and Python-style tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes browser navigation, interaction, session management, viewport, screenshot, and content-inspection guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
