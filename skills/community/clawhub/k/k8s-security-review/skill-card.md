## Description: <br>
Analyzes Kubernetes YAML manifests for security misconfigurations, best practices violations, and compliance risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, platform security teams, and Kubernetes administrators use this skill to review Kubernetes YAML before deployment and identify security misconfigurations, best-practice violations, and compliance risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Kubernetes manifests may contain Secret values, tokens, passwords, internal hostnames, private registry paths, or other sensitive infrastructure details. <br>
Mitigation: Redact sensitive values and confirm the provider's data handling terms before submitting production YAML to the external API. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/k8s-security-review) <br>
- [Kubernetes Security Review API Endpoint](https://api.mkkpro.com/security/k8s-security-review) <br>
- [Kubernetes Security Review API Docs](https://api.mkkpro.com:8022/docs) <br>
- [ToolWeb](https://toolweb.in) <br>
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON analysis report with findings, severity ratings, recommendations, and summary counts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Kubernetes YAML content as input and sends selected manifest content to an external provider API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
