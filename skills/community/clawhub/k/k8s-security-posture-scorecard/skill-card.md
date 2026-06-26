## Description: <br>
Assess Kubernetes cluster security posture across 30 controls covering RBAC, workload security, network policies, IaC, runtime monitoring, and secrets management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and security teams use this skill to collect Kubernetes cluster posture inputs, call the ToolWeb scorecard API, and present a prioritized security assessment across cluster, workload, network, IaC, runtime, secrets, and compliance controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Kubernetes posture details to the ToolWeb API and uses a ToolWeb API key that may affect quota or billing. <br>
Mitigation: Minimize submitted data, avoid optional sensitive notes, and confirm API key usage is authorized before running assessments. <br>
Risk: Cluster inputs could include sensitive operational details if users provide secrets, kubeconfig contents, tokens, private endpoints, or unnecessary internal identifiers. <br>
Mitigation: Do not submit secrets or credentials, and redact private infrastructure identifiers unless they are required for the assessment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/k8s-security-posture-scorecard) <br>
- [ToolWeb portal](https://portal.toolweb.in) <br>
- [ToolWeb platform](https://toolweb.in) <br>
- [ToolWeb API endpoint](https://portal.toolweb.in/apis/security/k8scorecard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with inline shell command examples and API-derived security findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and TOOLWEB_API_KEY; successful assessments send supplied Kubernetes posture details to ToolWeb.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
